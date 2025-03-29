import base64
import io
import pdf2image
import google.generativeai as genai
import os
from dotenv import load_dotenv
from io import BytesIO

# Load API keys
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in environment variables!")

genai.configure(api_key=GOOGLE_API_KEY)

def process_resume(uploaded_file, job_description):
    try:
        print("Reading uploaded file...")

        # Read file into memory
        pdf_stream = BytesIO(uploaded_file.read())
        print("PDF file read successfully.")

        # Convert PDF to images
        images = pdf2image.convert_from_bytes(pdf_stream.getvalue())
        print(f"Extracted {len(images)} pages from the PDF.")

        if not images:
            return {"error": "Failed to extract pages from PDF"}

        first_page = images[0]

        # Convert image to base64
        img_byte_arr = BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        print("Converted first page to an image.")

        pdf_content = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
        }]

        print("Prepared image for Gemini AI processing.")

        # Define ATS prompt
        ats_prompt = """
        You are an AI-powered Applicant Tracking System (ATS).
        Deeply Analyze the given resume against the provided job description.
        Accurately Provide integer values only for the given queries:
        1. A match percentage (out of 100%).
        2. Candidate's Name.
        3. Candidate's Email.
        4. Candidate's Phone Number.
        5. Candidate's Year of Experience.
        6. average of 10th, 12th and graduation score.
        """

        # Call Gemini AI API
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("Calling Gemini AI API...")
        response = model.generate_content([ats_prompt, pdf_content[0], job_description])
        print("Received response from Gemini AI.")

        # Extracting text from response
        candidate_data = response.candidates[0].content.parts[0].text  
        print("Extracted candidate data:", candidate_data)

        # Parse extracted text
        lines = candidate_data.split("\n")
        parsed_data = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in lines if ":" in line}

        return {
            "match_percentage": parsed_data.get("1. Match Percentage", "N/A"),
            "candidate_name": parsed_data.get("2. Candidate's Name", "N/A"),
            "candidate_email": parsed_data.get("3. Candidate's Email", "N/A"),
            "candidate_phone_number": parsed_data.get("4. Candidate's Phone Number", "N/A"),
            "candidate_year_of_experience": parsed_data.get("5. Candidate's Year of Experience", "N/A"),
            "average_10th_12th_graduation_score": parsed_data.get("6. Average of 10th, 12th and Graduation Score", "N/A")
        }

    except Exception as e:
        print(f"Error processing resume: {e}")
        return {"error": f"Error processing resume: {str(e)}"}
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
    """Convert PDF to an image and analyze it with Gemini AI."""
    try:
        # Read file into memory
        pdf_stream = BytesIO(uploaded_file.read())

        # Convert PDF to images
        images = pdf2image.convert_from_bytes(pdf_stream.getvalue())

        if not images:
            return {"error": "Failed to extract pages from PDF"}

        first_page = images[0]

        # Convert image to base64
        img_byte_arr = BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_content = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
        }]

        # Define ATS prompt
        ats_prompt = """
        You are an AI-powered Applicant Tracking System (ATS).
        Analyze the given resume against the provided job description.
        Provide only:
        1. A match percentage (out of 100%).
        """

        # Call Gemini AI API
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([ats_prompt, pdf_content[0], job_description])

        return {"score": response.text}

    except Exception as e:
        return {"error": f"Error processing resume: {str(e)}"}

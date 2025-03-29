from flask import Flask, request, jsonify
from flask_cors import CORS
from ats_scoring import process_resume

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# Temporary storage for file processing results
processed_results = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print("Received a file upload request.")  # Debug log

        # Validate file input
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        # Validate job description
        job_desc = request.form.get('job_description', '').strip()
        if not job_desc:
            return jsonify({"error": "Job description is required"}), 400

        # Process the resume and get the score
        result = process_resume(file, job_desc)

        if "error" in result:
            return jsonify(result), 500  # Return error if processing fails

        # Simulate storing file ID (using a simple counter)
        file_id = str(len(processed_results) + 1)
        processed_results[file_id] = result

        return jsonify({"message": "File uploaded successfully", "file_id": file_id}), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/get-score/<file_id>', methods=['GET'])
def get_score(file_id):
    try:
        print(f"Checking score for File ID: {file_id}")  # Debug log

        # Retrieve stored result
        if file_id not in processed_results:
            return jsonify({"error": "File ID not found"}), 404

        return jsonify(processed_results[file_id]), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Failed to fetch score"}), 500


if __name__ == '__main__':
    app.run(debug=True)

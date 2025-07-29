from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import json
import os

# --- Initialize Flask App ---
app = Flask(__name__)
CORS(app)

# --- Configuration ---
# It's highly recommended to set your API key as an environment variable
# for security.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Leave empty if not using a key
if not GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY environment variable not set.")


# --- The Main Detection Function using Gemini API ---
def detect_waste_from_image_gemini(image_bytes):
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key is not configured on the server."}

    # 1. Encode the image to Base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    # 2. Define the JSON schema for the expected response from Gemini
    # This ensures we get structured data back that matches our needs.
    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "name": {"type": "STRING"},
                "confidence": {"type": "INTEGER"},
                "binDescription": {"type": "STRING"},
                "tips": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"}
                }
            },
            "required": ["name", "confidence", "binDescription", "tips"]
        }
    }

    # 3. Create the prompt for the Gemini API
    prompt = (
        "Analyze the primary subject in this image as a piece of waste. "
        "Identify the item, estimate your confidence in this identification (0-100), "
        "and provide its proper disposal bin and 2-3 helpful disposal tips. "
        "Format your response as a JSON array according to the provided schema, "
        "containing only the single, most prominent waste item."
    )

    # 4. Construct the payload for the Gemini API request
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json",
            "response_schema": response_schema
        }
    }

    # 5. Make the API call
    try:
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={GEMINI_API_KEY}"
        response = requests.post(
            api_url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload)
        )
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        result = response.json()

        # 6. Extract and parse the content from the response
        if 'candidates' in result and result['candidates']:
            content_part = result['candidates'][0]['content']['parts'][0]
            # The response text is a JSON string, so we need to parse it
            detections = json.loads(content_part['text'])
            
            # Capitalize the name for better display
            for item in detections:
                item['name'] = item['name'].capitalize()

            return detections
        else:
            # Handle cases where the API returns no candidates (e.g., safety blocks)
            return {"error": "Analysis failed. The image might violate safety policies or could not be processed."}

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {e}")
        return {"error": f"Failed to communicate with the Gemini API. Details: {e}"}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"❌ Error parsing Gemini response: {e}")
        print(f"Raw response: {result}")
        return {"error": "Failed to parse the analysis result from the AI model."}


# --- API Endpoint ---
@app.route('/api/detect', methods=['POST'])
def detect_waste_endpoint():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    image_bytes = file.read()
    
    # Call the new Gemini-based detection function
    analysis_result = detect_waste_from_image_gemini(image_bytes)

    if isinstance(analysis_result, dict) and "error" in analysis_result:
        return jsonify(analysis_result), 500

    return jsonify(analysis_result)

# --- Run the Server ---
if __name__ == '__main__':
    # For production, consider using a proper WSGI server like Gunicorn or Waitress
    app.run(debug=True, port=5000)

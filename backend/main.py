# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import requests
# import base64
# import json
# import os
# from dotenv import load_dotenv
# from datetime import datetime
# from pymongo import MongoClient
# from bson import ObjectId
# # The google_search tool is not a standard package, so we remove the direct import.
# # from google_search import search

# # --- Load Environment Variables ---
# load_dotenv()

# # --- Initialize Flask App ---
# app = Flask(__name__)
# CORS(app)

# # --- MongoDB Connection ---
# try:
#     client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
#     client.admin.command('ismaster')
#     db = client['waste_detection_db']
#     history_collection = db['detection_history']
#     print("✅ MongoDB connected successfully.")
# except Exception as e:
#     print(f"❌ Could not connect to MongoDB. Error: {e}")
#     client = None

# # --- Configuration ---
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     print("⚠️ WARNING: GEMINI_API_KEY environment variable not set.")

# # --- Helper function ---
# def serialize_doc(doc):
#     if '_id' in doc:
#         doc['_id'] = str(doc['_id'])
#     return doc

# # --- Gemini Detection Function (remains the same) ---
# def detect_waste_from_image_gemini(image_bytes):
#     if not GEMINI_API_KEY:
#         return {"error": "Gemini API key is not configured on the server."}
#     base64_image = base64.b64encode(image_bytes).decode('utf-8')
#     response_schema = {
#         "type": "ARRAY",
#         "items": {
#             "type": "OBJECT",
#             "properties": { "name": {"type": "STRING"}, "confidence": {"type": "INTEGER"}, "binDescription": {"type": "STRING"}, "tips": { "type": "ARRAY", "items": {"type": "STRING"} } },
#             "required": ["name", "confidence", "binDescription", "tips"]
#         }
#     }
#     prompt = (
#         "Analyze the primary subject in this image as a piece of waste. "
#         "Identify the item, estimate your confidence (0-100), "
#         "and provide its proper disposal bin and 2-3 helpful disposal tips. "
#         "Format your response as a JSON array according to the provided schema, "
#         "containing only the single, most prominent waste item."
#     )
#     payload = {
#         "contents": [ { "parts": [ {"text": prompt}, { "inline_data": { "mime_type": "image/jpeg", "data": base64_image } } ] } ],
#         "generationConfig": { "response_mime_type": "application/json", "response_schema": response_schema }
#     }
#     try:
#         api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"
#         response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
#         response.raise_for_status()
#         result = response.json()
#         if 'candidates' in result and result['candidates']:
#             content_part = result['candidates'][0]['content']['parts'][0]
#             detections = json.loads(content_part['text'])
#             for item in detections:
#                 item['name'] = item['name'].capitalize()
#             return detections
#         else:
#             return {"error": "Analysis failed due to safety policies."}
#     except requests.exceptions.RequestException as e:
#         return {"error": f"API communication failed: {e}"}
#     except (KeyError, IndexError, json.JSONDecodeError) as e:
#         return {"error": "Failed to parse AI model result."}

# # --- API Endpoint for Detection ---
# @app.route('/api/detect', methods=['POST'])
# def detect_waste_endpoint():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file provided"}), 400
#     file = request.files['image']
#     image_bytes = file.read()
#     analysis_result = detect_waste_from_image_gemini(image_bytes)
#     if isinstance(analysis_result, dict) and "error" in analysis_result:
#         return jsonify(analysis_result), 500
#     if client and analysis_result:
#         try:
#             history_collection.insert_one({
#                 "timestamp": datetime.utcnow(),
#                 "detected_items": analysis_result,
#                 "detection_count": len(analysis_result)
#             })
#         except Exception as e:
#             print(f"❌ Error saving to MongoDB: {e}")
#     return jsonify(analysis_result)

# # --- API Endpoint to Get History ---
# @app.route('/api/history', methods=['GET'])
# def get_history():
#     if not client:
#         return jsonify({"error": "Database connection not available"}), 500
#     try:
#         history_records = history_collection.find().sort("timestamp", -1).limit(20)
#         result = [serialize_doc(record) for record in history_records]
#         return jsonify(result)
#     except Exception as e:
#         return jsonify({"error": "Could not fetch history"}), 500


# @app.route('/api/detect', methods=['POST'])
# def detect_waste_endpoint():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file provided"}), 400
#     file = request.files['image']
#     image_bytes = file.read()
#     analysis_result = detect_waste_from_image_gemini(image_bytes)
#     if isinstance(analysis_result, dict) and "error" in analysis_result:
#         return jsonify(analysis_result), 500
#     if client and analysis_result:
#         try:
#             history_collection.insert_one({
#                 "timestamp": datetime.utcnow(),
#                 "detected_items": analysis_result,
#                 "detection_count": len(analysis_result)
#             })
#         except Exception as e:
#             print(f"❌ Error saving to MongoDB: {e}")
#     return jsonify(analysis_result)

# # --- Run the Server ---
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)


from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# --- Load Environment Variables ---
load_dotenv()

# --- Initialize Flask App ---
app = Flask(__name__)
CORS(app)

# --- MongoDB Connection ---
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.admin.command('ismaster')
    db = client['waste_detection_db']
    history_collection = db['detection_history']
    print("✅ MongoDB connected successfully.")
except Exception as e:
    print(f"❌ Could not connect to MongoDB. Error: {e}")
    client = None

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY environment variable not set.")

# --- Helper function ---
def serialize_doc(doc):
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

# --- Gemini Detection Function (remains the same) ---
def detect_waste_from_image_gemini(image_bytes):
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key is not configured on the server."}
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": { "name": {"type": "STRING"}, "confidence": {"type": "INTEGER"}, "binDescription": {"type": "STRING"}, "tips": { "type": "ARRAY", "items": {"type": "STRING"} } },
            "required": ["name", "confidence", "binDescription", "tips"]
        }
    }
    prompt = (
        "Analyze this image and identify ALL visible waste items. "
        "For each waste item you can see, identify the item name, estimate your confidence (0-100), "
        "and provide its proper disposal bin and 2-3 helpful disposal tips. "
        "Format your response as a JSON array according to the provided schema, "
        "containing ALL waste items visible in the image (not just the most prominent one). "
        "If you see multiple items, include each one in the array. "
        "Focus on items that are clearly waste or recyclable materials."
    )
    payload = {
        "contents": [ { "parts": [ {"text": prompt}, { "inline_data": { "mime_type": "image/jpeg", "data": base64_image } } ] } ],
        "generationConfig": { "response_mime_type": "application/json", "response_schema": response_schema }
    }
    try:
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        if 'candidates' in result and result['candidates']:
            content_part = result['candidates'][0]['content']['parts'][0]
            detections = json.loads(content_part['text'])
            for item in detections:
                item['name'] = item['name'].capitalize()
            return detections
        else:
            return {"error": "Analysis failed due to safety policies."}
    except requests.exceptions.RequestException as e:
        return {"error": f"API communication failed: {e}"}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return {"error": "Failed to parse AI model result."}

# --- API Endpoint for Detection ---
@app.route('/api/detect', methods=['POST'])
def detect_waste_endpoint():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    image_bytes = file.read()
    analysis_result = detect_waste_from_image_gemini(image_bytes)
    if isinstance(analysis_result, dict) and "error" in analysis_result:
        return jsonify(analysis_result), 500
    if client and analysis_result:
        try:
            history_collection.insert_one({
                "timestamp": datetime.utcnow(),
                "detected_items": analysis_result,
                "detection_count": len(analysis_result)
            })
        except Exception as e:
            print(f"❌ Error saving to MongoDB: {e}")
    return jsonify(analysis_result)

# --- API Endpoint to Get History ---
@app.route('/api/history', methods=['GET'])
def get_history():
    if not client:
        return jsonify({"error": "Database connection not available"}), 500
    try:
        history_records = history_collection.find().sort("timestamp", -1).limit(20)
        result = [serialize_doc(record) for record in history_records]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Could not fetch history"}), 500

# --- Updated Mock Data for Recycling Centers ---
RECYCLING_CENTERS = [
    {"id": 1, "name": "Gayatri Towers Collection Point", "address": "Madeenaguda, Hyderabad, Telangana", "accepts": ["plastic bottle", "paper", "cardboard"], "url": "https://www.google.com/maps/place/Gayatri+Towers/@17.4929761,78.3399159,18.03z/data=!4m15!1m8!3m7!1s0x3bcb9261b260dcb5:0x4fa01c2c77f7b38b!2sMadeenaguda,+Telangana!3b1!8m2!3d17.4936856!4d78.3401293!16s%2Fm%2F0vxdb5b!3m5!1s0x3bcb9260fb6cf455:0x1ccb0fb98c56fd84!8m2!3d17.4925339!4d78.3419676!16s%2Fg%2F1pv6x_s8c?authuser=0&entry=ttu"},
    {"id": 2, "name": "Nexus Hyderabad Mall E-Waste Bin", "address": "Kukatpally, Hyderabad, Telangana", "accepts": ["cell phone", "laptop", "keyboard", "mouse", "remote", "e-waste"], "url": "https://www.google.com/maps/place/Nexus+Hyderabad+Mall/@17.4844243,78.3867705,17z/data=!3m1!4b1!4m6!3m5!1s0x3bcb919ef6c7c09d:0xe03175b81113bc71!8m2!3d17.4844243!4d78.3893454!16s%2Fg%2F11kqbr0d9l?authuser=0&entry=ttu"},
    {"id": 3, "name": "D-Mart Nizampet Plastics Collection", "address": "Nizampet, Hyderabad, Telangana", "accepts": ["plastic bottle", "plastic jug"], "url": "https://www.google.com/maps/place/D+-+Mart+Nizampet/@17.5225265,78.3720519,17z/data=!3m1!4b1!4m6!3m5!1s0x3bcb8d2b25b7275d:0x7fdf4d649b5825aa!8m2!3d17.5225265!4d78.3746268!16s%2Fg%2F11l6lrc3k7?authuser=0&entry=ttu"},
    {"id": 4, "name": "Patancheru Bus Station General Recycling", "address": "Patancheruvu, Hyderabad, Telangana 502319", "accepts": ["plastic bottle", "paper", "metal can", "glass jar"], "url": "https://www.google.com/maps/place/PATANCHERU+BUS+STATION,+Shanthi+Nagar,+Hyderabad,+Patancheruvu,+Telangana+502319/@17.5287836,78.261559,17z/data=!3m1!4b1!4m6!3m5!1s0x3bcbf2937a21d759:0x206c6d4aa14c84fd!8m2!3d17.5290259!4d78.2641665!16s%2Fg%2F11b8zckrn4?authuser=0&entry=ttu"},
    {"id": 5, "name": "Amazon Campus E-Waste & Cardboard", "address": "Financial District, Nanakramguda, Hyderabad", "accepts": ["cardboard", "paper", "e-waste", "cell phone", "laptop"], "url": "https://www.google.com/maps/place/Amazon+Hyderabad+Campus+(HYD13)/@17.4164679,78.33991,15.55z/data=!4m15!1m8!3m7!1s0x3bcb937ff83e0bd9:0xfdc750032731da04!2sFinancial+District,+Nanakramguda,+Telangana+500032!3b1!8m2!3d17.4117312!4d78.3424898!16s%2Fg%2F1txy0sjt!3m5!1s0x3bcb93877fae478f:0xef416c0438a2ef!8m2!3d17.4206226!4d78.3452099!16s%2Fg%2F11g6ml5q5d?authuser=0&entry=ttu"}
]

@app.route('/api/recycling-centers', methods=['GET'])
def get_recycling_centers():
    detected_types = []
    suggestions = []

    if client:
        try:
            # Fetch recent detection history to get detected waste types
            recent_history = history_collection.find().sort("timestamp", -1).limit(5)
            for record in recent_history:
                if 'detected_items' in record:
                    for item in record['detected_items']:
                        if 'name' in item:
                            # Convert to lowercase for consistent matching
                            detected_types.append(item['name'].lower()) 
            
            # Remove duplicates and process for comparison (e.g., "plastic bottle" -> "plastic bottle")
            # We'll use the exact names from 'accepts' for more precise matching
            detected_types = list(set(detected_types))

            # Find suggestions based on detected types
            for center in RECYCLING_CENTERS:
                for accepted_type in center['accepts']:
                    if accepted_type.lower() in detected_types: # Compare lowercase
                        suggestions.append(center)
                        break # Add center once if it accepts any detected type
            
            # Remove duplicate suggestions
            unique_suggestions = []
            seen_ids = set()
            for s in suggestions:
                if s['id'] not in seen_ids:
                    unique_suggestions.append(s)
                    seen_ids.add(s['id'])
            suggestions = unique_suggestions

        except Exception as e:
            print(f"❌ Error fetching history for recycling centers: {e}")
            # Continue even if there's a history error, just won't have suggestions

    return jsonify({
        "suggestions": suggestions,
        "detected_types": detected_types,
        "all_centers": RECYCLING_CENTERS
    })

# --- Run the Server ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
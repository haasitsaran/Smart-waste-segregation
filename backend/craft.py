# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import requests
# import json
# import os
# from dotenv import load_dotenv
# from pymongo import MongoClient
# from urllib.parse import urlparse, parse_qs
# from googleapiclient.discovery import build # Import for Google API client
# from googleapiclient.errors import HttpError # Import HttpError for specific error handling

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
#     print(f"❌ Craft Service: Could not connect to MongoDB. Error: {e}")
#     client = None

# # --- Configuration ---
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # This is for Gemini model calls
# YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY") # This is for direct YouTube Data API calls

# if not GEMINI_API_KEY:
#     print("⚠️ Craft Service: GEMINI_API_KEY environment variable not set.")
# if not YOUTUBE_API_KEY:
#     print("⚠️ Craft Service: YOUTUBE_API_KEY environment variable not set.")


# # --- Initialize YouTube API Client ---
# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"
# youtube_client = None
# if YOUTUBE_API_KEY: # Use the dedicated YouTube API key here
#     try:
#         youtube_client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
#         print("✅ Craft Service: YouTube API client initialized.")
#     except Exception as e:
#         print(f"❌ Craft Service: Could not initialize YouTube API client. Error: {e}")
# else:
#     print("⚠️ Craft Service: YouTube API client not initialized because YOUTUBE_API_KEY is missing.")


# # --- API Endpoint to Generate Craft Ideas ---
# @app.route('/api/craft-ideas', methods=['GET'])
# def get_craft_ideas():
#     if not client:
#         return jsonify({"error": "Database connection not available"}), 500
#     if not GEMINI_API_KEY: # Still need Gemini key for the prompt generation
#         return jsonify({"error": "Gemini API key not configured for AI model."}), 500
#     if not YOUTUBE_API_KEY or not youtube_client: # Need YouTube key and client for search
#         return jsonify({"error": "YouTube API key or client not configured on the server."}), 500

#     try:
#         # 1. Get the latest detected item from history
#         latest_record = history_collection.find_one(sort=[("timestamp", -1)])
#         if not latest_record or not latest_record.get('detected_items'):
#             return jsonify({"error": "No detection history found. Please scan an item first."}), 404

#         item_name = latest_record['detected_items'][0]['name']
        
#         # 2. Use youtube_client to find relevant videos
#         print(f"--- Searching YouTube for craft ideas with: {item_name} ---")
        
#         # Perform the Youtube
#         search_response = youtube_client.search().list(
#             q=f"craft ideas with {item_name} recycling", # Added "recycling" for more relevant results
#             part="id,snippet",
#             maxResults=5, # Get 5 results to provide good context
#             type="video"
#         ).execute()

#         youtube_results = [] # Renamed for clarity to avoid conflict with import name 'youtube'
#         for item in search_response.get("items", []):
#             if item["id"]["kind"] == "youtube#video":
#                 youtube_results.append({
#                     "title": item["snippet"]["title"],
#                     "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}", # Use standard YouTube URL format
#                     "videoId": item["id"]["videoId"]
#                 })
        
#         # 3. Prepare the search results for the Gemini prompt
#         search_context = ""
#         if youtube_results:
#             search_context = "\n".join([f"Title: {res['title']}, URL: {res['url']}" for res in youtube_results])
        
#         if not search_context:
#             return jsonify({"error": f"Could not find YouTube videos for craft ideas with '{item_name}'. Please try scanning a different item or check your network connection."}), 404

#         # 4. Craft the prompt for Gemini
#         craft_prompt = (
#             f"You are a creative DIY expert. Based on the following Youtube results for '{item_name}', "
#             f"generate a list of 3-4 engaging craft video ideas. For each idea, provide a catchy title, "
#             f"a short, exciting description, the original waste type, and the YouTube video ID (the part after 'v='). "
#             f"Your response MUST be ONLY a valid JSON array of objects. Do not include any other text or markdown. "
#             f'Example format: [{{"title": "Example Title", "wasteType": "Plastic Bottle", "description": "A cool craft.", "videoId": "exampleID123"}}]. '
#             f"Here are the search results:\n{search_context}"
#         )

#         # 5. Make the API call to Gemini
#         payload = {
#             "contents": [{"parts": [{"text": craft_prompt}]}],
#             "generationConfig": { "temperature": 0.2 }
#         }
        
#         api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"
#         response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
#         response.raise_for_status()
#         result = response.json()

#         if 'candidates' in result and result['candidates']:
#             raw_text = result['candidates'][0]['content']['parts'][0]['text']
#             cleaned_text = raw_text.strip().replace('```json', '').replace('```', '').strip()
            
#             craft_ideas = json.loads(cleaned_text)

#             # 6. Post-process craft_ideas to ensure videoId is correctly assigned
#             # We already have videoId from the direct YouTube API call, so just ensure it's used.
#             # This loop ensures the videoId is taken from the actual search results
#             # if a title match is found, making it more robust.
#             for idea in craft_ideas:
#                 found_id = None
#                 # Iterate over the results from the actual YouTube API call
#                 for search_res in youtube_results: # Use the renamed variable here
#                     # A more robust check: see if the idea's title is contained in a search result's title
#                     if idea.get('title') and search_res['title'].lower() in idea['title'].lower():
#                         found_id = search_res['videoId']
#                         break
                
#                 if found_id:
#                     idea['videoId'] = found_id
#                 elif 'videoId' not in idea or not idea['videoId']:
#                     # Fallback: if no match found by title, and if YouTube results exist,
#                     # just assign the videoId of the first YouTube result.
#                     # This is a heuristic and might not be perfect for every case.
#                     if youtube_results:
#                         idea['videoId'] = youtube_results[0]['videoId']
#                     else:
#                         idea['videoId'] = '' # No video ID available
                
#                 # Ensure the frontend URL for YouTube is correct (not a googleusercontent.com one)
#                 # The frontend will construct its own YouTube embed/link.

#             return jsonify(craft_ideas)
#         else:
#             return jsonify({"error": "Could not generate craft ideas from AI model response (no candidates)."}), 500

#     except HttpError as e: # Catch HttpError specifically for YouTube API issues
#         print(f"❌ YouTube API Error: {e.resp.status} - {e.content.decode()}")
#         return jsonify({"error": f"YouTube API Error: {e.content.decode()}"}), e.resp.status
#     except requests.exceptions.RequestException as e:
#         print(f"❌ Gemini API communication failed: {e}")
#         return jsonify({"error": f"Gemini API communication failed: {e}"}), 500
#     except (KeyError, IndexError, json.JSONDecodeError) as e:
#         print(f"❌ Error processing AI model result: {e}. Raw response might be malformed JSON.")
#         return jsonify({"error": f"Failed to parse AI model result or missing data: {e}"}), 500
#     except Exception as e:
#         print(f"❌ An unexpected error occurred: {e}")
#         return jsonify({"error": f"An internal error occurred while generating ideas: {e}"}), 500

# # --- Run the Craft Video Server ---
# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build # Import for Google API client
from googleapiclient.errors import HttpError # Import HttpError for specific error handling

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
    print(f"❌ Craft Service: Could not connect to MongoDB. Error: {e}")
    client = None

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # This is for Gemini model calls
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY") # This is for direct YouTube Data API calls

if not GEMINI_API_KEY:
    print("⚠️ Craft Service: GEMINI_API_KEY environment variable not set.")
if not YOUTUBE_API_KEY:
    print("⚠️ Craft Service: YOUTUBE_API_KEY environment variable not set.")


# --- Initialize YouTube API Client ---
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube_client = None
if YOUTUBE_API_KEY: # Use the dedicated YouTube API key here
    try:
        youtube_client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
        print("✅ Craft Service: YouTube API client initialized.")
    except Exception as e:
        print(f"❌ Craft Service: Could not initialize YouTube API client. Error: {e}")
else:
    print("⚠️ Craft Service: YouTube API client not initialized because YOUTUBE_API_KEY is missing.")


# --- API Endpoint to Generate Craft Ideas ---
@app.route('/api/craft-ideas', methods=['GET'])
def get_craft_ideas():
    if not client:
        return jsonify({"error": "Database connection not available"}), 500
    if not GEMINI_API_KEY: # Still need Gemini key for the prompt generation
        return jsonify({"error": "Gemini API key not configured for AI model."}), 500
    if not YOUTUBE_API_KEY or not youtube_client: # Need YouTube key and client for search
        return jsonify({"error": "YouTube API key or client not configured on the server."}), 500

    try:
        # 1. Get the latest detected item from history
        latest_record = history_collection.find_one(sort=[("timestamp", -1)])
        if not latest_record or not latest_record.get('detected_items'):
            return jsonify({"error": "No detection history found. Please scan an item first."}), 404

        item_name = latest_record['detected_items'][0]['name']

        # 2. Use youtube_client to find relevant videos
        print(f"--- Searching YouTube for craft ideas with: {item_name} ---")

        # Perform the Youtube
        search_response = youtube_client.search().list(
            q=f"craft ideas with {item_name} recycling", # Added "recycling" for more relevant results
            part="id,snippet",
            maxResults=5, # Get 5 results to provide good context
            type="video"
        ).execute()

        youtube_results = [] # Renamed for clarity to avoid conflict with import name 'youtube'
        for item in search_response.get("items", []):
            if item["id"]["kind"] == "youtube#video":
                # Extract thumbnail URL (using 'medium' quality)
                thumbnail_url = ""
                if "thumbnails" in item["snippet"] and "medium" in item["snippet"]["thumbnails"]:
                    thumbnail_url = item["snippet"]["thumbnails"]["medium"]["url"]

                youtube_results.append({
                    "title": item["snippet"]["title"],
                    # Use standard YouTube URL format for playback/linking
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "videoId": item["id"]["videoId"],
                    "thumbnailUrl": thumbnail_url # <--- ADDED THIS LINE
                })

        # 3. Prepare the search results for the Gemini prompt
        search_context = ""
        if youtube_results:
            search_context = "\n".join([f"Title: {res['title']}, URL: {res['url']}, VideoID: {res['videoId']}, Thumbnail: {res['thumbnailUrl']}" for res in youtube_results]) # <--- Updated search_context
        
        if not search_context:
            return jsonify({"error": f"Could not find YouTube videos for craft ideas with '{item_name}'. Please try scanning a different item or check your network connection."}), 404

        # 4. Craft the prompt for Gemini
        # Instruct Gemini to include thumbnailUrl in its JSON output
        craft_prompt = (
            f"You are a creative DIY expert. Based on the following Youtube results for '{item_name}', "
            f"generate a list of 3-4 engaging craft video ideas. For each idea, provide a catchy title, "
            f"a short, exciting description, the original waste type, the YouTube video ID (the part after 'v='), "
            f"and the YouTube thumbnail URL. " # <--- ADDED thumbnail URL instruction
            f"Your response MUST be ONLY a valid JSON array of objects. Do not include any other text or markdown. "
            f'Example format: [{{"title": "Example Title", "wasteType": "Plastic Bottle", "description": "A cool craft.", "videoId": "exampleID123", "thumbnailUrl": "https://example.com/thumb.jpg"}}]. ' # <--- Updated example format
            f"Here are the search results:\n{search_context}"
        )

        # 5. Make the API call to Gemini
        payload = {
            "contents": [{"parts": [{"text": craft_prompt}]}],
            "generationConfig": { "temperature": 0.2 }
        }

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        if 'candidates' in result and result['candidates']:
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            cleaned_text = raw_text.strip().replace('```json', '').replace('```', '').strip()

            craft_ideas = json.loads(cleaned_text)

            # 6. Post-process craft_ideas to ensure videoId and thumbnailUrl are correctly assigned
            # This loop ensures the videoId and thumbnailUrl are taken from the actual search results
            for idea in craft_ideas:
                found_id = None
                found_thumbnail = None
                # Iterate over the results from the actual YouTube API call
                for search_res in youtube_results:
                    # A more robust check: see if the idea's title is contained in a search result's title
                    if idea.get('title') and search_res['title'].lower() in idea['title'].lower():
                        found_id = search_res['videoId']
                        found_thumbnail = search_res['thumbnailUrl']
                        break

                if found_id:
                    idea['videoId'] = found_id
                elif 'videoId' not in idea or not idea['videoId']:
                    if youtube_results:
                        idea['videoId'] = youtube_results[0]['videoId']
                    else:
                        idea['videoId'] = '' # No video ID available

                if found_thumbnail: # <--- ADDED THIS BLOCK
                    idea['thumbnailUrl'] = found_thumbnail
                elif 'thumbnailUrl' not in idea or not idea['thumbnailUrl']:
                    if youtube_results:
                        idea['thumbnailUrl'] = youtube_results[0]['thumbnailUrl']
                    else:
                        idea['thumbnailUrl'] = '' # No thumbnail available

            return jsonify(craft_ideas)
        else:
            return jsonify({"error": "Could not generate craft ideas from AI model response (no candidates)."}), 500

    except HttpError as e: # Catch HttpError specifically for YouTube API issues
        print(f"❌ YouTube API Error: {e.resp.status} - {e.content.decode()}")
        return jsonify({"error": f"YouTube API Error: {e.content.decode()}"}), e.resp.status
    except requests.exceptions.RequestException as e:
        print(f"❌ Gemini API communication failed: {e}")
        return jsonify({"error": f"Gemini API communication failed: {e}"}), 500
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"❌ Error processing AI model result: {e}. Raw response might be malformed JSON.")
        return jsonify({"error": f"Failed to parse AI model result or missing data: {e}"}), 500
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return jsonify({"error": f"An internal error occurred while generating ideas: {e}"}), 500

# --- Run the Craft Video Server ---
if __name__ == '__main__':
    app.run(debug=True, port=5001)
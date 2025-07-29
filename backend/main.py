# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from ultralytics import YOLO
# import cv2
# import numpy as np
# import io

# # --- Initialize Flask App ---
# app = Flask(__name__)
# # Enable CORS to allow requests from your React frontend
# CORS(app)

# # --- Configuration ---
# # IMPORTANT: Make sure this path is correct relative to where you run the server.py file.
# # You might need to adjust it e.g., to 'yolo11n.pt' if it's in the same folder.
# MODEL_PATH = 'backend/yolo11n.pt'
# CONFIDENCE_THRESHOLD = 0.45

# # --- Waste Categorization & Bin Information ---
# # This dictionary maps detected objects to a category and provides disposal info.
# WASTE_INFO_MAPPING = {
#     # Biological
#     'banana': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Remove any stickers.", "Can be composted at home."]},
#     'apple': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Compost the core and seeds.", "Great for gardens."]},
#     'sandwich': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Remove non-compostable wrapping.", "Eat your leftovers!"]},
#     'orange': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Peels are great for compost.", "Avoid waxed peels in worm farms."]},
#     'broccoli': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Stalks are also compostable.", "Chop up to speed decomposition."]},
#     'carrot': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Tops and peels are compostable.", "A favorite for many compost heaps."]},
#     'hot dog': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Remove from bun if throwing separately.", "Meat products can attract pests in open compost."]},
#     'pizza': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Greasy boxes should not be recycled with paper.", "Food scraps are compostable."]},
#     'donut': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Best to eat it!", "Compostable if it's gone stale."]},
#     'cake': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Sugary items can go in green bins.", "Remove any plastic decorations."]},

#     # Paper
#     'book': {'category': 'paper', 'bin': 'Blue Bin (Paper)', 'tips': ["Donate if in good condition.", "Hardcovers may need to be disassembled."]},
    
#     # Glass
#     'wine glass': {'category': 'glass', 'bin': 'Check Local Rules', 'tips': ["Drinking glasses are often not recyclable with bottles/jars.", "Donate if not broken."]},
#     'cup': {'category': 'glass', 'bin': 'Check Local Rules', 'tips': ["Ceramic/Pyrex cups are not recyclable.", "Glass cups are often not either."]},
    
#     # Metal
#     'fork': {'category': 'metal', 'bin': 'General Waste or Metal Recycling', 'tips': ["Scrap metal facilities accept these.", "Not for curbside recycling."]},
#     'knife': {'category': 'metal', 'bin': 'General Waste or Metal Recycling', 'tips': ["Wrap sharp edges for safety.", "Donate to charity if in a set."]},
#     'spoon': {'category': 'metal', 'bin': 'General Waste or Metal Recycling', 'tips': ["A single spoon is usually not for curbside.", "Donate if possible."]},
#     'scissors': {'category': 'metal', 'bin': 'General Waste or Metal Recycling', 'tips': ["Wrap sharp edges.", "Check local scrap metal rules."]},
    
#     # Plastic
#     'bottle': {'category': 'plastic', 'bin': 'Blue Bin (Plastics)', 'tips': ["Empty and rinse.", "Keep the cap on."]},
#     'sports ball': {'category': 'plastic', 'bin': 'General Waste', 'tips': ["Usually not recyclable.", "Donate if still usable."]},
    
#     # E-Waste
#     'cell phone': {'category': 'e-waste', 'bin': 'E-Waste Drop-off', 'tips': ["Do not put in any bin!", "Contains hazardous materials.", "Wipe your data before recycling."]},
#     'laptop': {'category': 'e-waste', 'bin': 'E-Waste Drop-off', 'tips': ["Find a certified e-waste recycler.", "Never put in household bins."]},
#     'mouse': {'category': 'e-waste', 'bin': 'E-Waste Drop-off', 'tips': ["A common electronic item.", "Recycle with other computer peripherals."]},
#     'remote': {'category': 'e-waste', 'bin': 'E-Waste Drop-off', 'tips': ["Remove batteries before recycling.", "Batteries are recycled separately."]},
#     'keyboard': {'category': 'e-waste', 'bin': 'E-Waste Drop-off', 'tips': ["Can be recycled with other electronics.", "Consider donating if it works."]},
# }


# # --- Load The YOLO Model ---
# try:
#     model = YOLO(MODEL_PATH)
#     # Get the class names from the model
#     class_names = model.names
#     print(f"✅ Model '{MODEL_PATH}' loaded successfully.")
# except Exception as e:
#     print(f"❌ Error loading model from '{MODEL_PATH}'. Please ensure the path is correct.")
#     print(e)
#     model = None


# # --- The Main Detection Function ---
# def detect_waste_from_image(image_bytes):
#     """
#     Receives image bytes, runs YOLO detection, and returns structured results.
#     """
#     if not model:
#         return {"error": "Model is not loaded."}

#     # Convert image bytes to an OpenCV image
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     if frame is None:
#         return {"error": "Could not decode image."}

#     # Perform inference
#     results = model(frame, verbose=False) # verbose=False keeps the console clean
    
#     detections = []
#     # Process results
#     for r in results:
#         for box in r.boxes:
#             confidence = float(box.conf[0])
#             if confidence > CONFIDENCE_THRESHOLD:
#                 original_class_name = class_names[int(box.cls[0])]
                
#                 # Check if the detected object is in our mapping
#                 if original_class_name in WASTE_INFO_MAPPING:
#                     info = WASTE_INFO_MAPPING[original_class_name]
#                     detections.append({
#                         "name": original_class_name.replace('_', ' ').capitalize(),
#                         "confidence": int(confidence * 100),
#                         "binDescription": info['bin'],
#                         "tips": info['tips']
#                     })

#     if not detections:
#         return {
#             "name": "No recognizable waste detected",
#             "confidence": 100,
#             "binDescription": "Point the camera at a single item and try again.",
#             "tips": ["Ensure the object is well-lit.", "Get closer to the object."]
#         }

#     # Return the most confident detection
#     most_confident_detection = max(detections, key=lambda x: x['confidence'])
#     return most_confident_detection


# # --- API Endpoint ---
# @app.route('/api/detect', methods=['POST'])
# def detect_waste_endpoint():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file provided"}), 400

#     file = request.files['image']
#     image_bytes = file.read()

#     # Get the analysis from our new YOLO function
#     analysis_result = detect_waste_from_image(image_bytes)

#     if "error" in analysis_result:
#         return jsonify(analysis_result), 500

#     return jsonify(analysis_result)


# # --- Run the Server ---
# if __name__ == '__main__':
#     # Runs the server on http://127.0.0.1:5000
#     app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import numpy as np
import io

# --- Initialize Flask App ---
app = Flask(__name__)
CORS(app)

# --- Configuration ---
MODEL_PATH = 'backend/yolo11n.pt'
CONFIDENCE_THRESHOLD = 0.45

# --- Waste Categorization & Bin Information ---
WASTE_INFO_MAPPING = {
    # This mapping remains the same as before...
    'banana': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Remove any stickers.", "Can be composted at home."]},
    'apple': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Compost the core and seeds.", "Great for gardens."]},
    'sandwich': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Remove non-compostable wrapping.", "Eat your leftovers!"]},
    'orange': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Peels are great for compost.", "Avoid waxed peels in worm farms."]},
    'broccoli': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Stalks are also compostable.", "Chop up to speed decomposition."]},
    'carrot': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Tops and peels are compostable.", "A favorite for many compost heaps."]},
    'hot dog': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Remove from bun if throwing separately.", "Meat products can attract pests in open compost."]},
    'pizza': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Greasy boxes should not be recycled with paper.", "Food scraps are compostable."]},
    'donut': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Best to eat it!", "Compostable if it's gone stale."]},
    'cake': {'category': 'biological', 'bin': 'Green Bin (Compost)', 'tips': ["Sugary items can go in green bins.", "Remove any plastic decorations."]},
    'book': {'category': 'paper', 'bin': 'Blue Bin (Paper)', 'tips': ["Donate if in good condition.", "Hardcovers may need to be disassembled."]},
    'wine glass': {'category': 'glass', 'bin': 'Check Local Rules', 'tips': ["Drinking glasses are often not recyclable with bottles/jars.", "Donate if not broken."]},
    'cup': {'category': 'glass', 'bin': 'Check Local Rules', 'tips': ["Ceramic/Pyrex cups are not recyclable.", "Glass cups are often not either."]},
    'fork': {'category': 'metal', 'bin': 'General Waste or Metal Recycling', 'tips': ["Scrap metal facilities accept these.", "Not for curbside recycling."]},
    'knife': {'category': 'metal', 'bin': 'General Waste or Metal Recycling', 'tips': ["Wrap sharp edges for safety.", "Donate to charity if in a set."]},
    'spoon': {'category': 'metal', 'bin': 'General Waste or Metal Recycling', 'tips': ["A single spoon is usually not for curbside.", "Donate if possible."]},
    'scissors': {'category': 'metal', 'bin': 'General Waste or Metal Recycling', 'tips': ["Wrap sharp edges.", "Check local scrap metal rules."]},
    'bottle': {'category': 'plastic', 'bin': 'Blue Bin (Plastics)', 'tips': ["Empty and rinse.", "Keep the cap on."]},
    'sports ball': {'category': 'plastic', 'bin': 'General Waste', 'tips': ["Usually not recyclable.", "Donate if still usable."]},
    'cell phone': {'category': 'e-waste', 'bin': 'E-Waste Drop-off', 'tips': ["Do not put in any bin!", "Contains hazardous materials.", "Wipe your data before recycling."]},
    'laptop': {'category': 'e-waste', 'bin': 'E-Waste Drop-off', 'tips': ["Find a certified e-waste recycler.", "Never put in household bins."]},
    'mouse': {'category': 'e-waste', 'bin': 'E-Waste Drop-off', 'tips': ["A common electronic item.", "Recycle with other computer peripherals."]},
    'remote': {'category': 'e-waste', 'bin': 'E-Waste Drop-off', 'tips': ["Remove batteries before recycling.", "Batteries are recycled separately."]},
    'keyboard': {'category': 'e-waste', 'bin': 'E-Waste Drop-off', 'tips': ["Can be recycled with other electronics.", "Consider donating if it works."]},
}

# --- Load The YOLO Model ---
try:
    model = YOLO(MODEL_PATH)
    class_names = model.names
    print(f"✅ Model '{MODEL_PATH}' loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model from '{MODEL_PATH}'.")
    model = None

# --- The Main Detection Function ---
def detect_waste_from_image(image_bytes):
    if not model:
        return {"error": "Model is not loaded."}

    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is None:
        return {"error": "Could not decode image."}

    results = model(frame, verbose=False)
    
    detections = []
    for r in results:
        for box in r.boxes:
            confidence = float(box.conf[0])
            if confidence > CONFIDENCE_THRESHOLD:
                original_class_name = class_names[int(box.cls[0])]
                if original_class_name in WASTE_INFO_MAPPING:
                    info = WASTE_INFO_MAPPING[original_class_name]
                    detections.append({
                        "name": original_class_name.replace('_', ' ').capitalize(),
                        "confidence": int(confidence * 100),
                        "binDescription": info['bin'],
                        "tips": info['tips']
                    })

    # --- CHANGE: Return all sorted detections, not just the most confident one ---
    sorted_detections = sorted(detections, key=lambda x: x['confidence'], reverse=True)
    return sorted_detections # This will be a list of objects, or an empty list.

# --- API Endpoint ---
@app.route('/api/detect', methods=['POST'])
def detect_waste_endpoint():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    image_bytes = file.read()
    analysis_result = detect_waste_from_image(image_bytes)

    if "error" in analysis_result:
        return jsonify(analysis_result), 500

    # The result is already a JSON-serializable list
    return jsonify(analysis_result)

# --- Run the Server ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)

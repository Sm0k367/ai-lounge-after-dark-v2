from flask import request, jsonify, current_app
from app.api import bp
from app.services.hf_inference import HFInferenceService

@bp.route('/generate', methods=['POST'])
def generate_video():
    """
    Handles image upload, calls Hugging Face API via service, and returns video URL.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No selected image file"}), 400

    if image_file:
        hf_service = HFInferenceService()
        image_data = image_file.read()
        
        result = hf_service.generate_video_from_image(image_data)

        if isinstance(result, dict) and result.get("status") == "error":
            return jsonify({"error": result["message"]}), 500
        elif isinstance(result, dict) and result.get("status") == "loading":
            return jsonify({"message": result["message"], "status": "loading"}), 202 # Accepted, but not complete
        elif isinstance(result, str): # This is the video URL
            return jsonify({"video_url": result}), 200
        else:
            return jsonify({"error": "An unexpected response was received from the video generation service."}), 500
    
    return jsonify({"error": "Invalid request"}), 400
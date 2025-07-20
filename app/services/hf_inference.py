import requests
import os
import uuid
from flask import current_app

class HFInferenceService:
    def __init__(self):
        self.api_url = current_app.config['HF_API_URL']
        self.headers = {"Authorization": f"Bearer {current_app.config['HF_API_TOKEN']}"}
        self.videos_dir = os.path.join(current_app.root_path, current_app.config['VIDEOS_FOLDER'])

    def generate_video_from_image(self, image_data):
        """
        Calls the Hugging Face Inference API to generate a video from image data.
        Saves the video locally and returns its URL.
        """
        if not current_app.config['HF_API_TOKEN']:
            raise ValueError("Hugging Face API token is not configured.")

        try:
            response = requests.post(self.api_url, headers=self.headers, data=image_data)
            response.raise_for_status() # Raise an exception for HTTP errors

            if response.headers.get('Content-Type') == 'video/mp4':
                video_filename = f"{uuid.uuid4()}.mp4"
                video_path = os.path.join(self.videos_dir, video_filename)

                with open(video_path, 'wb') as f:
                    f.write(response.content)

                video_url = f"/videos/{video_filename}"
                return video_url
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get("error", "Unknown API error")
                    if "loading" in error_message.lower():
                        return {"status": "loading", "message": "Model is currently loading. Please try again in a few moments."}
                    return {"status": "error", "message": f"Hugging Face API error: {error_message}"}
                except ValueError:
                    return {"status": "error", "message": f"Hugging Face API returned non-JSON error: {response.text}"}

        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Network or API request error: {e}")
            return {"status": "error", "message": f"Network or API request error: {str(e)}"}
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred during video generation: {e}")
            return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
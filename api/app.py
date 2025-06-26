import os
from flask import Flask, render_template, request, session
import requests
import traceback

# Ensure the required environment variables are set
app = Flask(__name__, template_folder="../templates", static_folder="../static")

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")

app.secret_key = os.environ.get("SECRET_KEY", "dev")  

# Ensure the secret key is set for session management
@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    photographer_name = None
    photographer_url = None
    if "gallery" not in session:
        session["gallery"] = []
    try:
        if request.method == "POST":
            prompt = request.form.get("prompt")
            if prompt:
                response = requests.get(
                    "https://api.unsplash.com/photos/random",
                    params={
                        "query": prompt,
                        "orientation": "landscape",
                        "client_id": UNSPLASH_ACCESS_KEY
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    image_url = data["urls"]["regular"]
                    photographer_name = data["user"]["name"]
                    photographer_url = data["user"]["links"]["html"]
                    # Save to gallery
                    session["gallery"].append({
                        "image_url": image_url,
                        "photographer_name": photographer_name,
                        "photographer_url": photographer_url
                    })
                    session.modified = True
                else:
                    print("Error:", response.status_code, response.text)
        return render_template(
            "index.html",
            image_url=image_url,
            photographer_name=photographer_name,
            photographer_url=photographer_url,
            gallery=session.get("gallery", [])
        )
    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return "Internal Server Error", 500

# Route to get the gallery
@app.route("/reset", methods=["POST"])
def reset_gallery():
    session["gallery"] = []
    session.modified = True
    return ("", 204) # Reset the gallery without content  

if __name__ == "__main__":
    app.run(debug=True)



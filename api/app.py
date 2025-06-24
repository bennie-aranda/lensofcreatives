import os
from flask import Flask, render_template, request
import requests
import traceback

app = Flask(__name__, template_folder="../templates", static_folder="../static")

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    photographer_name = None
    photographer_url = None
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
                else:
                    print("Error:", response.status_code, response.text)
        return render_template(
            "index.html",
            image_url=image_url,
            photographer_name=photographer_name,
            photographer_url=photographer_url
        )
    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(debug=True)
    
    # this is a comment
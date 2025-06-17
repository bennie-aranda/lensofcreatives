from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 🔑 Replace with your actual Unsplash Access Key
UNSPLASH_ACCESS_KEY = 'DTLEWE9_Pd90KFiBxY70nt2AHkMi4_Vm3nDUhJi557A'

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None

    if request.method == "POST":
        mood = request.form.get("mood")
        if mood:
            try:
                response = requests.get(
                    "https://api.unsplash.com/photos/random",
                    params={
                        "query": mood,
                        "orientation": "landscape",
                        "client_id": UNSPLASH_ACCESS_KEY
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    image_url = data["urls"]["regular"]
                else:
                    print("Error:", response.status_code, response.text)
            except Exception as e:
                print("Exception occurred:", e)

    return render_template("index.html", image_url=image_url)

    handler = app
import os
from flask import Flask, render_template, request, session
import requests
import traceback
import json
import re
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import secrets

# Ensure the required environment variables are set
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Security Configuration
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
if not app.config['SECRET_KEY']:
    print("WARNING: SECRET_KEY not set, using fallback (NOT SECURE FOR PRODUCTION)")
    app.config['SECRET_KEY'] = "temporary-dev-key-change-in-production"

# Initialize security extensions only if in production
if os.environ.get("FLASK_ENV") == "production":
    # Force HTTPS and set security headers
    Talisman(app, 
        force_https=True,
        strict_transport_security=True,
        content_security_policy={
            'default-src': "'self'",
            'img-src': "'self' https://images.unsplash.com https://unsplash.com",
            'font-src': "'self' https://fonts.googleapis.com https://fonts.gstatic.com",
            'style-src': "'self' 'unsafe-inline' https://fonts.googleapis.com",
            'script-src': "'self' 'unsafe-inline'"
        })
    
    # Rate limiting
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
else:
    print("Development mode: Security features disabled")
    # Create a dummy limiter for development
    class DummyLimiter:
        def limit(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator
    limiter = DummyLimiter()

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")

if not UNSPLASH_ACCESS_KEY:
    print("WARNING: UNSPLASH_ACCESS_KEY not set, app may not function properly")

# AI keyword expansion using Hugging Face API
def expand_prompt_with_ai(user_prompt):
    """
    Use Hugging Face API to expand user prompt into better search keywords
    Falls back to original prompt if API fails
    """
    try:
        # Hugging Face API endpoint for text generation
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        # Create a prompt for keyword expansion
        expansion_prompt = f"Generate visual search keywords for: {user_prompt}. Keywords:"
        
        if not HUGGINGFACE_API_TOKEN:
            return enhance_prompt_fallback(user_prompt)
            
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": expansion_prompt,
            "parameters": {
                "max_new_tokens": 20,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # Extract keywords and clean them
                keywords = re.findall(r'\b\w+\b', generated_text.lower())
                # Filter out common words and keep relevant ones
                filtered_keywords = [k for k in keywords if len(k) > 2 and k not in ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all']]
                
                if filtered_keywords:
                    # Combine original prompt with AI-generated keywords
                    enhanced_prompt = f"{user_prompt} {' '.join(filtered_keywords[:3])}"
                    print(f"AI Enhanced: '{user_prompt}' -> '{enhanced_prompt}'")
                    return enhanced_prompt
    
    except Exception as e:
        print(f"AI expansion failed: {e}")
    
    # Fallback to simple keyword mapping if AI fails
    return enhance_prompt_fallback(user_prompt)

def enhance_prompt_fallback(user_prompt):
    """
    Simple keyword enhancement as fallback
    """
    keyword_map = {
        # Emotions -> Visual concepts
        'sad': 'melancholy rain gray solitude',
        'happy': 'bright colorful joy sunshine',
        'calm': 'peaceful serene nature zen',
        'energetic': 'dynamic vibrant movement',
        'creative': 'art inspiration design abstract',
        'focused': 'minimal clean workspace concentration',
        'motivated': 'success achievement goals mountain',
        'relaxed': 'beach sunset comfortable cozy',
        'inspired': 'light creativity innovation',
        'nostalgic': 'vintage retro memories warm',
        
        # Abstract concepts -> Concrete visuals
        'growth': 'plants sprouting sunrise progress',
        'freedom': 'open road birds flying sky',
        'strength': 'mountains rocks powerful',
        'beauty': 'flowers landscape elegant',
        'adventure': 'hiking travel exploration',
        'peace': 'meditation nature quiet',
        'innovation': 'technology modern futuristic',
        'teamwork': 'collaboration together unity',
    }
    
    enhanced = user_prompt.lower()
    for key, expansion in keyword_map.items():
        if key in enhanced:
            enhanced = f"{user_prompt} {expansion}"
            print(f"Fallback Enhanced: '{user_prompt}' -> '{enhanced}'")
            break
    
    return enhanced

# Main route with rate limiting
@app.route("/", methods=["GET", "POST"])
@limiter.limit("10 per minute")
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
                # 🤖 AI Enhancement: Expand user prompt with AI-generated keywords
                enhanced_prompt = expand_prompt_with_ai(prompt)
                
                response = requests.get(
                    "https://api.unsplash.com/photos/random",
                    params={
                        "query": enhanced_prompt,  # Use AI-enhanced prompt
                        "orientation": "landscape",
                        "client_id": UNSPLASH_ACCESS_KEY
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    # Validate response data
                    if "urls" in data and "regular" in data["urls"]:
                        image_url = data["urls"]["regular"]
                        photographer_name = data.get("user", {}).get("name", "Unknown")
                        photographer_url = data.get("user", {}).get("links", {}).get("html", "#")
                        # Save to gallery with validation
                        if image_url and photographer_name:
                            session["gallery"].append({
                                "image_url": image_url,
                                "photographer_name": photographer_name,
                                "photographer_url": photographer_url
                            })
                            session.modified = True
                    else:
                        print("Invalid response format from Unsplash API")
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

# Route to reset gallery with rate limiting
@app.route("/reset", methods=["POST"])
@limiter.limit("5 per minute")
def reset_gallery():
    session["gallery"] = []
    session.modified = True
    return ("", 204) # Reset the gallery without content  

if __name__ == "__main__":
    # Only enable debug in development
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode)



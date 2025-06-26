# Lens of Creatives - Security Update

## 🚨 IMPORTANT: Security Configuration Required

This update includes critical security improvements. You **MUST** configure environment variables before deployment.

## Required Environment Variables

Set these in your production environment (Vercel, Heroku, etc.):

```bash
# Generate a new secret key with: python3 -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-generated-secret-key-here

# Your API keys:
UNSPLASH_ACCESS_KEY=your-unsplash-access-key-here
HUGGINGFACE_API_TOKEN=your-huggingface-token-here

# Environment setting:
FLASK_ENV=production
```

## Security Features Added

✅ **HTTPS Enforcement** - Forces secure connections  
✅ **Rate Limiting** - Prevents abuse (10 requests/minute per IP)  
✅ **Security Headers** - CSP, HSTS, X-Frame-Options  
✅ **Secret Key Validation** - No more hardcoded secrets  
✅ **API Token Security** - All tokens from environment variables  
✅ **Input Validation** - Validates API responses  
✅ **Debug Mode Control** - Only enabled in development  

---

# Lens of Creatives

> **Find your next visual inspiration with AI-powered creativity**

A modern web app that displays inspiring images based on user prompts, enhanced with AI-powered keyword expansion and beautiful responsive design.

🌐 **Live Site:** https://www.lensofcreatives.com/

---

## ✨ Features

### 🤖 **AI-Powered Enhancement**
- **Intelligent keyword expansion** using Hugging Face API
- **Semantic understanding** of emotions and abstract concepts
- **Smart fallback system** for reliable operation
- **Enhanced search relevancy** for better visual matches

### 🎨 **Modern Design**
- **Beautiful gradient background** that complements hero imagery
- **Mountain landscape hero section** with stunning overlay effects
- **Google Fonts integration** (Inter) for modern typography
- **Smooth animations** and hover effects throughout
- **Professional shadows** and depth for visual appeal

### 📱 **Mobile-First Experience**
- **Fully responsive design** optimized for all devices
- **Touch-friendly interactions** with proper tap targets
- **Mobile-specific optimizations** and layouts
- **iOS Safari compatibility** with webkit fixes
- **Progressive enhancement** for better performance

### 🖼️ **Image Experience**
- **High-quality landscape images** from Unsplash API
- **Photographer attribution** with direct profile links
- **Image gallery** for browsing previous inspirations
- **Smooth loading animations** and transitions
- **One-click reset** functionality for fresh starts

---

## 🎯 How It Works

1. **User Input:** Enter any creative prompt (e.g., "feeling inspired", "need motivation")
2. **AI Enhancement:** System expands prompt with relevant visual keywords
3. **Smart Search:** Enhanced query searches Unsplash for perfect matches
4. **Beautiful Display:** Image appears with smooth animations and proper attribution
5. **Gallery Building:** Previous searches build a personal inspiration gallery

### 🧠 **AI Enhancement Examples:**
- `"feeling sad"` → `"feeling sad melancholy rain gray solitude"`
- `"creative inspiration"` → `"creative inspiration art design abstract"`
- `"adventure calling"` → `"adventure calling hiking travel exploration"`

---

## 🛠️ Tech Stack

### **Frontend**
- **HTML5** with semantic structure
- **Modern CSS** with Grid/Flexbox layouts
- **Vanilla JavaScript** for interactions
- **Google Fonts** (Inter) for typography
- **CSS Custom Properties** for theming

### **Backend**
- **Python 3.9+** with Flask framework
- **Hugging Face Transformers** for AI enhancement
- **Session management** for gallery persistence
- **Error handling** with graceful fallbacks

### **APIs & Services**
- **Unsplash API** for high-quality images
- **Hugging Face API** for AI text processing
- **Vercel** for serverless deployment

### **AI/ML**
- **Transformers library** for text processing
- **PyTorch** for model inference
- **Keyword mapping** fallback system
- **Semantic enhancement** algorithms

---

## 🚀 Getting Started

### **Prerequisites**
- Python 3.9 or higher
- Unsplash API account (free)
- Optional: Hugging Face account for production AI token

### **Local Development**
```bash
# Clone the repository
git clone https://github.com/bennie-aranda/lensofcreatives.git
cd lensofcreatives

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export UNSPLASH_ACCESS_KEY=your_unsplash_api_key
export SECRET_KEY=your_secret_key

# Run the application
python api/app.py
```

### **Testing AI Enhancement**
```bash
# Test the AI enhancement system
python test_ai_enhancement.py
```

### **Deployment**
The app is configured for **Vercel** deployment:
- Uses `vercel.json` for serverless configuration
- Environment variables set in Vercel dashboard
- Automatic deployments from GitHub

---

## 🔧 Configuration

### **Environment Variables**
```bash
UNSPLASH_ACCESS_KEY=your_unsplash_api_key    # Required
SECRET_KEY=your_flask_secret_key             # Required for sessions
HUGGINGFACE_TOKEN=your_hf_token             # Optional (uses demo token)
```

### **AI Enhancement Settings**
- **Free Tier**: Uses Hugging Face demo token (limited requests)
- **Production**: Set your own Hugging Face API token for unlimited usage
- **Fallback**: Always works with built-in keyword mapping

---

## 🧪 Features in Detail

### **Intelligent Keyword Expansion**
The AI system understands context and emotions:
- **Emotional states** → Visual concepts
- **Abstract ideas** → Concrete imagery
- **Mood descriptors** → Aesthetic styles
- **Creative prompts** → Artistic elements

### **Mobile Optimization**
- **Touch targets** sized for fingers (44px minimum)
- **Viewport optimization** for all screen sizes
- **Performance tuning** for mobile networks
- **iOS/Android compatibility** testing

### **Image Quality & Attribution**
- **High-resolution images** (1200px+ width)
- **Landscape orientation** for better display
- **Proper attribution** with photographer links
- **Loading optimization** with progressive enhancement

---

## 📊 Project Structure

```
lensofcreatives/
├── api/
│   └── app.py              # Flask backend with AI integration
├── static/
│   └── styles.css          # Modern CSS with mobile-first design
├── templates/
│   └── index.html          # HTML template with semantic structure
├── test_ai_enhancement.py  # AI testing script
├── requirements.txt        # Python dependencies
├── vercel.json            # Deployment configuration
└── README.md              # Project documentation
```

---

## 🔮 Future Enhancements

- [ ] **User accounts** for saving favorite inspirations
- [ ] **Advanced AI models** for even better keyword expansion
- [ ] **Multiple image orientations** (portrait, square)
- [ ] **Theme customization** and dark mode
- [ ] **Social sharing** features
- [ ] **Inspiration collections** and tagging
- [ ] **API rate limiting** and caching
- [ ] **Progressive Web App** features

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **[Unsplash](https://unsplash.com)** for providing beautiful, high-quality images
- **[Hugging Face](https://huggingface.co)** for AI/ML infrastructure and models
- **[Vercel](https://vercel.com)** for seamless deployment and hosting
- **[Google Fonts](https://fonts.google.com)** for the Inter typography

---

## 📞 Contact

**Bennie Aranda**  
- GitHub: [@bennie-aranda](https://github.com/bennie-aranda)  
- Website: [lensofcreatives.com](https://www.lensofcreatives.com)

---

*Built with ❤️ for creative minds everywhere*

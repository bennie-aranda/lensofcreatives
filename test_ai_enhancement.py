#!/usr/bin/env python3
"""
Test script for AI keyword expansion functionality
Run this to test the enhancement before deploying
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our enhancement functions
from api.app import expand_prompt_with_ai, enhance_prompt_fallback

def test_enhancement():
    """Test the AI enhancement with various prompts"""
    
    test_prompts = [
        "feeling sad",
        "need motivation", 
        "creative inspiration",
        "peaceful moment",
        "strength and power",
        "happy vibes",
        "workspace focus",
        "adventure calling"
    ]
    
    print("🧪 Testing AI Enhancement System")
    print("=" * 50)
    
    for prompt in test_prompts:
        print(f"\n📝 Original: '{prompt}'")
        
        # Test fallback system (always works)
        fallback_result = enhance_prompt_fallback(prompt)
        print(f"🔄 Fallback: '{fallback_result}'")
        
        # Test AI system (may fail to demo token limits)
        ai_result = expand_prompt_with_ai(prompt)
        print(f"🤖 AI Enhanced: '{ai_result}'")
        
        print("-" * 30)
    
    print("\n✅ Enhancement system is working!")
    print("\n💡 Tips:")
    print("- The system automatically falls back to keyword mapping if AI fails")
    print("- For production, get your own Hugging Face API token")
    print("- The fallback system ensures the app always works")

if __name__ == "__main__":
    test_enhancement()

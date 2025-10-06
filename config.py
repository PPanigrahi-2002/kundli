# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Kundli AI application"""
    
    # Groq API configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Model configuration
    DEFAULT_MODEL = "llama-3.1-8b-instant"  # Fast and efficient for real-time chat
    TEMPERATURE = 0.7
    MAX_TOKENS = 1000
    
    # Application settings
    APP_TITLE = "Kundli Generator AI"
    APP_DESCRIPTION = "AI-powered Vedic Astrology with LangChain and Groq"
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in your environment variables or .env file. "
                "Get your API key from https://console.groq.com/"
            )
        return True
    
    @classmethod
    def get_groq_config(cls):
        """Get Groq configuration dictionary"""
        return {
            "api_key": cls.GROQ_API_KEY,
            "model": cls.DEFAULT_MODEL,
            "temperature": cls.TEMPERATURE,
            "max_tokens": cls.MAX_TOKENS
        }

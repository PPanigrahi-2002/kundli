# ai_interpreter.py - Simplified version using Groq SDK directly
import os

DEPENDENCIES_AVAILABLE = True
IMPORT_ERROR_MSG = ""

try:
    from groq import Groq
except ImportError as e:
    IMPORT_ERROR_MSG = f"groq SDK failed: {e}"
    DEPENDENCIES_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

class KundliAIInterpreter:
    """
    AI-powered Kundli interpreter using Groq SDK directly
    Provides personalized astrological readings and interpretations
    """
    
    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError(f"Required AI dependencies are not installed. {IMPORT_ERROR_MSG}")
        
        # Get API key from config or environment
        try:
            from config import Config
            api_key = Config.GROQ_API_KEY
        except:
            api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("GROQ_API_KEY not found")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
        self.chat_history = []
    
    def _call_llm(self, system_prompt, user_prompt):
        """Call Groq LLM directly"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling AI: {str(e)}"
    
    def interpret_kundli(self, planets, ascendant, birth_info):
        """Generate comprehensive Kundli interpretation"""
        system_prompt = """You are an expert Vedic astrologer with deep knowledge of Jyotish (Indian astrology). 
        Analyze birth charts and provide comprehensive, accurate interpretations.
        Be warm, encouraging, and practical in your guidance."""
        
        planets_text = self._format_planets_for_ai(planets)
        
        user_prompt = f"""Analyze this Kundli (birth chart) and provide a comprehensive interpretation.
        
Birth Details: {birth_info}
Ascendant (Lagna): {ascendant}

Planetary Positions:
{planets_text}

Please provide:
1. Overall personality analysis based on ascendant and planetary positions
2. Key strengths and challenges indicated by the chart
3. Career and profession guidance
4. Relationship and marriage predictions
5. Health considerations
6. Lucky colors, numbers, and gemstones
7. General life guidance and remedies"""
        
        return self._call_llm(system_prompt, user_prompt)
    
    def get_daily_prediction(self, current_positions, birth_chart_summary):
        """Generate daily astrological predictions"""
        system_prompt = "You are a Vedic astrologer providing daily guidance. Be concise but meaningful."
        
        user_prompt = f"""Based on current planetary positions and the birth chart, provide today's predictions.

Current Positions: {current_positions}
Birth Chart: {birth_chart_summary}

Provide:
1. Today's overall energy
2. Best times for activities
3. Areas to focus on
4. Lucky colors and numbers
5. General advice"""
        
        return self._call_llm(system_prompt, user_prompt)
    
    def chat_with_astrologer(self, question, birth_chart_summary=""):
        """Chat with AI astrologer"""
        system_prompt = """You are a knowledgeable and friendly Vedic astrologer. 
        Answer questions about astrology accurately while being encouraging and helpful."""
        
        user_prompt = f"""Birth Chart Context: {birth_chart_summary}

Question: {question}

Provide a detailed, accurate answer based on Vedic astrology principles."""
        
        return self._call_llm(system_prompt, user_prompt)
    
    def get_astrological_insights(self, planets, ascendant, question_type="general"):
        """Get specific astrological insights"""
        system_prompt = f"You are a Vedic astrologer providing specific insights about {question_type}. Be practical and actionable."
        
        planets_text = self._format_planets_for_ai(planets)
        
        user_prompt = f"""Provide specific insights about {question_type} based on this birth chart:

Ascendant: {ascendant}
Planetary Positions:
{planets_text}

Focus specifically on {question_type} predictions, remedies, and guidance."""
        
        return self._call_llm(system_prompt, user_prompt)
    
    def _format_planets_for_ai(self, planets):
        """Format planetary positions for AI interpretation"""
        formatted_text = ""
        for planet, data in planets.items():
            formatted_text += f"{planet}: {data['degree']} (House {data['house']})\n"
        return formatted_text.strip()
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.chat_history = []

def create_ai_interpreter():
    """Create and return a new AI interpreter instance"""
    return KundliAIInterpreter()

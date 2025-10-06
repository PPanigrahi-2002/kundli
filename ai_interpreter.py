# ai_interpreter.py
import os
try:
    from langchain_groq import ChatGroq
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.memory import ConversationBufferMemory
    from dotenv import load_dotenv
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    print(f"AI dependencies not available: {e}")

if DEPENDENCIES_AVAILABLE:
    load_dotenv()

class KundliAIInterpreter:
    """
    AI-powered Kundli interpreter using LangChain and Groq
    Provides personalized astrological readings and interpretations
    """
    
    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Required AI dependencies are not installed. Please install langchain, langchain-groq, and python-dotenv.")
        
        # Initialize Groq chat model - using llama3-8b for fast responses
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.7,
            max_tokens=1000
        )
        
        # Setup memory for conversation context (using updated LangChain syntax)
        try:
            # Try the newer syntax first
            from langchain_community.memory import ConversationBufferMemory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history"
            )
        except ImportError:
            try:
                # Fallback to older syntax
                self.memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True
                )
            except Exception:
                # Final fallback - create a simple memory object
                self.memory = None
        
        # Create specialized prompts for different types of readings
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Setup different prompt templates for various astrological interpretations"""
        
        # Main Kundli interpretation prompt
        self.kundli_prompt = PromptTemplate(
            input_variables=["planets", "ascendant", "birth_info", "chat_history"],
            template="""
            You are an expert Vedic astrologer with deep knowledge of Jyotish (Indian astrology). 
            Analyze the following Kundli (birth chart) and provide a comprehensive interpretation.
            
            Birth Details: {birth_info}
            Ascendant (Lagna): {ascendant}
            
            Planetary Positions:
            {planets}
            
            Chat History: {chat_history}
            
            Please provide:
            1. Overall personality analysis based on ascendant and planetary positions
            2. Key strengths and challenges indicated by the chart
            3. Career and profession guidance based on planetary influences
            4. Relationship and marriage predictions
            5. Health considerations
            6. Lucky colors, numbers, and gemstones
            7. General life guidance and remedies
            
            Make the reading personal, insightful, and practical. Use traditional Vedic astrology 
            principles while making it accessible to modern readers. Keep the tone warm and encouraging.
            """
        )
        
        # Daily prediction prompt
        self.daily_prompt = PromptTemplate(
            input_variables=["current_positions", "birth_chart", "chat_history"],
            template="""
            You are a Vedic astrologer providing daily guidance. Based on the current planetary 
            positions and the person's birth chart, provide today's predictions.
            
            Current Planetary Positions: {current_positions}
            Birth Chart Summary: {birth_chart}
            
            Chat History: {chat_history}
            
            Provide:
            1. Today's overall energy and mood
            2. Best times for important activities
            3. Areas to focus on or avoid
            4. Lucky colors and numbers for today
            5. General advice and precautions
            
            Keep it concise but meaningful.
            """
        )
        
        # Chat prompt for general astrology questions
        self.chat_prompt = PromptTemplate(
            input_variables=["question", "birth_chart", "chat_history"],
            template="""
            You are a knowledgeable and friendly Vedic astrologer. Answer the user's question 
            about astrology, providing accurate information while being encouraging and helpful.
            
            User's Birth Chart Context: {birth_chart}
            Question: {question}
            Previous Conversation: {chat_history}
            
            Provide a detailed, accurate answer based on Vedic astrology principles. 
            If the question relates to their specific chart, incorporate relevant planetary 
            positions. Be warm, supportive, and practical in your guidance.
            """
        )
    
    def interpret_kundli(self, planets, ascendant, birth_info):
        """
        Generate comprehensive Kundli interpretation
        
        Args:
            planets: Dictionary of planetary positions
            ascendant: Ascendant information
            birth_info: Birth details (date, time, location)
            
        Returns:
            str: AI-generated Kundli interpretation
        """
        try:
            # Format planetary positions for the prompt
            planets_text = self._format_planets_for_ai(planets)
            
            # Create chain for Kundli interpretation
            if self.memory:
                kundli_chain = LLMChain(
                    llm=self.llm,
                    prompt=self.kundli_prompt,
                    memory=self.memory,
                    verbose=False
                )
            else:
                # Fallback without memory
                kundli_chain = LLMChain(
                    llm=self.llm,
                    prompt=self.kundli_prompt,
                    verbose=False
                )
            
            # Generate interpretation
            response = kundli_chain.run(
                planets=planets_text,
                ascendant=ascendant,
                birth_info=birth_info,
                chat_history=""
            )
            
            return response
            
        except Exception as e:
            return f"Sorry, I encountered an error while interpreting your Kundli: {str(e)}. Please try again."
    
    def get_daily_prediction(self, current_positions, birth_chart_summary):
        """
        Generate daily astrological predictions
        
        Args:
            current_positions: Current planetary positions
            birth_chart_summary: Summary of birth chart
            
        Returns:
            str: AI-generated daily prediction
        """
        try:
            if self.memory:
                daily_chain = LLMChain(
                    llm=self.llm,
                    prompt=self.daily_prompt,
                    memory=self.memory,
                    verbose=False
                )
            else:
                daily_chain = LLMChain(
                    llm=self.llm,
                    prompt=self.daily_prompt,
                    verbose=False
                )
            
            response = daily_chain.run(
                current_positions=current_positions,
                birth_chart=birth_chart_summary,
                chat_history=""
            )
            
            return response
            
        except Exception as e:
            return f"Sorry, I couldn't generate today's prediction: {str(e)}. Please try again."
    
    def chat_with_astrologer(self, question, birth_chart_summary=""):
        """
        Chat with AI astrologer for general questions
        
        Args:
            question: User's astrology-related question
            birth_chart_summary: Optional birth chart context
            
        Returns:
            str: AI astrologer's response
        """
        try:
            if self.memory:
                chat_chain = LLMChain(
                    llm=self.llm,
                    prompt=self.chat_prompt,
                    memory=self.memory,
                    verbose=False
                )
            else:
                chat_chain = LLMChain(
                    llm=self.llm,
                    prompt=self.chat_prompt,
                    verbose=False
                )
            
            response = chat_chain.run(
                question=question,
                birth_chart=birth_chart_summary,
                chat_history=""
            )
            
            return response
            
        except Exception as e:
            return f"Sorry, I couldn't process your question: {str(e)}. Please try again."
    
    def _format_planets_for_ai(self, planets):
        """
        Format planetary positions for AI interpretation
        
        Args:
            planets: Dictionary of planetary positions
            
        Returns:
            str: Formatted planetary information
        """
        formatted_text = ""
        for planet, data in planets.items():
            formatted_text += f"{planet}: {data['degree']} (House {data['house']})\n"
        
        return formatted_text.strip()
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
    
    def get_astrological_insights(self, planets, ascendant, question_type="general"):
        """
        Get specific astrological insights based on question type
        
        Args:
            planets: Planetary positions
            ascendant: Ascendant information
            question_type: Type of insight needed (career, love, health, etc.)
            
        Returns:
            str: Targeted astrological insight
        """
        try:
            # Create dynamic prompt based on question type
            insight_prompt = PromptTemplate(
                input_variables=["planets", "ascendant", "question_type"],
                template=f"""
                As a Vedic astrologer, provide specific insights about {question_type} based on this birth chart:
                
                Ascendant: {{ascendant}}
                Planetary Positions:
                {{planets}}
                
                Focus specifically on {question_type} predictions, remedies, and guidance. 
                Be practical and actionable in your advice.
                """
            )
            
            insight_chain = LLMChain(
                llm=self.llm,
                prompt=insight_prompt,
                verbose=False
            )
            
            planets_text = self._format_planets_for_ai(planets)
            response = insight_chain.run(
                planets=planets_text,
                ascendant=ascendant,
                question_type=question_type
            )
            
            return response
            
        except Exception as e:
            return f"Sorry, I couldn't provide {question_type} insights: {str(e)}. Please try again."

# Utility function to create interpreter instance
def create_ai_interpreter():
    """Create and return a new AI interpreter instance"""
    return KundliAIInterpreter()

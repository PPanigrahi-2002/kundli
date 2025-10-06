# ai_chat.py
import streamlit as st
try:
    from ai_interpreter import create_ai_interpreter, DEPENDENCIES_AVAILABLE
    from config import Config
    import json
except ImportError as e:
    st.error(f"AI features not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class KundliChatInterface:
    """
    Streamlit-based chat interface for AI-powered astrology conversations
    """
    
    def __init__(self):
        self.interpreter = None
        self.initialize_interpreter()
    
    def initialize_interpreter(self):
        """Initialize the AI interpreter with error handling"""
        if not DEPENDENCIES_AVAILABLE:
            return False
            
        try:
            Config.validate_config()
            self.interpreter = create_ai_interpreter()
            return True
        except ValueError as e:
            st.error(f"Configuration Error: {str(e)}")
            return False
        except Exception as e:
            st.error(f"Failed to initialize AI interpreter: {str(e)}")
            return False
    
    def render_chat_interface(self, birth_chart_data=None):
        """
        Render the main chat interface (legacy method - now handled in render_ai_features)
        
        Args:
            birth_chart_data: Optional birth chart data for personalized responses
        """
        if not self.interpreter:
            st.error("AI interpreter not available. Please check your configuration.")
            return
        
        # This method is now deprecated - chat interface is handled in render_ai_features
        st.info("Chat interface is now integrated into the main AI features section.")
    
    def get_ai_response(self, user_input, birth_chart_data=None):
        """
        Get AI response based on user input and birth chart context
        
        Args:
            user_input: User's question or message
            birth_chart_data: Optional birth chart data
            
        Returns:
            str: AI response
        """
        try:
            # Prepare birth chart context if available
            birth_chart_context = ""
            if birth_chart_data:
                birth_chart_context = self.format_birth_chart_context(birth_chart_data)
            
            # Get response from AI interpreter
            response = self.interpreter.chat_with_astrologer(
                question=user_input,
                birth_chart_summary=birth_chart_context
            )
            
            return response
            
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your question: {str(e)}. Please try again."
    
    def format_birth_chart_context(self, birth_chart_data):
        """
        Format birth chart data for AI context
        
        Args:
            birth_chart_data: Dictionary containing birth chart information
            
        Returns:
            str: Formatted birth chart context
        """
        try:
            context = "Birth Chart Information:\n"
            
            if "planets" in birth_chart_data:
                context += "Planetary Positions:\n"
                for planet, data in birth_chart_data["planets"].items():
                    context += f"- {planet}: {data['degree']} (House {data['house']})\n"
            
            if "ascendant" in birth_chart_data:
                context += f"Ascendant: {birth_chart_data['ascendant']}\n"
            
            if "birth_info" in birth_chart_data:
                context += f"Birth Details: {birth_chart_data['birth_info']}\n"
            
            return context
            
        except Exception as e:
            return f"Birth chart data available but formatting error: {str(e)}"
    
    def render_quick_insights(self, birth_chart_data):
        """
        Render quick insight buttons for common questions
        
        Args:
            birth_chart_data: Birth chart data for personalized insights
        """
        if not birth_chart_data or not self.interpreter:
            return
        
        st.subheader("🔮 Quick Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💼 Career Guidance", help="Get career and profession insights"):
                with st.spinner("Analyzing career prospects..."):
                    insight = self.interpreter.get_astrological_insights(
                        birth_chart_data["planets"],
                        birth_chart_data["ascendant"],
                        "career and profession"
                    )
                    st.write(insight)
            
            if st.button("💕 Love & Relationships", help="Get relationship predictions"):
                with st.spinner("Reading relationship stars..."):
                    insight = self.interpreter.get_astrological_insights(
                        birth_chart_data["planets"],
                        birth_chart_data["ascendant"],
                        "love, relationships and marriage"
                    )
                    st.write(insight)
        
        with col2:
            if st.button("🏥 Health Insights", help="Get health predictions"):
                with st.spinner("Checking health indicators..."):
                    insight = self.interpreter.get_astrological_insights(
                        birth_chart_data["planets"],
                        birth_chart_data["ascendant"],
                        "health and wellness"
                    )
                    st.write(insight)
            
            if st.button("💰 Finance & Wealth", help="Get financial guidance"):
                with st.spinner("Analyzing wealth indicators..."):
                    insight = self.interpreter.get_astrological_insights(
                        birth_chart_data["planets"],
                        birth_chart_data["ascendant"],
                        "finance, wealth and prosperity"
                    )
                    st.write(insight)
    
    def clear_chat_history(self):
        """Clear chat history"""
        if "messages" in st.session_state:
            st.session_state.messages = []
        if self.interpreter:
            self.interpreter.clear_memory()
        st.success("Chat history cleared!")

def render_ai_features(birth_chart_data=None):
    """
    Main function to render all AI features - simplified version
    
    Args:
        birth_chart_data: Optional birth chart data
    """
    # Simple AI features without complex state management
    st.subheader("🔮 AI Astrology Features")
    
    # Quick insights section
    if birth_chart_data:
        st.write("**Get instant insights about your chart:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💼 Career Guidance", key="career_btn"):
                try:
                    from ai_interpreter import create_ai_interpreter
                    interpreter = create_ai_interpreter()
                    insight = interpreter.get_astrological_insights(
                        birth_chart_data["planets"],
                        birth_chart_data["ascendant"],
                        "career and profession"
                    )
                    st.write(insight)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            if st.button("💕 Love & Relationships", key="love_btn"):
                try:
                    from ai_interpreter import create_ai_interpreter
                    interpreter = create_ai_interpreter()
                    insight = interpreter.get_astrological_insights(
                        birth_chart_data["planets"],
                        birth_chart_data["ascendant"],
                        "love, relationships and marriage"
                    )
                    st.write(insight)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("🏥 Health Insights", key="health_btn"):
                try:
                    from ai_interpreter import create_ai_interpreter
                    interpreter = create_ai_interpreter()
                    insight = interpreter.get_astrological_insights(
                        birth_chart_data["planets"],
                        birth_chart_data["ascendant"],
                        "health and wellness"
                    )
                    st.write(insight)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            if st.button("💰 Finance & Wealth", key="finance_btn"):
                try:
                    from ai_interpreter import create_ai_interpreter
                    interpreter = create_ai_interpreter()
                    insight = interpreter.get_astrological_insights(
                        birth_chart_data["planets"],
                        birth_chart_data["ascendant"],
                        "finance, wealth and prosperity"
                    )
                    st.write(insight)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Simple chat section
        st.subheader("💬 Ask AI Astrologer")
        
        question = st.text_input("Ask a question about your chart:", placeholder="e.g., What does my Moon sign say about my emotions?")
        
        if st.button("Ask AI", key="ask_ai_btn"):
            if question:
                try:
                    from ai_interpreter import create_ai_interpreter
                    interpreter = create_ai_interpreter()
                    birth_chart_context = f"Birth: {birth_chart_data['birth_info']}, Ascendant: {birth_chart_data['ascendant']}"
                    
                    response = interpreter.chat_with_astrologer(question, birth_chart_context)
                    st.write("**AI Response:**")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a question first!")
    
    else:
        st.info("Generate your Kundli first to get personalized AI insights!")
    
    # Settings section
    st.subheader("⚙️ AI Settings")
    st.info("""
    **AI Features:**
    - Powered by Groq's Llama 3.1 model
    - Trained on Vedic astrology principles
    - Provides personalized readings
    - Supports conversational interactions
    """)

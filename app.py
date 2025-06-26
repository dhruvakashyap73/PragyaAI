from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import logging
import traceback
import google.generativeai as genai
from dotenv import load_dotenv
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
load_dotenv()

# Add verbose logging for API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logger.error("GOOGLE_API_KEY not found in environment variables!")
else:
    # Mask the API key for security while logging
    masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "***"
    logger.info(f"API key loaded: {masked_key}")

# List available models first to help with debugging
try:
    genai.configure(api_key=api_key)
    logger.info("Generative AI configured successfully")

    # Log available models
    available_models = genai.list_models()
    logger.info(f"Available models: {[model.name for model in available_models]}")

    # Try each model name format - uncomment alternatives if the current one doesn't work
    model = genai.GenerativeModel('gemini-1.5-pro')
    # model = genai.GenerativeModel('gemini-1.0-pro')
    # model = genai.GenerativeModel('models/gemini-pro')

    logger.info("Model initialized successfully")
except Exception as e:
    logger.error(f"Error initializing Generative AI: {str(e)}")
    logger.error(traceback.format_exc())

# Updated system prompt to encourage concise responses and handle specific keywords
SYSTEM_PROMPT = """
You are Pragya, a friendly and knowledgeable AI assistant for REJAG Technologies. Your responses must be:
- IMPORTANT: Brief and to the point (1-3 sentences maximum).
- Focused on answering exactly what was asked with clear, relevant information.
- Conversational and professional, like a helpful expert guiding users.
- Warm and engaging, ensuring clarity while maintaining a business-friendly tone.

About REJAG:
{
Make use of the knowledge base :
    "what services does rejag technologies offer?": "REJAG Technologies provides POS solutions, business automation (ERP, Finance, CRM), web services (Digital Marketing, E-Commerce), Zoho financial solutions, and POS hardware.",
    "what are the key features of retail POS software?": "Retail POS software includes faster billing, efficient inventory management, e-commerce integration, loyalty programs, real-time sales reports, and mobile tracking apps.",
    "what is restaurant POS software?": "Restaurant POS software helps streamline operations with quick billing, kitchen order tickets (KOT) management, recipe management, and mobile apps for order-taking.",
    "what is distribution pos software?": "Distribution POS software manages sales, inventory, accounting, transportation, and warehouses, along with demand insights and optimization features.",
    "what is erp?": "ERP (Enterprise Resource Planning) integrates business functions like sales, finance, supply chain, and customer service for insights and analytics.",
    "what digital marketing services does rejag provide?": "REJAG offers SEO, SEM, social media marketing, reputation management, and lead generation services.",
    "what zoho financial solutions does rejag offer?": "REJAG provides Zoho Books, Zoho Inventory, Zoho Invoice, Zoho Subscriptions, Zoho Expense, and Zoho Checkout for business financial management.",
    "what is rejag affiliate web (raw)?": "RAW is an affiliate program designed to expand business networks and opportunities.",
    "does rejag technologies provide pos hardware?": "Yes, REJAG supplies essential POS hardware components like thermal paper rolls.",
    "Where the company is located?":"REJAG Technologies Pvt Ltd is located at #24, 4th Cross, Thirumalanagara, Attur Layout, Yelahanka New Town, Bangalore, Karnataka - 560064.",
    "who are your clients?": "Sure! REJAG has worked with businesses across various industries. Some notable clients include: Change tyre, go YAMAHA, DogMyCats, Satish Stores, Chicken World, Bulldog Spirits, Tarandeep and many others",
    "Who are the key partners of REJAG Technologies": "REJAG partners with industry leaders to offer top-notch solutions. Some key partners include: 
    * GoFrugal Technologies - ERP & POS software provider (REJAG is a Rockstar Partner).
    * Zoho - Suite of online productivity tools.
    * Microsoft - Cloud and enterprise solutions.
    * Google - Internet services and cloud computing.
    * Tally Solutions - ERP software for businesses."
    }

Remember to:
1. Keep all responses very brief and focused (maximum 50 words)
2. Answer exactly what was asked, without additional information
3. Be specific rather than general
4. Only provide information about REJAG Technologies's services when directly relevant

Handling Specific Keywords:
- If the user mentions "REJAG Technologies", focus on the mission, services, and clients.
- If the user mentions "POS", provide details on retail, restaurant, and distribution POS solutions.
- If the user mentions "services", discuss business automation, ERP, finance, CRM, digital marketing, and e-commerce.
- If the user mentions "technology" or "stack", explain REJAG’s expertise in POS software, ERP systems, and Zoho financial solutions.
- If the user mentions "clients", share insights on industries served, customer feedback, and REJAG’s recognition in SoftwareSuggest awards.
- If the user mentions "products", highlight POS software features, ERP capabilities, Zoho solutions, and POS hardware.
- If the user mentions "affiliates" or "partnerships", explain the Rejag Affiliate Web (RAW) program and its benefits.

Default Suggestions:
- What is your mission?
- What are your services?
- Who are your clients?
"""

class ConversationManager:
    def __init__(self):
        self.conversations = {}

    def get_conversation_history(self, session_id):
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                'messages': [],
                'context': {},
                'last_update': datetime.now()
            }
        return self.conversations[session_id]

    def add_message(self, session_id, role, content):
        conversation = self.get_conversation_history(session_id)
        conversation['messages'].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now()
        })
        conversation['last_update'] = datetime.now()

    def build_prompt(self, session_id, user_input):
        conversation = self.get_conversation_history(session_id)

        # Build conversation context
        context = SYSTEM_PROMPT + "\n\nPrevious conversation:\n"
        for msg in conversation['messages'][-5:]:  # Last 5 messages for context
            context += f"{msg['role']}: {msg['content']}\n"

        context += f"\nUser: {user_input}\n\nAssistant: "
        return context

    def get_suggestions_based_on_query(self, user_query):
        """Get suggested questions based on specific keywords in the user query"""
        user_query = user_query.lower()

        if "pos" in user_query:
            return ["What are the key features of retail POS software?", "What is restaurant POS software?", "What is distribution POS software?", "Does REJAG Technologies provide POS hardware?"]
        elif "services" in user_query:
            return ["What services does REJAG Technologies offer?", "What digital marketing services does REJAG provide?", "What Zoho financial solutions does REJAG offer?"]
        elif "erp" in user_query:
            return ["What is ERP?", "What services does REJAG Technologies offer related to ERP?"]
        elif "digital marketing" in user_query:
            return ["What digital marketing services does REJAG provide?", "Does REJAG offer SEO and social media marketing?"]
        elif "zoho" in user_query or "financial" in user_query:
            return ["What Zoho financial solutions does REJAG offer?", "Does REJAG provide Zoho Books and Zoho Invoice?"]
        elif "affiliate" in user_query:
            return ["What is REJAG Affiliate Web (RAW)?", "How does RAW help in business networking?"]
        else:
            # Default suggestions when no keywords match
            return ["What services does REJAG Technologies offer?", "What are the key features of retail POS software?", "What Zoho financial solutions does REJAG offer?"]

# Initialize conversation manager
conversation_manager = ConversationManager()

@app.route('/ask', methods=['POST'])
def handle_query():
    data = request.json
    user_input = data.get('query', '').strip()
    session_id = data.get('session_id', 'default')
    first_message = data.get('first_message', False)  # New parameter to check if it's the first message

    # Log incoming request
    logger.info(f"Received request: session_id={session_id}, query_length={len(user_input)}, first_message={first_message}")

    if not user_input:
        logger.warning("Empty query received")
        return jsonify({"error": "Query is required"}), 400

    try:
        # Build prompt with conversation history
        prompt = conversation_manager.build_prompt(session_id, user_input)

        # Add user message to history
        conversation_manager.add_message(session_id, 'User', user_input)

        # Generate response with better error handling
        logger.info("Sending request to Generative AI model")

        # Configure the model to provide shorter responses
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 150,  # Limit token length to force concise responses
        }

        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        # Verify the response is valid
        if not hasattr(response, 'text'):
            logger.error(f"Invalid response format: {response}")
            return jsonify({
                "error": "I received an invalid response format from the AI service. Please try again.",
                "debug_info": f"Response lacks 'text' attribute: {str(response)}"
            }), 500

        assistant_response = response.text.strip()
        logger.info(f"Received response from model: {len(assistant_response)} characters")

        # Add assistant response to history
        conversation_manager.add_message(session_id, 'Assistant', assistant_response)

        # For the initial greeting, don't add suggestions
        if first_message:
            logger.info("First message detected, returning without suggestions")
            return jsonify({
                "answer": assistant_response,
                "suggestions": []  # No suggestions for the first message
            })

        # Get suggestions based on keywords in the user query
        suggestions = conversation_manager.get_suggestions_based_on_query(user_input)

        # Ensure we have exactly 3 suggestions
        while len(suggestions) < 3:
            # Add fallback suggestions if we have fewer than 3
            if len(suggestions) == 0:
                suggestions.append("What is your mission?")
            elif len(suggestions) == 1:
                suggestions.append("What services do you offer?")
            elif len(suggestions) == 2:
                suggestions.append("How can REJAG Technologies help my business?")

        logger.info(f"Selected suggestions based on query keywords: {suggestions[:3]}")

        return jsonify({
            "answer": assistant_response,
            "suggestions": suggestions[:3]  # Ensure we return exactly 3 suggestions
        })

    except Exception as e:
        # Comprehensive error logging
        logger.error(f"Error processing request: {str(e)}")
        logger.error(traceback.format_exc())

        return jsonify({
            "error": "I apologize, but I encountered an issue processing your request. Please try again.",
            "debug_info": str(e)
        }), 500

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)
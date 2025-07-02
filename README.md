#  🤖 Pragya: Smart Help, Anytime 💬  
A Smart Customer Support Chatbot for **REJAG Technologies** powered by **Flask** and **Gemini LLM**.

---

### 🧠 Overview

**Pragya** is an intelligent, real-time customer support chatbot designed to deliver **quick, concise, and context-aware responses** to user queries about REJAG Technologies. Built with a hybrid architecture, it combines **static FAQ handling** and **LLM-driven dynamic replies** to offer accurate and human-like interactions 24/7.

---

### 🚀 Features

- **Natural Language Understanding** using Google’s **Gemini API**
- Dynamic, chat-based UI with seamless UX
- Suggestive follow-up questions to guide user flow
- FAQ keyword filtering for efficiency
- Error handling and logging with complete traceability
- Responsive, mobile-friendly chatbot widget
- Modular Flask backend with easy-to-expand routes

---

### 🛠️ Tech Stack

| Component     | Technology Used               |
|---------------|-------------------------------|
| Frontend      | HTML, CSS, JavaScript         |
| Backend       | Python, Flask                 |
| LLM Engine    | Google Gemini API             |
| Deployment    | Localhost / Cloud-compatible  |
| Logging       | Python logging module         |
| API Security  | Environment Variables (.env)  |

---

### 🧱 System Architecture

The following diagram illustrates the end-to-end architecture of the **Pragya Chatbot System** and how components interact:

![System Architecture Diagram](https://github.com/dhruvakashyap73/Pragya-Chatbot/blob/main/Photos/SystemArchitecture.jpg)


---

### 🔄 Workflow Overview

1. **User Interface (Browser):**
   - User types a query into the chatbot interface.
   - The message is sent asynchronously using **AJAX** to the Flask server.

2. **Flask Backend:**
   - Receives the message and processes it through the `ConversationManager`.
   - Performs **keyword-based validation** to detect FAQs or common intents.

3. **Gemini LLM Integration:**
   - If no direct FAQ match is found, a smart prompt is generated.
   - Prompt is sent to **Google Gemini API** for natural language response.

4. **Response Handling:**
   - The assistant’s reply is returned to the frontend.
   - Relevant **follow-up suggestions** are generated based on the query.

5. **Frontend Rendering:**
   - The UI displays the assistant’s response.
   - Suggestion buttons help users continue the conversation easily.

---

### 🧠 How It Works

1. The user interacts with a web-based chatbot interface.
2. Input is sent asynchronously (AJAX) to the Flask server.
3. The backend checks if the input matches known FAQ keywords.
4. If not matched, a structured prompt is generated for Gemini LLM.
5. The response is returned and displayed in the UI.
6. Suggested follow-up queries are generated dynamically.

---

### 💡 Smart Response Handling

- Prompt Engineering ensures replies are short, relevant, and brand-aligned.
- Session-based memory helps maintain context in multi-turn conversations.
- Keyword-driven suggestions personalize the interaction and guide users.

---

### 🎯 Future Enhancements

✅ Chat history database integration (MongoDB/PostgreSQL)<br>
🌐 Multilingual support<br>
✅ User authentication and personalization<br>
📊 Analytics dashboard for user behavior<br>
📱 Mobile PWA version<br>

---

#### 👨‍💻 Developed By<br>
Dhruva Kashyap<br>
B.E. Graduate from BNMIT in Artificial Intelligence & Machine Learning<br>

___



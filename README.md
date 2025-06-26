# Pragya: Smart Help, Anytime 🤖💬  
A Smart Customer Support Chatbot for **REJAG Technologies** powered by **Flask** and **Gemini LLM**.

---

## 🧠 Overview

**Pragya** is an intelligent, real-time customer support chatbot designed to deliver **quick, concise, and context-aware responses** to user queries about REJAG Technologies. Built with a hybrid architecture, it combines **static FAQ handling** and **LLM-driven dynamic replies** to offer accurate and human-like interactions 24/7.

---

## 🚀 Features

- **Natural Language Understanding** using Google’s **Gemini API**
- Dynamic, chat-based UI with seamless UX
- Suggestive follow-up questions to guide user flow
- FAQ keyword filtering for efficiency
- Error handling and logging with complete traceability
- Responsive, mobile-friendly chatbot widget
- Modular Flask backend with easy-to-expand routes

---

## 🛠️ Tech Stack

| Component     | Technology Used               |
|---------------|-------------------------------|
| Frontend      | HTML, CSS, JavaScript         |
| Backend       | Python, Flask                 |
| LLM Engine    | Google Gemini (via `genai`)   |
| Deployment    | Localhost / Cloud-compatible  |
| Logging       | Python logging module         |
| API Security  | Environment Variables (.env)  |

---

## 🧱 System Architecture

```mermaid
graph TD
    A[User Input via Chat UI] --> B[AJAX POST /ask]
    B --> C[Flask Backend]
    C --> D[ConversationManager]
    D -->|If FAQ Match| E[Return Predefined Answer]
    D -->|Else| F[Generate Prompt + Call Gemini API]
    F --> G[LLM Response]
    G --> H[Send Response to Frontend]
    H --> I[Render Reply + Suggestions]

# Expense AI Tracker (MVP)
 
## 🚀 Overview
 
Expense AI Tracker is an AI-powered personal finance assistant that allows users to record and retrieve expenses directly through WhatsApp using natural language.
 
Instead of manually filling forms, users simply send messages such as:
 
> "Spent ₹250 on lunch"
 
or
 
> "How much did I spend on food this month?"
 
The application uses Google Gemini to understand the user's intent, extracts structured information, stores it in a database, and returns human-readable responses.
 
---
 
## ✨ Features
 
- 💬 Record expenses using natural language
- 🤖 AI-powered intent detection using Gemini
- 🏷 Automatic category detection
- 💾 Store expenses in Supabase
- 🔍 Retrieve expenses through conversational queries
- 📱 WhatsApp integration using Meta Cloud API
- 📦 Modular project architecture
- ✅ Input validation using Pydantic
- ⚡ Built with FastAPI
---
 
## 💬 Example Conversation
 
### Saving an expense
 
**User:**
```
Spent ₹180 on lunch
```
 
**Bot:**
```
✅ Expense saved!
 
Item: Lunch
Category: Food
Amount: ₹180
```
 
### Retrieving expenses
 
**User:**
```
Show all my food expenses
```
 
**Bot:**
```
🍔 Lunch
₹180
 
🍕 Pizza
₹450
 
🍟 Fries
₹120
```
 
---
 
## 🏗 Architecture
 
```
                     WhatsApp User
                           │
                           ▼
                 Meta WhatsApp Cloud API
                           │
                           ▼
                    FastAPI Webhook
                           │
                           ▼
                 Message Processing Layer
                           │
               ┌───────────┴───────────┐
               ▼                       ▼
       Expense Service         Retrieval Service
               │                       │
               └───────────┬───────────┘
                           ▼
                    Gemini AI Service
                           │
                           ▼
                  SQLAlchemy CRUD Layer
                           │
                           ▼
                       Supabase
```
 
---
 
## 📁 Project Structure
 
```
app
│
├── api
│   ├── whatsapp.py
│   ├── expense.py
│   └── retrieval.py
│
├── database
│   ├── database.py
│   ├── crud.py
│   └── database_models.py
│
├── models
│   └── schemas.py
│
├── prompts
│   ├── intent_prompt.py
│   ├── expense_prompt.py
│   └── retrieval_prompt.py
│
├── services
│   ├── message_service.py
│   ├── intent_service.py
│   ├── expense_service.py
│   ├── retrieval_service.py
│   ├── gemini_service.py
│   └── whatsapp_service.py
│
├── utils
│   ├── formatter.py
│   └── whatsapp_formatter.py
│
├── config.py
└── main.py
```
 
---
 
## 🛠 Tech Stack
 
| Technology | Purpose |
|---|---|
| Python | Backend |
| FastAPI | Webhook & API Framework |
| SQLAlchemy | ORM |
| Supabase | Database |
| Google Gemini | Natural Language Understanding |
| Meta WhatsApp Cloud API | Messaging Platform |
| Pydantic | Data Validation |
| ngrok (Development) | Public Webhook Tunnel |
 
---
 
## 🔄 Request Flow
 
```
User sends WhatsApp message
        │
        ▼
Meta Cloud API
        │
        ▼
FastAPI Webhook
        │
        ▼
message_service.py
        │
        ▼
intent_service.py
        │
        ▼
Gemini identifies intent
        │
 ┌──────┴────────┐
 ▼               ▼
Expense      Retrieval
Service        Service
 │               │
 ▼               ▼
CRUD Layer  CRUD Layer
 │               │
 └──────┬────────┘
        ▼
     Supabase
        │
        ▼
      Formatter
        │
        ▼
    WhatsApp Reply
```
 
---
 
## ✅ Current Capabilities (MVP)
 
- [x] WhatsApp webhook integration
- [x] Expense extraction using Gemini
- [x] Automatic intent detection
- [x] Expense storage
- [x] Expense retrieval
- [x] Structured response formatting
- [x] Modular service-based architecture
---
 
## 🔮 Future Improvements
 
- 📊 Monthly analytics
- 📈 Expense visualizations
- 📅 Date-wise filtering
- 🧾 Receipt OCR
- 🎙 Voice note support
- 🌍 Multi-language support
- 👥 Multi-user authentication
- 📤 CSV/Excel export
- 💸 Budget tracking
- 🔔 Spending alerts
---
 
## 🧱 Design Principles
 
This project follows a layered architecture to keep business logic independent of the API layer.
 
```
API
 ↓
Services
 ↓
Database (CRUD)
 ↓
Supabase
```
 
Each layer has a single responsibility:
 
- **API Layer** – Receives webhook requests and routes them.
- **Service Layer** – Contains business logic and AI orchestration.
- **Database Layer** – Handles all database operations.
- **Prompt Layer** – Stores prompt templates for Gemini.
- **Utility Layer** – Formats responses for WhatsApp.
---
 
## 🏁 MVP Status
 
> ✅ **Expense AI Tracker MVP Completed**
 
Current functionality includes end-to-end conversational expense tracking through WhatsApp with AI-powered intent detection, structured expense extraction, database persistence, and conversational retrieval.
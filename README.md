---
title: career_conversation
app_file: app.py
sdk: gradio
sdk_version: 6.8.0
---
# Personal AI Website Assistant (Gemini + Gradio + Tool Calling)

An **Agentic AI chatbot** that acts as a personal assistant for your website.
It answers questions about your **career, experience, and skills** by reading your **LinkedIn profile and personal summary**, and can also **capture leads automatically** by detecting emails from visitors.

If a visitor shares their email or asks a question you can't answer, the system automatically **calls tools** that log the interaction and send you a **Pushover notification**.

This project demonstrates **LLM tool-calling, context injection, and conversational interfaces** using **Google Gemini and Gradio**.

---

# Features

* 🤖 **AI Chat Assistant** powered by Google Gemini
* 📄 Uses **LinkedIn PDF + personal summary** as context
* 🧠 Maintains **chat history**
* 🛠 **Tool calling agent**
* 📩 **Lead capture** when users provide their email
* 🔔 **Push notifications** using Pushover
* 🌐 Interactive **Gradio web UI**

---

# Tech Stack

* Python
* Google Gemini API
* Gradio
* Pushover API
* PyPDF
* dotenv

---

# Project Structure

```
personal-ai-assistant/
│
├── app.py
├── .env
├── requirements.txt
│
├── me/
│   ├── linkedin.pdf
│   └── summary.txt
│
└── README.md
```

---

# How It Works

```
User message
      ↓
Gradio Chat UI
      ↓
Gemini LLM
      ↓
Context injected (LinkedIn + summary)
      ↓
Model decides:
   ├── respond normally
   ├── call record_user_details()
   └── call record_unknown_question()
      ↓
Tool executes
      ↓
Push notification sent
```

---

# Installation

## 1️⃣ Clone the repository

```
git clone https://github.com/yourusername/personal-ai-assistant.git
cd personal-ai-assistant
```

---

## 2️⃣ Create virtual environment

### Windows

```
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

# Required Environment Variables

Create a `.env` file in the root directory.

```
GEMINI_API_KEY=your_gemini_api_key
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_app_token
```

---

# Getting API Keys

## Gemini API

Get your key from:

https://ai.google.dev/

---

## Pushover

Create an app at:

https://pushover.net/apps/build

Then obtain:

* User Key
* API Token

---

# Running the Application

Start the server:

```
python app.py
```

You will see something like:

```
Running on http://127.0.0.1:7860
```

Open the URL in your browser.

---

# Example Interaction

### Visitor

```
Hi, what experience do you have in AI?
```

### Assistant

```
I have worked on several AI and data science projects...
```

---

### Visitor

```
My email is test@email.com
```

### Tool Triggered

```
record_user_details()
```

You receive a **Pushover notification**:

```
Recording interest from Name not provided
Email: test@email.com
```

---

# Example Tool Calls

## Record user contact

```
record_user_details(
   email="user@email.com",
   name="John",
   notes="Interested in collaboration"
)
```

---

## Record unanswered question

```
record_unknown_question(
   question="What is your favorite football team?"
)
```

---

# requirements.txt

```
google-generativeai
gradio
python-dotenv
pypdf
requests
protobuf==4.25.3
```

---

# Why This Project Is Valuable

This project demonstrates **real-world LLM engineering concepts**:

* Tool calling agents
* Context grounding
* Conversational interfaces
* Lead capture automation
* Notification pipelines
* Prompt engineering

These are **core patterns used in production AI systems**.

---

# Future Improvements

* Add **vector database (RAG)** instead of raw prompt context
* Deploy on **Docker**
* Add **conversation memory storage**
* Add **analytics dashboard for captured leads**
* Deploy on **cloud (AWS / GCP / Render)**

---


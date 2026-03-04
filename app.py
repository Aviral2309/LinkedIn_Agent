from dotenv import load_dotenv
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
import google.generativeai as genai

load_dotenv(override=True)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return {"recorded": "ok"}


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name"},
            "notes": {"type": "string", "description": "Additional conversation context"},
        },
        "required": ["email"]
    }
}


record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Record any question that couldn't be answered",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The unanswered question"}
        },
        "required": ["question"]
    }
}


tools = [
    {"function_declarations": [record_user_details_json, record_unknown_question_json]}
]


class Me:

    def __init__(self):

        self.model = model
        self.name = "Aviral Mittal"

        reader = PdfReader("me/linkedin.pdf")

        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text

        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    def system_prompt(self):
        system_prompt = f"""You are acting as {self.name}. You are answering questions on {self.name}'s website,
        particularly questions related to {self.name}'s career, background, skills and experience.
        Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible.
        Be professional and engaging.
        If you don't know the answer to any question, use the record_unknown_question tool.
        If the user provides their email or wants to connect, use the record_user_details tool.
        """
        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"Stay in character as {self.name}."
        return system_prompt

    def chat(self, message, history):

        messages = [{"role": "user", "parts": [{"text": self.system_prompt()}]}]

        for h in history:
            role = "user" if h["role"] == "user" else "model"
            messages.append({
                "role": role,
                "parts": [{"text": h["content"]}]
            })

        messages.append({"role": "user", "parts": [{"text": message}]})

        response = self.model.generate_content(
            messages,
            tools=tools
        )

        parts = response.candidates[0].content.parts

        print("Gemini Response Parts:", parts)

        # normal text
        if hasattr(parts[0], "text") and parts[0].text:
            print("Text response:", parts[0].text)
            return parts[0].text

        # tool call
        if hasattr(parts[0], "function_call"):

            print("Function call detected!")

            tool_call = parts[0].function_call
            tool_name = tool_call.name
            arguments = dict(tool_call.args)

            print("Tool:", tool_name)
            print("Arguments:", arguments)

            tool = globals().get(tool_name)

            if tool:
                result = tool(**arguments)
                print("Tool executed:", result)
                return f"{tool_name} executed."

        return "No valid response"


if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat).launch()
from flask import Flask, request, jsonify, render_template_string
import openai
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Email credentials from Render env vars
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Load index.html
with open("index.html", "r") as f:
    INDEX_HTML = f.read()

@app.route("/")
def home():
    return render_template_string(index.html)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    user_email = data.get("email")

    if not message:
        return jsonify({"reply": "Please say something!"})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use a correct model name
            messages=[{"role": "user", "content": message}],
            temperature=0.7,
            max_tokens=150,
        )
        reply = response['choices'][0]['message']['content']

        if user_email:
            send_email(user_email, message, reply)

        return jsonify({"reply": reply})

    except Exception as e:
        print("OpenAI API error:", str(e))  # Log the actual error
        return jsonify({"reply": "Something went wrong: " + str(e)})

def send_email(user_email, user_message, bot_reply):
    try:
        msg = MIMEText(f"User: {user_email}\nMessage: {user_message}\nReply: {bot_reply}")
        msg["Subject"] = "New Chatbot Interaction"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent!")
    except Exception as e:
        print("Failed to send email:", e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

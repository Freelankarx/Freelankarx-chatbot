from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

openai.api_key = os.environ.get("OPENAI_API_KEY")
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    # CORS preflight
    if request.method == "OPTIONS":
        return '', 200, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST"
        }

    # Handle POST chat request
    try:
        data = request.get_json()
        message = data.get("message", "")
        user_email = data.get("email", "")

        if not message:
            return jsonify({"reply": "No message provided."}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Shopify/dropshipping expert assistant."},
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message.content.strip()

        if user_email:
            send_email(user_email, message, reply)

        return jsonify({"reply": reply})

    except Exception as e:
        print("Chat error:", str(e))
        return jsonify({"reply": f"Something went wrong: {str(e)}"}), 500

def send_email(user_email, user_message, bot_reply):
    try:
        msg = MIMEText(f"User: {user_email}\n\nMessage: {user_message}\n\nBot reply:\n{bot_reply}")
        msg["Subject"] = "New Freelankarx Chatbot Message"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent to", EMAIL_ADDRESS)
    except Exception as e:
        print("Email error:", e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

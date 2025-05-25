from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)
CORS(app)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

@app.route("/lead", methods=["POST"])
def receive_lead():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    service = data.get("service")
    urgency = data.get("urgency")
    budget = data.get("budget")
    recommendation = data.get("recommendation")
    score = data.get("score")

    msg = EmailMessage()
    msg["Subject"] = f"New Lead from Freelankarx Assistant: {name}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    msg.set_content(f"""
New Lead Details:

Name: {name}
Email: {email}
Service: {service}
Urgency: {urgency}
Budget: {budget}
Recommended Plan: {recommendation}
Lead Score: {score}/10
""")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return jsonify({"success": True, "message": "Lead received and email sent."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Freelankarx Assistant Backend Running"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

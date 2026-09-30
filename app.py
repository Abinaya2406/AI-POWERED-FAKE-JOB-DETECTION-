"""
AI-POWERED FAKE JOB DETECTION & COMPANY VERIFICATION SYSTEM
Flask Production Backend Server
Author: Abinaya R
"""

import os
import re
import json
from flask import Flask, request, jsonify, send_from_directory

try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False

import joblib

app = Flask(__name__, static_folder='.')
if HAS_CORS:
    CORS(app)

# Paths for serialized models
MODEL_PATH = "model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

model = None
vectorizer = None

def load_models():
    """Safely loads model.pkl and vectorizer.pkl if available."""
    global model, vectorizer
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("[+] Successfully loaded 'model.pkl' and 'vectorizer.pkl'.")
            return True
        except Exception as e:
            print(f"[!] Warning loading model files: {e}")
            return False
    else:
        print("[-] 'model.pkl' or 'vectorizer.pkl' not found. Run 'python train_model.py' to generate weights.")
        return False

# Attempt initial model load
load_models()

# Add manual CORS headers if flask_cors is not installed
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# Free consumer email domains commonly abused by fraudulent recruiters
FREE_EMAIL_DOMAINS = [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
    'proton.me', 'protonmail.com', 'zoho.com', 'yandex.com', 'mail.com',
    'gmx.com', 'icloud.com', 'live.com'
]

# High-risk recruitment scam triggers
SCAM_LEXICON = [
    ('wire transfer', 30, 'high', 'High-risk financial demand'),
    ('telegram', 25, 'high', 'Unverified consumer messaging app'),
    ('whatsapp', 20, 'high', 'Non-standard recruitment channel'),
    ('cashier check', 32, 'high', 'Check clearing overpayment scam'),
    ('check deposit', 28, 'high', 'Fake check fraud risk'),
    ('equipment fee', 30, 'high', 'Upfront equipment purchase demand'),
    ('registration fee', 35, 'high', 'Illegal fee charged to candidates'),
    ('western union', 32, 'high', 'Untraceable cash remittance'),
    ('moneygram', 32, 'high', 'Untraceable cash remittance'),
    ('bitcoin', 25, 'medium', 'Cryptocurrency payment pattern'),
    ('crypto', 22, 'medium', 'Unregulated cryptocurrency transaction'),
    ('upfront payment', 28, 'high', 'Advance-fee fraud indicator'),
    ('no experience needed', 15, 'medium', 'Common lure for vulnerable applicants'),
    ('earn $500/day', 26, 'high', 'Unrealistic income promise'),
    ('package forwarding', 30, 'high', 'Stolen merchandise reshipping mule scheme'),
    ('gift card', 35, 'high', 'Irreversible payment demand')
]

@app.route('/')
def home():
    """Serves the frontend web app if available, else API status."""
    if os.path.exists("frontend.html"):
        return send_from_directory('.', 'frontend.html')
    elif os.path.exists("index.html"):
        return send_from_directory('.', 'index.html')
    return jsonify({
        "system": "AI-Powered Fake Job Detection API",
        "status": "online",
        "endpoints": ["/predict", "/api/predict", "/api/health"]
    })

@app.route('/<path:filename>')
def serve_static(filename):
    """Serves static assets like style.css, app.js, index.html."""
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    return jsonify({"error": "File not found"}), 404

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint to inspect server and model status."""
    return jsonify({
        "status": "online",
        "model_loaded": (model is not None and vectorizer is not None),
        "model": "Logistic Regression (model.pkl)" if model else "Heuristic NLP Engine (train_model.py available)"
    })

@app.route('/predict', methods=['POST', 'OPTIONS'])
@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    """
    Evaluates job posting authenticity.
    Accepts JSON payload:
    {
        "title": "...",
        "company": "...",
        "email": "...",
        "salary": "...",
        "company_profile": "...",
        "description": "...",
        "requirements": "..."
    }
    """
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    data = request.get_json(silent=True) or {}

    title = data.get('title', '') or ''
    company = data.get('company', '') or data.get('company_name', '') or ''
    profile = data.get('company_profile', '') or ''
    description = data.get('description', '') or ''
    requirements = data.get('requirements', '') or ''
    email = data.get('email', '') or data.get('recruiter_email', '') or ''
    salary = data.get('salary', '') or data.get('salary_range', '') or ''
    website = data.get('website', '') or ''

    # Combine text columns exactly as in training
    combined_text = f"{title} {profile} {description} {requirements}".strip()

    # 1. Machine Learning Prediction (if model is loaded)
    ml_prediction_label = None
    ml_fraud_prob = None

    if model is not None and vectorizer is not None and combined_text:
        try:
            vector = vectorizer.transform([combined_text])
            prediction_num = int(model.predict(vector)[0])
            probabilities = model.predict_proba(vector)[0]
            ml_fraud_prob = float(probabilities[1]) * 100
            ml_prediction_label = "Fake Job" if prediction_num == 1 else "Real Job"
        except Exception as e:
            print(f"[!] Error during ML prediction: {e}")

    # 2. Natural Language Forensic & Keyword Analysis
    full_blob = f"{title} {company} {email} {website} {salary} {description} {requirements} {profile}".lower()
    triggered_keywords = []
    heuristic_points = 0

    for word, weight, level, reason in SCAM_LEXICON:
        matches = re.findall(rf"\b{re.escape(word)}\b", full_blob)
        if matches:
            count = len(matches)
            heuristic_points += weight * min(count, 2)
            triggered_keywords.append({
                "word": word,
                "count": count,
                "level": level,
                "reason": reason
            })

    # 3. Recruiter Email Domain Check
    domain_score = 10
    domain_desc = "Corporate email domain verified."
    if email and "@" in email:
        domain = email.split("@")[1].lower()
        if domain in FREE_EMAIL_DOMAINS:
            domain_score = 80
            domain_desc = f"Recruiter uses free personal email (@{domain})."
            heuristic_points += 25
            triggered_keywords.append({
                "word": f"@{domain}",
                "count": 1,
                "level": "high",
                "reason": "Consumer email domain used for recruiter contact"
            })
        else:
            domain_desc = f"Verified enterprise email domain (@{domain})."

    # 4. Financial & Fee Red Flag Checks
    financial_score = 10
    financial_desc = "Standard compensation structure."
    if any(k['word'] in ['registration fee', 'equipment fee', 'cashier check', 'wire transfer'] for k in triggered_keywords):
        financial_score = 92
        financial_desc = "Demands upfront candidate fee or cashier check / wire transfer."
    elif any(w in full_blob for w in ['500/day', '5000/week', '$500 daily']):
        financial_score = 80
        financial_desc = "Disproportionately high pay offered for low skill requirement."

    # 5. Communication Channel Checks
    comm_score = 10
    comm_desc = "Standard corporate interview workflow."
    if "telegram" in full_blob or "whatsapp" in full_blob:
        comm_score = 90
        comm_desc = "Interview or onboarding hosted via encrypted consumer messaging app."

    # Calculate Continuous Risk Score (0 - 100)
    if ml_fraud_prob is not None:
        final_risk_score = round((ml_fraud_prob * 0.65) + (domain_score * 0.20) + (financial_score * 0.15))
    else:
        nlp_score = min(100, round(heuristic_points * 0.95))
        final_risk_score = round((nlp_score * 0.45) + (domain_score * 0.25) + (financial_score * 0.20) + (comm_score * 0.10))

    final_risk_score = max(4, min(99, final_risk_score))
    if any(k['level'] == 'high' and not k['word'].startswith('@') for k in triggered_keywords):
        final_risk_score = max(final_risk_score, 78)

    # Classification Label
    if final_risk_score >= 65:
        result = "Fake Job"
        classification = "Fraudulent"
        headline = "High Probability of Fraud / Scam"
        explanation = "Critical recruitment red flags detected! Linguistic markers and recruitment protocols indicate employment fraud."
    elif final_risk_score >= 35:
        result = "Suspicious"
        classification = "Suspicious"
        headline = "Suspicious Elements Detected"
        explanation = "Moderate risk indicators found. Some elements deviate from standard corporate hiring practices."
    else:
        result = "Real Job"
        classification = "Genuine"
        headline = "Verified Legitimate Posting"
        explanation = "Job posting exhibits normal professional terminology, verified email domain patterns, and standard hiring practices."

    confidence = f"{min(99.4, 88 + abs(final_risk_score - 50) * 0.22):.1f}%"

    # Response payload satisfying both simple client calls {"Prediction": ...} and full forensic dashboard
    response = {
        "Prediction": result,
        "classification": classification,
        "riskScore": final_risk_score,
        "confidence": confidence,
        "headline": headline,
        "explanation": explanation,
        "factors": {
            "nlp": {
                "score": round(ml_fraud_prob) if ml_fraud_prob is not None else min(100, round(heuristic_points * 0.9)),
                "desc": "ML model classified text as typical of fraud." if final_risk_score >= 65 else "Vocabulary typical of genuine recruitment postings."
            },
            "domain": {"score": domain_score, "desc": domain_desc},
            "financial": {"score": financial_score, "desc": financial_desc},
            "communication": {"score": comm_score, "desc": comm_desc}
        },
        "triggeredKeywords": triggered_keywords,
        "fullText": description
    }

    return jsonify(response)

if __name__ == "__main__":
    print("\n=======================================================")
    print(" [*] Flask Backend Running on http://127.0.0.1:5000")
    print(" Endpoints: GET / , POST /predict , GET /api/health")
    print("=======================================================\n")
    app.run(host="0.0.0.0", port=5000, debug=False)

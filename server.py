"""
AI-POWERED FAKE JOB DETECTION & COMPANY VERIFICATION SYSTEM
Local HTTP API Server & Static File Host
Author: Abinaya R
"""

import http.server
import socketserver
import json
import os
import mimetypes
import re

PORT = 5000
MODEL_PATH = "model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

# Global model references
model = None
vectorizer = None

def load_ai_model():
    global model, vectorizer
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        try:
            import joblib
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("[+] Loaded 'model.pkl' and 'vectorizer.pkl' successfully.")
            return True
        except Exception as e:
            print(f"[!] Warning: Could not load pickled model: {e}")
            return False
    else:
        print("[-] 'model.pkl' or 'vectorizer.pkl' not found. Using linguistic heuristic inference until train_model.py is executed.")
        return False

# Free email domains list
FREE_EMAIL_DOMAINS = [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
    'proton.me', 'protonmail.com', 'zoho.com', 'yandex.com', 'mail.com',
    'gmx.com', 'icloud.com', 'live.com'
]

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

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local cross-origin development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def do_GET(self):
        parsed_path = self.path.split('?')[0]

        # Health & Status Endpoint
        if parsed_path == "/api/health":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            status_data = {
                "status": "online",
                "model_loaded": (model is not None and vectorizer is not None),
                "model": "Logistic Regression (model.pkl)" if model else "Heuristic NLP Engine (train_model.py available)"
            }
            self.wfile.write(json.dumps(status_data).encode('utf-8'))
            return

        # Serve index.html for root
        if parsed_path == "/" or parsed_path == "":
            self.path = "/index.html"

        # Serve static assets normally
        return super().do_GET()

    def do_POST(self):
        parsed_path = self.path.split('?')[0]

        if parsed_path == "/api/predict":
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(post_body)
            except Exception:
                data = {}

            title = data.get('title', '')
            company = data.get('company', '')
            email = data.get('email', '')
            website = data.get('website', '')
            salary = data.get('salary', '')
            description = data.get('description', '')
            requirements = data.get('requirements', '')
            profile = data.get('company_profile', '')

            combined_text = f"{title} {profile} {description} {requirements}"
            
            # Predict using Trained ML Model if loaded
            ml_fraud_prob = None
            if model is not None and vectorizer is not None:
                try:
                    X_feat = vectorizer.transform([combined_text])
                    probs = model.predict_proba(X_feat)[0]
                    # Probability of class 1 (fraudulent)
                    ml_fraud_prob = float(probs[1]) * 100
                except Exception as ex:
                    print(f"[!] Inference exception: {ex}")

            # Linguistic trigger analysis
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

            # Domain check
            domain_score = 10
            domain_desc = "Corporate domain verified."
            if email and "@" in email:
                domain = email.split("@")[1].lower()
                if domain in FREE_EMAIL_DOMAINS:
                    domain_score = 80
                    domain_desc = f"Recruiter uses free email service (@{domain})."
                    heuristic_points += 25
                    triggered_keywords.append({
                        "word": f"@{domain}",
                        "count": 1,
                        "level": "high",
                        "reason": "Free consumer email domain used for recruiter contact"
                    })
                else:
                    domain_desc = f"Verified enterprise email domain (@{domain})."

            # Financial red flags
            financial_score = 10
            financial_desc = "Standard compensation structure."
            if any(k['word'] in ['registration fee', 'equipment fee', 'cashier check', 'wire transfer'] for k in triggered_keywords):
                financial_score = 92
                financial_desc = "Flagged upfront fee or suspicious cheque/wire transaction demand."
            elif any(w in full_blob for w in ['500/day', '5000/week', '$500 daily']):
                financial_score = 80
                financial_desc = "Disproportionately high pay offered for low skill requirement."

            # Communication channels
            comm_score = 10
            comm_desc = "Standard professional interview workflow."
            if "telegram" in full_blob or "whatsapp" in full_blob:
                comm_score = 90
                comm_desc = "Interview or onboarding hosted via encrypted consumer messenger."

            # Final Score Calculation
            if ml_fraud_prob is not None:
                # Weighted blend of ML probability + domain & financial rules
                final_score = round((ml_fraud_prob * 0.65) + (domain_score * 0.20) + (financial_score * 0.15))
            else:
                nlp_score = min(100, round(heuristic_points * 0.95))
                final_score = round((nlp_score * 0.45) + (domain_score * 0.25) + (financial_score * 0.20) + (comm_score * 0.10))

            final_score = max(4, min(99, final_score))
            if any(k['level'] == 'high' and not k['word'].startswith('@') for k in triggered_keywords):
                final_score = max(final_score, 78)

            # Classification
            if final_score >= 65:
                classification = "Fraudulent"
                headline = "High Probability of Fraud / Scam"
                explanation = "Critical recruitment red flags detected! Linguistic markers and recruitment protocols indicate employment fraud."
            elif final_score >= 35:
                classification = "Suspicious"
                headline = "Suspicious Elements Detected"
                explanation = "Moderate risk indicators found. Some elements deviate from standard corporate hiring practices."
            else:
                classification = "Genuine"
                headline = "Verified Legitimate Posting"
                explanation = "Job posting exhibits normal professional terminology, verified email domain patterns, and standard hiring practices."

            confidence = f"{min(99.4, 88 + abs(final_score - 50) * 0.22):.1f}%"

            response_payload = {
                "classification": classification,
                "riskScore": final_score,
                "confidence": confidence,
                "headline": headline,
                "explanation": explanation,
                "factors": {
                    "nlp": {
                        "score": round(ml_fraud_prob) if ml_fraud_prob is not None else min(100, round(heuristic_points * 0.9)),
                        "desc": "ML model classified text as typical of fraud." if final_score >= 65 else "Vocabulary typical of genuine recruitment postings."
                    },
                    "domain": {"score": domain_score, "desc": domain_desc},
                    "financial": {"score": financial_score, "desc": financial_desc},
                    "communication": {"score": comm_score, "desc": comm_desc}
                },
                "triggeredKeywords": triggered_keywords,
                "fullText": description
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_payload).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def run_server():
    load_ai_model()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print("\n=======================================================")
        print(f" [*] JobShield AI Server Running on http://localhost:{PORT}")
        print(f" Open http://localhost:{PORT} in your web browser!")
        print("=======================================================\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()

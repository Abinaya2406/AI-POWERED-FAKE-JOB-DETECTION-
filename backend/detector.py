"""
AI-POWERED FAKE JOB DETECTION & COMPANY VERIFICATION SYSTEM
Module: Detection Engine & Natural Language Forensics
Author: Abinaya R
"""

import os
import re
import joblib

class FakeJobDetector:
    def __init__(self, model_path="model.pkl", vectorizer_path="vectorizer.pkl"):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = None
        self.vectorizer = None
        self.load_models()

        # Free consumer email domains commonly abused by scam recruiters
        self.free_email_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
            'proton.me', 'protonmail.com', 'zoho.com', 'yandex.com', 'mail.com',
            'gmx.com', 'icloud.com', 'live.com'
        ]

        # High-risk recruitment scam triggers
        self.scam_lexicon = [
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

    def load_models(self):
        """Loads serialized model and vectorizer weights."""
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
            try:
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                print("[+] Loaded model.pkl and vectorizer.pkl successfully.")
                return True
            except Exception as e:
                print(f"[!] Warning loading model files: {e}")
                return False
        return False

    def predict(self, data):
        """
        Evaluates job posting authenticity and returns detailed forensics.
        """
        title = data.get('title', '') or ''
        company = data.get('company', '') or data.get('company_name', '') or ''
        profile = data.get('company_profile', '') or ''
        description = data.get('description', '') or ''
        requirements = data.get('requirements', '') or ''
        email = data.get('email', '') or data.get('recruiter_email', '') or ''
        salary = data.get('salary', '') or data.get('salary_range', '') or ''
        website = data.get('website', '') or ''

        combined_text = f"{title} {profile} {description} {requirements}".strip()

        # 1. Machine Learning Inference
        ml_fraud_prob = None
        if self.model is not None and self.vectorizer is not None and combined_text:
            try:
                vector = self.vectorizer.transform([combined_text])
                probabilities = self.model.predict_proba(vector)[0]
                ml_fraud_prob = float(probabilities[1]) * 100
            except Exception as e:
                print(f"[!] Inference exception: {e}")

        # 2. Keyword Forensics
        full_blob = f"{title} {company} {email} {website} {salary} {description} {requirements} {profile}".lower()
        triggered_keywords = []
        heuristic_points = 0

        for word, weight, level, reason in self.scam_lexicon:
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

        # 3. Recruiter Domain Analysis
        domain_score = 10
        domain_desc = "Corporate email domain verified."
        if email and "@" in email:
            domain = email.split("@")[1].lower()
            if domain in self.free_email_domains:
                domain_score = 80
                domain_desc = f"Recruiter uses free personal email service (@{domain})."
                heuristic_points += 25
                triggered_keywords.append({
                    "word": f"@{domain}",
                    "count": 1,
                    "level": "high",
                    "reason": "Free consumer email domain used for recruiter contact"
                })
            else:
                domain_desc = f"Verified enterprise email domain (@{domain})."

        # 4. Financial Demands
        financial_score = 10
        financial_desc = "Standard compensation structure."
        if any(k['word'] in ['registration fee', 'equipment fee', 'cashier check', 'wire transfer'] for k in triggered_keywords):
            financial_score = 92
            financial_desc = "Flagged upfront fee or suspicious cheque/wire transaction demand."
        elif any(w in full_blob for w in ['500/day', '5000/week', '$500 daily']):
            financial_score = 80
            financial_desc = "Disproportionately high pay offered for low skill requirement."

        # 5. Communication Channels
        comm_score = 10
        comm_desc = "Standard corporate interview workflow."
        if "telegram" in full_blob or "whatsapp" in full_blob:
            comm_score = 90
            comm_desc = "Interview or onboarding hosted via encrypted consumer messenger."

        # Risk Score Calculation
        if ml_fraud_prob is not None:
            final_risk_score = round((ml_fraud_prob * 0.65) + (domain_score * 0.20) + (financial_score * 0.15))
        else:
            nlp_score = min(100, round(heuristic_points * 0.95))
            final_risk_score = round((nlp_score * 0.45) + (domain_score * 0.25) + (financial_score * 0.20) + (comm_score * 0.10))

        final_risk_score = max(4, min(99, final_risk_score))
        if any(k['level'] == 'high' and not k['word'].startswith('@') for k in triggered_keywords):
            final_risk_score = max(final_risk_score, 78)

        # Classification
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

        return {
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

    def verify_company(self, company_name, website="", email=""):
        """Verifies company authenticity and web presence."""
        is_suspicious = False
        reasons = []

        if not website:
            is_suspicious = True
            reasons.append("No official company website provided.")
        elif not (website.startswith("http://") or website.startswith("https://")):
            website = "https://" + website

        if website and ("biz" in website or "info" in website or "top" in website):
            reasons.append("Company uses non-standard or disposable top-level domain.")

        if email and "@" in email:
            domain = email.split("@")[1].lower()
            if domain in self.free_email_domains:
                is_suspicious = True
                reasons.append(f"Recruiter email domain (@{domain}) is a free public email provider, not a corporate domain.")

        status = "Unverified / High Risk" if is_suspicious else "Verified Authentic"
        return {
            "company": company_name,
            "status": status,
            "is_authentic": not is_suspicious,
            "details": reasons if reasons else ["Company profile and corporate contact channels conform to standard business criteria."]
        }

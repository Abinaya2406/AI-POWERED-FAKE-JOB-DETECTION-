"""
AI-POWERED FAKE JOB DETECTION & COMPANY VERIFICATION SYSTEM
API Testing & Verification Script
Author: Abinaya R
"""

import json
import urllib.request

API_URL = "http://localhost:5000/predict"

def test_job(name, payload):
    print(f"\n=======================================================")
    print(f" Testing: {name}")
    print(f"=======================================================")
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"[*] HTTP Status: {response.status}")
            print(f"[*] Prediction:     {result.get('Prediction')}")
            print(f"[*] Fraud Risk:     {result.get('riskScore')}%")
            print(f"[*] Confidence:     {result.get('confidence')}")
            print(f"[*] Classification: {result.get('classification')}")
            
            keywords = result.get('triggeredKeywords', [])
            if keywords:
                print(f"[*] Flagged Words:  {[k['word'] for k in keywords]}")
            else:
                print("[*] Flagged Words:  None (Clean)")
    except Exception as e:
        print(f"[!] Request failed: {e}")

if __name__ == "__main__":
    # Test Case 1: High-Risk Telegram & Cashier Cheque Scam
    scam_job = {
        "title": "Remote Data Entry Operator",
        "company_profile": "Offshore Crypto Wealth Partners",
        "description": "Earn $500/day. No experience needed. Immediate start! All interviews conducted on Telegram with HR manager @Recruiter. Candidate must buy equipment via wire transfer using cashier check sent by company.",
        "requirements": "Must have Telegram installed and an active personal checking account for check deposit.",
        "email": "hiring.manager@gmail.com",
        "salary": "$500 / day"
    }
    test_job("High-Risk Telegram Scam", scam_job)

    # Test Case 2: Verified Genuine Software Engineering Role
    legit_job = {
        "title": "Senior Full Stack Software Engineer",
        "company_profile": "Stripe powers online commerce for businesses of all sizes worldwide.",
        "description": "We are seeking a Senior Full Stack Engineer to architect robust distributed APIs, design scalable backend microservices, and collaborate closely with product management and security teams.",
        "requirements": "5+ years of production experience with TypeScript, Go, or Python. Strong background in distributed systems, RESTful API design, and cloud architectures.",
        "email": "careers@stripe.com",
        "salary": "$175,000 - $195,000 / year"
    }
    test_job("Verified Genuine Stripe Role", legit_job)

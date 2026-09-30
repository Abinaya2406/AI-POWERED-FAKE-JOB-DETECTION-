# 🛡️ JobShield AI — Backend Service

Production-grade Flask REST API for AI-Powered Fake Job Detection and Company Verification.

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
# From the project root:
python app.py

# Or:
python backend.py
```

The server will bind to `http://127.0.0.1:5000`.

---

## 📡 API Endpoints

### 1. Fake Job Detection Inference
* **URL**: `/predict` or `/api/predict`
* **Method**: `POST`
* **Headers**: `Content-Type: application/json`
* **Request Body**:
  ```json
  {
    "title": "Remote Data Entry Operator",
    "company": "Apex Crypto Investments",
    "email": "recruiter.apex@gmail.com",
    "salary": "$500 / day",
    "description": "Urgent hiring! Telegram interview. We send cashier checks to buy equipment via wire transfer.",
    "requirements": "Telegram required. Active bank account.",
    "company_profile": "Offshore digital asset advisory."
  }
  ```
* **Response**:
  ```json
  {
    "Prediction": "Fake Job",
    "classification": "Fraudulent",
    "riskScore": 92,
    "confidence": "97.2%",
    "headline": "High Probability of Fraud / Scam",
    "factors": {
      "nlp": { "score": 92, "desc": "ML model classified text as typical of fraud." },
      "domain": { "score": 80, "desc": "Recruiter uses free email (@gmail.com)." },
      "financial": { "score": 92, "desc": "Demands upfront fee or cashier check / wire transfer." },
      "communication": { "score": 90, "desc": "Interview on consumer messaging app." }
    },
    "triggeredKeywords": [
      { "word": "wire transfer", "level": "high", "reason": "High-risk financial demand" },
      { "word": "telegram", "level": "high", "reason": "Unverified consumer messaging app" }
    ]
  }
  ```

---

### 2. Company Verification
* **URL**: `/api/verify-company`
* **Method**: `POST`
* **Request Body**:
  ```json
  {
    "company": "Stripe, Inc.",
    "website": "https://stripe.com",
    "email": "careers@stripe.com"
  }
  ```
* **Response**:
  ```json
  {
    "company": "Stripe, Inc.",
    "status": "Verified Authentic",
    "is_authentic": true,
    "details": ["Company profile and corporate contact channels conform to standard business criteria."]
  }
  ```

---

### 3. Server Health
* **URL**: `/api/health`
* **Method**: `GET`
* **Response**:
  ```json
  {
    "status": "online",
    "model_loaded": true,
    "engine": "TF-IDF + Logistic Regression (JobShield Engine)"
  }
  ```

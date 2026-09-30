"""
AI-POWERED FAKE JOB DETECTION & COMPANY VERIFICATION SYSTEM
Module: API Route Controllers
Author: Abinaya R
"""

from flask import Blueprint, request, jsonify
from .detector import FakeJobDetector

api_bp = Blueprint('api', __name__)
detector = FakeJobDetector()

@api_bp.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    data = request.get_json(silent=True) or {}
    result = detector.predict(data)
    return jsonify(result)

@api_bp.route('/verify-company', methods=['POST', 'OPTIONS'])
def verify_company():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    data = request.get_json(silent=True) or {}
    company_name = data.get('company', '')
    website = data.get('website', '')
    email = data.get('email', '')

    result = detector.verify_company(company_name, website, email)
    return jsonify(result)

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "online",
        "model_loaded": (detector.model is not None and detector.vectorizer is not None),
        "engine": "TF-IDF + Logistic Regression (JobShield Engine)"
    })

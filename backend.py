"""
AI-POWERED FAKE JOB DETECTION & COMPANY VERIFICATION SYSTEM
Backend Application Entry Point
Author: Abinaya R
"""

import os
import sys
from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("\n=======================================================")
    print(f" [*] JobShield AI Backend Running on http://127.0.0.1:{port}")
    print(" Endpoints:")
    print("   - GET  /              (Serves Web Frontend)")
    print("   - POST /predict       (Job Fraud Inference API)")
    print("   - POST /api/predict   (Enhanced Risk Scoring API)")
    print("   - GET  /api/health    (Model & Server Status)")
    print("=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)

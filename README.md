AI-Powered Fake Job Detection and Company Verification System
📌 Overview

AI-Powered Fake Job Detection and Company Verification System is an AI-driven web application designed to protect job seekers from fraudulent job postings and recruitment scams. The system uses Artificial Intelligence, Machine Learning, and Natural Language Processing (NLP) to analyze job descriptions, recruiter information, company details, salary patterns, and website authenticity. It classifies job postings as Genuine or Fake, provides a Fraud Risk Score, verifies company legitimacy, and alerts users about suspicious job offers in real time.

🚀 Features
User Registration & Secure Login
AI-Based Fake Job Detection
Company Verification
Recruiter Profile Validation
Fraud Risk Score Generation
NLP-Based Job Description Analysis
Suspicious Email & Domain Detection
Job Scam Reporting
Resume Upload & Job Matching
Admin Dashboard
Real-Time Notifications
Responsive User Interface
🛠️ Tech Stack
Frontend
React.js
HTML5
CSS3
JavaScript (ES6)
Bootstrap / Tailwind CSS
Backend
Node.js
Express.js
Database
MongoDB Atlas
AI / Machine Learning
Python
Scikit-learn
TensorFlow
Pandas
NumPy
Natural Language Processing (NLP)
Hugging Face Transformers (BERT)
spaCy
NLTK
APIs
Google Safe Browsing API
Whois API (Domain Verification)
Google Maps API (Optional)
Deployment
Vercel (Frontend)
Render (Backend & AI)
MongoDB Atlas (Database)
Version Control
Git & GitHub
📂 Project Structure
AI-Fake-Job-Detection-System
│
├── client/
│   ├── public/
│   ├── src/
│   └── package.json
│
├── server/
│   ├── controllers/
│   ├── routes/
│   ├── models/
│   ├── middleware/
│   ├── config/
│   ├── server.js
│   └── package.json
│
├── ai-model/
│   ├── fake_job_prediction.py
│   ├── model.pkl
│   ├── tokenizer.pkl
│   └── requirements.txt
│
├── database/
│
├── assets/
│
├── README.md
│
├── requirements.txt
│
└── .gitignore
▶️ Installation
git clone https://github.com/yourusername/AI-Fake-Job-Detection-System.git

cd AI-Fake-Job-Detection-System

# Install Backend Dependencies
npm install

# Install Frontend Dependencies
cd client
npm install

# Install AI Dependencies
cd ../ai-model
pip install -r requirements.txt

# Start Backend
cd ../server
npm start

# Start Frontend
cd ../client
npm start

# Run AI Model
cd ../ai-model
python fake_job_prediction.py
📖 How to Use
Register or log in to the application.
Upload or paste a job posting.
The AI analyzes the job description using NLP.
The system verifies the company and recruiter details.
A Fraud Risk Score and prediction (Genuine/Fake) are generated.
Users can view detailed reasons behind the prediction.
Report suspicious job postings to help improve the detection system.
Admin users can monitor reports, manage users, and update the AI model.
🧠 AI Concepts Used
Artificial Intelligence (AI)
Machine Learning
Natural Language Processing (NLP)
Transformer-Based Language Models (BERT)
Text Classification
Fraud Detection
Explainable AI (XAI)
Company & Domain Verification
Real-Time Risk Assessment
📊 Modules
User Authentication
Fake Job Detection
NLP-Based Job Analysis
Company Verification
Recruiter Validation
Fraud Risk Score Generation
Job Scam Reporting
Admin Dashboard
Analytics & Reports
Notification System
🎯 Project Objectives
Detect fake job postings with high accuracy using AI.
Protect job seekers from recruitment fraud and scams.
Verify company and recruiter authenticity.
Generate an explainable fraud risk score for every job posting.
Improve trust in online recruitment platforms.
Reduce financial and personal losses caused by fake job offers.
👨‍💻 Developed By

Your Name

Department: Computer and Communication Engineering

College: V.S.B Engineering College

Guide: Guide Name

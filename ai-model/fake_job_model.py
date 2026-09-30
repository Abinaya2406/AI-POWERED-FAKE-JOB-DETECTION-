"""
AI-POWERED FAKE JOB DETECTION & COMPANY VERIFICATION SYSTEM
Module: Machine Learning Model Training & Evaluation
Author: Abinaya R
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

def create_sample_dataset(csv_path):
    """
    Bootstraps an initial dataset of genuine and fraudulent job postings
    if 'dataset/fake_job_postings.csv' is not yet present.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    sample_data = {
        'title': [
            # Fraudulent Postings (1)
            "Remote Data Entry Clerk - Immediate Start",
            "Urgent: Financial Transaction Assistant (Crypto / Telegram)",
            "Home Based Administrative Assistant $500/day",
            "Package Forwarding & Shipping Inspector",
            "Customer Service Representative - Wire Transfer Specialist",
            "Executive Assistant - Cashier Check Processing",
            "Online Mystery Shopper & Gift Card Evaluator",
            "Urgent Hiring: Data Typist with Registration Fee",
            # Genuine Postings (0)
            "Senior Software Engineer - Cloud Infrastructure",
            "Product Marketing Manager - Enterprise B2B SaaS",
            "Registered Nurse - Intensive Care Unit (ICU)",
            "Financial Analyst - Corporate FP&A",
            "Human Resources Talent Acquisition Specialist",
            "DevOps Engineer - Kubernetes & CI/CD Pipelines",
            "Full Stack Web Developer (React / Node.js)",
            "Content Marketing Associate - SEO & Copywriting"
        ],
        'company_profile': [
            # Fraudulent
            "Apex Global Investments is a rapid international digital wealth advisory.",
            "Offshore Crypto Wealth Partners specializes in high-yield daily arbitrage.",
            "QuickWork Solutions offers high paying flexible jobs for anyone worldwide.",
            "Global Freight Logistics manages urgent international parcel deliveries.",
            "Swift Money Express facilitates rapid cross-border peer-to-peer transfers.",
            "Elite Management Partners connects remote talent with private VIP executives.",
            "Secret Shopper Network reviews major retail chains across North America.",
            "FastTrack Employment helps students and beginners earn instant income.",
            # Genuine
            "Stripe is a financial infrastructure platform for the internet.",
            "Atlassian builds collaboration software like Jira, Confluence, and Trello.",
            "Mayo Clinic is a nonprofit American academic medical center focused on health care.",
            "Deloitte provides industry-leading audit, consulting, tax, and advisory services.",
            "Google's mission is to organize the world's information and make it universally accessible.",
            "Red Hat is the world's leading provider of enterprise open source software solutions.",
            "Shopify is a leading provider of essential internet infrastructure for commerce.",
            "HubSpot is an inbound marketing, sales, and customer service platform."
        ],
        'description': [
            # Fraudulent
            "Earn $500 to $1,000 daily working 2 hours from home. No experience needed. Immediate hire. All interviews conducted on Telegram with HR manager. Candidate must purchase equipment via wire transfer using cashier check sent by company.",
            "We urgently require a crypto transaction assistant to deposit checks and convert funds to Bitcoin and Western Union. Free laptop provided after paying $150 refundable registration fee.",
            "Flexible work from home administrative role. We send you a company check for $3,500 to buy home office supplies from our designated vendor. Contact recruiter on WhatsApp.",
            "Receive high value parcels at your home address, inspect contents, and repackage and reship to international addresses within 24 hours. Keep equipment as bonus.",
            "Process client payments using your personal bank account. Receive 10% commission on all transfers completed through MoneyGram or wire transfer. Immediate start.",
            "Looking for trustworthy assistant. Must be willing to deposit business checks into personal account and forward remaining balance via Zelle or wire transfer.",
            "Secret shopper needed. We will send you an upfront check for $2,000. Cash check, buy $1,500 in iTunes/Steam gift cards, send card codes to supervisor, keep $500.",
            "Typing jobs available for students and homemakers. Pay $50 registration fee to receive typing assignment files. Guaranteed earnings of $800/week.",
            # Genuine
            "We are seeking a Senior Software Engineer to design, build, and maintain scalable APIs, microservices, and distributed cloud systems. Comprehensive medical, dental, and 401k benefits.",
            "Join our marketing team to lead product launch campaigns, conduct customer research, collaborate with engineering, and drive enterprise pipeline growth.",
            "Provide compassionate patient care in our state-of-the-art intensive care unit. Active RN license and BLS certification required. Rotating shifts with overtime opportunities.",
            "Support quarterly budgeting, financial modeling, variance analysis, and executive presentations. Strong Excel and SQL proficiency required.",
            "Manage end-to-end recruitment lifecycle for engineering and product roles. Source candidates on LinkedIn Recruiter and partner with hiring managers.",
            "Automate deployment pipelines using GitHub Actions, Terraform, and Docker. Monitor production Kubernetes clusters with Prometheus and Grafana.",
            "Build modern web applications using React, Next.js, TypeScript, and REST APIs. Participate in code reviews and agile sprint planning.",
            "Write engaging blog posts, customer case studies, and whitepapers to improve organic search rankings and generate qualified inbound leads."
        ],
        'requirements': [
            # Fraudulent
            "Must have smartphone and active Telegram account. Must have active bank account for check deposit.",
            "WhatsApp installed. Willingness to transfer funds quickly. No resume needed.",
            "Basic typing skills. Must be ready to pay equipment fee or deposit check immediately.",
            "Valid home address to receive packages. Fast reshipping turnaround.",
            "Personal checking account. Good communication via SMS and WhatsApp.",
            "Discretion and confidentiality. Ability to wire funds same day.",
            "Ability to purchase gift cards and submit photos of PIN codes promptly.",
            "No prior qualifications needed. Registration fee payment required.",
            # Genuine
            "BS in Computer Science or 5+ years equivalent software engineering experience. Proficient in Go, Python, or Java.",
            "3+ years experience in B2B product marketing. Proven track record of successful software launches.",
            "Bachelor of Science in Nursing (BSN). Current state RN licensure and ACLS certification.",
            "Degree in Finance or Accounting. 2+ years financial analysis or corporate FP&A experience.",
            "3+ years technical recruiting experience. Experience with ATS platforms like Greenhouse or Lever.",
            "Strong Linux fundamentals, AWS/GCP certification, and production Kubernetes experience.",
            "Proficient in HTML5, modern CSS, JavaScript, React, and Node.js backend integrations.",
            "Excellent portfolio of published B2B articles. Strong understanding of technical SEO and keyword research."
        ],
        'fraudulent': [
            1, 1, 1, 1, 1, 1, 1, 1,  # 8 Fake Postings
            0, 0, 0, 0, 0, 0, 0, 0   # 8 Genuine Postings
        ]
    }
    df = pd.DataFrame(sample_data)
    df.to_csv(csv_path, index=False)
    print(f"[*] Initialized starter dataset at '{csv_path}' with {len(df)} postings.")

def train():
    dataset_path = os.path.join("dataset", "fake_job_postings.csv")
    if not os.path.exists(dataset_path):
        create_sample_dataset(dataset_path)

    # 1. Load dataset
    print(f"[+] Loading dataset from {dataset_path}...")
    data = pd.read_csv(dataset_path)

    # 2. Combine text columns
    data['text'] = (
        data['title'].fillna('') + " " +
        data['company_profile'].fillna('') + " " +
        data['description'].fillna('') + " " +
        data['requirements'].fillna('')
    )

    X = data['text']
    y = data['fraudulent']

    # 3. Convert text into numerical features
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_vec = vectorizer.fit_transform(X)

    # 4. Split data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42
    )

    # 5. Train model
    model = LogisticRegression(class_weight='balanced', max_iter=1000)
    model.fit(X_train, y_train)

    # 6. Predict & Evaluate
    predictions = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, predictions))

    # 7. Save model and vectorizer
    joblib.dump(model, "model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")
    print("Model Saved Successfully!")

if __name__ == "__main__":
    train()

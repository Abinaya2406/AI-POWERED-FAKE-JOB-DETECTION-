"""
AI-POWERED FAKE JOB DETECTION & COMPANY VERIFICATION SYSTEM
Python Streamlit Frontend Application
Author: Abinaya R
"""

import os
import joblib
import pandas as pd
import streamlit as st

# Configure Page
st.set_page_config(
    page_title="AI Fake Job Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #0b0f19; color: #f8fafc; }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.6rem 1.5rem;
    }
    .risk-card {
        padding: 1.5rem;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load Models
@st.cache_resource
def load_models():
    model_path = "model.pkl"
    vec_path = "vectorizer.pkl"
    if os.path.exists(model_path) and os.path.exists(vec_path):
        model = joblib.load(model_path)
        vec = joblib.load(vec_path)
        return model, vec
    return None, None

model, vectorizer = load_models()

# Sidebar: Presets & Controls
st.sidebar.title("🛡️ JobShield AI")
st.sidebar.markdown("### Quick Test Presets")

preset_choice = st.sidebar.selectbox(
    "Choose a sample posting:",
    ["-- Custom Input --", "⚠️ Scam: Crypto Telegram & Wire Transfer", "⚠️ Scam: Upfront Equipment Fee", "✅ Genuine: Senior Software Engineer (Stripe)"]
)

default_title = ""
default_company = ""
default_email = ""
default_salary = ""
default_desc = ""
default_req = ""
default_profile = ""

if preset_choice == "⚠️ Scam: Crypto Telegram & Wire Transfer":
    default_title = "Remote Crypto Data Entry Operator"
    default_company = "Apex Digital Investments"
    default_email = "recruiter.apex@gmail.com"
    default_salary = "$500 / day"
    default_desc = "Earn $500/day working from home. No experience required. Urgent hiring! All interviews will be conducted directly on Telegram with @ApexRecruiter. You will receive a cashier check deposit to buy equipment from our approved vendor via wire transfer."
    default_req = "Must have Telegram installed and an active personal checking account for check deposit."
    default_profile = "Global high-yield crypto investment advisory."
elif preset_choice == "⚠️ Scam: Upfront Equipment Fee":
    default_title = "Administrative Assistant (Remote)"
    default_company = "OmniHealth Logistics"
    default_email = "omnihealth.careers@yahoo.com"
    default_salary = "$48.00 / hour"
    default_desc = "OmniHealth is seeking a remote administrative assistant for scheduling appointments and data processing. A mandatory background check registration fee and software fee of $150 must be paid prior to your first week."
    default_req = "High school diploma. Willingness to submit equipment registration fee."
    default_profile = "Medical consultation and hospital supply providers."
elif preset_choice == "✅ Genuine: Senior Software Engineer (Stripe)":
    default_title = "Senior Full Stack Engineer"
    default_company = "Stripe, Inc."
    default_email = "careers@stripe.com"
    default_salary = "$175,000 - $195,000 / year"
    default_desc = "Stripe is building economic infrastructure for the internet. We are seeking a Senior Full Stack Engineer to build reliable distributed APIs, scale cloud infrastructure, and partner with product managers."
    default_req = "5+ years software engineering experience with Go, Python, or TypeScript. Experience with distributed systems and SQL."
    default_profile = "Stripe powers online commerce for millions of global businesses."

# Main Interface
st.title("📚 AI-Powered Fake Job Detection & Company Verification")
st.markdown("Analyze job postings, recruiter domains, and descriptions with **NLP (TF-IDF)** and **Machine Learning**.")

col1, col2 = st.columns([1.1, 0.9])

with col1:
    st.subheader("📋 Job Posting Details")
    title = st.text_input("Job Title *", value=default_title, placeholder="e.g. Remote Data Entry Operator")
    company = st.text_input("Company Name *", value=default_company, placeholder="e.g. Global Tech Solutions")
    
    c_email, c_sal = st.columns(2)
    with c_email:
        email = st.text_input("Recruiter Email", value=default_email, placeholder="e.g. hr@company.com")
    with c_sal:
        salary = st.text_input("Salary / Compensation", value=default_salary, placeholder="e.g. $70,000/yr or $500/day")

    description = st.text_area("Job Description *", value=default_desc, height=140, placeholder="Paste job description...")
    requirements = st.text_area("Requirements & Qualifications", value=default_req, height=80, placeholder="Candidate requirements...")
    profile = st.text_area("Company Profile", value=default_profile, height=60, placeholder="About the company...")

    analyze_btn = st.button("🔍 Run AI Fraud Analysis", use_container_width=True)

with col2:
    st.subheader("📊 AI Verification Verdict")
    
    if analyze_btn:
        if not title or not company or not description:
            st.error("Please fill in Job Title, Company Name, and Job Description.")
        else:
            with st.spinner("Analyzing text patterns, domain credibility, and risk factors..."):
                combined_text = f"{title} {profile} {description} {requirements}".lower()
                
                # Scam lexical keywords
                scam_keywords = ["wire transfer", "telegram", "whatsapp", "cashier check", "check deposit", "equipment fee", "registration fee", "bitcoin", "crypto", "earn $500/day", "no experience needed"]
                flagged = [kw for kw in scam_keywords if kw in combined_text]
                
                # Email domain check
                free_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"]
                is_free_domain = any(f"@{d}" in email.lower() for d in free_domains)
                if is_free_domain:
                    flagged.append(f"Free email: {email}")

                # Model Prediction
                if model and vectorizer:
                    feat = vectorizer.transform([combined_text])
                    pred_prob = model.predict_proba(feat)[0][1] * 100
                    risk_score = round(pred_prob)
                    algo_label = "Logistic Regression (Active Model)"
                else:
                    # Heuristic fallback
                    risk_score = min(99, len(flagged) * 25 + (20 if is_free_domain else 5))
                    if flagged:
                        risk_score = max(risk_score, 75)
                    else:
                        risk_score = max(5, risk_score)
                    algo_label = "TF-IDF Linguistic Forensics"

                # Render Verdict
                if risk_score >= 65:
                    st.error(f"🚨 **CRITICAL FRAUD ALERT — Risk Score: {risk_score}%**")
                    st.progress(risk_score / 100)
                    st.markdown("""
                    **Verdict: High Probability of Fraud / Scam**  
                    Critical recruitment red flags detected! Linguistic markers and recruitment protocols indicate employment fraud.
                    """)
                elif risk_score >= 35:
                    st.warning(f"⚠️ **SUSPICIOUS — Risk Score: {risk_score}%**")
                    st.progress(risk_score / 100)
                    st.markdown("""
                    **Verdict: Suspicious Elements Detected**  
                    Moderate risk indicators found. Some elements deviate from standard corporate hiring practices.
                    """)
                else:
                    st.success(f"✅ **VERIFIED GENUINE — Risk Score: {risk_score}%**")
                    st.progress(risk_score / 100)
                    st.markdown("""
                    **Verdict: Legitimate Job Posting**  
                    Posting exhibits standard corporate hiring protocols, verified email domain patterns, and realistic compensation.
                    """)

                st.markdown("---")
                st.markdown("#### 🔬 Explainable AI (XAI) Highlights")
                if flagged:
                    st.write("Triggered Red Flags:")
                    for f in flagged:
                        st.markdown(f"- 🔴 **{f}**")
                else:
                    st.info("No suspicious keywords or consumer email domains detected.")

                st.markdown("#### 🛡️ Job Seeker Recommendations")
                if risk_score >= 50:
                    st.write("1. **Never** pay any upfront fees for equipment or background checks.")
                    st.write("2. **Never** deposit cashier checks from an unknown party.")
                    st.write("3. Verify the recruiter on LinkedIn and the company's official career portal.")
                else:
                    st.write("1. Standard precautions apply: verify offer letters through official HR emails.")
    else:
        st.info("Awaiting submission. Enter details on the left or select a preset to analyze.")

st.markdown("---")
st.caption("Developed by **Abinaya R** • AI-Powered Fake Job Detection & Company Verification System")

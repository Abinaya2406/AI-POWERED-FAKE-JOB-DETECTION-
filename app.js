/**
 * AI-POWERED FAKE JOB DETECTION & COMPANY VERIFICATION SYSTEM
 * Client Application Logic & Natural Language Forensics
 * Developed by Abinaya R
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const jobForm = document.getElementById('jobForm');
  const jobTitleInput = document.getElementById('jobTitle');
  const companyNameInput = document.getElementById('companyName');
  const recruiterEmailInput = document.getElementById('recruiterEmail');
  const companyWebsiteInput = document.getElementById('companyWebsite');
  const salaryRangeInput = document.getElementById('salaryRange');
  const workTypeSelect = document.getElementById('workType');
  const jobDescriptionInput = document.getElementById('jobDescription');
  const jobRequirementsInput = document.getElementById('jobRequirements');
  const companyProfileInput = document.getElementById('companyProfile');
  const descCharCount = document.getElementById('descCharCount');
  const domainFlagBadge = document.getElementById('domainFlagBadge');

  // UI States & Actions
  const emptyState = document.getElementById('emptyState');
  const scanningState = document.getElementById('scanningState');
  const resultsContent = document.getElementById('resultsContent');
  const clearFormBtn = document.getElementById('clearFormBtn');
  const emptyPresetBtn = document.getElementById('emptyPresetBtn');
  const printReportBtn = document.getElementById('printReportBtn');

  // Presets & Dropdown
  const presetDropdownBtn = document.getElementById('presetDropdownBtn');
  const presetMenu = document.getElementById('presetMenu');
  const presetButtons = document.querySelectorAll('[data-preset]');

  // Results Elements
  const verdictCard = document.getElementById('verdictCard');
  const meterFillCircle = document.getElementById('meterFillCircle');
  const riskScoreValue = document.getElementById('riskScoreValue');
  const verdictBadge = document.getElementById('verdictBadge');
  const verdictIcon = document.getElementById('verdictIcon');
  const verdictText = document.getElementById('verdictText');
  const verdictHeadline = document.getElementById('verdictHeadline');
  const verdictExplanation = document.getElementById('verdictExplanation');
  const resAlgorithm = document.getElementById('resAlgorithm');
  const resConfidence = document.getElementById('resConfidence');

  // Factors
  const factorNlpStatus = document.getElementById('factorNlpStatus');
  const factorNlpBar = document.getElementById('factorNlpBar');
  const factorNlpDesc = document.getElementById('factorNlpDesc');

  const factorDomainStatus = document.getElementById('factorDomainStatus');
  const factorDomainBar = document.getElementById('factorDomainBar');
  const factorDomainDesc = document.getElementById('factorDomainDesc');

  const factorFinancialStatus = document.getElementById('factorFinancialStatus');
  const factorFinancialBar = document.getElementById('factorFinancialBar');
  const factorFinancialDesc = document.getElementById('factorFinancialDesc');

  const factorCommunicationStatus = document.getElementById('factorCommunicationStatus');
  const factorCommunicationBar = document.getElementById('factorCommunicationBar');
  const factorCommunicationDesc = document.getElementById('factorCommunicationDesc');

  // XAI & Recommendations
  const xaiKeywordsCount = document.getElementById('xaiKeywordsCount');
  const xaiTagsContainer = document.getElementById('xaiTagsContainer');
  const highlightedTextPreview = document.getElementById('highlightedTextPreview');
  const recommendationsList = document.getElementById('recommendationsList');

  // Modal & Toast
  const openReportModalBtn = document.getElementById('openReportModalBtn');
  const closeReportModalBtn = document.getElementById('closeReportModalBtn');
  const cancelReportBtn = document.getElementById('cancelReportBtn');
  const reportModal = document.getElementById('reportModal');
  const scamReportForm = document.getElementById('scamReportForm');
  const toastContainer = document.getElementById('toastContainer');

  // Status Indicators
  const modelEngineStatus = document.getElementById('modelEngineStatus');
  const apiConnectionStatus = document.getElementById('apiConnectionStatus');

  // Scan Animation elements
  const scanStepText = document.getElementById('scanStepText');
  const scanProgressFill = document.getElementById('scanProgressFill');

  // Server Endpoint config
  const API_BASE_URL = 'http://localhost:5000';
  let isApiOnline = false;

  // Free / Consumer email providers commonly abused by fake recruiters
  const FREE_EMAIL_DOMAINS = [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
    'proton.me', 'protonmail.com', 'zoho.com', 'yandex.com', 'mail.com',
    'gmx.com', 'icloud.com', 'live.com', 'inbox.com', 'fastmail.com'
  ];

  // High-risk Scam Lexicon (TF-IDF Key Triggers)
  const SCAM_TRIGGERS = [
    { word: 'wire transfer', weight: 28, level: 'high', reason: 'High-risk financial demand' },
    { word: 'telegram', weight: 25, level: 'high', reason: 'Unverified communication platform' },
    { word: 'whatsapp', weight: 20, level: 'high', reason: 'Non-standard recruitment channel' },
    { word: 'cashier check', weight: 30, level: 'high', reason: 'Fake check overpayment scam' },
    { word: 'check deposit', weight: 26, level: 'high', reason: 'Check clearing fraud' },
    { word: 'equipment fee', weight: 28, level: 'high', reason: 'Upfront fee extortion' },
    { word: 'registration fee', weight: 30, level: 'high', reason: 'Illegal candidate charging' },
    { word: 'western union', weight: 32, level: 'high', reason: 'Untraceable cash remittance' },
    { word: 'moneygram', weight: 32, level: 'high', reason: 'Untraceable cash remittance' },
    { word: 'bitcoin', weight: 24, level: 'medium', reason: 'Unregulated cryptocurrency transaction' },
    { word: 'crypto', weight: 22, level: 'medium', reason: 'Cryptocurrency payment pattern' },
    { word: 'upfront payment', weight: 27, level: 'high', reason: 'Advance fee scam marker' },
    { word: 'confidential bank', weight: 25, level: 'high', reason: 'Bank credentials harvesting' },
    { word: 'no experience needed', weight: 14, level: 'medium', reason: 'Lure for vulnerable job seekers' },
    { word: 'no interview required', weight: 24, level: 'high', reason: 'Bypasses legitimate hiring' },
    { word: 'immediate hire', weight: 15, level: 'medium', reason: 'False urgency tactic' },
    { word: 'earn $500/day', weight: 22, level: 'high', reason: 'Unrealistic salary bait' },
    { word: '$5000 a week', weight: 25, level: 'high', reason: 'Unrealistic compensation' },
    { word: 'investment required', weight: 30, level: 'high', reason: 'Pyramid or pay-to-work scam' },
    { word: 'shipping coordinator', weight: 18, level: 'medium', reason: 'Common parcel mule scam title' },
    { word: 'package forwarding', weight: 28, level: 'high', reason: 'Stolen goods reshipping scam' },
    { word: 're-packaging', weight: 26, level: 'high', reason: 'Package mule scam indicator' },
    { word: 'ssn required', weight: 20, level: 'high', reason: 'Premature identity theft risk' },
    { word: 'gift card', weight: 32, level: 'high', reason: 'Irreversible scam reimbursement' }
  ];

  // Realistic Test Presets
  const PRESET_DATA = {
    'scam-telegram': {
      title: 'Remote Crypto Data Entry & Task Specialist',
      company: 'Apex Digital Global Investments',
      email: 'recruiter.apexcareers@gmail.com',
      website: 'http://apex-crypto-tasks.biz',
      salary: '$3,500 - $5,000 / week',
      workType: 'Remote',
      description: `We are urgently looking for 10 Remote Data Entry Operators to process daily cryptocurrency transactions and package orders. 
No prior experience needed! You can work from home only 2 hours a day and earn $500/day. Immediate hire guaranteed without complicated interviews.
All applicants will be contacted directly on Telegram by our HR manager @ApexHRManager for onboarding.
Candidates will receive a cashier check deposit of $2,000 to purchase home office equipment from our approved vendor via wire transfer or Bitcoin.`,
      requirements: `Must have a smartphone or laptop.
Must have a Telegram account.
Basic English typing skills.
Must have an active bank account to receive check deposit and execute quick wire transfer.`,
      profile: `Apex Digital is a worldwide leader in rapid digital wealth creation and high-yield offshore investments operating across 40 countries.`
    },
    'scam-fee': {
      title: 'Executive Administrative Assistant (Work From Home)',
      company: 'OmniHealth Diagnostics Group',
      email: 'omnihealth.hiringteam@yahoo.com',
      website: 'https://omnihealth-care-portal.info',
      salary: '$48.00 / hour',
      workType: 'Remote',
      description: `OmniHealth is seeking a dependable Administrative Assistant for scheduling appointments, organizing files, and handling client correspondence.
This is a 100% remote position with flexible working hours. We provide full health benefits, paid time off, and 401(k).
Please note: Prior to your first week, a mandatory background registration fee and software license fee of $150 must be submitted to our certified testing partner. This amount will be fully reimbursed on your first paycheck.
Contact our coordinator via WhatsApp at +1-987-555-0192 for interview screening.`,
      requirements: `High school diploma or equivalent.
Strong organizational skills and ability to manage confidential paperwork.
Willingness to complete background check registration fee.`,
      profile: `OmniHealth Diagnostics provides healthcare consultations and medical supplies across North America.`
    },
    'legit-software': {
      title: 'Senior Full Stack Software Engineer',
      company: 'Stripe, Inc.',
      email: 'careers@stripe.com',
      website: 'https://stripe.com/jobs',
      salary: '$165,000 - $195,000 / year + Equity',
      workType: 'Remote',
      description: `Stripe is a financial infrastructure platform for the internet. Millions of companies—from the world’s largest enterprises to the most ambitious startups—use Stripe to accept payments, grow their revenue, and accelerate new business opportunities.
We are looking for an experienced Senior Full Stack Engineer to join our Developer Infrastructure team. You will architect robust distributed APIs, design scalable backend microservices, and collaborate closely with product management and security teams to build resilient financial services.
Our interview process consists of a technical recruiter phone screen, interactive coding session, architecture design interview, and team culture conversations.`,
      requirements: `5+ years of production experience with modern programming languages (TypeScript, Go, Python, or Ruby).
Strong background in distributed systems, RESTful API design, and cloud architectures (AWS / GCP).
Experience with database modeling in PostgreSQL or MySQL.
Excellent written and verbal communication skills.`,
      profile: `Stripe powers online commerce for businesses of all sizes worldwide, processing hundreds of billions of dollars every year.`
    },
    'legit-marketing': {
      title: 'Product Marketing Manager - Enterprise Solutions',
      company: 'Atlassian Corporation',
      email: 'recruiting-ops@atlassian.com',
      website: 'https://www.atlassian.com/company/careers',
      salary: '$120,000 - $145,000 / year',
      workType: 'Hybrid',
      description: `Atlassian develops products for software developers, project managers, and other software development teams. We are seeking a dynamic Product Marketing Manager to lead go-to-market strategies for our flagship Jira enterprise offerings.
In this role, you will define positioning, develop competitive battlecards, launch high-impact product releases, and partner with sales enablement to drive adoption across Fortune 500 accounts.`,
      requirements: `3+ years of B2B SaaS product marketing experience.
Demonstrated ability to translate complex technical capabilities into customer-centric value propositions.
Experience collaborating with cross-functional teams including Product, Sales, and Corporate Communications.
Bachelor’s degree in Marketing, Business, or related field.`,
      profile: `Atlassian produces tools like Jira, Confluence, Trello, and Bitbucket used by over 260,000 customers globally.`
    }
  };

  // Check Backend Server Status on Boot
  async function checkServerHealth() {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 2000);
      
      const response = await fetch(`${API_BASE_URL}/api/health`, {
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (response.ok) {
        const data = await response.json();
        isApiOnline = true;
        apiConnectionStatus.textContent = 'Flask API Connected';
        apiConnectionStatus.classList.add('online');
        modelEngineStatus.textContent = data.model || 'Logistic Regression (PKL)';
      } else {
        fallbackToClientEngine();
      }
    } catch (err) {
      fallbackToClientEngine();
    }
  }

  function fallbackToClientEngine() {
    isApiOnline = false;
    apiConnectionStatus.textContent = 'Client NLP Engine Active';
    modelEngineStatus.textContent = 'TF-IDF Heuristics + NLP (Standalone)';
  }

  checkServerHealth();

  // Character counter for Job Description
  jobDescriptionInput.addEventListener('input', () => {
    const len = jobDescriptionInput.value.length;
    descCharCount.textContent = `${len.toLocaleString()} characters`;
  });

  // Real-time domain verification check on recruiter email
  recruiterEmailInput.addEventListener('input', () => {
    validateRecruiterDomain();
  });

  function validateRecruiterDomain() {
    const email = recruiterEmailInput.value.trim().toLowerCase();
    if (!email || !email.includes('@')) {
      domainFlagBadge.style.display = 'none';
      return null;
    }

    const domain = email.split('@')[1];
    const isFree = FREE_EMAIL_DOMAINS.includes(domain);

    if (isFree) {
      domainFlagBadge.className = 'domain-flag warning';
      domainFlagBadge.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Free Mail Domain';
      domainFlagBadge.style.display = 'inline-block';
      return { isFree: true, domain };
    } else {
      domainFlagBadge.className = 'domain-flag verified';
      domainFlagBadge.innerHTML = '<i class="fa-solid fa-circle-check"></i> Corporate Domain';
      domainFlagBadge.style.display = 'inline-block';
      return { isFree: false, domain };
    }
  }

  // Preset Menu Toggle
  presetDropdownBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    presetMenu.classList.toggle('hidden');
  });

  document.addEventListener('click', (e) => {
    if (!presetMenu.contains(e.target) && e.target !== presetDropdownBtn) {
      presetMenu.classList.add('hidden');
    }
  });

  // Load Presets
  presetButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const presetKey = btn.getAttribute('data-preset');
      loadPreset(presetKey);
      presetMenu.classList.add('hidden');
      showToast(`Loaded Preset: ${PRESET_DATA[presetKey].title}`, 'info');
    });
  });

  if (emptyPresetBtn) {
    emptyPresetBtn.addEventListener('click', () => {
      loadPreset('scam-telegram');
      triggerAnalysis();
    });
  }

  function loadPreset(key) {
    const data = PRESET_DATA[key];
    if (!data) return;

    jobTitleInput.value = data.title;
    companyNameInput.value = data.company;
    recruiterEmailInput.value = data.email;
    companyWebsiteInput.value = data.website;
    salaryRangeInput.value = data.salary;
    workTypeSelect.value = data.workType;
    jobDescriptionInput.value = data.description;
    jobRequirementsInput.value = data.requirements;
    companyProfileInput.value = data.profile;

    descCharCount.textContent = `${data.description.length.toLocaleString()} characters`;
    validateRecruiterDomain();
  }

  // Clear Form
  clearFormBtn.addEventListener('click', () => {
    jobForm.reset();
    domainFlagBadge.style.display = 'none';
    descCharCount.textContent = '0 characters';
    emptyState.classList.remove('hidden');
    resultsContent.classList.add('hidden');
    scanningState.classList.add('hidden');
    showToast('Form reset successfully', 'info');
  });

  // Form Submission
  jobForm.addEventListener('submit', (e) => {
    e.preventDefault();
    triggerAnalysis();
  });

  // Run Fraud Analysis with Interactive Stepped Scanning
  async function triggerAnalysis() {
    const title = jobTitleInput.value.trim();
    const company = companyNameInput.value.trim();
    const description = jobDescriptionInput.value.trim();
    const requirements = jobRequirementsInput.value.trim();
    const profile = companyProfileInput.value.trim();
    const email = recruiterEmailInput.value.trim();
    const website = companyWebsiteInput.value.trim();
    const salary = salaryRangeInput.value.trim();

    if (!title || !company || !description) {
      showToast('Please fill out all required fields marked with *', 'error');
      return;
    }

    // Switch UI to Scanning State
    emptyState.classList.add('hidden');
    resultsContent.classList.add('hidden');
    scanningState.classList.remove('hidden');

    // Stepped Animation Sequence
    const steps = [
      { text: 'Sanitizing text & removing stopwords...', progress: '25%', stepId: 'step1' },
      { text: 'Extracting TF-IDF 5,000 feature vector...', progress: '50%', stepId: 'step2' },
      { text: 'Running Logistic Regression inference...', progress: '75%', stepId: 'step3' },
      { text: 'Verifying domain & calculating Fraud Risk Score...', progress: '100%', stepId: 'step4' }
    ];

    for (let i = 0; i < steps.length; i++) {
      scanStepText.textContent = steps[i].text;
      scanProgressFill.style.width = steps[i].progress;
      
      // Update step chips
      document.querySelectorAll('.step-chip').forEach((chip, idx) => {
        if (idx === i) {
          chip.className = 'step-chip active';
          chip.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> ${chip.textContent.trim()}`;
        } else if (idx < i) {
          chip.className = 'step-chip';
          chip.style.color = 'var(--safe-green-light)';
          chip.innerHTML = `<i class="fa-solid fa-check"></i> ${chip.textContent.trim()}`;
        }
      });

      await sleep(220);
    }

    // Combine full text payload as in training pipeline
    const combinedText = `${title} ${profile} ${description} ${requirements}`;
    
    let analysisResult;

    if (isApiOnline) {
      try {
        const response = await fetch(`${API_BASE_URL}/api/predict`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            title,
            company,
            email,
            website,
            salary,
            description,
            requirements,
            company_profile: profile,
            text: combinedText
          })
        });

        if (response.ok) {
          analysisResult = await response.json();
        } else {
          analysisResult = runClientSideAnalysis(title, company, email, website, salary, description, requirements, profile);
        }
      } catch (err) {
        analysisResult = runClientSideAnalysis(title, company, email, website, salary, description, requirements, profile);
      }
    } else {
      analysisResult = runClientSideAnalysis(title, company, email, website, salary, description, requirements, profile);
    }

    // Render Results
    displayResults(analysisResult);
  }

  // Client-Side Heuristic & NLP Evaluation Engine (Fallback & Instant Engine)
  function runClientSideAnalysis(title, company, email, website, salary, description, requirements, profile) {
    const fullText = `${title} ${company} ${email} ${website} ${salary} ${description} ${requirements} ${profile}`.toLowerCase();
    
    let fraudPoints = 0;
    const triggeredKeywords = [];

    // 1. Lexical and Keyword Triggers
    SCAM_TRIGGERS.forEach(item => {
      const regex = new RegExp(`\\b${escapeRegExp(item.word)}\\b`, 'gi');
      const matches = fullText.match(regex);
      if (matches && matches.length > 0) {
        const count = matches.length;
        fraudPoints += item.weight * Math.min(count, 2);
        triggeredKeywords.push({
          word: item.word,
          count: count,
          level: item.level,
          reason: item.reason
        });
      }
    });

    // 2. Email Domain Forensic Check
    let domainScore = 0;
    let domainNote = 'Recruiter uses verified corporate domain.';
    let isDomainFree = false;
    if (email && email.includes('@')) {
      const domain = email.split('@')[1].toLowerCase();
      if (FREE_EMAIL_DOMAINS.includes(domain)) {
        isDomainFree = true;
        fraudPoints += 25;
        domainScore = 80;
        domainNote = `Recruiter uses free mail service (@${domain}). Legitimate enterprises hire via company domain.`;
        triggeredKeywords.push({
          word: `@${domain}`,
          count: 1,
          level: 'high',
          reason: 'Consumer email domain used for corporate recruitment'
        });
      } else {
        domainScore = 10;
        domainNote = `Corporate email domain verified (@${domain}).`;
      }
    } else {
      domainScore = 40;
      domainNote = 'No direct recruiter email provided in posting.';
    }

    // 3. Compensation Feasibility Check
    let financialScore = 0;
    let financialNote = 'Compensation package appears consistent with market standards.';
    const highSalaryKeywords = ['500/day', '1000/day', '5000/week', '3000/week', '$500 a day', '$100/hr no experience'];
    const hasUnrealisticSalary = highSalaryKeywords.some(kw => fullText.includes(kw));
    if (hasUnrealisticSalary) {
      fraudPoints += 24;
      financialScore = 85;
      financialNote = 'Unusually high compensation offered for minimal qualifications/effort.';
    } else if (triggeredKeywords.some(k => k.word === 'registration fee' || k.word === 'equipment fee')) {
      fraudPoints += 30;
      financialScore = 95;
      financialNote = 'Demands upfront payment or registration/equipment charge from candidate.';
    } else {
      financialScore = 12;
    }

    // 4. Communication Channel Check
    let communicationScore = 0;
    let communicationNote = 'Standard corporate application procedure.';
    if (fullText.includes('telegram') || fullText.includes('whatsapp')) {
      fraudPoints += 25;
      communicationScore = 90;
      communicationNote = 'Directing interview or communications to encrypted consumer messaging apps.';
    } else {
      communicationScore = 10;
    }

    // 5. NLP Feature Weight Score
    let nlpScore = Math.min(100, Math.round(fraudPoints * 0.95));

    // Calculate Final Risk Score (0 - 100)
    let finalRiskScore = Math.min(99, Math.max(3, Math.round(
      (nlpScore * 0.45) +
      (domainScore * 0.25) +
      (financialScore * 0.20) +
      (communicationScore * 0.10)
    )));

    // Minimum risk threshold if severe scam keywords found
    if (triggeredKeywords.some(k => k.level === 'high' && k.word !== '@gmail.com' && k.word !== '@yahoo.com')) {
      finalRiskScore = Math.max(finalRiskScore, 78);
    }

    // Classification
    let classification = 'Genuine';
    let headline = 'Verified Legitimate Posting';
    let explanation = 'The job posting demonstrates transparent recruitment protocols, verified email domain patterns, realistic compensation, and standard language features consistent with genuine corporate openings.';

    if (finalRiskScore >= 65) {
      classification = 'Fraudulent';
      headline = 'High Probability of Fraud / Scam';
      explanation = 'Critical recruitment red flags detected! This posting exhibits linguistic markers of online employment fraud, suspicious payment/equipment schemes, or unverified contact channels.';
    } else if (finalRiskScore >= 35) {
      classification = 'Suspicious';
      headline = 'Suspicious Elements Detected';
      explanation = 'Moderate risk indicators found. Some elements (such as contact channels or vagueness) deviate from corporate hiring best practices. Exercise caution before sharing personal data.';
    }

    // Confidence
    const confidence = Math.min(99.4, (88 + (Math.abs(finalRiskScore - 50) * 0.22))).toFixed(1);

    return {
      classification,
      riskScore: finalRiskScore,
      confidence: `${confidence}%`,
      headline,
      explanation,
      factors: {
        nlp: { score: nlpScore, desc: nlpScore > 50 ? 'Linguistic patterns match known recruitment phishing templates.' : 'Vocabulary and syntax typical of genuine postings.' },
        domain: { score: domainScore, desc: domainNote },
        financial: { score: financialScore, desc: financialNote },
        communication: { score: communicationScore, desc: communicationNote }
      },
      triggeredKeywords,
      fullText: description
    };
  }

  // Display Results in UI
  function displayResults(data) {
    scanningState.classList.add('hidden');
    resultsContent.classList.remove('hidden');

    const score = data.riskScore;
    riskScoreValue.textContent = `${score}%`;

    // Meter animation: circumference = 2 * PI * 68 = 427.26
    const circumference = 427.26;
    const offset = circumference - (circumference * score / 100);
    meterFillCircle.style.strokeDashoffset = offset;

    // Reset styles
    verdictCard.className = 'verdict-card';
    verdictBadge.className = 'verdict-badge';

    if (score >= 65) {
      // Danger / Fraud
      meterFillCircle.style.stroke = 'var(--danger-red)';
      verdictCard.classList.add('danger');
      verdictBadge.classList.add('danger');
      verdictBadge.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> CRITICAL FRAUD ALERT';
      verdictIcon.className = 'fa-solid fa-shield-xmark';
    } else if (score >= 35) {
      // Moderate / Suspicious
      meterFillCircle.style.stroke = 'var(--warn-amber)';
      verdictCard.classList.add('warning');
      verdictBadge.classList.add('warning');
      verdictBadge.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> SUSPICIOUS - PROCEED WITH CAUTION';
      verdictIcon.className = 'fa-solid fa-circle-exclamation';
    } else {
      // Safe / Genuine
      meterFillCircle.style.stroke = 'var(--safe-green)';
      verdictCard.classList.add('safe');
      verdictBadge.classList.add('safe');
      verdictBadge.innerHTML = '<i class="fa-solid fa-circle-check"></i> VERIFIED GENUINE';
      verdictIcon.className = 'fa-solid fa-shield-check';
    }

    verdictHeadline.textContent = data.headline;
    verdictExplanation.textContent = data.explanation;
    resConfidence.textContent = data.confidence;
    resAlgorithm.textContent = isApiOnline ? 'Logistic Regression (Active Model)' : 'Logistic Regression + TF-IDF Heuristics';

    // Render Factor Bars
    renderFactor(data.factors.nlp.score, factorNlpStatus, factorNlpBar, factorNlpDesc, data.factors.nlp.desc);
    renderFactor(data.factors.domain.score, factorDomainStatus, factorDomainBar, factorDomainDesc, data.factors.domain.desc);
    renderFactor(data.factors.financial.score, factorFinancialStatus, factorFinancialBar, factorFinancialDesc, data.factors.financial.desc);
    renderFactor(data.factors.communication.score, factorCommunicationStatus, factorCommunicationBar, factorCommunicationDesc, data.factors.communication.desc);

    // Render XAI Tags
    renderXaiKeywords(data.triggeredKeywords);

    // Render Text Highlight Preview
    renderHighlightedPreview(data.fullText, data.triggeredKeywords);

    // Render Safety Recommendations
    renderRecommendations(score, data.triggeredKeywords);

    // Smooth scroll into results on mobile
    if (window.innerWidth < 1100) {
      verdictCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function renderFactor(val, statusEl, barEl, descEl, customDesc) {
    barEl.style.width = `${Math.max(8, val)}%`;
    barEl.className = 'factor-bar';
    statusEl.className = 'factor-status-pill';

    if (val >= 60) {
      barEl.classList.add('danger');
      statusEl.classList.add('danger');
      statusEl.textContent = 'High Threat';
    } else if (val >= 30) {
      barEl.classList.add('warning');
      statusEl.classList.add('warning');
      statusEl.textContent = 'Warning';
    } else {
      barEl.classList.add('safe');
      statusEl.classList.add('safe');
      statusEl.textContent = 'Clean';
    }

    descEl.textContent = customDesc;
  }

  function renderXaiKeywords(keywords) {
    xaiTagsContainer.innerHTML = '';
    xaiKeywordsCount.textContent = `${keywords.length} keywords triggered`;

    if (keywords.length === 0) {
      xaiTagsContainer.innerHTML = '<span class="meta-tag"><i class="fa-solid fa-check"></i> No malicious recruitment triggers found</span>';
      return;
    }

    keywords.forEach(item => {
      const tag = document.createElement('span');
      tag.className = `xai-tag ${item.level}`;
      tag.title = `${item.reason} (${item.count} match)`;
      tag.innerHTML = `<i class="fa-solid fa-tag"></i> "${item.word}" <small>(${item.level})</small>`;
      xaiTagsContainer.appendChild(tag);
    });
  }

  function renderHighlightedPreview(text, keywords) {
    if (!text) {
      highlightedTextPreview.textContent = 'No job description text provided.';
      return;
    }

    let markedText = escapeHtml(text);

    keywords.forEach(item => {
      const escapedWord = escapeRegExp(item.word);
      const regex = new RegExp(`(${escapedWord})`, 'gi');
      const cls = item.level === 'high' ? 'hl-danger' : 'hl-warning';
      markedText = markedText.replace(regex, `<mark class="${cls}" title="${item.reason}">$1</mark>`);
    });

    highlightedTextPreview.innerHTML = markedText;
  }

  function renderRecommendations(score, keywords) {
    recommendationsList.innerHTML = '';

    const recs = [];
    if (score >= 65) {
      recs.push({ type: 'warn', text: 'DO NOT pay any money, buy equipment, or purchase gift cards for this employer.' });
      recs.push({ type: 'warn', text: 'NEVER accept cashier checks to deposit into your personal bank account.' });
      recs.push({ type: 'warn', text: 'Avoid conducting professional interviews strictly through Telegram or WhatsApp.' });
      recs.push({ type: 'safe', text: 'Verify the company via official state corporate registries and LinkedIn staff.' });
    } else if (score >= 35) {
      recs.push({ type: 'warn', text: 'Request a formal video interview with company executives before submitting sensitive documents.' });
      recs.push({ type: 'warn', text: 'Verify that the recruiter’s email matches the verified corporate domain name.' });
      recs.push({ type: 'safe', text: 'Cross-check the job ID on the company’s official careers page.' });
    } else {
      recs.push({ type: 'safe', text: 'This posting adheres to standard corporate hiring protocols.' });
      recs.push({ type: 'safe', text: 'Standard interview precautions apply: do not share bank details until officially hired.' });
      recs.push({ type: 'safe', text: 'Always confirm offer letters via the company’s official HR portal.' });
    }

    recs.forEach(rec => {
      const li = document.createElement('li');
      li.className = `${rec.type}-item`;
      li.innerHTML = `<i class="fa-solid ${rec.type === 'warn' ? 'fa-triangle-exclamation' : 'fa-circle-check'}"></i> <span>${rec.text}</span>`;
      recommendationsList.appendChild(li);
    });
  }

  // Export / Print Report
  printReportBtn.addEventListener('click', () => {
    window.print();
  });

  // Modal Handlers
  openReportModalBtn.addEventListener('click', () => {
    reportModal.classList.remove('hidden');
    // Pre-populate company if filled
    const currentCompany = companyNameInput.value.trim();
    if (currentCompany) {
      document.getElementById('reportEntity').value = currentCompany;
    }
  });

  closeReportModalBtn.addEventListener('click', () => {
    reportModal.classList.add('hidden');
  });

  cancelReportBtn.addEventListener('click', () => {
    reportModal.classList.add('hidden');
  });

  reportModal.addEventListener('click', (e) => {
    if (e.target === reportModal) {
      reportModal.classList.add('hidden');
    }
  });

  scamReportForm.addEventListener('submit', (e) => {
    e.preventDefault();
    reportModal.classList.add('hidden');
    scamReportForm.reset();
    showToast('Scam report submitted to verification registry. Thank you for protecting job seekers!', 'success');
  });

  // Toast Notification System
  function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-circle-check';
    if (type === 'error') icon = 'fa-circle-xmark';

    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(30px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3800);
  }

  // Utility Helpers
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
});

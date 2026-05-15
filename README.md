# Credit Assessment System

A full-featured **AI-powered Loan Application & Credit Assessment System** built with Flask and SQLite. It simulates a complete lending workflow with automated risk scoring and a **Maker-Checker approval process**, tailored for financial institutions and fintech companies.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

## ✨ Key Features

### Applicant Experience
- Clean and responsive loan application form
- Simulated **CIBIL score** generation using PAN and Aadhaar (India-specific)
- Instant AI-based credit assessment
- Detailed score breakdown with component-wise visualization
- Application tracking via unique ID

### Operations Dashboard
- Centralized dashboard with search and filter functionality
- **Maker-Checker Workflow**:
  - Submit application for approval
  - Approve or Reject with notes and audit trail
- Status management: `PENDING`, `AWAITING_APPROVAL`, `APPROVED`, `REJECTED`
- Full audit trail (who submitted, who approved, timestamps)

### AI Credit Scoring Engine
The system uses a transparent weighted scoring model:

| Component                  | Weight | Description                        |
|---------------------------|--------|------------------------------------|
| Credit Score              | 30%    | Based on simulated CIBIL score     |
| Income to Loan Ratio      | 25%    | Repayment capacity                 |
| Employment Stability      | 20%    | Years in current employment        |
| Debt-to-Income Ratio      | 15%    | Existing financial burden          |
| Loan Purpose              | 10%    | Risk associated with purpose       |

**Risk Levels**: Low (≥70), Medium (50-69), High (<50)

## 🛠️ Tech Stack

- **Framework**: Flask (Python)
- **Database**: SQLite3 with schema migration support
- **Templating**: Jinja2
- **Frontend**: HTML, CSS, Bootstrap
- **Deployment**: Ready for local, VPS, or containerized environments

## 📁 Project Structure

```bash
credit-assessment-system/
├── app.py                    # Main Flask application
├── credit_assessment.db      # SQLite database (auto-created)
├── templates/
│   ├── index.html
│   ├── apply.html
│   ├── dashboard.html
│   └── result.html
├── static/                   # CSS, JS, images (add as needed)
├── README.md
└── requirements.txt
```
## 🚀 Quick Start

  **1. Clone the Repository**
  
    git clone https://github.com/dineshbangera09/creditassesment.git
    cd credit-assessment-system
    
  **2. Create and Activate Virtual Environment**
  
    python -m venv venv
    # For Windows
    venv\Scripts\activate
    # For Linux / macOS
    source venv/bin/activate
    
  **3. Install Dependencies**
  
    pip install flask
    
    Or using requirements file:
    
    pip install -r requirements.txt
    
  **4. Run the Application**
  
    python app.py
    Default URL: http://192.168.42.56:5000

Tip: Change the host to 0.0.0.0 in app.py for access from other devices on the network.


## 📋 How to Use

  - Visit the homepage and click Apply Now
  - Fill in personal and financial details (PAN & Aadhaar are mandatory for score simulation)
  - Submit to receive instant AI assessment result
  - Go to Dashboard to view all applications
  - Use Submit for Approval → Approve / Reject as Checker

## 🔧 Configuration
You can customize the following in app.py:
  - Database path (DATABASE)
  - Scoring weights and thresholds in calculate_ai_score()
  - Loan purpose categories and their scores
  - Server host and port

## 🧪 Testing
  - Use sample PAN like ABCDE1234F and any 12-digit Aadhaar number
  - Try different income, debt, and employment combinations to test scoring logic
  - Test Maker-Checker flow by submitting and then approving/rejecting from the dashboard.

## 📊 Database Schema

The application includes tables with:

  - Applicant information
  - Financial parameters
  - AI-generated scores
  - Workflow status and audit fields

Schema is auto-initialized and supports safe migrations.

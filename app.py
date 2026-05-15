import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g
from datetime import datetime
import os

app = Flask(__name__)
DATABASE = 'credit_assessment.db'

# Database initialization
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                applicant_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                annual_income REAL NOT NULL,
                credit_score INTEGER NOT NULL,
                loan_amount REAL NOT NULL,
                loan_purpose TEXT NOT NULL,
                employment_years INTEGER NOT NULL,
                existing_debt REAL NOT NULL,
                ai_score REAL,
                risk_level TEXT,
                status TEXT DEFAULT 'PENDING',
                submitted_by TEXT,
                submitted_at DATETIME,
                approved_by TEXT,
                approved_at DATETIME,
                approval_notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
        # Attempt to add new columns for existing databases (migration safe)
        try:
            db.execute("ALTER TABLE applications ADD COLUMN submitted_by TEXT")
            db.execute("ALTER TABLE applications ADD COLUMN submitted_at DATETIME")
            db.execute("ALTER TABLE applications ADD COLUMN approved_by TEXT")
            db.execute("ALTER TABLE applications ADD COLUMN approved_at DATETIME")
            db.execute("ALTER TABLE applications ADD COLUMN approval_notes TEXT")
            db.commit()
        except Exception:
            # Columns likely already exist or SQLite version doesn't support IF NOT EXISTS; ignore
            pass

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# AI Assessment Engine
def calculate_ai_score(data):
    """
    AI-powered credit scoring algorithm
    Factors:
    - Credit score weight: 30%
    - Income to loan ratio: 25%
    - Employment stability: 20%
    - Debt-to-income ratio: 15%
    - Loan purpose factor: 10%
    """
    credit_score = int(data.get('credit_score', 0))
    annual_income = float(data.get('annual_income', 0))
    loan_amount = float(data.get('loan_amount', 0))
    employment_years = int(data.get('employment_years', 0))
    existing_debt = float(data.get('existing_debt', 0))
    loan_purpose = data.get('loan_purpose', '')
    
    # 1. Credit Score Component (0-100) - 30% weight
    credit_component = min(100, (credit_score / 850) * 100)
    
    # 2. Income to Loan Ratio (0-100) - 25% weight
    if annual_income > 0 and loan_amount > 0:
        income_ratio = annual_income / loan_amount
        if income_ratio >= 5:
            loan_component = 100
        elif income_ratio >= 3:
            loan_component = 75
        elif income_ratio >= 2:
            loan_component = 50
        elif income_ratio >= 1:
            loan_component = 25
        else:
            loan_component = 10
    else:
        loan_component = 0
    
    # 3. Employment Stability (0-100) - 20% weight
    if employment_years >= 5:
        employment_component = 100
    elif employment_years >= 3:
        employment_component = 80
    elif employment_years >= 1:
        employment_component = 60
    else:
        employment_component = 40
    
    # 4. Debt-to-Income Ratio (0-100) - 15% weight
    if annual_income > 0:
        dti = existing_debt / annual_income
        if dti <= 0.1:
            debt_component = 100
        elif dti <= 0.2:
            debt_component = 80
        elif dti <= 0.3:
            debt_component = 60
        elif dti <= 0.4:
            debt_component = 40
        else:
            debt_component = 20
    else:
        debt_component = 0
    
    # 5. Loan Purpose Factor (0-100) - 10% weight
    purpose_scores = {
        'home': 90,
        'business': 80,
        'education': 85,
        'debt_consolidation': 70,
        'medical': 75,
        'vehicle': 80,
        'personal': 65,
        'other': 60
    }
    purpose_component = purpose_scores.get(loan_purpose, 60)
    
    # Calculate weighted total
    total_score = (
        (credit_component * 0.30) +
        (loan_component * 0.25) +
        (employment_component * 0.20) +
        (debt_component * 0.15) +
        (purpose_component * 0.10)
    )
    
    return round(total_score, 2)

def determine_risk_level(score):
    if score >= 70:
        return 'LOW'
    elif score >= 50:
        return 'MEDIUM'
    else:
        return 'HIGH'

def determine_status(score):
    if score >= 70:
        return 'APPROVED'
    elif score >= 50:
        return 'PENDING'
    else:
        return 'REJECTED'

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        data = request.form

        # Simulate CIBIL score fetch based on PAN/Aadhaar (Indian regulatory simulation)
        def simulate_cibil_score(pan, aadhaar):
            # Deterministic pseudo-random score for demo (not real CIBIL logic)
            base = sum([ord(c) for c in pan.upper() if c.isalnum()]) + sum([int(d) for d in aadhaar if d.isdigit()])
            score = 600 + (base % 251)  # Range: 600-850
            return min(850, max(300, score))

        pan = data.get('pan', '').upper()
        aadhaar = data.get('aadhaar', '')
        credit_score = simulate_cibil_score(pan, aadhaar)
        # Add credit_score to data for AI scoring
        data = dict(data)
        data['credit_score'] = credit_score

        # Calculate AI score
        ai_score = calculate_ai_score(data)
        risk_level = determine_risk_level(ai_score)
        status = determine_status(ai_score)

        # Save to database
        db = get_db()
        db.execute('''
            INSERT INTO applications (
                applicant_name, email, phone, annual_income, credit_score,
                loan_amount, loan_purpose, employment_years, existing_debt,
                ai_score, risk_level, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('applicant_name'),
            data.get('email'),
            data.get('phone'),
            float(data.get('annual_income')),
            int(credit_score),
            float(data.get('loan_amount')),
            data.get('loan_purpose'),
            int(data.get('employment_years')),
            float(data.get('existing_debt')),
            ai_score,
            risk_level,
            status
        ))
        db.commit()

        # Get the last inserted ID
        app_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

        return redirect(url_for('result', id=app_id))

    return render_template('apply.html')

@app.route('/dashboard')
def dashboard():
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    db = get_db()
    query = 'SELECT * FROM applications WHERE 1=1'
    params = []
    
    if search:
        query += ' AND (applicant_name LIKE ? OR email LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    if status_filter:
        query += ' AND status = ?'
        params.append(status_filter)
    
    query += ' ORDER BY created_at DESC'
    
    applications = db.execute(query, params).fetchall()
    return render_template('dashboard.html', applications=applications, search=search, status_filter=status_filter)


# Maker-Checker actions
@app.route('/submit/<int:id>', methods=['POST'])
def submit_for_approval(id):
    db = get_db()
    submitted_by = request.form.get('submitted_by', 'maker')
    submitted_at = datetime.utcnow()
    db.execute('''
        UPDATE applications SET status = ?, submitted_by = ?, submitted_at = ? WHERE id = ?
    ''', ('AWAITING_APPROVAL', submitted_by, submitted_at, id))
    db.commit()
    return redirect(url_for('dashboard'))


@app.route('/approve/<int:id>', methods=['POST'])
def approve(id):
    db = get_db()
    approved_by = request.form.get('approved_by', 'checker')
    approval_notes = request.form.get('approval_notes', '')
    approved_at = datetime.utcnow()
    db.execute('''
        UPDATE applications SET status = ?, approved_by = ?, approved_at = ?, approval_notes = ? WHERE id = ?
    ''', ('APPROVED', approved_by, approved_at, approval_notes, id))
    db.commit()
    return redirect(url_for('dashboard'))


@app.route('/reject/<int:id>', methods=['POST'])
def reject(id):
    db = get_db()
    approved_by = request.form.get('approved_by', 'checker')
    approval_notes = request.form.get('approval_notes', '')
    approved_at = datetime.utcnow()
    db.execute('''
        UPDATE applications SET status = ?, approved_by = ?, approved_at = ?, approval_notes = ? WHERE id = ?
    ''', ('REJECTED', approved_by, approved_at, approval_notes, id))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/result/<int:id>')
def result(id):
    db = get_db()
    app = db.execute('SELECT * FROM applications WHERE id = ?', (id,)).fetchone()
    
    if app is None:
        return "Application not found", 404
    
    # Calculate score breakdown for display
    credit_score = app['credit_score']
    annual_income = app['annual_income']
    loan_amount = app['loan_amount']
    employment_years = app['employment_years']
    existing_debt = app['existing_debt']
    loan_purpose = app['loan_purpose']
    
    # Component breakdown
    components = {
        'credit_score': {
            'name': 'Credit Score',
            'value': min(100, (credit_score / 850) * 100),
            'weight': 30,
            'display': f'{credit_score} (300-850)'
        },
        'income_loan_ratio': {
            'name': 'Income to Loan Ratio',
            'value': min(100, (annual_income / loan_amount * 100) if loan_amount > 0 else 0),
            'weight': 25,
            'display': f'₹{annual_income:,.0f} / ₹{loan_amount:,.0f}'
        },
        'employment': {
            'name': 'Employment Stability',
            'value': min(100, (employment_years / 5) * 100),
            'weight': 20,
            'display': f'{employment_years} years'
        },
        'debt_ratio': {
            'name': 'Debt to Income Ratio',
            'value': min(100, max(0, 100 - (existing_debt / annual_income * 100))) if annual_income > 0 else 0,
            'weight': 15,
            'display': f'${existing_debt:,.0f} / ${annual_income:,.0f}'
        },
        'purpose': {
            'name': 'Loan Purpose',
            'value': {'home': 90, 'business': 80, 'education': 85, 'debt_consolidation': 70, 
                     'medical': 75, 'vehicle': 80, 'personal': 65, 'other': 60}.get(loan_purpose, 60),
            'weight': 10,
            'display': loan_purpose.title()
        }
    }
    
    return render_template('result.html', application=app, components=components)

if __name__ == '__main__':
    # Ensure DB schema/migrations are applied on every startup
    init_db()
    app.run(debug=True, port=5000, host='192.168.42.56') # <-- add host='0.0.0.0'
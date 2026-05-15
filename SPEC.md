# AI Credit Assessment Web Application

## Project Overview
- **Project Name**: AI Credit Assessment
- **Type**: Full-stack web application (Flask + SQLite)
- **Core Functionality**: AI-powered credit underwriting system that evaluates loan applications, provides risk assessment, and speeds up approval decisions
- **Target Users**: Lending institutions, loan officers, and credit analysts

---

## Technology Stack
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI/ML**: Rule-based scoring algorithm (simulates AI assessment)

---

## UI/UX Specification

### Color Palette
| Role | Color | Hex Code |
|------|-------|----------|
| Primary | Deep Navy | `#0a1628` |
| Secondary | Electric Blue | `#00d4ff` |
| Accent | Emerald Green | `#00c896` |
| Warning | Amber | `#ffb800` |
| Danger | Coral Red | `#ff4757` |
| Background | Dark Slate | `#0f1a2e` |
| Card Background | Navy Blue | `#152238` |
| Text Primary | White | `#ffffff` |
| Text Secondary | Silver | `#94a3b8` |

### Typography
- **Headings**: "Outfit", sans-serif (Google Fonts)
- **Body**: "DM Sans", sans-serif (Google Fonts)
- **Monospace**: "JetBrains Mono" (for numbers/data)

### Layout Structure
- **Header**: Fixed top navigation with logo and nav links
- **Hero Section**: Full-width banner with headline and CTA
- **Features Section**: 3-column grid showcasing key features
- **Application Form**: Centered card with input fields
- **Dashboard**: Table view of applications with status badges
- **Footer**: Simple footer with copyright

### Responsive Breakpoints
- Mobile: < 768px (single column)
- Tablet: 768px - 1024px (2 columns)
- Desktop: > 1024px (3 columns)

### Visual Effects
- Glassmorphism cards with backdrop blur
- Gradient borders on hover
- Smooth transitions (0.3s ease)
- Subtle glow effects on interactive elements
- Animated counter numbers
- Pulse animation on status badges

---

## Database Schema

### Table: `applications`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment ID |
| applicant_name | TEXT | Full name of applicant |
| email | TEXT | Email address |
| phone | TEXT | Phone number |
| annual_income | REAL | Annual income in USD |
| credit_score | INTEGER | Existing credit score (300-850) |
| loan_amount | REAL | Requested loan amount |
| loan_purpose | TEXT | Purpose of loan |
| employment_years | INTEGER | Years of employment |
| existing_debt | REAL | Current debt obligations |
| ai_score | REAL | AI calculated credit score (0-100) |
| risk_level | TEXT | LOW/MEDIUM/HIGH |
| status | TEXT | PENDING/APPROVED/REJECTED |
| created_at | DATETIME | Application submission timestamp |

---

## Functionality Specification

### Core Features

1. **Landing Page**
   - Hero section with value proposition
   - Feature highlights (3 cards)
   - Call-to-action to apply

2. **Credit Application Form**
   - Personal info (name, email, phone)
   - Financial info (income, employment years)
   - Loan details (amount, purpose)
   - Credit info (current score, existing debt)
   - Real-time form validation
   - Submit triggers AI assessment

3. **AI Assessment Engine**
   - Calculates score based on multiple factors:
     - Credit score weight: 30%
     - Income to loan ratio: 25%
     - Employment stability: 20%
     - Debt-to-income ratio: 15%
     - Loan purpose factor: 10%
   - Risk classification:
     - Score ≥ 70: LOW risk → APPROVED
     - Score 50-69: MEDIUM risk → PENDING
     - Score < 50: HIGH risk → REJECTED

4. **Dashboard**
   - List of all applications
   - Filter by status
   - Search by name/email
   - View application details
   - Status badges with colors

5. **Application Details**
   - Full application info
   - AI score breakdown
   - Risk assessment explanation

---

## Page Structure

### 1. Home Page (`/`)
- Landing page with hero and features

### 2. Apply Page (`/apply`)
- Credit application form

### 3. Dashboard Page (`/dashboard`)
- Admin view of all applications

### 4. Result Page (`/result/<id>`)
- Individual application result

---

## Acceptance Criteria

1. ✅ Landing page loads with hero, features, and CTA button
2. ✅ Application form validates all required fields
3. ✅ Form submission creates database record
4. ✅ AI assessment calculates score and risk level
5. ✅ Dashboard displays all applications in table
6. ✅ Status badges show correct colors (green/yellow/red)
7. ✅ Application details page shows full information
8. ✅ Responsive design works on mobile/tablet/desktop
9. ✅ Database persists between server restarts
10. ✅ All interactive elements have hover states
# Grantify

## Project Overview
Grantify is a comprehensive grant management platform designed to streamline the entire grant lifecycle. The system caters to three primary user roles—Organization Administrators, Applicants, and Evaluators—each with tailored features to ensure efficiency, transparency, and user engagement.

---

## User Stories

### 1. Organization Administrator
*As an organization administrator, I want to create and manage a call for proposals so that I can attract quality applications, monitor submissions, and efficiently evaluate proposals to select the best projects for funding.*

#### Acceptance Criteria
- Dashboard Access: The admin logs in and accesses a personalized dashboard.
- Grant Creation: The admin can create a new grant call by filling out a form with details such as the grant title, description, application deadline, eligibility criteria, and budget.
- Proposal Management: The admin views a list of proposals submitted against each grant call, with options to filter by status (e.g., pending, under review, approved).
- Evaluation Coordination: The system assigns proposals to evaluators, and the admin can monitor evaluation progress and review aggregated scores.
- Workflow Control: After evaluations, the admin can move proposals to the final decision stage, send notifications to applicants, and generate summary reports.

---

### 2. Applicant
*As an applicant, I want to submit my proposal and track its progress so that I stay informed about the evaluation process and can receive feedback for improvement.*

#### Acceptance Criteria
- Proposal Submission: The applicant logs in, selects an open grant call, and fills out a detailed proposal submission form, including file attachments.
- Status Tracking: The applicant can view the current status of their proposal (submitted, under review, feedback available, or decision made).
- Feedback & Notifications: The applicant receives email notifications about any status updates or feedback provided by evaluators.

---

### 3. Evaluator
*As an evaluator, I want to review assigned proposals, score them, and provide detailed feedback so that I can contribute to a fair and transparent grant selection process.*

#### Acceptance Criteria
- Dashboard Access: The evaluator logs in and accesses a personalized dashboard that displays all proposals assigned for evaluation.
- Proposal Review: The evaluator can open each assigned proposal to view submission details, attached documents, and any supplementary information provided by the applicant.
- Scoring & Feedback: The evaluator can enter a numeric score and provide written feedback for each proposal through an intuitive evaluation form.
- Evaluation Submission: Once the evaluation is completed, the evaluator can submit their assessment, and the system confirms the submission with a notification.
- Review History: The evaluator can view a history of submitted evaluations, allowing them to reference past feedback and scores if needed.

---

## Django Apps to Create in the Project

To modularize the project, following Django apps will be created:

1. **`accounts_app`** (Accounts & Authentication App)
   - Purpose: Handle user registration, login, and role-based access
   - User Roles: Admin, Organization Representative, Evaluator, Applicant.
   - Features: Secure password hashing, Profile management, Role-specific dashboards

2. **`calls_app`** (Grant Calls App )
   - Purpose: Allow organizations to create, update, and publish grant calls.
   - Feature 1: Form for entering grant details (title, description, deadline, eligibility, budget)
   - Feature 2: Call status management (draft, open, closed)

3. **`proposals_app`** (Proposal Submission App)
   - Purpose: Enable applicants to submit proposals.
   - Feature 1: Detailed proposal form with file uploads (documents, supporting evidence)
   - Feature 2: Status tracking (submitted, under review, feedback provided, accepted/rejected)

4. **`evaluation_app`** (Evaluation & Workflow App)
   - Purpose: Support evaluators in reviewing and scoring proposals.
   - Features: 
        - Assignment of proposals to evaluators
        - Scoring system with automated calculations
        - Comment and feedback mechanism
        - Preselection and final selection workflows
   - Workflow Management:
        - Admin controls to move proposals through different stages (from submission to evaluation to final decision)

5. **`messaging`** (Handles private user messaging)
   - Models: `Message`
   - Views: Inbox, Outbox, Compose message
   - Templates: Messaging interface

6. **`admin_panel`** (For administrative management and analytics)
   - Models: None (Uses Django admin)
   - Templates: Dashboard UI

7. **`frontend`** (For UI presentation using HTML, CSS, and JS)
   - Static files: CSS, JS, Images
   - Templates: Base templates and homepage
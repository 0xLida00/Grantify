# User Story

## Organization Administrator

### User Story:
As an organization administrator, I want to create and manage a call for proposals so that I can attract quality applications, monitor submissions, and efficiently evaluate proposals to select the best projects for funding.

### Acceptance Criteria:
• *Dashboard Access*: The admin logs in and accesses a personalized dashboard.
• *Grant Creation*: The admin can create a new grant call by filling out a form with details such as the grant title, description, application deadline, eligibility criteria, and budget.
• *Proposal Management*: The admin views a list of proposals submitted against each grant call, with options to filter by status (e.g., pending, under review, approved).
• *Evaluation Coordination*: The system assigns proposals to evaluators, and the admin can monitor evaluation progress and review aggregated scores.
• *Workflow Control*: After evaluations, the admin can move proposals to the final decision stage, send notifications to applicants, and generate summary reports.


## Applicant

### User Story:
As an applicant, I want to submit my proposal and track its progress so that I stay informed about the evaluation process and can receive feedback for improvement.

### Acceptance Criteria:
• *Proposal Submission*: The applicant logs in, selects an open grant call, and fills out a detailed proposal submission form, including file attachments.
• *Status Tracking*: The applicant can view the current status of their proposal (submitted, under review, feedback available, or decision made).
• *Feedback & Notifications*: The applicant receives email notifications about any status updates or feedback provided by evaluators.


## Evaluator

### User Story:
As an evaluator, I want to review assigned proposals, score them, and provide detailed feedback so that I can contribute to a fair and transparent grant selection process.

### Acceptance Criteria:
• *Dashboard Access*: The evaluator logs in and accesses a personalized dashboard that displays all proposals assigned for evaluation.
• *Proposal Review*: The evaluator can open each assigned proposal to view submission details, attached documents, and any supplementary information provided by the applicant.
• *Scoring & Feedback*: The evaluator can enter a numeric score and provide written feedback for each proposal through an intuitive evaluation form.
• *Evaluation Submission*: Once the evaluation is completed, the evaluator can submit their assessment, and the system confirms the submission with a notification.
• *Review History*: The evaluator can view a history of submitted evaluations, allowing them to reference past feedback and scores if needed.
---

# Suggested Modules / Django Apps

## 	1. Accounts & Authentication App (accounts_app)
• *Purpose*: Handle user registration, login, and role-based access.
• *User Roles*: Admin, Organization Representative, Evaluator, Applicant.
        •	Features:
        •	Secure password hashing
        •	Profile management
        •	Role-specific dashboards

## 2. Grant Calls App (calls_app)
• *Purpose*: Allow organizations to create, update, and publish grant calls.
• *Features*:
	•	Form for entering grant details (title, description, deadline, eligibility, budget)
	•	Call status management (draft, open, closed)
	
## 3. Proposal Submission App (proposals_app)
• *Purpose*: Enable applicants to submit proposals.
• *Features*:
	•	Detailed proposal form with file uploads (documents, supporting evidence)
	•	Status tracking (submitted, under review, feedback provided, accepted/rejected)
	
## 4. Evaluation & Workflow App (evaluation_app)
• *Purpose*: Support evaluators in reviewing and scoring proposals.
• *Features*:
	•	Assignment of proposals to evaluators
	•	Scoring system with automated calculations
	•	Comment and feedback mechanism
	•	Preselection and final selection workflows
• *Workflow Management*:
	•	Admin controls to move proposals through different stages (from submission to evaluation to final decision)
	
## 5. Reporting & Analytics App (reports_app)
• *Purpose*: Provide insights into the grant process.
• *Features*:
	•	Dashboards and reports for overall grant performance
	•	Metrics on submissions, evaluation scores, and post-award project progress
• *Integration*: Optionally integrate external APIs (e.g., for email notifications or document verification) to enhance functionality.

## 6. Notifications & Communication App (alerts_app)
• *Purpose*: Manage email/SMS notifications, in-app messaging, or alerts to keep all users informed about status changes and updates.
• *Features*:
    • Email Notifications – Automatically send emails when key actions occur (e.g., proposal submission, grant call publication).
    • SMS Alerts – Optionally provide SMS notifications for urgent updates.
    • In-App Messaging – Display real-time alerts and notifications within the user dashboard.
    • Push Notifications – Support mobile or web-based push alerts for a more interactive experience.
    • Notification Preferences – Allow users to customize notification settings such as frequency and 
    delivery channels.

## 7. Audit & Logging App (audit_app)
• *Purpose*: Track user activities, changes, and critical system events for compliance, security, and troubleshooting in a multi-user environment.
• *Features*:
    • User Activity Logging – Record actions like logins, data modifications, and key transactions.
    • Change Tracking – Maintain an audit trail of modifications to important data such as grant call
    details or proposal statuses.
    • System Events – Log errors, warnings, and significant system events to aid in troubleshooting and 
    performance monitoring.
    • Secure Log Storage – Ensure logs are stored securely with access limited to authorized personnel.
    • Reporting Interface – Provide an admin dashboard for reviewing, filtering, and generating reports 
    on logged events.

## 8. Help & Support/Feedback App (support_app)
• *Purpose*: Offer a system for users to raise support tickets, provide feedback, and access self-help resources like FAQs, thereby improving overall user experience.
• *Features*:
    • Support Ticket System – Enable users to create and track support requests for any issues 
    encountered.
    • Feedback Forms – Allow users to submit suggestions, report bugs, or offer general feedback.
    • FAQ Section – Provide a searchable repository of frequently asked questions and troubleshooting 
    tips.
    • Ticket Status Updates – Keep users informed about the progress and resolution of their support 
    tickets.
    • Admin Interface – Include a management console for support staff to review, categorize, and 
    resolve tickets efficiently.
    • Live Chat (Optional) – Consider integrating a real-time chat feature for immediate support if 
    needed.
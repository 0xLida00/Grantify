# Grantify
Grantify is a full-stack web application designed to streamline the grant application process for organizations and individuals. It provides a user-friendly interface to manage grant opportunities, track applications, and collaborate with team members.

## Features
- **User Authentication**: Secure user registration and login using JWT-based authentication.
- **Grant Management**: Create, edit, and delete grant opportunities with detailed descriptions and deadlines.
- **Application Tracking**: Track the status of grant applications, including submission dates and updates.
- **Search and Filter**: Easily search and filter grants based on keywords, categories, or deadlines.
- **Notifications**: Receive email or in-app notifications for upcoming deadlines and updates.
- **Responsive Design**: Fully responsive UI for seamless use on desktop and mobile devices.

## Tech Stack
- **Backend**: Python, Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Development Tools**: Visual Studio Code, Git, GitHub
- **Deployment**: Deployed on Render

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/0xlida00/grantify.git
    cd grantify
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    - Create a `.env` file in the root directory.
    - Add the following variables:
      ```

4. Start the development server:
    ```bash
    python manage.py runserver
    ```

5. Access the app at `http://127.0.0.1:8000`.

### Deployment on Render
1. **Create a Render Account**:
   - Sign up at [Render](https://render.com/) if you don’t already have an account.

2. **Create a New Web Service**:
   - Link your GitHub repository to Render.
   - Select the branch you want to deploy.

3. **Set Environment Variables**:
   - Go to the **Environment** tab in your Render service.
   - Add the following environment variables:
     ```
     SECRET_KEY=your-production-secret-key
     DATABASE_URL=your-production-database-url
     ```

4. **Update `settings.py`**:
   - Ensure the following is already configured in `settings.py`:
     ```python
     import os

     DEBUG = False
     ALLOWED_HOSTS = ['your-render-app-url']  # Replace with your Render app URL
     ```

5. **Install Gunicorn**:
   - Ensure `gunicorn` is listed in your `requirements.txt` file:
     ```
     gunicorn
     ```

6. **Start Command**:
   - Make sure to add the below to the start command:
     ```
     gunicorn Grantify_Project.wsgi:application
     ```

7. **Deploy**:
   - Deploy the app on Render. Render will automatically detect the Python environment and install dependencies.

8. **Access Your App**:
   - Once deployed, access your app at the Render-provided URL.

---

### Notes
- **Environment Variables**: Keep sensitive values like `SECRET_KEY` and `DATABASE_URL` secure in the Render environment variables.
- **Static and Media Files**: Cloudinary is used for media file storage. Ensure the `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET` are correctly configured in `.env`.


## Usage
1. Register or log in to your account.
2. Browse available grants or create new grant opportunities.
3. Track your applications and collaborate with team members.
4. Add to your ToDO list and update your tasks list as you progress.
5. Stay updated with notifications for deadlines and changes.

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.

## Contact
For questions or feedback, please contact Lidao Betema at [rodrigue.betema@gmail.com].
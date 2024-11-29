
# Role-Based-Access-Control-RBAC-UI Demostrate by Flask Application with JWT Authentication

This Flask application implements a basic user management system with role-based access control. It uses **JWT (JSON Web Tokens)** for authentication and includes features like login, registration, and protected routes.

## Features
1. **User Authentication**:
   - Login with user credentials.
   - Register new users with role assignment.

2. **JWT Integration**:
   - Secure authentication using JWT stored in cookies.
   - Role-based access to protected routes.

3. **Security Features**:
   - Passwords hashed using `bcrypt`.
   - Limits login attempts to prevent brute force attacks.

4. **Role-Based Access Control**:
   - Managers, Admins, and Employees have varying levels of access to project, employee, and company details.

5. **Session Management**:
   - Sessions are cleared on logout.

6. **Templating**:
   - User-friendly HTML templates are used for rendering pages like login, register, dashboard, and error states.

## Prerequisites
Make sure you have the following installed:
- Python 3.8 or later
- Required libraries (install via `pip`)

## Installation
1. Clone the repository or copy the code files.
   ```bash
   git clone https://github.com/MohansGopi/Role-Based-Access-Control-RBAC-UI
   ```
3. Install the required Python libraries:
   ```bash
   pip install flask flask-jwt-extended bcrypt
   ```

4. Add your secret keys in a separate file named `secret_key.py`:
   ```python
   # secret_key.py
   jwt_secret_key = "your_jwt_secret_key"
   flask_secret_key = "your_flask_secret_key"
   ```

## How to Run
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`.

## Routes
### Public Routes
1. `/`: Main page. Redirects to login or shows the dashboard if logged in.
2. `/login`: Login page. Handles user login.
3. `/register`: Registration page. Allows new users to create accounts.

### Protected Routes
1. `/protected`: Displays protected data based on the user role. Accessible only to authenticated users with JWT.

### Logout
1. `/logout`: Clears the session and JWT cookies.

## File Structure
```bash
project/
│
├── app.py               # Main application file
├── secret_key.py        # Contains JWT and Flask secret keys
├── user_database/       # Directory for storing user credentials
│   └── user_credentials.json
├── templates/           # HTML templates
│   ├── index.html       # Dashboard page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   └── blocked_page.html# Blocked user page
└── README.md            # Documentation
```

## Usage
1. **Login**: 
   - Access the `/login` route.
   - Enter valid credentials. If invalid, you’ll be prompted with an error.
   - After 4 incorrect attempts, users are temporarily blocked for 10 minutes. Repeated failures extend the block duration.

2. **Register**:
   - Access the `/register` route.
   - Fill in the form fields. Passwords must match and meet validation requirements.

3. **Protected Content**:
   - Access the `/protected` route after logging in.
   - Content displayed depends on the user’s role (`MANAGER`, `ADMIN`, `EMPLOYEE`).

4. **Logout**:
   - Click the logout button to clear the session and cookies.

## Role-Based Access
- **Manager**:
  - Can view project and employee details.
- **Admin**:
  - Can view project, employee, and company details.
- **Employee**:
  - Can only view project details.

## Security Notes
- Passwords are hashed using `bcrypt` before being stored in the JSON file.
- JWT tokens are stored in cookies with a 1-day expiration.

## Future Improvements
1. Migrate from JSON-based storage to a database (e.g., SQLite, PostgreSQL).
2. Enhance password validation rules.
3. Add email verification during registration.
4. Use HTTPS for secure cookie transmission.


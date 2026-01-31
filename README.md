# Doit - Task Management Application
#### Video Demo: <https://youtu.be/WwoOwium5dA?si=Kk1cY447ELKyypoK>
#### Description:
"Doit" is a web-based task management application built to help users organize their daily lives efficiently. The project uses Python (Flask) and SQLite for the backend, with HTML, CSS, JavaScript, and Bootstrap handling the frontend.

I chose this project because it presented a manageable challenge, allowing me to focus on consolidating the core technologies learned during CS50. My goal was to bridge the gap between server-side logic and user interface design without being overwhelmed by entirely unfamiliar tools.

### Features & User Flow

When a user first visits the website, they are automatically redirected to the **Login page**. I designed this page to be as flexible as possible: the form accepts either a **username or an email** in the primary field, improving user experience. Underneath the sign-in button, a link to the **Register page** ensures new users don't feel lost.

The Register page requires four inputs: Email, Username, Password, and Password Confirmation. Upon successful registration, the user is redirected to the main dashboard.

Inside the application, the workflow is divided into tabs accessible via a sidebar:
1.  **Tasks (Home):** Displays a table of ongoing tasks with their title, description, and due date. Users can mark tasks as completed using a check circle button.
2.  **New Task:** A form to create tasks with a Title, Description (optional), and a generic date picker for the Due Date.
3.  **Completed:** A history log displaying all finished tasks with their title, description and date of completion.
4.  **Account:** A dropdown menu offering:
    * **Profile Details:** View/Edit email, username, birth date, and password. **Security Feature:** All profile changes require the current password to be saved.
    * **Logout:** Ends the session.

### Distinctiveness and Complexity

This project satisfies the distinctiveness and complexity requirements of CS50 in several ways. Unlike the standard "Finance" problem set, "Doit" implements a more robust user authentication system and complex database relationships regarding task status and history.

* **Authentication Logic:** The login system is polymorphic, accepting either an email or a username, requiring a custom SQL query to check both fields in the database.
* **Security:** The profile update section implements an extra layer of security. It does not simply update the database; it verifies the user's current password hash before committing any changes to sensitive data (like email or username).
* **Database Design:** The SQLite database tracks not just task content, but states (ongoing vs. completed) and timestamps for creation and completion, allowing for the separation of "active" and "history" views.
* **Frontend Logic:** The application uses a simple and modern design (via Bootstrap) and manages dynamic routing to ensure users cannot access internal pages without a valid session.

### Future Improvements

While the application is fully functional, there are several features I would love to implement in a future version (v2.0):

* **Email Notifications:** Adding the features to send automated emails to users 24 hours before a task is due, and implementing a "Forgot Password" feature to allow users to recover their accounts via a secure email link if they cannot log in.
* **Task Categorization:** Adding a "Category" or "Tag" system (e.g., Work, Personal, School) with color-coded badges in the main table to help users visualize their priorities at a glance.
* **Drag and Drop:** Implementing a JavaScript library to allow users to reorder tasks manually or drag them to the "Completed" area.
* **Mobile Responsiveness:** The current version of the application was developed with a **desktop-first approach**. As my primary focus during this project was on consolidating backend logic and database integrity, the interface does not yet adapt to smaller screens (phones or tablets). A major goal for version 2.0 is to implement full responsiveness, ensuring the sidebar collapses into a hamburger menu and tables transform into card views for mobile users.

### File Structure

- `app.py`: The main controller of the application. It initializes the Flask app, configures the SQLite database, and contains all the route definitions (`/completed`, `/login`, `/register`, `/new`, `/profile`, `/`) and the logic for handling POST/GET requests.
- `app.db`: The SQLite database file containing tables for `users` and `tasks`.
- `requirements.txt`: Lists all Python libraries required to run the project.
- `static/`: Contains static assets.
    - `styles.css`: Custom CSS to override Bootstrap defaults and style the sidebar/tables.
    - `script.js`: Frontend logic for UI interactions.
- `templates/`: Contains the HTML Jinja2 templates.
    - `completed.html`: The view for completed tasks.
    - `layout.html`: The base template containing the sidebar and flash messages.
    - `login.html` & `register.html`: Auth pages.
    - `new.html`: The form to create new tasks.
    - `profile.html`: The user settings page.
    - `tasks.html`: The main dashboard for active tasks.
    

### How to Run

1. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the Flask application:
    ```bash
    flask run
    ```

3. Open your browser and visit:
    ```
    http://127.0.0.1:5000
    ```


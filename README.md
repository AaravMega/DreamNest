# DreamNest 🏡

DreamNest is a Flask website that helps users plan, organize, and begin the journey of building their dream home — all in one place.

## Features

- Home page with vision & feature overview
- House & Villa gallery
- User sign up / login (secure password hashing)
- Personal dashboard with saved dream home plans
- Dream Home Planning form (house type, plot size, bedrooms, budget, style, location)
- Budget Planning calculator (area × cost per sq. ft.)
- Home Loan Planning calculator (EMI, total payment, total interest)
- About Us, FAQ (with accordion), and Contact Us (saves messages to database) pages
- Responsive, premium blue & white design with a mobile nav menu

## Project Structure

```
dreamnest/
├── app.py                  # Flask application (routes, logic, database)
├── requirements.txt        # Python dependencies
├── dreamnest.db             # SQLite database (auto-created on first run)
├── templates/               # Jinja2 HTML templates
│   ├── base.html
│   ├── home.html
│   ├── gallery.html
│   ├── about.html
│   ├── faq.html
│   ├── contact.html
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── plan_home.html
│   ├── budget_planning.html
│   ├── loan_planning.html
│   └── services.html
└── static/
    ├── css/style.css        # Blue & white theme styling
    ├── js/script.js         # Nav menu, FAQ accordion, flash auto-dismiss
    └── images/               # (optional) add your own images here
```

## How to Run in VS Code

1. **Open the folder** `dreamnest` in VS Code.

2. **Create a virtual environment** (recommended), open a terminal in VS Code (`` Ctrl+` ``) and run:

   ```bash
   python -m venv venv
   ```

   Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**

   ```bash
   python app.py
   ```

5. Open your browser and go to:

   ```
   http://127.0.0.1:5000
   ```

The database (`dreamnest.db`) is created automatically the first time you run the app — no manual setup needed.

## Notes for Your College Project

- The site is fully functional: sign up, log in, create dream home plans, and use the budget/loan calculators.
- The gallery currently uses simple illustrated house/villa graphics (SVG) instead of stock photos, so there are no copyright/licensing concerns for submission. You can replace them with your own photos by adding image files to `static/images/` and updating the templates.
- Feel free to change the secret key in `app.py` (`app.secret_key`) before deploying anywhere public.
- To reset all data, simply delete `dreamnest.db` and restart the app — it will be recreated automatically.

## Next Steps / Ideas to Extend

- Add real photos to the gallery
- Add email notifications when a contact form is submitted
- Add an admin page to view contact messages and manage users
- Deploy to a host like Render, PythonAnywhere, or Railway

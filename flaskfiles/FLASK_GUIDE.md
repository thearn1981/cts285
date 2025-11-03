# Datamon Flask App - Complete Guide for Beginners

## 📚 What is Flask?

Flask is a **lightweight web framework** for Python. Unlike Streamlit (which handles everything for you), Flask gives you more control. You write:
- **Python code** (the backend logic)
- **HTML templates** (what users see)
- **CSS** (how it looks)

Think of it like this:
- **Flask = Brain** (Python code that makes decisions)
- **HTML = Body** (structure of your web pages)
- **CSS = Clothes** (styling and appearance)

---

## 🗂️ File Structure

Your Flask app needs a specific folder structure:

```
datamon-flask/
├── datamon_flask.py              # Main Flask app (the brain)
├── AnswerChecker_flask.py        # Answer checking logic
├── requirements_flask.txt        # List of dependencies
├── templates/                    # HTML files (what users see)
│   ├── base.html                # Base template (header, footer)
│   ├── index.html               # Main menu page
│   ├── answer_checker.html      # Answer Checker game
│   └── coming_soon.html         # Placeholder for other games
└── static/                       # Static files (CSS, images, JS)
    └── css/
        └── style.css            # All the styling
```

---

## 🚀 Installation & Running

### Step 1: Install Flask
```bash
pip install Flask
```

Or use the requirements file:
```bash
pip install -r requirements_flask.txt
```

### Step 2: Run the App
```bash
python datamon_flask.py
```

### Step 3: Open in Browser
Go to: **http://127.0.0.1:5000**

That's it! Your app is running! 🎉

---

## 🧠 How Flask Works - Key Concepts

### 1. **Routes** (URLs and Functions)

In Flask, you connect URLs to Python functions using **routes**:

```python
@app.route('/')
def index():
    return render_template('index.html')
```

**Translation:**
- When someone visits `http://127.0.0.1:5000/` 
- Flask runs the `index()` function
- Which shows them the `index.html` page

**More examples:**
```python
@app.route('/answer-checker')          # URL: /answer-checker
@app.route('/answer-checker/submit')   # URL: /answer-checker/submit
```

### 2. **Templates** (HTML with Superpowers)

Flask uses **Jinja2** templating, which lets you mix Python and HTML:

```html
<!-- Regular HTML -->
<h1>Welcome</h1>

<!-- HTML + Python (Jinja2) -->
<h1>Welcome, {{ username }}!</h1>
<p>You have {{ points }} points</p>
```

**Variables from Python:**
```python
@app.route('/profile')
def profile():
    return render_template('profile.html', username='Alex', points=42)
```

**If statements:**
```html
{% if score >= 8 %}
    <p>Great job! 🌟</p>
{% else %}
    <p>Keep practicing! 💪</p>
{% endif %}
```

**Loops:**
```html
{% for problem in problems %}
    <li>{{ problem }}</li>
{% endfor %}
```

### 3. **Sessions** (Remembering Data)

HTTP is **stateless** (forgets everything between requests). Sessions solve this:

```python
from flask import session

# Store data
session['player_points'] = 100

# Retrieve data
points = session.get('player_points', 0)  # 0 is default if not found
```

**In our app:**
- `session['player_points']` - Tracks total points
- `session['ac_score']` - Current quiz score
- `session['ac_problem_count']` - Which problem you're on

### 4. **Forms and POST Requests**

**Two types of HTTP requests:**
- **GET**: Just viewing a page (like clicking a link)
- **POST**: Sending data (like submitting a form)

**HTML Form:**
```html
<form method="POST" action="/answer-checker/submit">
    <input type="text" name="problem">
    <button type="submit">Submit</button>
</form>
```

**Flask Handler:**
```python
@app.route('/answer-checker/submit', methods=['POST'])
def submit_answer():
    problem = request.form.get('problem')  # Get form data
    # Process the answer...
    return redirect(url_for('answer_checker'))
```

### 5. **Flash Messages** (Temporary Alerts)

Show feedback to users:

```python
from flask import flash

if is_correct:
    flash('✅ Correct!', 'success')
else:
    flash('❌ Wrong!', 'error')
```

**Display in HTML:**
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

### 6. **Template Inheritance** (DRY - Don't Repeat Yourself)

Instead of copying headers/footers to every page:

**base.html** (parent template):
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Datamon{% endblock %}</title>
</head>
<body>
    <header>Common header here</header>
    
    {% block content %}{% endblock %}
    
    <footer>Common footer here</footer>
</body>
</html>
```

**index.html** (child template):
```html
{% extends "base.html" %}

{% block title %}Main Menu{% endblock %}

{% block content %}
    <h1>Welcome to Datamon!</h1>
{% endblock %}
```

---

## 🔍 Understanding the Code

### Main App (`datamon_flask.py`)

```python
from flask import Flask, render_template, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for sessions

@app.route('/')
def index():
    # Initialize points if first visit
    if 'player_points' not in session:
        session['player_points'] = 0
    
    # Show the menu page with current points
    return render_template('index.html', points=session['player_points'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Key points:**
1. `Flask(__name__)` - Creates the app
2. `app.secret_key` - Required for sessions (use a random string)
3. `@app.route()` - Decorator that connects URLs to functions
4. `render_template()` - Displays an HTML file
5. `debug=True` - Auto-reloads when you change code

### Answer Checking Logic

```python
def check_answer(problem):
    # Split "4+4=8" into equation and answer
    equation, user_answer = problem.split('=')
    
    # Find the operator (+, -, *, /)
    for symbol in operators:
        if symbol in equation:
            left, right = equation.split(symbol)
            
            # Calculate correct answer
            correct = operators[symbol](float(left), float(right))
            
            # Check if user is right
            if float(user_answer) == correct:
                return True, correct, None
            else:
                return False, correct, None
```

---

## 🎨 CSS Explained

CSS (Cascading Style Sheets) controls appearance:

```css
/* Select elements and style them */
.game-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 15px;
    transition: transform 0.3s ease;
}

.game-card:hover {
    transform: translateY(-5px);  /* Move up on hover */
}
```

**Common properties:**
- `background` - Background color/gradient
- `padding` - Space inside element
- `margin` - Space outside element
- `border-radius` - Rounded corners
- `transition` - Smooth animations
- `transform` - Move, rotate, scale elements

---

## 🔧 Common Customizations

### Change Colors

In `style.css`, find the color codes and change them:
```css
/* Purple gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to blue gradient */
background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);

/* Or solid color */
background: #ff6b6b;
```

### Change Port

If port 5000 is busy:
```python
app.run(debug=True, port=8080)  # Use port 8080 instead
```

### Add New Routes

```python
@app.route('/leaderboard')
def leaderboard():
    # Get top players
    return render_template('leaderboard.html')
```

---

## 🐛 Troubleshooting

### "Address already in use"
Another program is using port 5000. Change the port:
```python
app.run(debug=True, port=5001)
```

### Templates Not Found
Make sure your files are in the `templates/` folder, not the root directory.

### Changes Not Showing
- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Or stop and restart the Flask server

### Session Data Not Saving
Make sure you have `app.secret_key` set in your Flask app.

---

## 📖 Learning Resources

### Official Documentation
- Flask: https://flask.palletsprojects.com/
- Jinja2 Templates: https://jinja.palletsprojects.com/
- HTML: https://developer.mozilla.org/en-US/docs/Web/HTML
- CSS: https://developer.mozilla.org/en-US/docs/Web/CSS

### Flask Concepts to Learn Next
1. **Databases** - Store user data permanently (SQLite, PostgreSQL)
2. **User Authentication** - Login/signup systems
3. **RESTful APIs** - Let other apps interact with yours
4. **Deployment** - Put your app on the internet (Heroku, PythonAnywhere)

---

## 🎯 Next Steps for Datamon

### Add Memory Bank & Electro Flash
1. Create the game logic in Python
2. Create HTML templates
3. Add routes in `datamon_flask.py`
4. Update the menu to link to them

### Add Features
- **Timer** - Add countdown for each problem
- **Leaderboard** - Store high scores
- **Difficulty levels** - Easy, medium, hard
- **Sound effects** - Play sounds on correct/wrong
- **Animations** - Add more visual feedback

---

## ❓ Quick Reference

### Flask Commands
```python
# Create app
app = Flask(__name__)

# Route (URL)
@app.route('/path')
def function_name():
    pass

# Render HTML
return render_template('file.html', var=value)

# Redirect
return redirect(url_for('function_name'))

# Get form data
data = request.form.get('field_name')

# Session
session['key'] = value
value = session.get('key', default)

# Flash message
flash('Message', 'category')
```

### Jinja2 Templates
```html
<!-- Variable -->
{{ variable_name }}

<!-- If statement -->
{% if condition %}
    content
{% endif %}

<!-- Loop -->
{% for item in items %}
    {{ item }}
{% endfor %}

<!-- Extend template -->
{% extends "base.html" %}
{% block content %}{% endblock %}
```

---

## 🤝 Need Help?

Flask has a great community! If you get stuck:
1. Read the error message carefully
2. Check the Flask documentation
3. Google the error message
4. Ask on Stack Overflow
5. Check Flask's GitHub issues

Remember: Every developer googles errors constantly - it's part of the job! 😊

Good luck building your Flask app! 🚀

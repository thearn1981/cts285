# Flask Architecture - Visual Guide

## 🏗️ How Flask Connects Everything

```
┌─────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                      │
│  (Chrome, Firefox, etc.)                                    │
│                                                             │
│  Shows: HTML + CSS → What user sees                        │
└─────────────────────────────────────────────────────────────┘
                           ↕ HTTP Requests/Responses
┌─────────────────────────────────────────────────────────────┐
│                      FLASK SERVER                           │
│                   (datamon_flask.py)                        │
│                                                             │
│  ┌─────────────────────────────────────────────────┐       │
│  │              ROUTES (URLs)                      │       │
│  │                                                 │       │
│  │  @app.route('/')                               │       │
│  │  ├─> index()                                   │       │
│  │  │   └─> Shows menu                            │       │
│  │  │                                              │       │
│  │  @app.route('/answer-checker')                 │       │
│  │  ├─> answer_checker()                          │       │
│  │  │   └─> Shows game                            │       │
│  │  │                                              │       │
│  │  @app.route('/answer-checker/submit')          │       │
│  │  └─> submit_answer()                           │       │
│  │      ├─> Check answer                          │       │
│  │      └─> Update score                          │       │
│  └─────────────────────────────────────────────────┘       │
│                           ↕                                 │
│  ┌─────────────────────────────────────────────────┐       │
│  │              SESSION (Memory)                    │       │
│  │                                                 │       │
│  │  session['player_points'] = 42                 │       │
│  │  session['ac_score'] = 8                       │       │
│  │  session['ac_problem_count'] = 9               │       │
│  └─────────────────────────────────────────────────┘       │
│                           ↕                                 │
│  ┌─────────────────────────────────────────────────┐       │
│  │         GAME LOGIC (Business Logic)             │       │
│  │      (AnswerChecker_flask.py)                   │       │
│  │                                                 │       │
│  │  check_answer(problem)                         │       │
│  │  ├─> Parse equation                            │       │
│  │  ├─> Calculate correct answer                  │       │
│  │  └─> Return result                             │       │
│  └─────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                           ↕
┌─────────────────────────────────────────────────────────────┐
│                    TEMPLATES (HTML)                         │
│                   (templates/ folder)                       │
│                                                             │
│  base.html          → Header, footer, layout               │
│  index.html         → Main menu (extends base)             │
│  answer_checker.html→ Game page (extends base)             │
│  coming_soon.html   → Placeholder pages                    │
└─────────────────────────────────────────────────────────────┘
                           ↕
┌─────────────────────────────────────────────────────────────┐
│                      STATIC FILES                           │
│                    (static/ folder)                         │
│                                                             │
│  css/style.css      → All styling (colors, layout, etc.)   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Request Flow Example

Let's trace what happens when a user submits an answer:

```
1. USER ACTION
   │
   ├─> User types "4+4=8" in form
   ├─> Clicks "Check Answer" button
   └─> Browser sends POST request to /answer-checker/submit
       
2. FLASK RECEIVES REQUEST
   │
   ├─> Flask finds matching route: @app.route('/answer-checker/submit')
   ├─> Calls function: submit_answer()
   └─> Gets form data: request.form.get('problem')
       
3. PROCESS ANSWER
   │
   ├─> Calls: check_answer('4+4=8')
   ├─> AnswerChecker_flask.py processes it
   ├─> Returns: (True, 8.0, None)  # Correct!
   └─> Updates session: session['ac_score'] += 1
       
4. SEND FEEDBACK
   │
   ├─> Creates flash message: flash('✅ Correct!', 'success')
   ├─> Redirects back to: /answer-checker
   └─> Browser loads answer_checker.html
       
5. DISPLAY RESULT
   │
   ├─> Template shows flash message (green alert)
   ├─> Updates progress bar
   ├─> Shows next problem or results
   └─> User sees the feedback!
```

---

## 🔄 The Request-Response Cycle

```
Browser                Flask Server              Templates
   │                        │                        │
   │──── GET / ────────────>│                        │
   │                        │                        │
   │                        │──── render index.html ─>│
   │                        │                        │
   │<─── HTML + CSS ────────┼────────────────────────│
   │                        │                        │
   │ (User clicks button)   │                        │
   │                        │                        │
   │─── POST /start ───────>│                        │
   │                        │                        │
   │                        │ (Update session)       │
   │                        │                        │
   │<─── Redirect ──────────│                        │
   │                        │                        │
   │──── GET /game ────────>│                        │
   │                        │                        │
   │                        │──── render game.html ──>│
   │                        │                        │
   │<─── HTML + CSS ────────┼────────────────────────│
   │                        │                        │
```

---

## 🗂️ File Relationships

```
datamon_flask.py (Main controller)
    │
    ├─> imports AnswerChecker_flask.py
    │   └─> Uses check_answer() function
    │
    ├─> renders templates/base.html
    │   └─> Other templates extend this
    │
    ├─> renders templates/index.html
    │   └─> Main menu page
    │
    ├─> renders templates/answer_checker.html
    │   └─> Game page
    │
    └─> Uses session to store:
        ├─> player_points (total score)
        ├─> ac_score (current quiz score)
        └─> ac_problem_count (progress)

All HTML files link to:
    └─> static/css/style.css (styling)
```

---

## 🎯 Data Flow

```
┌──────────────────────────────────────────────────┐
│            User enters "4+4=8"                   │
└──────────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│   Form POSTs to /answer-checker/submit          │
└──────────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│   Flask: request.form.get('problem')             │
│   Result: "4+4=8"                                │
└──────────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│   Call: check_answer("4+4=8")                    │
│   │                                              │
│   ├─> Split: equation="4+4", answer="8"         │
│   ├─> Find operator: "+"                        │
│   ├─> Split: left="4", right="4"                │
│   ├─> Calculate: 4 + 4 = 8                      │
│   ├─> Compare: 8 == 8 ✓                         │
│   └─> Return: (True, 8.0, None)                 │
└──────────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│   Flask processes result:                        │
│   │                                              │
│   ├─> flash('✅ Correct!', 'success')           │
│   ├─> session['ac_score'] = 1                   │
│   ├─> session['ac_problem_count'] = 1           │
│   └─> redirect(url_for('answer_checker'))       │
└──────────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│   Template renders with new data:                │
│   │                                              │
│   ├─> Shows green success alert                 │
│   ├─> Updates progress bar (10%)                │
│   ├─> Shows "Problem 2 of 10"                   │
│   └─> Shows current score: 1                    │
└──────────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│         User sees feedback! 🎉                   │
└──────────────────────────────────────────────────┘
```

---

## 🎨 Template Inheritance Visualization

```
base.html (Parent)
┌────────────────────────────────────┐
│ <html>                             │
│   <head>                           │
│     <title>{% block title %}</title>│
│   </head>                          │
│   <body>                           │
│     <header>Common header</header> │
│                                    │
│     {% block content %}            │← Child content goes here
│     {% endblock %}                 │
│                                    │
│     <footer>Common footer</footer> │
│   </body>                          │
│ </html>                            │
└────────────────────────────────────┘
           ↑           ↑           ↑
           │           │           │
    ┌──────┘           │           └──────┐
    │                  │                  │
┌───────┐      ┌──────────────┐    ┌──────────┐
│index  │      │answer_checker│    │coming_   │
│.html  │      │.html         │    │soon.html │
└───────┘      └──────────────┘    └──────────┘

Each child does:
{% extends "base.html" %}
{% block content %}
  <!-- Their unique content -->
{% endblock %}
```

---

## 💾 Session Storage Visualization

```
Browser                                Flask Server
┌─────────────┐                       ┌──────────────────┐
│             │                       │ SESSION STORAGE  │
│             │                       │                  │
│  Cookie:    │                       │ User ABC123:     │
│  session_id │<──────────────────────│ ├─ points: 42   │
│  = ABC123   │                       │ ├─ score: 8     │
│             │                       │ └─ count: 9     │
│             │                       │                  │
│             │                       │ User XYZ789:     │
│             │                       │ ├─ points: 15   │
│             │                       │ ├─ score: 3     │
│             │                       │ └─ count: 4     │
└─────────────┘                       └──────────────────┘

When user visits:
1. Browser sends cookie (ABC123)
2. Flask looks up ABC123 in session storage
3. Flask loads that user's data
4. Flask uses it in templates
5. Any changes are saved back to ABC123
```

---

## 🔍 Route Matching

```
User visits URL:              Flask matches route:
http://127.0.0.1:5000/   →   @app.route('/')
http://127.0.0.1:5000/answer-checker   →   @app.route('/answer-checker')
http://127.0.0.1:5000/answer-checker/submit   →   @app.route('/answer-checker/submit')

Flask automatically:
1. Parses the URL
2. Finds matching route
3. Calls the function
4. Returns the response
```

---

## 🚀 Full Application Flow

```
START
  │
  ├─> User opens browser
  ├─> Goes to http://127.0.0.1:5000/
  │
  ├─> Flask receives GET request to /
  ├─> Calls index() function
  ├─> Checks session for player_points
  ├─> Renders index.html with points
  │
  ├─> Browser shows menu with 3 game cards
  ├─> User clicks "Answer Checker"
  │
  ├─> Flask receives GET request to /answer-checker
  ├─> Calls answer_checker() function
  ├─> Initializes game state in session
  ├─> Renders answer_checker.html
  │
  ├─> Browser shows welcome screen
  ├─> User clicks "Start Quiz"
  │
  ├─> Flask receives POST request to /answer-checker/start
  ├─> Calls start_quiz() function
  ├─> Sets game_active = True in session
  ├─> Redirects to /answer-checker
  │
  ├─> Browser shows problem 1 form
  ├─> User enters answer and clicks submit
  │
  ├─> Flask receives POST request to /answer-checker/submit
  ├─> Calls submit_answer() function
  ├─> Gets problem from form
  ├─> Calls check_answer()
  ├─> Updates score in session
  ├─> Creates flash message
  ├─> Redirects to /answer-checker
  │
  ├─> Browser shows feedback and next problem
  ├─> Repeats for 10 problems
  │
  ├─> After problem 10, shows results
  ├─> Adds score to total points
  ├─> User clicks "Back to Menu"
  │
  └─> Returns to main menu with updated points!
```

---

## 💡 Key Takeaways

1. **Flask = Controller** - Directs traffic and makes decisions
2. **Templates = View** - What users see
3. **Logic Functions = Model** - Business logic and calculations
4. **Session = Memory** - Remembers user data
5. **Routes = URLs** - Maps URLs to functions

This is the **MVC Pattern** (Model-View-Controller)!

---

## 🎓 Understanding Through Analogies

**Flask App = Restaurant**

- **Routes** = Menu (tells what's available)
- **Functions** = Chefs (prepare what was ordered)
- **Templates** = Plates (how food is presented)
- **Session** = Tab (remembers what you ordered)
- **Static files** = Decorations (makes it look nice)

**When a customer orders:**
1. They look at menu (routes)
2. Chef receives order (function is called)
3. Chef cooks (processes logic)
4. Food is plated nicely (renders template)
5. Served to customer (HTML sent to browser)
6. Added to tab (session updated)

---

Hope this helps you visualize how everything connects! 🎯

# Learning Process Documentation
## Citizen Wellness Portal - PROCESS.md

**Citizen Name:** Teresa Hearn    
**Date Started:** 11/26/2025
**Date Completed:** 12/4/2025
**Total Time Spent:** [X hours]

## Part 1: Initial Understanding

### What I knew Before Starting
> Befoe this assigment, this was not my first time playing around streamlit. In Advanced Python Class for the
> the final project, my group decided to use streamlit over flask for the simplicity of some of the functions.

### First Impressions
> While I some of he ways you can customize flask makes its more appealing if you are looking for a specific look that you 
> may not be able to achieve with streamlit.  Streamlit on the other hand if has some cool features and while we used streamlit
> having some extra time to kinda explore some of the other ways that streamlit is different from flask is nice and helpful.

## Part 2: LLM-Assisted Learning

### Prompt 1: Understanding the differences between the two and how request/response cycle differs

**Initial Prompt:**
I know Flask but not Streamlit. Explain Streamlit's execution model— how does it differ from Flask's request/response cycle? What happens when a user clicks a button?

**Key insights from response:**
> In Flask:
> browser sends an HTTP request (GET/POST/etc)
> Flask matches it to a route function (@app.route("/..."))
> Only that function runs, builds a response(HTML,JSON,etc), and returns it.
> The server is basically stateless between requests unless you:
    * Store stuff in a database/session/cache or use globals
> So: request comes in → handler runs → response goes out.

>In streamlit:
> there are no explicit routes and no template rendering step. 
> instead the python script describes the UI top-to bottom.
> streamlit re0runs your entire script from top to bottom.
> On first page load:

Streamlit runs your script from line 1 to the end.

As it hits Streamlit calls (st.title, st.text_input, st.button, etc.), it:

Builds the UI for the browser, and

Connects each widget to internal state.

When the user types in a text_input, clicks a button, moves a slider, etc.:

The browser sends updated widget state to the Streamlit server (over WebSocket/HTTP under the hood).

Streamlit re-runs your script from the top, using the current values of all widgets.

The page is re-rendered based on the new state.

There’s no manual render_template, no separate “view” and “controller”.
The script is your view/controller, and it’s always evaluated top-to-bottom.

Per-user sessions

Each connected user (or even each browser tab) gets its own session.

Streamlit maintains:

Each session’s widget values

Optional st.session_state for extra state you want to track

So st.text_input or st.button values are per user by default.

**Follow-up prompt:**
Can you make a side by side model showing the differences.

**key insight from response**
Concept	                Flask           	                        Streamlit
------------------------------------------------------------------------------------------------------------------
Entry point	            Many route functions	                    One main script (optionally split into modules)
Trigger for code    	HTTP request	                            Any UI interaction / page load
Scope of execution	    Only the matched route handler	            Entire script reruns top-to-bottom
State persistence	    DB, session, globals, etc.	                Widget state + st.session_state per user session
Templates / HTML	    Manual templates (render_template)	        UI defined directly in Python (st.* calls)
Button click	        New HTTP request to a route	                Sends widget update → reruns script → st.button True once

**What I Understood After This Exchange:**
> That how things are ran is different. Flask only uses the function that as called and streamlit reruns the whole thing.

### Prompt 2: ["Session State Basics"]

**Initial Prompt:**
can you in simple terms explain to me Session state Basics for streamlit

**Key Insights from Response:**
> Since the script is re ran every time seesion states help remember things between these reruns.
> Because without it:
> counters reset
> form inputs disappear
> temporary values vanish
> your app "forgets" everything each rerun
> Session state lets you store values that should survive those reruns.
> Session state will remember anything you need it to remember:
> numbers
> strings
> lists
> objects
> flags(like "button clicked?" or "tab opened?")

**Follow-up Prompt (if any):**
> soo if i run a session state "tessa" today and then close it, and then i create other sessions between then and say tomorrow and i go > back to session state "tessa" does the data still stored or no?

**What I Understood After This Exchange:**
> Sessions states help remember things for that current session which is super helpful.
> Sessions does not survive after closing the crowser tab, referesing the page or restarting the streamlit server.
> If you wanted to persist over night or between sessions you would need to save to something like: a CSV, a JSON file, 
> a SQLite database, or a cloud database.
### Prompt 3: ["Building the Login Form"]

**Initial Prompt:**
> In building a login form what are some approaches to consider and which is the best and why.

**Key Insights from Response:**
> That while there are a few different ways to build a login form using sqlite with hashed passwords seemed to be the best
> solution for the project considering hard coding would be to much and not as secure as sqlite with hashed passwords.

**Follow-up prompt**
> in very simple step by step explain how i would build a login form using a sqlite database

**What Worked vs. What I Had to Modify:**
> The LLM did create a working code that worked.  I had to get some help from copilot to help with the env,
> since even tho i set up my virtual enviroment and installed streamlit it was still giving a error.
> once i ws finally able to tess the login of the created database and login it was succesfull.

---

### Prompt 4: [Deciding on which navigation would be best to use]

**Initial Prompt:**
> Great so lets move on.. I need both login and registration in my Streamlit app. Should I use st.tabs, st.sidebar navigation, or 
> Streamlit's multipage app feature? What are the tradeoffs?"
**Key Insights from Response:**
> That while there are a few different ways to build a login form using sqlite with hashed passwords seemed to be the best
> solution for the project considering hard coding would be to much and not as secure as sqlite with hashed passwords.

**Key Insights from Response:**
> there are three differen layout/navigation paterns to choose from.

> For st.tabs :
 > It would show both login and register on the same main screen as two tabs.
 > pros:
 > perfect for closely related things like login and sign up.
 > users can easily flip between "login" and "register." 
 > easy logic.
 > Cons:
 > not great if the app grows into many "real pages." (Dashboard, reports, admins, etc.)   
 > can not deep link to a tab (URL is the same)
 > When it’s a good fit:
 > Small/medium app.
 > You want login + register together on a single “entry” screen.
 > You’re still learning and want to keep it simple.

> For Side bar naigation. (st.sidebar.radio/selectbox)
 > The sidebar as a mini menu with options like "login", "register", "home", etc.
 > Pros:
 > Still one python file and one session_state.
 > easy to add more "pages" later with out  multipage structure.
 > users always see the navigation in one place (sidebar)
 > Cons: 
 > slightly more code to manage "what to show when" (you write your own route.)
 > login/registration feel like sperate pages, even though you might want them grouped together visually.
 > if users are not logged in, you must uard pages manually.
 > The sidebar nav still shows options like “Main App” even if they aren’t allowed yet (unless you hide/adjust it).
 > When it’s a good fit:
 > You expect to grow the app soon (more screens).
 > You’re okay with manual routing logic.
 > You like having a fixed navigation area.

> For Streamlit Multipage Apps (pages/ folder):
 >You split your app into multiple files:
  > Home.py
  > pages/Login.py
  > pages/Register.py
  > pages/Dashboard.py
 > Pros:
  > Best structure for larger apps.
  > Each page is its own script → cleaner, more modular code.
  > You can keep login logic in Home.py and protect other pages using st.session_state.
 > Cons:
  > More moving parts:
   > Multiple files
   > Imports for shared functions
   > Need to think about how pages share state
   > For just Login + Register, this is overkill.
   > Can be a little confusing when you’re still learning how reruns + session_state work.
 > When it’s a good fit
  > You’re building a multi-page tool (analytics app, dashboard suite, etc.).
  > You already understand Streamlit basics and want better organization.

**Follow-up prompt**
> What should I use for the login and registration for the citizen-wellness-portal?

**Key Insights from Response:**
> st.tabs was recommended for what I am creating since I am still learning streamlit and how session_state work.
> It will make a good flow between login and registering.
> The app is small and medium right now.



---

### Prompt 5: [Additional Topic]

**Prompt:**
```
[Your prompt]
```

**What I Learned:**
> [Key takeaway]

---

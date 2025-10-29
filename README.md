# Datamon Streamlit App - Setup Instructions

## What You'll Need
- Python 3.7 or higher
- pip (Python package installer)

## Installation Steps

### 1. Install Streamlit
Open your terminal/command prompt and run:
```bash
pip install streamlit
```

Or if you have the requirements.txt file:
```bash
pip install -r requirements.txt
```

### 2. Run the App
Navigate to the folder containing your files and run:
```bash
streamlit run datamon_streamlit.py
```

### 3. Use the App
- Your web browser should automatically open to `http://localhost:8501`
- If it doesn't, manually open that URL in your browser
- The app will reload automatically whenever you save changes to the code!

## File Structure
```
your-project-folder/
├── datamon_streamlit.py          # Main app file
├── AnswerChecker_streamlit.py    # Answer Checker game
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

## Key Features Added

### 🎨 Visual Improvements
- **Buttons instead of text menu** - Click to navigate
- **Progress bars** - See how far you are in the quiz
- **Color-coded feedback** - Green for correct, red for wrong
- **Emojis** - Makes it more fun! 🎉

### 💾 Session State
- **Points persist** - Your score is saved as you play
- **Game state management** - The app remembers where you are

### 🎮 Enhanced Gameplay
- **Clear instructions** - Users know what to do
- **Instant feedback** - See results immediately
- **Balloons celebration** - Special effect for correct answers!

## How It Works (Technical Explanation)

### Session State
Streamlit apps reload from top to bottom every time you interact with them. To remember data (like your points), we use `st.session_state`:

```python
if 'player_points' not in st.session_state:
    st.session_state.player_points = 0
```

This creates a variable that persists across reruns.

### Page Navigation
We use a state variable to track which page to show:

```python
if st.session_state.current_page == 'menu':
    show_menu()
elif st.session_state.current_page == 'answer_checker':
    answer_checker_page()
```

When you click a button, we change `current_page` and call `st.rerun()` to refresh the app.

### Forms
Forms prevent the page from rerunning on every keystroke:

```python
with st.form(key="my_form"):
    user_input = st.text_input("Enter problem:")
    submit = st.form_submit_button("Submit")
    
    if submit:
        # Process the input
```

## Next Steps

### Adding Memory Bank and Electro Flash
When you're ready to add the other games:

1. Create `memorybank_streamlit.py` and `ElectroFlash_streamlit.py`
2. Import them in `datamon_streamlit.py`
3. Uncomment the button code in the menu
4. Add the page logic in the main() function

### Customization Ideas
- Change colors with `st.set_page_config()`
- Add a leaderboard with a database
- Include timer challenges
- Add sound effects (using `st.audio()`)

## Troubleshooting

### Port Already in Use
If you get an error about port 8501 being in use:
```bash
streamlit run datamon_streamlit.py --server.port 8502
```

### App Not Loading
- Check that all files are in the same folder
- Make sure you're running the command from the correct directory
- Try closing and reopening your browser

## Questions?
Feel free to ask! Some things to explore:
- How does `st.session_state` work?
- What do `st.rerun()` and forms do?
- How can you style the app differently?

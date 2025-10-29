"""
Datamon - Answer Checker (Streamlit Version)

A math problem helper that helps students, teachers and parents
make math fun.

Haylee Kaheel Teresa Aryan James
"""

import streamlit as st
import operator

# A dictionary of operators and their corresponding functions
operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def check_answer(problem):
    """
    Check if the user's answer to a math problem is correct
    Returns: (is_correct, correct_answer, error_message)
    """
    try:
        equation, user_answer = problem.split('=')
        operator_symbol = None
        first_num = second_num = None

        matched = [(symbol, equation.split(symbol)) for symbol in operators if symbol in equation]

        if not matched or len(matched[0][1]) != 2:
            return False, None, "Invalid equation format. Use format like: 4+4=8"

        operator_symbol, (left, right) = matched[0]
        first_num = float(left)
        second_num = float(right)

        operator_function = operators[operator_symbol]
        correct_answer = operator_function(first_num, second_num)

        if float(user_answer) == correct_answer:
            return True, correct_answer, None
        else:
            return False, correct_answer, None

    except Exception as e:
        return False, None, f"Error: {str(e)}"


def answer_checker_page():
    """The Answer Checker game page in Streamlit"""
    
    # Initialize session state variables for this game
    if 'ac_score' not in st.session_state:
        st.session_state.ac_score = 0
    
    if 'ac_problem_count' not in st.session_state:
        st.session_state.ac_problem_count = 0
    
    if 'ac_game_active' not in st.session_state:
        st.session_state.ac_game_active = False
    
    # Header
    st.title("📝 Answer Checker")
    
    # Back to menu button
    if st.button("← Back to Menu"):
        # Reset game state when going back
        st.session_state.ac_game_active = False
        st.session_state.ac_problem_count = 0
        st.session_state.ac_score = 0
        st.session_state.current_page = 'menu'
        st.rerun()
    
    st.markdown("---")
    
    # Game instructions
    if not st.session_state.ac_game_active:
        st.markdown("""
        ### How to Play:
        1. You'll solve **10 math problems**
        2. Enter problems in the format: `4+4=8`
        3. Supported operations: `+`, `-`, `*`, `/`
        4. Each correct answer earns you **1 point**!
        
        **Example problems:**
        - `5+3=8` ✅
        - `10-4=6` ✅
        - `6*7=42` ✅
        - `15/3=5` ✅
        """)
        
        if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
            st.session_state.ac_game_active = True
            st.session_state.ac_problem_count = 0
            st.session_state.ac_score = 0
            st.rerun()
    
    else:
        # Game is active
        if st.session_state.ac_problem_count < 10:
            # Show progress
            st.progress((st.session_state.ac_problem_count) / 10)
            st.markdown(f"**Problem {st.session_state.ac_problem_count + 1} of 10**")
            st.markdown(f"**Current Score: {st.session_state.ac_score}** 🌟")
            
            # Input form
            with st.form(key=f"problem_form_{st.session_state.ac_problem_count}"):
                problem = st.text_input(
                    "Enter your math problem:",
                    placeholder="e.g., 4+4=8",
                    key=f"input_{st.session_state.ac_problem_count}"
                )
                submit_button = st.form_submit_button("Check Answer", type="primary")
                
                if submit_button:
                    if problem.strip():
                        is_correct, correct_answer, error_msg = check_answer(problem.strip())
                        
                        if error_msg:
                            st.error(f"❌ {error_msg}")
                        elif is_correct:
                            st.success("✅ Correct! Great job!")
                            st.balloons()
                            st.session_state.ac_score += 1
                            st.session_state.ac_problem_count += 1
                            st.rerun()
                        else:
                            st.error(f"❌ Wrong! The correct answer is {correct_answer}")
                            st.session_state.ac_problem_count += 1
                            st.rerun()
                    else:
                        st.warning("⚠️ Please enter a problem!")
        
        else:
            # Quiz completed
            st.markdown("---")
            st.header("🎉 Quiz Complete!")
            
            # Calculate percentage
            percentage = (st.session_state.ac_score / 10) * 100
            
            # Show results with color coding
            if percentage >= 80:
                st.success(f"### Excellent! You scored {st.session_state.ac_score}/10 ({percentage}%)")
                st.balloons()
            elif percentage >= 60:
                st.info(f"### Good job! You scored {st.session_state.ac_score}/10 ({percentage}%)")
            else:
                st.warning(f"### Keep practicing! You scored {st.session_state.ac_score}/10 ({percentage}%)")
            
            # Add points to total
            st.session_state.player_points += st.session_state.ac_score
            
            st.markdown(f"**Points earned: +{st.session_state.ac_score}** 🌟")
            st.markdown(f"**Total Points: {st.session_state.player_points}** 🏆")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Play Again", use_container_width=True):
                    st.session_state.ac_game_active = False
                    st.session_state.ac_problem_count = 0
                    st.session_state.ac_score = 0
                    st.rerun()
            
            with col2:
                if st.button("🏠 Back to Menu", use_container_width=True):
                    st.session_state.ac_game_active = False
                    st.session_state.ac_problem_count = 0
                    st.session_state.ac_score = 0
                    st.session_state.current_page = 'menu'
                    st.rerun()

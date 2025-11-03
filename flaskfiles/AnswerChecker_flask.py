"""
Datamon - Answer Checker (Flask Version)

A math problem helper that helps students, teachers and parents
make math fun.

Haylee Kaheel Teresa Aryan James
"""

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
    
    Args:
        problem (str): Math problem in format "4+4=8"
    
    Returns:
        tuple: (is_correct, correct_answer, error_message)
               - is_correct (bool): True if answer is correct
               - correct_answer (float): The correct answer
               - error_message (str): Error message if any, None otherwise
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

    except ValueError as e:
        return False, None, "Please enter valid numbers"
    except Exception as e:
        return False, None, f"Error: {str(e)}"

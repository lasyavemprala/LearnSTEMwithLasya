import streamlit as st
import random
import statistics

st.title("Learn STEM with Lasya!")

# Initialize session state variables
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'equation' not in st.session_state:
    st.session_state.equation = ""
if 'numbers' not in st.session_state:
    st.session_state.numbers = []
if 'stat_question' not in st.session_state:
    st.session_state.stat_question = ""
if 'answer_checked' not in st.session_state:
    st.session_state.answer_checked = False  # New variable to track if answer has been checked

# Dropdown menu for selecting the type of question
question_type = st.selectbox("Select the type of question", ["Solve for X", "Statistical Estimators"])

def generate_equation(difficulty):
    """Generates a random linear equation with integer solutions
    and adjustable difficulty.
    """
    while True:  # Keep generating until an integer solution is found
        a = random.randint(1 + difficulty, 10 + difficulty)
        b = random.randint(1 + difficulty * 10, 50 + difficulty * 10)
        c = random.randint(1 + difficulty, 10 + difficulty)
        d = random.randint(1 + difficulty * 10, 50 + difficulty * 10)
        sign1 = random.choice(['+', '-'])
        sign2 = random.choice(['+', '-'])

        # Calculate potential answer to check if it's an integer
        if sign1 == '+':
            left_side = b
        else:
            left_side = -b

        if sign2 == '+':
            right_side = d
        else:
            right_side = -d

        if (a - c) != 0 and (right_side - left_side) % (a - c) == 0:  # Check for integer solution
            equation = f"{a}x {sign1} {b} = {c}x {sign2} {d}"
            return equation

def calculate_answer(equation):
    """Calculates the correct answer for the given equation."""
    a, sign1, b, eq, c, sign2, d = equation.split()
    a, b, c, d = map(int, [a.replace('x', ''), b, c.replace('x', ''), d])
    left_side = b if sign1 == '+' else -b
    right_side = d if sign2 == '+' else -d
    return (right_side - left_side) / (a - c)

def check_answer(user_answer, correct_answer):
    """Checks if the user's answer is correct and updates the score."""
    try:
        user_answer = float(user_answer)
        if abs(user_answer - correct_answer) < 1e-6:
            st.session_state.score += 1
            st.success("Correct!")
            return True
        else:
            st.error(f"Incorrect. The correct answer is x = {correct_answer}")
            return False
    except ValueError:
        st.error("Invalid input. Please enter a numerical value.")
        return False

def generate_stat_question():
    """Generates a random set of numbers and a statistical question."""
    num_count = random.randint(5, 15)
    numbers = [random.randint(1, 100) for _ in range(num_count)]
    st.session_state.numbers = numbers
    question_type = random.choice(['mean', 'median', 'mode', 'range'])
    st.session_state.stat_question = question_type
    return f"Calculate the {question_type} of the following numbers: {numbers}"

def calculate_stat_answer(numbers, question_type):
    """Calculates the correct answer for the given statistical question."""
    if question_type == 'mean':
        return statistics.mean(numbers)
    elif question_type == 'median':
        return statistics.median(numbers)
    elif question_type == 'mode':
        return statistics.mode(numbers)
    elif question_type == 'range':
        return max(numbers) - min(numbers)

def check_stat_answer(user_answer, correct_answer):
    """Checks if the user's answer is correct and updates the score."""
    try:
        user_answer = float(user_answer)
        if abs(user_answer - correct_answer) < 1e-6:
            st.session_state.score += 1
            st.success("Correct!")
            return True
        else:
            st.error(f"Incorrect. The correct answer is {correct_answer}")
            return False
    except ValueError:
        st.error("Invalid input. Please enter a numerical value.")
        return False

# Game logic
if st.session_state.question_count < 25:
    
    if question_type == "Solve for X":

        # Use CSS to style the button
        st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #800080;  /* Purple color */
        color: white;
    }
    </style>""", unsafe_allow_html=True)

        if st.button("Click to get YOUR question Now!", key="custom_button"):
            difficulty = st.session_state.score // 5
            st.session_state.equation = generate_equation(difficulty)
            st.session_state.answer_checked = False  # Reset the answer_checked flag
            st.session_state.user_answer = "" 

        st.write(f"Solve for x: {st.session_state.equation}")
        st.session_state.user_answer = "" 
        user_answer = st.text_input("Your answer (x = )")

        if st.button("Check Answer") and not st.session_state.answer_checked:
            if check_answer(user_answer, calculate_answer(st.session_state.equation)):
                st.session_state.question_count += 1
            else:
                st.session_state.score = max(0, st.session_state.score - 1)
            st.session_state.answer_checked = True  # Set the answer_checked flag to True
            st.write(f"Current Score: {st.session_state.score} \n")
            st.write(f" ------------------------------------------- \n")
            st.write(f"  Click the top button to get next question \n")
            st.write(f" ------------------------------------------- \n")

    elif question_type == "Statistical Estimators":
        # Use CSS to style the button
        st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #191970;  /* Dark blue shade color */
        color: white;
    }
    </style>""", unsafe_allow_html=True)
        if st.button("Click to get YOUR question Now!", key="custom_button"):
            st.session_state.user_answer = "" 
            st.session_state.equation = generate_stat_question()
            st.session_state.answer_checked = False  # Reset the answer_checked flag

        st.write(st.session_state.equation)
        user_answer = st.text_input("Your answer")

        if st.button("Check Answer") and not st.session_state.answer_checked:
            correct_answer = calculate_stat_answer(st.session_state.numbers, st.session_state.stat_question)
            if check_stat_answer(user_answer, correct_answer):
                st.session_state.question_count += 1
            else:
                st.session_state.score = max(0, st.session_state.score - 1)
            st.session_state.answer_checked = True  # Set the answer_checked flag to True
            st.write(f"Current Score: {st.session_state.score} \n")
            st.write(f" ------------------------------------------- \n")
            st.write(f"  Click the top button to get next question \n")
            st.write(f" ------------------------------------------- \n")

else:
    st.write("Game Over!")
    st.write(f"Final Score: {st.session_state.score}")
    if st.button("Play Again"):
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.equation = ""
        st.session_state.numbers = []
        st.session_state.stat_question = ""
        st.session_state.answer_checked = False  # Reset the answer_checked flag
        st.experimental_rerun()
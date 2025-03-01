import streamlit as st
import random
import statistics
#from dotenv import load_dotenv
import os

# Load environment variables
#load_dotenv()
#user_name_terms = os.getenv("USER_NAME_TERMS").split(",")
user_name_terms = st.secrets["USER_NAME_TERMS"]
user_name_terms = user_name_terms.split(",")

# Initialize authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Authentication
st.title("Learn STEM with Lasya!")
user_name = st.text_input("Enter your term (user name)")
secret_code = st.text_input("Enter your secret code", type="password")

if st.button("Authenticate"):
    if user_name in user_name_terms and secret_code == user_name:
        st.session_state.authenticated = True
        st.success("Authentication successful!")
    else:
        st.session_state.authenticated = False
        st.error("Invalid term or secret code.")

# Initialize session state variables (only if authenticated)
if st.session_state.authenticated:
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
        st.session_state.answer_checked = False
    if 'interest_params' not in st.session_state:
        st.session_state.interest_params = {}

    # Dropdown menu for selecting the type of question
    question_type = st.selectbox("Select the type of question", 
                                ["Solve for X", "Statistical Estimators", "Interest Calculations"])

# Existing functions remain unchanged
def generate_equation(difficulty):
    while True:
        a = random.randint(1 + difficulty, 10 + difficulty)
        b = random.randint(1 + difficulty * 10, 50 + difficulty * 10)
        c = random.randint(1 + difficulty, 10 + difficulty)
        d = random.randint(1 + difficulty * 10, 50 + difficulty * 10)
        sign1 = random.choice(['+', '-'])
        sign2 = random.choice(['+', '-'])
        if sign1 == '+': left_side = b
        else: left_side = -b
        if sign2 == '+': right_side = d
        else: right_side = -d
        if (a - c) != 0 and (right_side - left_side) % (a - c) == 0:
            equation = f"{a}x {sign1} {b} = {c}x {sign2} {d}"
            return equation

def calculate_answer(equation):
    a, sign1, b, eq, c, sign2, d = equation.split()
    a, b, c, d = map(int, [a.replace('x', ''), b, c.replace('x', ''), d])
    left_side = b if sign1 == '+' else -b
    right_side = d if sign2 == '+' else -d
    return (right_side - left_side) / (a - c)

def check_answer(user_answer, correct_answer):
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
    num_count = random.randint(5, 15)
    numbers = [random.randint(1, 100) for _ in range(num_count)]
    st.session_state.numbers = numbers
    question_type = random.choice(['mean', 'median', 'mode', 'range'])
    st.session_state.stat_question = question_type
    return f"Calculate the {question_type} of the following numbers: {numbers}"

def calculate_stat_answer(numbers, question_type):
    if question_type == 'mean': return statistics.mean(numbers)
    elif question_type == 'median': return statistics.median(numbers)
    elif question_type == 'mode': return statistics.mode(numbers)
    elif question_type == 'range': return max(numbers) - min(numbers)

def check_stat_answer(user_answer, correct_answer):
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

def generate_interest_question():
    principal = random.randint(1000, 10000) * 10
    rate = random.randint(1, 10)
    time = random.randint(1, 5)
    is_compound = random.choice([True, False])
    st.session_state.interest_params = {'principal': principal, 'rate': rate, 'time': time, 'is_compound': is_compound}
    if is_compound:
        return (f"Calculate the compound interest earned with a principal of ${principal:,}, "
                f"an annual interest rate of {rate}%, compounded annually for {time} years.")
    else:
        return (f"Calculate the simple interest earned with a principal of ${principal:,}, "
                f"an annual interest rate of {rate}% for {time} years.")

def calculate_interest_answer(params):
    p = params['principal']
    r = params['rate'] / 100
    t = params['time']
    if params['is_compound']:
        total_amount = p * (1 + r) ** t
        interest = total_amount - p
    else:
        interest = p * r * t
    return round(interest, 2)

def check_interest_answer(user_answer, correct_answer):
    try:
        user_answer = float(user_answer)
        if abs(user_answer - correct_answer) < 1:
            st.session_state.score += 1
            st.success("Correct!")
            return True
        else:
            st.error(f"Incorrect. The correct answer is ${correct_answer:,.2f}")
            return False
    except ValueError:
        st.error("Invalid input. Please enter a numerical value.")
        return False

# Game logic (only shows if authenticated)
if st.session_state.authenticated and st.session_state.question_count < 25:
    if question_type == "Solve for X":
        st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #800080;
            color: white;
        }
        </style>""", unsafe_allow_html=True)

        if st.button("Click to get YOUR question Now!", key="custom_button"):
            difficulty = st.session_state.score // 5
            st.session_state.equation = generate_equation(difficulty)
            st.session_state.answer_checked = False
            st.session_state.user_answer = ""

        st.write(f"Solve for x: {st.session_state.equation}")
        user_answer = st.text_input("Your answer (x = )")

        if st.button("Check Answer") and not st.session_state.answer_checked:
            correct_answer = calculate_answer(st.session_state.equation)
            if check_answer(user_answer, correct_answer):
                st.session_state.question_count += 1
            st.session_state.answer_checked = True
            st.write(f"Current Score: {st.session_state.score}")
            st.write("-------------------------------------------")
            st.write("Click the top button to get next question")
            st.write("-------------------------------------------")

    elif question_type == "Statistical Estimators":
        st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #191970;
            color: white;
        }
        </style>""", unsafe_allow_html=True)
        if st.button("Click to get YOUR question Now!", key="custom_button"):
            st.session_state.user_answer = ""
            st.session_state.equation = generate_stat_question()
            st.session_state.answer_checked = False

        st.write(st.session_state.equation)
        user_answer = st.text_input("Your answer")

        if st.button("Check Answer") and not st.session_state.answer_checked:
            correct_answer = calculate_stat_answer(st.session_state.numbers, st.session_state.stat_question)
            if check_stat_answer(user_answer, correct_answer):
                st.session_state.question_count += 1
            st.session_state.answer_checked = True
            st.write(f"Current Score: {st.session_state.score}")
            st.write("-------------------------------------------")
            st.write("Click the top button to get next question")
            st.write("-------------------------------------------")

    elif question_type == "Interest Calculations":
        st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #006400;
            color: white;
        }
        </style>""", unsafe_allow_html=True)
        if st.button("Click to get YOUR question Now!", key="custom_button"):
            st.session_state.user_answer = ""
            st.session_state.equation = generate_interest_question()
            st.session_state.answer_checked = False

        st.write(st.session_state.equation)
        user_answer = st.text_input("Your answer ($)")

        if st.button("Check Answer") and not st.session_state.answer_checked:
            correct_answer = calculate_interest_answer(st.session_state.interest_params)
            if check_interest_answer(user_answer, correct_answer):
                st.session_state.question_count += 1
            st.session_state.answer_checked = True
            st.write(f"Current Score: {st.session_state.score}")
            st.write("-------------------------------------------")
            st.write("Click the top button to get next question")
            st.write("-------------------------------------------")

elif st.session_state.authenticated:
    st.write("Game Over!")
    st.write(f"Final Score: {st.session_state.score}")
    if st.button("Play Again"):
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.equation = ""
        st.session_state.numbers = []
        st.session_state.stat_question = ""
        st.session_state.interest_params = {}
        st.session_state.answer_checked = False
        st.experimental_rerun()
else:
    st.write("Please authenticate to start playing!")
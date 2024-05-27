import streamlit as st
import pandas as pd
import ast
import random
import numpy as np


df = pd.read_csv('words.csv')
df2 = pd.read_csv('seq_ques.csv')


test_no = 0
while df2['status'].iloc[test_no] != "None":
    test_no += 1


test_no += 1

# Initialize session state variables
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.answers = []
    st.session_state.random_numbers = ast.literal_eval(
        df2['test_seq'].iloc[test_no-1])
    st.session_state.answer_index = 0
    st.session_state.correct_answers = []
    st.session_state.sentence_seq = []


# Start From here


def show_question():

    list_seq = st.session_state.random_numbers
    arr = ['sentence1', 'sentence2', 'sentence3', 'sentence4', 'sentence5']
    st.session_state.sentence_seq.append(arr[random.randint(0, len(arr)-1)])

    st.write(
        f"Question {st.session_state.question_index + 1}/{30}")
    st.write(
        f"{df[st.session_state.sentence_seq[st.session_state.question_index]].iloc[list_seq[st.session_state.question_index]]}.".replace(df['word'].iloc[list_seq[st.session_state.question_index]], "_________"))

    list_a = ast.literal_eval(
        df['option_result'].iloc[list_seq[st.session_state.question_index]])
    answer = st.radio("Select an option:", list_a[:5],
                      index=0, key=f"q{st.session_state.question_index}")

    return list_a.index(answer), list_a[-1]


def make_seq(wrong_arr, no, status):

    df = pd.read_csv('seq_ques.csv')
    df1 = pd.read_csv('words.csv')

    df.at[no, 'wrong_word'] = str(wrong_arr)
    df.at[no, 'status'] = status

    print(type(wrong_arr))

    prev_seq = df.at[no, 'test_seq']

    wrong_seq = df.at[no, 'wrong_word']

    prev_seq = eval(prev_seq)

    wrong_seq = eval(wrong_seq)

    print("prev_seq", prev_seq,  type(prev_seq))
    print("wrong_seq", wrong_seq, type(wrong_seq))

    range_values = list(range(len(df1['word'])))

    range_values = [
        x for x in range_values if x not in prev_seq + wrong_seq]

    combined_sources = [prev_seq, wrong_seq, range_values]

    combined_probs = [0.10, 0.25, 0.65]

    def weighted_random_choice():
        chosen_list = random.choices(
            combined_sources, weights=combined_probs, k=1)[0]
        return random.choice(chosen_list) if chosen_list else None

    num_elements = 30
    result_array = [weighted_random_choice() for _ in range(num_elements)]

    result_array = [x for x in result_array if x is not None]

    df.at[no+1, 'test_seq'] = str(result_array)

    df.to_csv('seq_ques.csv', index=False)
    return 1


# Function to calculate the score


def calculate_score_wrong_answer():

    score = sum([1 for i in range(30)
                if st.session_state.answers[i] == st.session_state.correct_answers[i]])
    return score


# Display the current question or the final score
if st.session_state.question_index < 30:
    user_answer_index, correct_answer_ind = show_question()

    df.to_csv('question_seq.csv', index=False)
    if st.button("Next"):
        st.session_state.answers.append(user_answer_index)
        st.session_state.correct_answers.append(correct_answer_ind)
        st.session_state.question_index += 1
        st.experimental_rerun()
else:

    score = calculate_score_wrong_answer()

    st.write(
        f"You've completed the quiz! Your score is {score}/{30}.")
    st.write("Your answers were:")
    for i in range(30):
        st.write(
            f"Q{i+1}: {df[st.session_state.sentence_seq[i]].iloc[st.session_state.random_numbers[i]]}")

        list_a = ast.literal_eval(
            df['option_result'].iloc[st.session_state.random_numbers[i]])
        st.write(
            f"Your answer: {list_a[st.session_state.answers[i]]}")
        st.write(
            f"Correct answer: {list_a[st.session_state.correct_answers[i]]}")
    wrong_num = list(filter(lambda x: x not in st.session_state.correct_answers,
                            st.session_state.random_numbers))
    print(type(wrong_num))
    make_seq(wrong_num, test_no-1, "Done")

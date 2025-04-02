from general_functions import *
from random import sample
from time import sleep


def load_questions(subject, limit=10):
    subject_data = load_csv(f"{subject.title()}_questions.csv")
    random_indices = sample(range(len(subject_data)), limit if (limit < len(subject_data)) else len(subject_data))
    questions = [subject_data[i] for i in random_indices]
    for question in questions:
        random_options = sample(range(4), 4)
        question['options'] = [eval(question['options'])[i] for i in random_options]
    return questions


def take_test(user_name, subject, questions):
    print(f"\n---------------- {subject.upper()} -----------------")
    user_answers = []
    score = 0
    q_no = 0
    total_questions = len(questions)
    print(f"{subject} test will start soon")
    print(f"There are {total_questions} questions")
    sleep(3)
    for q in questions:
        q_no += 1
        print(f"\n{q_no}. {q['question']}")
        for i, option in enumerate(q['options'], 1):
            print(f"{i}) {option}")

        user_choice = get_valid_choice(4)

        if not (user_choice == -1):
            user_answers.append(user_choice - 1)
            action = f'answered "{q['options'][user_choice - 1]}" for the question "{q['question']} "'
            action += f"- Correct Answer: {q['answer']}"
            log_action(user_name, action)
            if q["options"][user_choice - 1] == q["answer"]:
                score += 1
        else:
            action = f"didn't answer for {q['question']}"
            log_action(user_name, action)
            user_answers.append(user_choice)
            print("Nab give up")

    action = f"completed the {subject} test with the score of {score}/{total_questions}"
    print(f"\nTest completed! {user_name}, you scored {score} out of {total_questions} in {subject}.")
    log_action(user_name, action)
    print("\nSolutions:")
    print_questions(questions, user_answers)
    return score


def test_page(user_data):
    print("Select a subject:")
    print("1. Biology")
    print("2. Physics")
    print("3. Chemistry")
    print("4. Maths")

    subject = ""
    subject_choice = get_valid_choice(4)
    if subject_choice == 1:
        subject = "Biology"
    if subject_choice == 2:
        subject = "Physics"
    if subject_choice == 3:
        subject = "Chemistry"
    if subject_choice == 4:
        subject = "Maths"
    if subject_choice == -1:
        print("Too many invalid choices, starting with Biology.")
        subject = "Biology"

    if not (questions := load_questions(subject)):
        print(f"No questions available for the {subject} subject.")
        return

    if (user_name := get_valid_name()) == -1:
        return user_name

    log_action(user_name, f"started {subject} test")
    score = take_test(user_name, subject, questions)

    for item in user_data:
        if item['Name'] == user_name:
            item[subject] = score

    update_csv(user_data, "user_data.csv")

import os
import pandas as pd
from datetime import datetime


def load_previous_user_data():
    if os.path.exists("user_data.csv"):
        df = pd.read_csv("user_data.csv")
        return df.to_dict("records")
    return []


def load_csv(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    else:
        print(f'The file path "{file_path}" does not exists.')
        return []


def update_csv(user_data, file_path):
    df = pd.DataFrame(user_data)
    df.to_csv(file_path, index=False)


def custom_print(limit, nab_str="Enter your choice "):
    if limit <= 1:
        print("Invalid: limit <= 2. setting limit to 2")
        limit = 2

    print(nab_str, end='(')
    for i in range(limit):
        if i == (limit - 2):
            print(i + 1, end=' ')
        elif i < (limit - 1):
            print(i + 1, end=', ')
        else:
            print(f"or {i + 1}", end="): ")


def get_valid_choice(limit, admin=False):
    if admin:
        custom_print(limit)
        try:
            if 1 <= (admin_choice := int(input())) <= limit:
                return admin_choice
            else:
                return -1
        except ValueError:
            return -1

    l_count = 0
    custom_print(limit)
    while True:
        try:
            if 1 <= (choice := int(input())) <= limit:
                return choice
            else:
                l_count += 1
        except ValueError:
            l_count += 1

        if l_count == 3:
            return -1

        print("Invalid input, please enter a valid number.")
        custom_print(limit)


def get_valid_name():
    user_data = load_csv("user_data.csv")
    nab_count = 0
    while True:
        if nab_count == 5:
            return -1

        name = input("Enter your name: ").strip()

        if not name.replace(' ', '').isalpha():
            print("Please enter a valid name with alphabetic characters only.")
            nab_count += 1
            continue

        if any(name.title() == item['Name'] for item in user_data):
            return name.title()

        print("\nName not found.")
        nab_count += 1


def print_questions(data, user_answers=None):
    if not data:
        print("No questions available for the subject")
    elif not user_answers:
        for i, q in enumerate(data, 1):
            print(f"{i}. {q['question']} -Correct Answer: {q['answer']}")
    else:
        for i, q in enumerate(data):
            print(f"{i+1}. {q['question']} -Correct Answer: {q['answer']}")
            user_choice = user_answers[i]
            if not user_choice == -1:
                print(f"Your answered: {q['options'][user_choice]}")
                continue
            print("Not answered!")


def log_action(user, action, admin=False):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    system_file = "system_logs.txt"
    admin_file = "admin_logs.txt"

    if admin:
        with open(admin_file, "a") as file:
            file.write(f"{user} - {action} - {timestamp}\n")
            print(f"Log entry added for Admin: {user}")
    else:
        with open(system_file, "a") as file:
            file.write(f"{user} - {action} - {timestamp}\n")

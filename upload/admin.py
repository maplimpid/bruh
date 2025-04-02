from general_functions import *
import matplotlib.pyplot as plt


def verify_admin():
    admin_data = load_csv("admin_data.csv")
    action = "logged in"
    key = input("Enter your key: ").strip()

    for item in admin_data:
        if key == item["Key"]:
            log_action(item["Name"], action, True)
            return True, item["Name"]
    else:
        print("Key not found")
        return False, -1


def print_graph(title, x_values, y_vales):
    positions = range(len(y_vales))
    plt.bar(positions, y_vales)
    plt.xticks(positions, x_values)
    plt.title(title)
    plt.show()


def admin_page(user_data):
    verified, current_admin = verify_admin()
    if not verified:
        return 3

    while True:
        print("\nAdmin Menu:")
        print("1. Show User Data")
        print("2. Show Score Graph")
        print("3. Show Subject Distribution")
        print("4. Quiz Modification")
        print("5. Update the List of Eligible Users")
        print("6. Show Admin log")
        print("7. Exit ")

        choice = get_valid_choice(7, True)

        if choice == 1:
            if not user_data:
                print("No user data is available")
            else:
                print("\nUser data:")
                print(pd.DataFrame(user_data))

        if choice == 2:
            if not user_data:
                print("No user data is available")
            else:
                print("\nSelect the Mode")
                print("1. User Score Graph")
                print("2. Subject Score Graph")
                print("3. Go back to Admin Menu")

                subjects = ["Biology", "Physics", "Chemistry", "Maths"]

                sub_choice = get_valid_choice(2, True)
                if sub_choice == 1:
                    scores = []
                    name = input("\nEnter the username: ").title()
                    if not (any(name == item["Name"] for item in user_data)):
                        print("Username not found.")
                        continue
                    for item in user_data:
                        if item["Name"] == name:
                            scores = [item[subject] for subject in subjects]
                    title = f"\nScore of the user: {name}"
                    print_graph(title, subjects, scores)

                if sub_choice == 2:
                    names = []
                    scores = []
                    print("\nSubjects available:")
                    for i, element in enumerate(subjects, 1):
                        print(f"{i}. {element}")
                    user_choice = get_valid_choice(len(subjects), True)
                    if user_choice == -1:
                        print("Invalid!")
                        continue
                    subject = subjects[user_choice - 1]
                    if not (subject in subjects):
                        print("Subject not found.")
                        continue
                    for item in user_data:
                        names.append(item["Name"])
                        scores.append((item[subject]))
                    title = f"\nUser scores for subject: {subject}"
                    print_graph(title, names, scores)

                    if sub_choice == 3:
                        continue

                if not (1 <= sub_choice <= 3):
                    print("Invalid!")

        if choice == 3:
            print("There's noting!")

        if choice == 4:
            print("\nSelect a subject for modification")
            print("1. Biology")
            print("2. Physics")
            print("3. Chemistry")
            print("4. Maths")

            subject = ""
            subject_choice = get_valid_choice(4, True)

            if subject_choice == 1:
                subject = "Biology"
            if subject_choice == 2:
                subject = "Physics"
            if subject_choice == 3:
                subject = "Chemistry"
            if subject_choice == 4:
                subject = "Maths"
            if not (1 <= subject_choice <= 4):
                print("Invalid!")

            print(f"\nSubject choice: {subject}")
            print("1. Add Questions to Subject")
            print("2. Delete Question from Subject")
            print("3, Show All Questions in Subject")
            print("4. Go back to Admin Menu")
            mod_choice = get_valid_choice(4, True)
            file_path = f"{subject}_questions.csv"
            questions = load_csv(file_path)

            if mod_choice == 1:
                print(f"\nAdding a question to {subject}")
                action = f"added question to subject: {subject}"
                question = input("\nEnter the question: ")
                options = [input(f"Enter option {i+1}: ") for i in range(4)]
                answer = int(input("Enter the correct option (1, 2, 3 or 4): "))
                if not (1 <= answer <= 4):
                    print("Failed!")
                    continue
                questions.append({
                    "question": question,
                    "options": options,
                    "answer": options[answer - 1]
                })
                print("Question successfully added!")
                update_csv(questions, file_path)
                log_action(current_admin, action, True)

            if mod_choice == 2:
                print(f"\nDeleting a question from {subject}")
                print("\nAll questions: ")
                print_questions(questions)
                question_number = int(input("Enter the question number: "))
                action = f"deleted a question in subject: {subject}"
                if not (1 <= question_number <= len(questions)):
                    print("Failed")
                    continue
                del questions[question_number - 1]
                print("Question successfully deleted!")
                update_csv(questions, file_path)
                log_action(current_admin, action, True)

            if mod_choice == 3:
                print(f"\nAll questions in subject: {subject} ")
                print_questions(questions)

            if mod_choice == 4:
                continue

            if not (1 <= mod_choice <= 4):
                print("Invalid!")

        if choice == 5:
            print("\nSelect the Modification Mode")
            print("1. Add New Users")
            print("2. Remove an existing User")
            print("3. Go back to Admin Menu")

            nab = False
            mod_choice = get_valid_choice(3, True)

            if mod_choice == 1:
                if not user_data:
                    print("\nList of Usernames already taken:")
                for i, name in enumerate(user_data, 1):
                    print(f'{i}. {name["Name"]}')
                n = int(input("\nEnter the number of new users: "))
                action = f"added {n} new user(s)"
                new_users = [input(f"Enter the user {i+1}: ") for i in range(n)]
                for new_user in new_users:
                    if any(new_user.title() == item['Name'] for item in user_data):
                        print("Username is taken!")
                        nab = True
                if nab:
                    continue

                for name in new_users:
                    user_data.append({
                        "Name": name.title(),
                        "Biology": 0,
                        "Physics": 0,
                        "Chemistry": 0,
                        "Maths": 0
                    })
                update_csv(user_data, "user_data.csv")
                print(f"Successfully added {n} user(s)")
                log_action(current_admin, action, True)

            if mod_choice == 2:
                print("\nList of Eligible Users:")
                for i, name in enumerate(user_data, 1):
                    print(f'{i}. {name["Name"]}')
                del_choice = int(input("Enter the user no. you want to remove: "))
                if not (1 <= del_choice <= len(user_data)):
                    print("Failed!")
                    continue
                deleted_user = user_data[del_choice - 1]['Name']
                action = f"removed user: {deleted_user}"
                del user_data[del_choice - 1]
                update_csv(user_data, "user_data.csv")
                print(f"Successfully removed the user: {deleted_user}")
                log_action(current_admin, action, True)

            if mod_choice == 3:
                continue

            if not (1 <= mod_choice <= 3):
                print("Invalid!")

        if choice == 6:
            print("\nAdmin log: ")
            with open('admin_logs.txt', 'r') as file:
                print(file.read())

        if choice == 7:
            return

        if not (1 <= choice < 7):
            print("Invalid!")

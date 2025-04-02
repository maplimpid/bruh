from test import *
from admin import *


def main():
    print("nab " * 10)
    print("WELCOME")
    file_path = "user_data.csv"
    user_data = load_csv(file_path)

    while True:
        print("\n---------------- HOME MENU -----------------\n")

        if not user_data:
            print("No user data was found, opening Admin page")
            choice = 2
        else:
            print("Options:")
            print("1. Start Test")
            print("2. Admin Page")
            print("3. Exit")
            choice = get_valid_choice(3)

        if choice == 1:
            print("\n---------------- TEST PAGE -----------------\n")
            choice = test_page(user_data)

        if choice == 2:
            print("\n---------------- ADMIN PAGE -----------------\n")
            choice = admin_page(user_data)

        if choice == -1:
            print("\nToo many invalid choices, closing the program.")
            return

        if choice == 3:
            print("\nClosing the program...")
            return


if __name__ == '__main__':
    main()

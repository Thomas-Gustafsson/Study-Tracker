# Written by Thomas Gustafsson
# Last updated 2023-03-18
import json

# define the data structure to store course information
courses = {}

# load the saved data from a JSON file, if it exists
try:
    with open("courses.json", "r") as f:
        courses = json.load(f)
except FileNotFoundError:
    pass

# a function to add a new course to the program
def add_course():
    print("\n┌──────────────────────────────────────────┐")
    print("│              ADD NEW COURSE              │")
    print("└──────────────────────────────────────────┘\n")
    name = input("Enter the name of the course: ")
    credits = int(input("Enter the number of credit hours for the course: "))
    duration = int(input("Enter the duration of the course in weeks: "))
    courses[name] = {"credits": credits, "study_time": 0, "duration": duration}
    save_data()
    print("Course added successfully!")
    input("\nPress Enter to continue...")

def delete_course():
    print("\n┌──────────────────────────────────────────┐")
    print("│              REMOVE COURSE               │")
    print("└──────────────────────────────────────────┘\n")
    print("Courses:")
    for i, course in enumerate(courses):
        print(f"{i+1}. {course}: {courses[course]['study_time']} minutes")

    # Prompt user to select a course to remove
    course_num = int(input("Select a course to remove by number: "))
    course_name = list(courses.keys())[course_num-1]

    # Confirm deletion with user
    confirm = input(f"Are you sure you want to remove {course_name}? (y/n): ")

    if confirm.lower() == 'y':
        # Remove the course from the dictionary
        del courses[course_name]
        save_data()
        print(f"{course_name} has been removed from the list of courses.")
    else:
        print("Deletion cancelled.")
    input("\nPress Enter to continue...")

# a function to add study time for a specific course
def add_study_time():
    # Print list of courses and their study times
    print("\n┌──────────────────────────────────────────┐")
    print("│              ADD STUDY TIME              │")
    print("└──────────────────────────────────────────┘\n")
    print("Courses:")
    for i, course in enumerate(courses):
        print(f"{i+1}. {course}: {courses[course]['study_time']} minutes")

    # Prompt user to select a course
    course_num = int(input("Select a course by number: "))
    course_name = list(courses.keys())[course_num-1]

    # Prompt user to enter study time
    study_time = int(input("Enter study time in minutes: "))

    # Update the study time for the selected course
    courses[course_name]['study_time'] += study_time
    save_data()
    print(f"{study_time} minutes of study time added for {course_name}.")
    input("\nPress Enter to continue...")

# define a function to display the total study time for each course and overall
def display_study_time():
    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│                         STUDY TIME                          │")
    print("└─────────────────────────────────────────────────────────────┘\n")
    print("{:<25} {:<15} {:<15} {:<10} {:<15}".format("COURSE", "STUDY TIME", "CREDITS", "TIME/CR", "EXPECTED TIME"))
    print("{:<25} {:<15} {:<15} {:<10} {:<15}".format("------", "----------", "-------", "-------", "-------------"))
    total_time = 0
    for name, info in courses.items():
        time = info["study_time"]
        credits = info["credits"]
        duration = info["duration"]
        total_time += time
        time_per_credit = round(time/(credits*60), 2)
        expected_time = round((credits/1.5) * 40, 2)
        print("{:<25} {:<15} {:<15} {:<10} {:<15}".format(name, time, credits, time_per_credit, expected_time))
    print("\nTotal study time: {} minutes".format(total_time))
    input("\nPress Enter to continue...")

# define a function to save the data to a JSON file
def save_data():
    with open("courses.json", "w") as f:
        json.dump(courses, f)

while True:
    print("\n╭───────────────────────────────────────╮")
    print("│           STUDY TRACKER MENU          │")
    print("├───────────────────────────────────────┤")
    print("│ Enter 'create' to create a course     │")
    print("│ Enter 'add' to add study time         │")
    print("│ Enter 'display' to display study time │")
    print("│                                       │")
    print("│ Enter 'delete' to delete a course     │")
    print("│ Enter 'exit' to exit the program      │")
    print("╰───────────────────────────────────────╯\n")

    action = input("Your choice: ")

    if action == "new":
        add_course()
    elif action == "add":
        add_study_time()
    elif action =="delete":
        delete_course()
    elif action == "display":
        display_study_time()
    elif action == "graph":
        graph_study_time()
    elif action == "quit":
        break
    else:
        print("\nInvalid action. Please try again.")
        input("Press Enter to continue...")

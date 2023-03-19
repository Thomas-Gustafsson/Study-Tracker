# Written by Thomas Gustafsson
# Last updated 2023-03-19
import json
from datetime import datetime

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
    credits = float(input("Enter the number of credits for the course: "))
    duration = float(input("Enter the duration of the course in weeks: "))
    start_date = input("Enter the start date of the course (yyyy-mm-dd): ")
    courses[name] = {"credits": credits, "study_time": 0, "duration": duration, "start_date": start_date}
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
    hours = int(input("First enter study time in hours: "))
    minutes = int(input("Enter remaining study time minutes: "))
    study_time = hours * 60 + minutes

    # Update the study time for the selected course
    courses[course_name]['study_time'] += study_time
    save_data()
    print(f"{hours} hours and {minutes} minutes of study time added for {course_name}.")
    input("\nPress Enter to continue...")


# define a function to display the total study time for each course and overall
def display_study_time():
    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│                         STUDY TIME                          │")
    print("└─────────────────────────────────────────────────────────────┘\n")
    print("{:<25} {:<15} {:<15} {:<15} {:<20}".format("COURSE", "STUDY TIME", "CREDITS", "TIME/CR", "EXPECTED TIME/CR"))
    print("{:<25} {:<15} {:<15} {:<15} {:<20}".format("------", "----------", "-------", "-------", "-------------"))
    total_time = 0
    for name, info in courses.items():
        time = info["study_time"]
        credits = info["credits"]
        duration = info["duration"]
        start_date = datetime.strptime(info["start_date"], '%Y-%m-%d').date()
        days_since_start = (datetime.now().date() - start_date).days
        total_time += time
        time_per_credit = round(time/(credits*60), 2)
        expected_time = round(((((credits/1.5)*40)/duration)/7) * days_since_start, 2)
        study_time_str = f"{time//60}h {time%60}m"
        time_per_credit_str = f"{time_per_credit:.2f}h"
        expected_time_str = f"{expected_time:.2f}h"
        print("{:<25} {:<15} {:<15} {:<15} {:<20}".format(name, study_time_str, credits, time_per_credit_str, expected_time_str))
    total_time_str = f"{total_time//60}h {total_time%60}m"
    print("\nTotal study time: {}".format(total_time_str))
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
    print("│ Enter 'display' to display overview   │")
    print("│                                       │")
    print("│ Enter 'delete' to delete a course     │")
    print("│ Enter 'exit' to exit the program      │")
    print("╰───────────────────────────────────────╯\n")

    action = input("Your choice: ")

    if action == "create":
        add_course()
    elif action == "add":
        add_study_time()
    elif action =="delete":
        delete_course()
    elif action == "display":
        display_study_time()
    elif action == "exit":
        break
    else:
        print("\nInvalid action. Please try again.")
        input("Press Enter to continue...")

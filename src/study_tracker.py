# By Thomas Gustafsson
# Last updated 2024-12-10

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

    # Input validation for credits and duration
    while True:
        try:
            credits = float(input("Enter the number of credits for the course: "))
            if credits <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive number for credits.")

    while True:
        try:
            duration = float(input("Enter the duration of the course in weeks: "))
            if duration <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive number for duration.")

    # Input validation for date
    while True:
        start_date_str = input("Enter the start date of the course (yyyy-mm-dd): ")
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            break
        except ValueError:
            print("Invalid date format. Please use yyyy-mm-dd.")

    courses[name] = {"credits": credits, "study_time": 0, "duration": duration, "start_date": start_date_str}
    save_data()
    print("Course added successfully!")
    input("\nPress Enter to continue...")

# a function to delete a course
def delete_course():
    print("\n┌──────────────────────────────────────────┐")
    print("│              REMOVE COURSE               │")
    print("└──────────────────────────────────────────┘\n")
    print("Courses:")
    for i, course in enumerate(courses):
        print(f"{i+1}. {course}: {courses[course]['study_time']} minutes")

    course_input = input("Enter course number or name to delete: ")

    # Check if input is a number to select by index
    if course_input.isdigit():
        course_num = int(course_input) - 1
        if 0 <= course_num < len(courses):
            course_name = list(courses.keys())[course_num]
        else:
            print("Invalid course number.")
            return
    # Otherwise, assume it's the course name
    else:
        course_name = course_input
        if course_name not in courses:
            print("Course not found.")
            return

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
    print("\n┌──────────────────────────────────────────┐")
    print("│              ADD STUDY TIME              │")
    print("└──────────────────────────────────────────┘\n")
    print("Courses:")
    for i, course in enumerate(courses):
        print(f"{i+1}. {course}: {courses[course]['study_time']} minutes")

    course_num = int(input("Select a course by number: "))
    course_name = list(courses.keys())[course_num-1]

    # Input validation for study time
    while True:
        try:
            hours = int(input("First enter study time in hours: "))
            minutes = int(input("Enter remaining study time minutes: "))
            if hours < 0 or minutes < 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter valid positive numbers for study time.")

    study_time = hours * 60 + minutes
    courses[course_name]['study_time'] += study_time
    save_data()
    print(f"{hours} hours and {minutes} minutes of study time added for {course_name}.")
    input("\nPress Enter to continue...")

# define a function to display the total study time for each course and overall
def display_study_time():
    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│                         STUDY TIME                          │")
    print("└─────────────────────────────────────────────────────────────┘\n")
    print("{:<25} {:<15} {:<15} {:<15} {:<15} {:<20}".format("COURSE", "STUDY TIME", "CREDITS", "TIME/CR", "PROGRESS", "EXPECTED TIME/CR"))
    print("{:<25} {:<15} {:<15} {:<15} {:<15} {:<20}".format("------", "----------", "-------", "-------", "--------", "-------------"))
    
    total_time = 0
    for name, info in courses.items():
        time = info["study_time"]
        credits = info["credits"]
        duration = info["duration"]
        start_date = datetime.strptime(info["start_date"], '%Y-%m-%d').date()
        days_since_start = (datetime.now().date() - start_date).days
        
        if days_since_start < 0:
            print(f"{name} has not started yet.")
            continue
        
        total_time += time
        time_per_credit = round(time/(credits*60), 2)
        expected_time = round(((((credits/1.5)*40)/duration)/7) * days_since_start, 2)
        progress = round((time/60) / expected_time * 100, 2) if expected_time > 0 else 0
        
        study_time_str = f"{time//60}h {time%60}m"
        time_per_credit_str = f"{time_per_credit:.2f}h"
        progress_str = f"{progress}%"
        expected_time_str = f"{expected_time:.2f}h"
        
        print("{:<25} {:<15} {:<15} {:<15} {:<15} {:<20}".format(name, study_time_str, credits, time_per_credit_str, progress_str, expected_time_str))
    
    total_time_str = f"{total_time//60}h {total_time%60}m"
    print("\nTotal study time: {}".format(total_time_str))
    input("\nPress Enter to continue...")

# define a function to save the data to a JSON file
def save_data():
    with open("courses.json", "w") as f:
        json.dump(courses, f)

# Main loop for the study tracker
while True:
    print("\n╭───────────────────────────────────────╮")
    print("│           STUDY TRACKER MENU          │")
    print("├───────────────────────────────────────┤")
    print("│ Enter 'create' to create a course     │")
    print("│ Enter 'add' to add study time         │")
    print("│ Enter 'display' to display overview   │")
    print("│ Enter 'delete' to delete a course     │")
    print("│ Enter 'exit' to exit the program      │")
    print("╰───────────────────────────────────────╯\n")

    action = input("Your choice: ")

    if action == "create":
        add_course()
    elif action == "add":
        add_study_time()
    elif action == "display":
        display_study_time()
    elif action == "delete":
        delete_course()
    elif action == "exit":
        break
    else:
        print("\nInvalid action. Please try again.")
        input("Press Enter to continue...")

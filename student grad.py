# AI Assistant for Grading Students

def calculate_grade(marks):
    """Returns grade based on average marks"""
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"

def student_grading():
    subjects = int(input("Enter number of subjects: "))
    total = 0
    student_marks = {}

    for i in range(subjects):
        subject = input(f"Enter subject {i+1} name: ")
        marks = float(input(f"Enter marks for {subject} (out of 100): "))
        student_marks[subject] = marks
        total += marks

    avg = total / subjects
    grade = calculate_grade(avg)

    print("\n--- Student Report ---")
    for subject, marks in student_marks.items():
        print(f"{subject}: {marks}")
    print(f"Average Marks: {avg:.2f}")
    print(f"Final Grade: {grade}")

# Run the assistant
if _name_ == "_main_":
    student_grading()
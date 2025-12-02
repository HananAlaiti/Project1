import os
import matplotlib.pyplot as plt

DATA_DIR = "data"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, "assignments.txt")
SUBMISSIONS_DIR = os.path.join(DATA_DIR, "submissions")

def load_students():
    students = {}
    with open(STUDENTS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            student_id_str = line[:3].strip()
            # normalize: remove leading zeros by converting to int then str
            student_id = str(int(student_id_str))
            name = line[3:].strip()
            students[name] = student_id
    return students

def load_assignments():
    assignments = {}
    with open(ASSIGNMENTS_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        for i in range(0, len(lines), 3):
            assignment_name = lines[i]
            assignment_id_str = lines[i+1].strip()
            assignment_id = str(int(assignment_id_str))  # normalize
            points = float(lines[i+2])
            assignments[assignment_name] = (assignment_id, points)
    return assignments

def load_submissions():
    submissions = {}
    for filename in os.listdir(SUBMISSIONS_DIR):
        if not filename.endswith('.txt'):
            continue
        with open(os.path.join(SUBMISSIONS_DIR, filename), 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) < 3:
                    continue
                student_id_str = parts[0].strip()
                assignment_id_str = parts[1].strip()
                percent_str = parts[2].strip()

                # Normalize IDs
                try:
                    student_id = str(int(student_id_str))
                    assignment_id = str(int(assignment_id_str))
                    percent = float(percent_str)
                except ValueError:
                    continue  # skip bad lines

                if student_id not in submissions:
                    submissions[student_id] = {}
                submissions[student_id][assignment_id] = percent
    return submissions

def student_grade(students, assignments, submissions):
    student_name = input("What is the student's name: ")
    if student_name not in students:
        print("Student not found")
        return
    student_id = students[student_name]

    weighted_sum = 0
    total_points = 0

    student_submissions = submissions.get(student_id)
    if student_submissions is None:
        print("0%")
        return

    for assignment_name, (assignment_id, points) in assignments.items():
        score = student_submissions.get(assignment_id)
        if score is None:
            score = 0
        weighted_sum += score * points
        total_points += points

    if total_points == 0:
        print("0%")
        return

    grade = round(weighted_sum / total_points)
    print(f"{grade}%")

def assignment_stats(assignments, submissions):
    assignment_name = input("What is the assignment name: ")
    if assignment_name not in assignments:
        print("Assignment not found")
        return
    assignment_id, _ = assignments[assignment_name]

    scores = []
    for student_subs in submissions.values():
        score = student_subs.get(assignment_id)
        if score is not None:
            scores.append(score)

    if not scores:
        print("No scores found")
        return

    print(f"Min: {round(min(scores))}%")
    print(f"Avg: {round(sum(scores) / len(scores))}%")
    print(f"Max: {round(max(scores))}%")

def assignment_graph(assignments, submissions):
    assignment_name = input("What is the assignment name: ")
    if assignment_name not in assignments:
        print("Assignment not found")
        return
    assignment_id, _ = assignments[assignment_name]

    scores = []
    for student_subs in submissions.values():
        score = student_subs.get(assignment_id)
        if score is not None:
            scores.append(score)

    if not scores:
        print("No scores found")
        return

    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Scores for {assignment_name}")
    plt.xlabel("Percentage")
    plt.ylabel("Number of students")
    plt.show()

def main():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    selection = input("Enter your selection: ")

    if selection == "1":
        student_grade(students, assignments, submissions)
    elif selection == "2":
        assignment_stats(assignments, submissions)
    elif selection == "3":
        assignment_graph(assignments, submissions)
    else:
        print("Invalid selection")

if __name__ == "__main__":
    main()
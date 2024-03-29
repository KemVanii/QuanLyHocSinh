import json
import os
import hashlib


def filter_by_subject_id(scoreboard, subjectId):
    return scoreboard.subject_id == subjectId


def isPass(score_boards):
    grouped_subjects = {}
    for score_board in score_boards:
        subject_id = score_board.subject_id
        if subject_id not in grouped_subjects:
            grouped_subjects[subject_id] = []
        grouped_subjects[subject_id].append(score_board)
    for subject, sb in grouped_subjects.items():
        if len(sb[0].scores) == 0 or len(sb[1].scores) == 0:
            return False
        average1 = calSemesterAverage(sb[0].scores)
        average2 = calSemesterAverage(sb[1].scores)
        if ((average1 + average2) / 2) < 5:
            return False
    return True


def filter_student(students, previousSemesters, currSemesters, filterBy):
    students_filter = []
    for student in students:
        score_boards_filter = []  # filter score_boards in previous grade
        isInClass = False
        for score_board in student.score_boards:
            if (score_board.semester_id == currSemesters[0].id
                    or score_board.semester_id == currSemesters[1].id):
                isInClass = True
                break
            if (score_board.semester_id == previousSemesters[0].id
                    or score_board.semester_id == previousSemesters[1].id):
                score_boards_filter.append(score_board)
        if isInClass:
            continue
        if isPass(score_boards_filter) == filterBy:
            students_filter.append(student)
    return students_filter


def calSemesterAverage(scores):
    totalCoefficient = 0
    averageScore = 0
    for score in scores:
        if score.type == '15p':
            averageScore = averageScore + score.value
            totalCoefficient = totalCoefficient + 1
        elif score.type == '45p':
            averageScore = averageScore + score.value * 2
            totalCoefficient = totalCoefficient + 2
        else:
            averageScore = averageScore + score.value * 3
            totalCoefficient = totalCoefficient + 3
    return averageScore / totalCoefficient


def loadPolicies(app):
    json_file_path = os.path.join(app.root_path, 'static', 'policies.json')
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Update app.config with data from the JSON file
    for key, value in data.items():
        app.config[key] = value


def get_previous_school_year(current_school_year):
    parts = current_school_year.split('-')
    start_year = int(parts[0])
    end_year = int(parts[1])
    previous_start_year = start_year - 1
    previous_end_year = end_year - 1
    previous_school_year = f'{previous_start_year:02d}-{previous_end_year:02d}'
    return previous_school_year


def type_sort_avg_score(avg_score):
    if avg_score >= 8:
        return "Giỏi"
    elif avg_score >= 6.5:
        return "Khá"
    elif avg_score >= 5:
        return "Trung bình"
    else:
        return "Yếu"


def createDataScoresfromReqForm(request, score_boards):
    dataScores = []
    for score_board in score_boards:
        dataScore = {
            'score_board_id': score_board.id,
            '15p': request.form.getlist(f'15p{score_board.id}[]'),
            '45p': request.form.getlist(f'45p{score_board.id}[]'),
            'ck': request.form.get(f'ck{score_board.id}')
        }
        dataScores.append(dataScore)
    return dataScores

import json
import os
def filter_by_subject_id(scoreboard, subjectId):
    return scoreboard.subject_id == subjectId


def isPass(score_boards, subjects):
    for subject in subjects:
        sb_filter = list(filter(lambda scoreboard: filter_by_subject_id(scoreboard, subject.id), score_boards))
        print(sb_filter)
        average1 = calSemesterAverage(sb_filter[0].scores)
        average2 = calSemesterAverage(sb_filter[1].scores)
        if ((average1 + average2) / 2) < 5:
            return False
    return True


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
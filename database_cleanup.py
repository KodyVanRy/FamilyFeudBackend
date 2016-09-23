import database
from database_models import *

database.init_db()

count = 0
print(len(Survey.query.all()))
for _survey in Survey.query.all():
    answers = Answer.query.filter_by(survey=_survey.id)
    surveyValue = 0
    for answer in answers:
        surveyValue += answer.value
    if surveyValue > 100:
        print _survey.title + str(surveyValue) + " - " + str(_survey.id)
        m_answers = []
        for answer in answers:
            if answer.answer.lower() in m_answers:
                database.db_session.delete(answer)
                count += 1
            else:
                m_answers.append(answer.answer.lower())

print (str(count))

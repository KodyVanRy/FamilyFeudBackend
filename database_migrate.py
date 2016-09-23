from database import *
from database_models import *

init_db()

surveys = Survey.query.all()
print len(surveys)
# x = 0
# for survey in surveys:
#     x += 1
#     if x % 50:
#         print str(x) + " : " + survey.title
#     answers = Answer.query.filter_by(survey=survey.id).all()
#     if len(answers) <= 1:
#         db_session.delete(survey)
#     else:
#         survey.answer_count = len(answers)
#     db_session.commit()

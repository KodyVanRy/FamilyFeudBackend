import simplejson as json

from database import *
from database_models import *

f = open("/home/kody/Downloads/mfile4.html")
l = f.read()
k = eval(l)
j2 = json.dumps(k)
j = json.loads(j2)
f.close()

init_db()

for k, v in j.iteritems():
    survey = Survey(v["prompt"])
    db_session.add(survey)
    db_session.commit()
    for m in v["answers"]:
        answer = Answer(survey.id, m["answer"], m["value"])
        db_session.add(answer)
    db_session.commit()

print len(Answer.query.filter_by(survey=1).all())
print Survey.query.filter_by(id=1).first().title

print len(j)
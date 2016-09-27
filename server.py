import helper
from flask import Flask, request, jsonify
import game

app = Flask(__name__)

m_game = None


@app.route('/api/host')
def api_host():
    global m_game
    try:
        # if mGame is None:
        #     print mGame
        #     mGame = game.Game(952)
        #     print mGame
        if m_game is not None:
            if m_game.survey is not None:
                return jsonify({"title": m_game.survey.survey})
        return jsonify({
            "title": "Sorry no game data available, please either select assistant or "
                     "have someone on another device become assistant"})
    except Exception as e:
        print e


@app.route('/api/survey/set')
def set_survey():
    global m_game
    if "id" in request.json.keys():
        if m_game is None:
            m_game = game.Game(int(request.json.get("id")))
        else:
            m_game.survey = game.get_survey(int(request.json.get("id")))


@app.route('/api/random')
def get_new_survey():
    _min = 1
    _max = 8
    search = ""
    if "min" in request.json.keys():
        _min = int(request.json.get("min"))
    if "max" in request.json.keys():
        _max = int(request.json.get("max"))
    if "search" in request.json.keys():
        search = int(request.json.get("search"))

    return jsonify(helper.get_random_survey(_min, _max, search))


@app.route('/api/surveys')
def get_surveys():
    _min = 1
    _max = 8
    search = ""
    count = -1
    start = 0
    if "min" in request.json.keys():
        _min = int(request.json.get("min"))
    if "max" in request.json.keys():
        _max = int(request.json.get("max"))
    if "search" in request.json.keys():
        search = request.json.get("search")
    if "count" in request.json.keys():
        count = int(request.json.get("count"))
    if "start" in request.json.keys():
        start = int(request.json.get("start"))

    return jsonify(helper.get_surveys(_min, _max, search, count, start))


@app.route("/api/game/test")
def test():
    global m_game
    return str(m_game.survey.answers)


@app.route("/api/game/answer")
def click_num():
    if "num" in request.json.keys():
        print request.json.get("num")
        m_game.click_answer(request.json.get("num"))
    return jsonify({"answers": m_game.clicked_answers})


@app.route("/get_clicked")
def get_clicked():
    print str(m_game.clicked_answers)
    return jsonify({"answers": m_game.clicked_answers})


@app.route("/get_game")
def get_game():
    return jsonify({"answers": m_game.clicked_answers})


@app.route("/api/families/edit")
def edit_families():
    f1 = request.json.get("family1")
    f2 = request.json.get("family2")
    m_game.family1.name = f1["name"]
    m_game.family2.name = f2["name"]
    m_game.family1.score = f1["score"]
    m_game.family2.score = f2["score"]


# region html

#
# @app.route('/')
# def home():
#     try:
#         return render_template("home.html")
#     except Exception as e:
#         print e
#
#
# @app.route('/host')
# def host():
#     print amount_of_surveys()
#     if request.args.get("id") is not None:
#         choose_survey(request.args.get("id"))
#     try:
#         if mGame.survey is None:
#             get_new_survey()
#         return render_template("host.html", survey=mGame.survey)
#
#     except Exception as e:
#         print e
#
#
# @app.route('/assistant')
# def assistant():
#     surveys = Survey.query.all()
#     return render_template("assistant_home.html", items=surveys)
#
#
# @app.route('/assistant2')
# def assistant2():
#     m_str = ""
#     for S in Answer.query.filter_by(survey=mGame.survey.id).all():
#         m_str = m_str + S.answer + ", "
#     return m_str


# endregion

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

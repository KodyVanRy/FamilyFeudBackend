#!/usr/bin/pythong
import helper
from flask import Flask, request, jsonify
import game
# from game import SINGLE, DOUBLE, TRIPLE, SUDDEN_DEATH, FAST_MONEY

app = Flask(__name__)

m_game = None
game_mode = game.SETUP


@app.route('/')
def _home_():
    return "Welcome to Family Feud"


@app.route('/api/host')
def api_host():
    try:
        if m_game is not None:
            if m_game.survey is not None:
                return jsonify({"title": m_game.survey.survey})
        return jsonify({
            "title": "Sorry no game data available, please either select assistant or "
                     "have someone on another device become assistant"})
    except Exception as e:
        print e


@app.route('/api/game_state')
def api_game_state():
    global game_mode
    if request.json is not None and "mode" in request.json.keys():
        game_mode = int(request.json.get("mode"))
    elif "mode" in request.args.keys():
        game_mode = int(request.args.get("mode"))
    return jsonify({"game_mode": game_mode})


@app.route('/api/surveys/set')
def set_survey():
    global m_game
    if request.json is not None and "id" in request.json.keys():
        m_game = game.Game(int(request.json.get("id")))
    elif "id" in request.args.keys():
        m_game = game.Game(int(request.args.get("id")))
    if game_mode == game.SUDDEN_DEATH:
        m_game.survey.answers = m_game.survey.answers[:1]
    return api_host()


@app.route('/api/surveys/get/random')
def get_new_survey():
    _min = 1
    _max = 8
    search = ""
    if request.json is not None:
        if "min" in request.json.keys():
            _min = int(request.json.get("min"))
        if "max" in request.json.keys():
            _max = int(request.json.get("max"))
        if "search" in request.json.keys():
            search = int(request.json.get("search"))
    if request.args is not None:
        if "min" in request.args.keys():
            _min = int(request.args.get("min"))
        if "max" in request.args.keys():
            _max = int(request.args.get("max"))
        if "search" in request.args.keys():
            search = str(request.args.get("search"))

    return jsonify(helper.get_random_survey(_min, _max, search))


@app.route('/api/surveys/get')
def get_surveys():
    _min = 1
    _max = 8
    search = ""
    start = 0
    count = 10
    if request.json is not None:
        if "min" in request.json.keys():
            _min = int(request.json.get("min"))
        if "max" in request.json.keys():
            _max = int(request.json.get("max"))
        if "start" in request.json.keys():
            start = int(request.json.get("start"))
        if "count" in request.json.keys():
            count = int(request.json.get("count"))
        if "search" in request.json.keys():
            search = int(request.json.get("search"))
    if request.args is not None:
        if "min" in request.args.keys():
            _min = int(request.args.get("min"))
        if "max" in request.args.keys():
            _max = int(request.args.get("max"))
        if "start" in request.args.keys():
            start = int(request.args.get("start"))
        if "count" in request.args.keys():
            count = int(request.args.get("count"))
        if "search" in request.args.keys():
            search = str(request.args.get("search"))

    return jsonify(helper.get_surveys(_min, _max, search, start, count))


@app.route("/api/answers")
def click_num():
    if request.json is not None and "clicked" in request.json.keys():
        return jsonify({"answers": eval(request.json.get("clicked"))})
    if request.args is not None and "clicked" in request.args.keys():
        return jsonify({"answers": [int(arg) for arg in request.args.get("clicked").split(",")]})
    return jsonify({"answers": None})


@app.route("/api/game/get")
def get_clicked():
    print str(m_game.survey.answers)
    return jsonify({"answers": helper.get_answers_json(m_game),
                    "game_mode": game_mode})


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
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, jsonify
from core.saju_chain import get_saju_response
from core.tarot_chain import get_tarot_response
from core.title_summary_chain import get_title_summary  # LLM 기반 요약 함수 추가
from datetime import datetime

app = Flask(__name__)

@app.route("/api/project/new", methods=["POST"])
def generate_title():
    data = request.get_json()
    first_question = data.get("first_question")

    if not first_question:
        return jsonify({
            "isSuccess": False,
            "code": "COMMON4000",
            "message": "입력되지 않은 필수값이 있습니다.",
            "result": "BAD_REQUEST"
        }), 400

    try:
        title = get_title_summary(first_question)  # LLM을 활용한 제목 요약
        return jsonify({
            "isSuccess": True,
            "code": "COMMON200",
            "message": "요청에 성공했습니다.",
            "result": {
                "title": title
            }
        })
    except Exception as e:
        return jsonify({
            "isSuccess": False,
            "code": "COMMON4000",
            "message": str(e),
            "result": "BAD_REQUEST"
        }), 400

@app.route("/api/saju/consult", methods=["POST"])
def saju_consult():
    data = request.get_json()
    question = data.get("question")
    sajuData = data.get("sajuData")

    try:
        birth_date = sajuData["basicInfo"]["birthDate"]
        birth = f"{birth_date['year']}년 {birth_date['month']}월 {birth_date['day']}일"
        time = birth_date["time"]
        gender = sajuData["basicInfo"]["gender"]
        ilgan = sajuData["sajuPillars"]["dayPillar"]["sky"]["name"] + "일간"

        # 오행 분석 문자열 예시
        five_elements = sajuData["fiveElements"]
        oheng = ", ".join([f"{k} {v}" for k, v in five_elements.items()])

        result = get_saju_response(
    birth=birth,
    time=time,
    gender=gender,
    ilgan=ilgan,
    ilju="",     
    ilji="",     # 필요 시 추가
    oheng=oheng,
    sibsin="",   # 필요 시 추가
    question=question
)

        return jsonify({
            "isSuccess": True,
            "code": "COMMON200",
            "message": "요청에 성공했습니다.",
            "result": {
                "consultation_id": 3,
                "question": question,
                "result": result.get("summary", "결과 없음") + "\n\n📚 **출처**: " + ", ".join(result.get("source", [])),
                "created_at": datetime.now().isoformat(timespec='minutes')
            }
        })

    except Exception as e:
        return jsonify({
            "isSuccess": False,
            "code": "COMMON4000",
            "message": str(e),
            "result": "BAD_REQUEST"
        }), 400

@app.route("/api/tarot/consult", methods=["POST"])
def tarot_consult():
    data = request.get_json()
    question = data.get("question")
    cards = data.get("cards")

    if not question or not cards:
        return jsonify({
            "isSuccess": False,
            "code": "COMMON4000",
            "message": "입력되지 않은 필수값이 있습니다.",
            "result": "BAD_REQUEST"
        }), 400

    try:
        result = get_tarot_response(selected_cards=cards, question=question)

        return jsonify({
            "isSuccess": True,
            "code": "COMMON200",
            "message": "요청에 성공했습니다.",
            "result": {
                "consultation_id": 5,
                "question": question,
                "result": result.get("summary", "결과 없음") + "\n\n📚 **출처**: " + ", ".join(result.get("source", [])),
                "created_at": datetime.now().isoformat(timespec='minutes')
            }
        })

    except Exception as e:
        return jsonify({
            "isSuccess": False,
            "code": "COMMON4000",
            "message": str(e),
            "result": "BAD_REQUEST"
        }), 400

if __name__ == "__main__":
    app.run(debug=True, port=8080)

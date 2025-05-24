from flask import Flask, request, jsonify
from core.saju_chain import get_saju_response
from core.tarot_chain import get_tarot_response

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    query_type = data.get("type")  # 'saju' or 'tarot'

    try:
        if query_type == "saju":
            result = get_saju_response(
                birth=data.get("birth"),
                time=data.get("time"),
                gender=data.get("gender"),
                ilgan=data.get("ilgan"),       # 예: "신금"
                ilji=data.get("ilji"),         # 예: "자"
                ilju=data.get("ilju"),         # 예: "신자"
                oheng=data.get("oheng"),       # 예: "금 수 과다, 화 기운 부족"
                sibsin=data.get("sibsin"),     # 예: ["편재", "정관"]
                question=data.get("question")
            )
        elif query_type == "tarot":
            result = get_tarot_response(
                question=data.get("question"),
                selected_cards=data.get("cards")  # 예: ["The Lovers", "The Moon"]
            )
        else:
            return jsonify({"error": "Invalid type: 'saju' or 'tarot' expected."}), 400

        return jsonify(result if result else {"error": "Invalid response format"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
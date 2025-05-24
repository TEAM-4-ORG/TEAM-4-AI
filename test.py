# test.py

from core.saju_chain import get_saju_response, show_retrieved_docs

from core.tarot_chain import get_tarot_response
import json

# 사주 테스트

# 예시 질문
question = "내 사주 풀이 해줘."

# print("\n--- 검색된 문서 보기 ---")
#show_retrieved_docs(question)
saju_input = {
    "birth": "2001년 10월 3일",
    "time": "21:10",
    "gender": "female",
    "ilgan": "신금",
    "ilju": "신해",  
    "ilji": "해수",  
    "oheng_analysis": "화 기운 부족, 금/수 기운 많음", 
    "sibsin_analysis": "정관, 정인, 상관, 편재", 
    "question": question
}


saju_result = get_saju_response(**saju_input)

print("[사주 응답 결과]")
print(json.dumps(saju_result, indent=2, ensure_ascii=False))


# 타로 테스트
# tarot_input = {
#     "cards": ["The Lovers", "The Moon", "The Tower"],
#     "question": "지금 연애를 계속해도 될까요?"
# }

# tarot_result = get_tarot_response(**tarot_input)
# print("\n [타로 응답 결과]")
# print(json.dumps(tarot_result, indent=2, ensure_ascii=False))

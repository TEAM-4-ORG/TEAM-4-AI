# test.py

from core.saju_chain import get_saju_response
from core.tarot_chain import get_tarot_response
import json

# 사주 테스트
saju_input = {
    "birth": "1993년 7월 21일",
    "time": "09:30",
    "gender": "female",
    "ilgan": "신금",
    "palja": "丁丑년 己巳월 辛亥일 癸巳시",
    "oheng": "화 기운 부족, 금/수 기운 많음",
    "question": "올해 연애운은 어떤가요?"
}

saju_result = get_saju_response(**saju_input)
print("[사주 응답 결과]")
print(json.dumps(saju_result, indent=2, ensure_ascii=False))

#
# # 타로 테스트
# tarot_input = {
#     "cards": ["The Lovers", "The Moon", "The Tower"],
#     "question": "지금 연애를 계속해도 될까요?"
# }
#
# tarot_result = get_tarot_response(tarot_input)
# print("\n [타로 응답 결과]")
# print(json.dumps(tarot_result, indent=2, ensure_ascii=False))

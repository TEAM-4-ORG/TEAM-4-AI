import requests
import pytest
import json

BASE_URL = "http://127.0.0.1:5000" # Flask 서버 주소 및 포트

NEW_SAJU_PAYLOAD = {
    "user_id": 1,
    "project_id": 1,
    "question": "내 사주 분석해줘",
    "sajuData": {
        "basicInfo": {
            "birthDate": {
                "birth": "2000-08-24",
                "time": "21:52"
            },
            "gender": "여자"
        },
        "sajuPillars": {
            "yearPillar": {
                "sky": {
                    "name": "경",
                    "symbol": "금",
                    "sign": "양",
                    "key": 7,
                    "code": "庚",
                    "color": "white"
                },
                "ground": {
                    "name": "진",
                    "symbol": "토",
                    "sign": "양",
                    "key": 15,
                    "code": "辰",
                    "color": "yellow",
                    "innerAttri": "194"
                }
            },
            "monthPillar": {
                "sky": {
                    "name": "갑",
                    "symbol": "목",
                    "sign": "양",
                    "key": 1,
                    "code": "甲",
                    "color": "green"
                },
                "ground": {
                    "name": "신",
                    "symbol": "금",
                    "sign": "양",
                    "key": 19,
                    "code": "申",
                    "color": "white",
                    "innerAttri": "486"
                }
            },
            "dayPillar": {
                "sky": {
                    "name": "갑",
                    "symbol": "목",
                    "sign": "양",
                    "key": 1,
                    "code": "甲",
                    "color": "green"
                },
                "ground": {
                    "name": "인",
                    "symbol": "목",
                    "sign": "양",
                    "key": 13,
                    "code": "寅",
                    "color": "green",
                    "innerAttri": "420"
                }
            },
            "timePillar": {
                "sky": {
                    "name": "을",
                    "symbol": "목",
                    "sign": "음",
                    "key": 2,
                    "code": "乙",
                    "color": "green"
                },
                "ground": {
                    "name": "해",
                    "symbol": "수",
                    "sign": "양",
                    "key": 22,
                    "code": "亥",
                    "color": "black",
                    "innerAttri": "408"
                }
            }
        },
        "fiveElements": {
            "wood": 4,
            "fire": 0,
            "earth": 1,
            "metal": 2,
            "water": 1
        },
        "analysis": {
            "hop": {
                "skyHop": [],
                "bangHop": [],
                "somHop": None,
                "banHop": [],
                "sixHop": [
                    "인해합"
                ]
            },
            "chung": {
                "skyChung": [
                    "갑경충"
                ],
                "groundChung": [
                    "인신충"
                ]
            },
            "decades": {
                "decades": [
                    {
                        "year": 2015,
                        "sky": {
                            "name": "계",
                            "symbol": "수",
                            "sign": "음",
                            "key": 10,
                            "code": "癸",
                            "color": "black"
                        },
                        "ground": {
                            "name": "미",
                            "symbol": "토",
                            "sign": "음",
                            "key": 18,
                            "code": "未",
                            "color": "yellow",
                            "innerAttri": "315"
                        }
                    },
                    {
                        "year": 2025,
                        "sky": {
                            "name": "임",
                            "symbol": "수",
                            "sign": "양",
                            "key": 9,
                            "code": "壬",
                            "color": "black"
                        },
                        "ground": {
                            "name": "오",
                            "symbol": "화",
                            "sign": "음",
                            "key": 17,
                            "code": "午",
                            "color": "red",
                            "innerAttri": "253"
                        }
                    },
                    {
                        "year": 2035,
                        "sky": {
                            "name": "신",
                            "symbol": "금",
                            "sign": "음",
                            "key": 8,
                            "code": "辛",
                            "color": "white"
                        },
                        "ground": {
                            "name": "사",
                            "symbol": "화",
                            "sign": "양",
                            "key": 16,
                            "code": "巳",
                            "color": "red",
                            "innerAttri": "462"
                        }
                    },
                    {
                        "year": 2045,
                        "sky": {
                            "name": "경",
                            "symbol": "금",
                            "sign": "양",
                            "key": 7,
                            "code": "庚",
                            "color": "white"
                        },
                        "ground": {
                            "name": "진",
                            "symbol": "토",
                            "sign": "양",
                            "key": 15,
                            "code": "辰",
                            "color": "yellow",
                            "innerAttri": "194"
                        }
                    },
                    {
                        "year": 2055,
                        "sky": {
                            "name": "기",
                            "symbol": "토",
                            "sign": "음",
                            "key": 6,
                            "code": "己",
                            "color": "yellow"
                        },
                        "ground": {
                            "name": "묘",
                            "symbol": "목",
                            "sign": "음",
                            "key": 14,
                            "code": "卯",
                            "color": "green",
                            "innerAttri": "011"
                        }
                    },
                    {
                        "year": 2065,
                        "sky": {
                            "name": "무",
                            "symbol": "토",
                            "sign": "양",
                            "key": 5,
                            "code": "戊",
                            "color": "yellow"
                        },
                        "ground": {
                            "name": "인",
                            "symbol": "목",
                            "sign": "양",
                            "key": 13,
                            "code": "寅",
                            "color": "green",
                            "innerAttri": "420"
                        }
                    },
                    {
                        "year": 2075,
                        "sky": {
                            "name": "정",
                            "symbol": "화",
                            "sign": "음",
                            "key": 4,
                            "code": "丁",
                            "color": "red"
                        },
                        "ground": {
                            "name": "축",
                            "symbol": "토",
                            "sign": "음",
                            "key": 12,
                            "code": "丑",
                            "color": "yellow",
                            "innerAttri": "975"
                        }
                    },
                    {
                        "year": 2085,
                        "sky": {
                            "name": "병",
                            "symbol": "화",
                            "sign": "양",
                            "key": 3,
                            "code": "丙",
                            "color": "red"
                        },
                        "ground": {
                            "name": "자",
                            "symbol": "수",
                            "sign": "음",
                            "key": 11,
                            "code": "子",
                            "color": "black",
                            "innerAttri": "899"
                        }
                    },
                    {
                        "year": 2095,
                        "sky": {
                            "name": "을",
                            "symbol": "목",
                            "sign": "음",
                            "key": 2,
                            "code": "乙",
                            "color": "green"
                        },
                        "ground": {
                            "name": "해",
                            "symbol": "수",
                            "sign": "양",
                            "key": 22,
                            "code": "亥",
                            "color": "black",
                            "innerAttri": "408"
                        }
                    },
                    {
                        "year": 2105,
                        "sky": {
                            "name": "갑",
                            "symbol": "목",
                            "sign": "양",
                            "key": 1,
                            "code": "甲",
                            "color": "green"
                        },
                        "ground": {
                            "name": "술",
                            "symbol": "토",
                            "sign": "양",
                            "key": 21,
                            "code": "戌",
                            "color": "yellow",
                            "innerAttri": "734"
                        }
                    }
                ]
            }
        }
    }
}

# /api/project/new 엔드포인트 테스트
def test_generate_title_success():
    """
    유효한 first_question으로 제목 생성 요청 성공 테스트
    """
    url = f"{BASE_URL}/api/project/new"
    headers = {"Content-Type": "application/json"}
    payload = {"first_question": "오늘의 연애운은?"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # 200 이외의 상태 코드에 대해 예외 발생
        
        data = response.json()
        assert data["isSuccess"] == True
        assert data["code"] == "COMMON200"
        assert "title" in data["result"]
        print(f"\n[SUCCESS] generate_title_success: {data}")
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API 요청 실패: {e}")
    except AssertionError as e:
        pytest.fail(f"응답 데이터 검증 실패: {e}, 응답: {response.json()}")

def test_generate_title_missing_question():
    """
    first_question 누락 시 에러 응답 테스트
    """
    url = f"{BASE_URL}/api/project/new"
    headers = {"Content-Type": "application/json"}
    payload = {} # first_question 누락
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        assert response.status_code == 400
        data = response.json()
        assert data["isSuccess"] == False
        assert data["code"] == "COMMON4000"
        assert "입력되지 않은 필수값이 있습니다." in data["message"]
        print(f"\n[SUCCESS] generate_title_missing_question: {data}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"API 요청 실패: {e}")
    except AssertionError as e:
        pytest.fail(f"응답 데이터 검증 실패: {e}, 응답: {response.json()}")


# /api/saju/consult 엔드포인트 테스트
def test_saju_consult_success():
    """
    새로운 사주 데이터로 사주 상담 요청 성공 테스트
    """
    url = f"{BASE_URL}/api/saju/consult"
    headers = {"Content-Type": "application/json"}
    payload = NEW_SAJU_PAYLOAD # 위에서 정의한 데이터를 사용

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # 200 이외의 상태 코드에 대해 예외 발생
        
        data = response.json()
        assert data["isSuccess"] == True
        assert data["code"] == "COMMON200"
        assert "consultation_id" in data["result"]
        assert "question" in data["result"]
        assert "result" in data["result"] # 'result' 필드가 응답에 포함되어야 함
        assert "created_at" in data["result"]
        print(f"\n[SUCCESS] test_saju_consult_with_new_data_success: {data}")

    except requests.exceptions.RequestException as e:
        # 에러 발생 시 서버 응답 내용을 추가하여 디버깅에 도움
        pytest.fail(f"API 요청 실패: {e}, 서버 응답: {response.text if 'response' in locals() else 'N/A'}")
    except AssertionError as e:
        pytest.fail(f"응답 데이터 검증 실패: {e}, 응답: {response.text}")


def test_saju_consult_invalid_data():
    """
    필수 사주 데이터 누락 시 에러 응답 테스트 (birthDate 누락)
    """
    # URL을 서버의 실제 유효성 검사 엔드포인트로 확인 및 수정
    # 만약 서버가 `/api/saju/consult`에서 유효성 검사를 처리한다면 아래 URL로 변경
    url = f"{BASE_URL}/api/saju/consult" # <--- 이 부분을 확인하고 필요하면 수정
    headers = {"Content-Type": "application/json"}
    payload = {
        "question": "제 사주 좀 봐주세요.",
        "sajuData": {
            "basicInfo": {
                # "birthDate": {"year": 1990, "month": 5, "day": 10, "time": "오전 10시 30분"}, # 누락
                "gender": "남"
            },
            "sajuPillars": {}, # 빈 값
            "fiveElements": {}  # 빈 값
        }
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # 첫 번째 assert: 예상하는 400 상태 코드를 받았는지 확인
        # 만약 404가 계속 발생한다면, 서버 라우팅 문제가 확실합니다.
        assert response.status_code == 400, f"예상치 못한 상태 코드: {response.status_code}, 응답 내용: {response.text}"
        
        # 상태 코드가 400일 때만 JSON 파싱 시도
        try:
            data = response.json()
        except json.JSONDecodeError:
            pytest.fail(f"JSON 디코딩 실패: 응답이 JSON 형식이 아닙니다. 응답 내용: {response.text}")

        assert data["isSuccess"] == False
        assert data["code"] == "COMMON4000"
        # 수정된 부분: data["message"]가 단순히 'birthDate'를 포함하는지 확인
        assert "'birthDate'" in data["message"] # 또는 data["message"] == "'birthDate'" 로 정확히 일치하는지 확인할 수도 있습니다.
        assert data["result"] == "BAD_REQUEST" # 'bad request' in data["result"].lower() 대신 직접 비교
        print(f"\n[SUCCESS] saju_consult_invalid_data: {data}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"API 요청 실패: {e}, 서버 응답: {response.text if 'response' in locals() else 'N/A'}")
    except AssertionError as e:
        # 이 부분에서는 이제 response.json() 대신 data 객체를 사용
        pytest.fail(f"응답 데이터 검증 실패: {e}, 응답: {data if 'data' in locals() else response.text}")


# /api/tarot/consult 엔드포인트 테스트
def test_tarot_consult_success():
    """
    유효한 타로 카드 및 질문으로 타로 상담 요청 성공 테스트
    """
    url = f"{BASE_URL}/api/tarot/consult"
    headers = {"Content-Type": "application/json"}
    payload = {
        "question": "이번 주 애정운은 어떤가요?",
        "cards": ["The Lovers", "The Fool", "The World"]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        
        data = response.json()
        assert data["isSuccess"] == True
        assert data["code"] == "COMMON200"
        assert "consultation_id" in data["result"]
        assert "question" in data["result"]
        assert "result" in data["result"]
        assert "created_at" in data["result"]
        print(f"\n[SUCCESS] tarot_consult_success: {data}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"API 요청 실패: {e}")
    except AssertionError as e:
        pytest.fail(f"응답 데이터 검증 실패: {e}, 응답: {response.json()}")

def test_tarot_consult_missing_cards():
    """
    타로 카드 누락 시 에러 응답 테스트
    """
    url = f"{BASE_URL}/api/tarot/consult"
    headers = {"Content-Type": "application/json"}
    payload = {
        "question": "이번 주 애정운은 어떤가요?"
        # "cards": [...] # cards 누락
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        assert response.status_code == 400
        data = response.json()
        assert data["isSuccess"] == False
        assert data["code"] == "COMMON4000"
        assert "입력되지 않은 필수값이 있습니다." in data["message"]
        print(f"\n[SUCCESS] tarot_consult_missing_cards: {data}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"API 요청 실패: {e}")
    except AssertionError as e:
        pytest.fail(f"응답 데이터 검증 실패: {e}, 응답: {response.json()}")

def test_tarot_consult_missing_question():
    """
    질문 누락 시 에러 응답 테스트
    """
    url = f"{BASE_URL}/api/tarot/consult"
    headers = {"Content-Type": "application/json"}
    payload = {
        # "question": "이번 주 애정운은 어떤가요?", # question 누락
        "cards": ["The Lovers", "The Fool", "The World"]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        assert response.status_code == 400
        data = response.json()
        assert data["isSuccess"] == False
        assert data["code"] == "COMMON4000"
        assert "입력되지 않은 필수값이 있습니다." in data["message"]
        print(f"\n[SUCCESS] tarot_consult_missing_question: {data}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"API 요청 실패: {e}")
    except AssertionError as e:
        pytest.fail(f"응답 데이터 검증 실패: {e}, 응답: {response.json()}")
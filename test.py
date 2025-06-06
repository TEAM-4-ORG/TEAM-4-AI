import requests
import pytest
import json

BASE_URL = "http://127.0.0.1:5000" # Flask 서버 주소 및 포트

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


# /api/saju/content 엔드포인트 테스트
def test_saju_consult_success():
    """
    유효한 사주 데이터로 사주 상담 요청 성공 테스트
    """
    url = f"{BASE_URL}/api/saju/content"
    headers = {"Content-Type": "application/json"}
    payload = {
        "question": "제 올해 사업운은 어떤가요?",
        "sajuData": {
            "basicInfo": {
                "birthDate": {"year": 1990, "month": 5, "day": 10, "time": "오전 10시 30분"},
                "gender": "남"
            },
            "sajuPillars": {
                "yearPillar": {"sky": {"name": "庚", "code": "Geng"}, "ground": {"name": "午", "code": "Wu"}},
                "monthPillar": {"sky": {"name": "辛", "code": "Xin"}, "ground": {"name": "巳", "code": "Si"}},
                "dayPillar": {"sky": {"name": "壬", "code": "Ren"}, "ground": {"name": "申", "code": "Shen"}},
                "timePillar": {"sky": {"name": "乙", "code": "Yi"}, "ground": {"name": "巳", "code": "Si"}}
            },
            "fiveElements": {
                "목": 1, "화": 2, "토": 1, "금": 2, "수": 2
            },
            "analysis": {
                "decades": {
                    "decades": [
                        {"year": 2020, "sky": {"name": "甲", "code": "Jia"}, "ground": {"name": "寅", "code": "Yin"}},
                        {"year": 2030, "sky": {"name": "乙", "code": "Yi"}, "ground": {"name": "卯", "code": "Mao"}}
                    ]
                }
            }
        }
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
        print(f"\n[SUCCESS] saju_consult_success: {data}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"API 요청 실패: {e}")
    except AssertionError as e:
        pytest.fail(f"응답 데이터 검증 실패: {e}, 응답: {response.json()}")

def test_saju_consult_invalid_data():
    """
    필수 사주 데이터 누락 시 에러 응답 테스트 (birthDate 누락)
    """
    url = f"{BASE_URL}/api/saju/content"
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
        
        assert response.status_code == 400
        data = response.json()
        assert data["isSuccess"] == False
        assert data["code"] == "COMMON4000"
        # 수정된 부분: data["message"]가 단순히 'birthDate'를 포함하는지 확인
        assert "'birthDate'" in data["message"] # 또는 data["message"] == "'birthDate'" 로 정확히 일치하는지 확인할 수도 있습니다.
        assert data["result"] == "BAD_REQUEST" # 'bad request' in data["result"].lower() 대신 직접 비교
        print(f"\n[SUCCESS] saju_consult_invalid_data: {data}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"API 요청 실패: {e}")
    except AssertionError as e:
        pytest.fail(f"응답 데이터 검증 실패: {e}, 응답: {response.json()}")



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
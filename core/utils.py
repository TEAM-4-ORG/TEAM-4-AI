import json
import re

def extract_json(response_str):
    match = re.search(r"```json\s*(\{.*?\})\s*```", response_str, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    try:
        return json.loads(response_str)
    except Exception:
        return None
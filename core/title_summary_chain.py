from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from core.utils import extract_json
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  

# 프롬프트 템플릿 정의
template = """
아래 사용자의 첫 질문을 바탕으로 이 프로젝트의 주제를 한 줄로 요약해 주세요. 
간결하고 명확하게 요약하며, 불필요한 설명은 하지 마세요.

질문:
{question}

응답 형식:
{{"title": "여기에 요약 제목을 넣어주세요"}}
"""

prompt = PromptTemplate(
    input_variables=["question"],
    template=template
)

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.5)
chain = LLMChain(llm=llm, prompt=prompt)

def get_title_summary(first_question: str) -> str:
    response = chain.run({"question": first_question})
    parsed = extract_json(response)
    return parsed.get("title", "요약 제목 없음")

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from .utils import extract_json
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 문서 불러오기 및 분할
files = ["사주 인사이트.txt", "사주혁명.txt","동양미래예측학 석하명리의 일간 해석방법에 관한 연구.txt","타로와 사주명리학 신살의 상관 고찰.txt"]

from langchain.text_splitter import RecursiveCharacterTextSplitter

# 문서 로드
docs = []
for file in files:
    loader = TextLoader(f"data/{file}", encoding="utf-8")
    docs.extend(loader.load())

# 문서 chunking
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(docs)

embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectordb = Chroma.from_documents(split_docs, embedding, persist_directory="./db_saju")  

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
당신은 사주 전문 AI 상담가입니다.

사용자는 사주에 대한 지식이 없을 수도 있으므로, 전문 용어는 쉽게 풀어 설명해 주세요.  
질문이 사주와 직접적인 관련이 없어 보여도, 사주 정보를 바탕으로 자연스럽게 연결 지어 친절하고 구체적으로 답변해 주세요.

답변은 마치 친절한 상담사가 말하듯 따뜻하고 이해하기 쉬운 말투로 작성합니다.  
반드시 마크다운 문법을 적용해 시각적으로 보기 좋게 구성하세요. (`### 제목`, `**중요 내용**`, 리스트, 표 등 사용 가능)

결과는 오직 아래와 같은 **JSON 형식**으로만 출력하며,
JSON 외 텍스트는 절대 포함하지 마세요.

[문서]
{context}

답변을 생성할 때 **내용의 근거가 된 문서의 출처**를 `source` 항목에 반드시 포함해 주세요.  
출처는 문서에 나온 그대로 사용하고, 거짓된 예시는 넣지 마세요.

[질문]
{question}

응답 형식 예시:
{{
  "summary": "### ...내용...",
  "advice": "### ...내용...",
  "source": [
    "《보기쉬운 사주만세력》, 동학사 저, 2003",
    "https://www.sajubaju.com/"
  ]
}}

`source` 항목에서는 답변의 근거를 명확히 제시하고,
신뢰할 수 있는 출처가 있는 경우 1개 이상 출처(문서/책/논문/사이트 등)를 명확히 작성하세요.
"""
)

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4-turbo", temperature=0.7),
    retriever=vectordb.as_retriever(search_kwargs={"k": 5}),
    chain_type_kwargs={"prompt": prompt}
)


def get_saju_response(birth, time, gender, sajuPillars, fiveElements, analysis, question):
    # print("\n--- get_saju_response Input Parameters ---")
    # print(f"birth: {birth}")
    # print(f"time: {time}")
    # print(f"gender: {gender}")
    # print(f"sajuPillars: {sajuPillars}")
    # print(f"fiveElements: {fiveElements}")
    # print(f"analysis: {analysis}")
    # print(f"question: {question}")
    # print("-------------------------------------------\n")
    # analysis = analysis or {}
    year = sajuPillars["yearPillar"]
    month = sajuPillars["monthPillar"]
    day = sajuPillars["dayPillar"]
    hour = sajuPillars["timePillar"]

    decades = analysis.get("decades", {}).get("decades", [])
    decades_str = " / ".join([
        f"{d['year']}년: {d['sky']['name']}({d['sky']['code']})-{d['ground']['name']}({d['ground']['code']})"
        for d in decades
    ]) if decades else ""

    question_context = f"생년월일: {birth} {time}, 성별: {gender}\n"
    question_context += f"연주: {year['sky']['name']}({year['sky']['code']})-{year['ground']['name']}({year['ground']['code']})\n"
    question_context += f"월주: {month['sky']['name']}({month['sky']['code']})-{month['ground']['name']}({month['ground']['code']})\n"
    question_context += f"일주: {day['sky']['name']}({day['sky']['code']})-{day['ground']['name']}({day['ground']['code']})\n"
    question_context += f"시주: {hour['sky']['name']}({hour['sky']['code']})-{hour['ground']['name']}({hour['ground']['code']})\n"
    question_context += f"오행 분포: {', '.join([f'{k} {v}' for k, v in fiveElements.items()])}\n"

    if "hop" in analysis:
        hops = analysis["hop"]
        all_hops = []
        if hops.get('skyHop'):
            all_hops.extend(hops['skyHop'])
        if hops.get('bangHop'):
            all_hops.extend(hops['bangHop'])
        if hops.get('somHop'): # somHop이 null이 아닌 경우만 추가
            all_hops.append(hops['somHop'])
        if hops.get('banHop'):
            all_hops.extend(hops['banHop'])
        if hops.get('sixHop'):
            all_hops.extend(hops['sixHop'])
        if all_hops: # 합 정보가 있을 경우에만 추가
            question_context += f"합: {', '.join(all_hops)}\n"
    if "chung" in analysis:
        chungs = analysis["chung"]
        question_context += f"충(천간/지지 충): {chungs.get('skyChung', []) + chungs.get('groundChung', [])}\n"
    if decades_str:
        question_context += f"대운 흐름: {decades_str}\n"

    full_question = f"{question_context}\n질문: {question}"
#    print(f"\n--- Full Question sent to LLM ---\n{full_question}\n-----------------------------------\n") # 이 라인을 추가

    response = qa.run(full_question)
    return extract_json(response)


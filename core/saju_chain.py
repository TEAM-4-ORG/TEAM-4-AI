from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from .utils import extract_json
import os
from dotenv import load_dotenv

# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY=""
loader = TextLoader("data/saju_data.txt", encoding="utf-8")
docs = loader.load()
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectordb = Chroma.from_documents(docs, embedding, persist_directory="./db_saju")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
당신은 사주 전문 AI 상담가입니다.
아래의 문서와 질문을 참고하여, 사용자에게 사주 해석 결과를 제공하세요.  
반드시 JSON 형식으로 응답하고, 내용에 사용된 문서의 출처도 포함하세요.  
텍스트 설명 없이 순수 JSON만 출력해 주세요.

[문서]
{context}

[질문]
{question}

응답 예시:
{{
  "summary": "...",
  "advice": "...",
  "birth_info": "1997년 5월 3일, 여성, 신금 일간",
  "topic": "연애운",
  "source": ["사주 인사이트"]
}}
"""
)

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.7),
    retriever=vectordb.as_retriever(search_kwargs={"k": 2}),
    chain_type_kwargs={"prompt": prompt}
)

def get_saju_response(birth, time, gender, ilgan, palja, oheng, question):
    full_question = f"{birth} {time} {gender}, 일간 {ilgan}, 오행 분석 {oheng}. {question}"
    response = qa.run(full_question)
    return extract_json(response)
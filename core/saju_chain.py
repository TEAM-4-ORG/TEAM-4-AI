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
files = ["사주 인사이트.txt", "사주혁명.txt"]

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
다음 문서를 참고하여 사용자의 질문에 답변해 주세요.  
결과는 JSON 형식으로 출력하세요. 각 항목은 마크다운 문법을 적용해 구성하세요.  
텍스트 설명 없이 순수 JSON만 출력해 주세요.

[문서]
{context}

[질문]
{question}

응답 형식 예시:
{{
  "summary": "### ...내용...",
  "advice": "### ...내용...",
  "source": ["사주 인사이트", "사주혁명"]
}}
"""
)

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4-turbo", temperature=0.7),
    retriever=vectordb.as_retriever(search_kwargs={"k": 5}),
    chain_type_kwargs={"prompt": prompt}
)


def get_saju_response(birth, time, gender, ilgan, ilju, ilji, oheng, sibsin, question):
    full_question = f"{birth} {time} {gender}, 일간: {ilgan}, 일주: {ilju}, 일지: {ilji}, 오행: {oheng}, 십신: {sibsin}. {question}"
    response = qa.run(full_question)
    return extract_json(response)


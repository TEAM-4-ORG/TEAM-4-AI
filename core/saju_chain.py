from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from .utils import extract_json
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

files=["사주 인사이트.txt","사주혁명.txt"]

docs = []
for file in files:
    loader = TextLoader(f"data/{file}", encoding="utf-8")
    docs.extend(loader.load())
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

vectordb = Chroma.from_documents(docs, embedding, persist_directory="./db_saju")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
당신은 사주 전문 AI 상담가입니다.
다음 문서를 참고하여 사용자의 질문에 답변해 주세요.  
결과는 반드시 JSON 형식으로 반환하며, 마지막에 사용한 문서 출처를 마크다운 형식으로 명확히 포함하세요.  
텍스트 설명 없이 순수 JSON만 출력해 주세요.

[문서]
{context}

[질문]
{question}

응답 형식 예시:
{{
  "summary": "사주 해석 결과를 2~3문장으로 자세히 서술해주세요.",
  "advice": "구체적인 생활 조언을 1~2문장으로 제시해주세요.",
  "source": ["사주 인사이트", "명리학 개론"]
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

# def show_retrieved_docs(question):
#     retriever = vectordb.as_retriever(search_kwargs={"k": 5})
#     docs = retriever.get_relevant_documents(question)
#     for i, doc in enumerate(docs, 1):
#         print(f"\n 문서 {i}:\n{doc.page_content}")

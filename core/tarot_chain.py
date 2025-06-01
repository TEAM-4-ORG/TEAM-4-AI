from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from .utils import extract_json
import os
from dotenv import load_dotenv

#실제 작동시 보안때문에 아래코드 사용
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 위 코드 주석하고 아래에 직접 키 입력해도 됨
#OPENAI_API_KEY=""
files=["타로입문서.txt","암기할 필요 없는 타로.txt"]

docs = []
for file in files:
    loader = TextLoader(f"data/{file}", encoding="utf-8")
    docs.extend(loader.load())
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectordb = Chroma.from_documents(docs, embedding, persist_directory="./db_tarot")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
당신은 타로 전문가 AI입니다.

다음 문서와 질문을 참고하여 사용자의 질문에 답변을 제공하세요.  
결과는 JSON 형식으로 출력하고, 반드시 마크다운 형식으로 출처를 포함하세요.  
텍스트 설명 없이 JSON만 출력해 주세요.

[문서]
{context}

[질문]
{question}

응답 예시:
{{
  "summary": "...",
  "advice": "...",
  "card_used": ["The Lovers", "The Moon"],
  "topic": "연애운",
  "source": ["타로입문서"]
}}
"""
)

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4-turbo", temperature=0.7),
    retriever=vectordb.as_retriever(search_kwargs={"k": 2}),
    chain_type_kwargs={"prompt": prompt}
)

def get_tarot_response(cards,question):
    full_question = f"선택한 카드는 {', '.join(cards)}입니다. 질문: {question}"
    response = qa.run(full_question)
    return extract_json(response)

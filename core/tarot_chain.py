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

files = ["암기할 필요 없는 타로.txt","타로입문서.txt","타로와 사주명리학 신살의 상관 고찰.txt"]

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
vectordb = Chroma.from_documents(split_docs, embedding, persist_directory="./db_tarot") 

# 프롬프트 정의
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
당신은 타로 전문가 AI입니다.

다음 문서와 질문을 참고하여 사용자의 질문에 답변을 제공하세요.  
결과는 JSON 형식으로 출력하세요. 각 항목은 마크다운 문법을 적용해 구성하세요.  
텍스트 설명 없이 JSON만 출력해 주세요.

[문서]
{context}

[질문]
{question}

응답 예시:
{{
  "summary": "### 🧾...내용...",
  "advice": "### 💡...내용...",
  "card_used": ["The Lovers", "The Moon"],
  "topic": "연애운",
  "source": ["타로입문서"]
}}
"""
)

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4-turbo", temperature=0.7),
    retriever=vectordb.as_retriever(search_kwargs={"k": 5}),
    chain_type_kwargs={"prompt": prompt}
)

def get_tarot_response(selected_cards, question):
    full_question = f"선택한 카드는 {', '.join(selected_cards)}입니다. 질문: {question}"
    response = qa.run(full_question)
    return extract_json(response)

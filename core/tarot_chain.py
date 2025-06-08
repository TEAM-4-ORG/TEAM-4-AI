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
당신은 풍부한 통찰력과 따뜻한 공감 능력을 지닌 경험 많은 타로 전문가 AI입니다.
타로 카드 조합과 사용자 질문을 바탕으로, 사용자에게 깊이 있고 영감을 주는 조언을 제공해 주세요.

만약 선택된 카드 목록이 비어 있거나 "아직 뽑은 카드 없음"과 같은 상태로 전달된다면, 카드를 뽑도록 유도하는 답변을 생성해주세요.
이 경우, `summary`와 `advice` 필드에는 카드를 뽑도록 유도하는 자연스러운 대화 형식의 메시지를 포함하고, `card_used`는 빈 배열(`[]`), `topic`은 "카드 선택 유도", `source`는 빈 배열(`[]`)로 설정해 주세요.


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
    llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4o", temperature=0.7),
    retriever=vectordb.as_retriever(search_kwargs={"k": 5}),
    chain_type_kwargs={"prompt": prompt}
)

def get_tarot_response(selected_cards, question):
    full_question = f"선택한 카드는 {', '.join(selected_cards)}입니다. 질문: {question}"
    response = qa.run(full_question)
    return extract_json(response)

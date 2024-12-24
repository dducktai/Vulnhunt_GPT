import os
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import argparse
from langchain_openai import OpenAIEmbeddings

# Load environment variables
os.environ["OPENAI_API_KEY"] = ""
os.environ['PINECONE_API_KEY'] = ''

api_key = os.environ["PINECONE_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Initialize Pinecone
pc = Pinecone(api_key=api_key)
index_name = "vulnhunt-gpt"

# Ensure the index exists
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
if index_name not in existing_indexes:
    raise ValueError(f"Index {index_name} not found. Please ensure the index is created before running this.")


embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
# Load the Pinecone VectorStore = connect to it
vectorstore = PineconeVectorStore(
    index_name=index_name,
    embedding=embeddings
)



llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name='gpt-3.5-turbo',
    temperature=0.0
)

qa = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

def get_multiline_input(prompt="Nhập prompt của bạn (kết thúc bằng dòng trống):"):
    print(prompt)
    lines = []
    while True:
        line = input()  # Đọc từng dòng
        if line.strip() == "":  # Nếu dòng trống, dừng nhập
            break
        lines.append(line)
    return "\n".join(lines)  # Ghép các dòng thành một chuỗi

if __name__ == "__main__":
    print("===================== VULNHUNT-GPT ====================")
    user_prompt = "give me the vulnerability of this code, then give me the remediation of the vulnerability " + get_multiline_input("Nhập prompt của bạn (kết thúc bằng dòng trống):")
    
    # Gọi LLM để lấy kết quả
    response = qa.invoke(user_prompt)
    
    # Lấy phần "answer" và "sources" từ kết quả trả về
    answer = response.get("answer", "Không tìm thấy câu trả lời.")
    sources = response.get("sources", "Không tìm thấy nguồn.")
    
    # In kết quả định dạng lại
    print("--------------------------------")
    print("\nKết quả truy vấn:")
    print(answer, end= "")
    print(f"\nNguồn:\n{sources}")
    print("--------------------------------")

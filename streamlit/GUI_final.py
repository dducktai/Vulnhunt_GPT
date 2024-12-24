import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import module_preprocessing

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
module_preprocessing.configure_api(api_key="")
model = module_preprocessing.create_model()
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "vulnhunt-gpt-final"

# Ensure the index exists
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
if index_name not in existing_indexes:
    st.error(f"Index {index_name} not found. Please ensure the index is created before running this.")
    st.stop()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
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

# Streamlit App
st.set_page_config(
    page_title="VulnHunt-GPT",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)



# Custom CSS for better UI
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f4f4f9;
    }
    .sidebar .sidebar-content {
        background: #2b3e50;
        color: white;
    }
    .css-1aumxhk {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    .css-1q8dd3e {
        font-family: "Roboto", sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.write("Cấu hình và tuỳ chọn.")

# Main App Interface
st.title("🔍 VulnHunt-GPT")
st.write(
    """
    ### Công cụ phân tích và tìm kiếm lỗ hổng trong hợp đồng thông minh Solidity.
    Nhập mã Solidity của bạn vào ô bên dưới, nhấn **Analyze** để nhận kết quả.
    """
)

# Layout with two columns
col1, col2 = st.columns([2, 1])

with col1:
# Input for Solidity smart contract or query
    user_input = st.text_area("Enter Solidity Smart Contract:", height=200)
    # print(user_input)

with col2:
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmTXXbOYR3NhD29AnL76vrZBDMk6gbTFD8Cg&s",
        use_container_width=False,
        width=200
    )
    st.write("### Hướng dẫn:")
    st.markdown(
        """
        - 🔴 **Nhập mã Solidity bạn cần phân tích.**
        - 🔴 **Nhấn nút `Analyze` để phân tích.**
        - 🔴 **Xem kết quả và giải pháp phía dưới.**
        """
    )


# Button to analyze
if st.button("Analyze"):
    if not user_input.strip():
        st.error("⚠️ Vui lòng nhập nội dung hợp lệ.")
    else:
        with st.spinner("⏳ Đang phân tích, vui lòng chờ..."):
            # Preprocess and prepare the user input
            chat_session = module_preprocessing.start_chat_session(model, user_input)
            response = module_preprocessing.send_message(chat_session, user_input)
            formatted_response = module_preprocessing.process_response(response)
            # Save results
            module_preprocessing.save_response(formatted_response)
            user_prompt = f"""
                You are VulnHunt—GPT. You will analyze the Solidity smart contract in order to find any vulnerabilities. 
                When you find vulnerabilities, you will answer always in this way:
                — Vulnerabilities: and
                — Remediation: 
                For Vulnerabilities you will describe any vulnerabilities that you have found and what cause them. 
                For Remediation you will suggest the remediation and any possible fixes to the source code
            """ + formatted_response

            # Query the LLM
            try:
                response = qa.invoke(user_prompt)
                answer = response.get("answer", "No answer found.")
                sources = response.get("sources", "No sources found.")
    
                    # Display results
                st.success("✅ Phân tích hoàn tất!")
                st.subheader("🎯 Kết quả phân tích:")
                st.text_area("Vulnerabilities and Remediations:", answer, height=300)

                st.subheader("📚 Nguồn tham khảo:")
                st.write(sources)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
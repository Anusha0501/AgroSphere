import os
import base64
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain

# Load environment variables
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# ====== Background Image ======

def get_base64_bg(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_bg(image_path):
    base64_img = get_base64_bg(image_path)
    ext = image_path.split(".")[-1]
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(to bottom, rgba(255, 255, 255, 0.85), rgba(245, 255, 245, 0.9)),
                        url("data:image/{ext};base64,{base64_img}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            font-family: 'Segoe UI', sans-serif;
            color: #2e4e1f;
        }}
        h1 {{
            font-size: 2.2em;
            text-align: center;
            color: #2e4e1f;
            margin-bottom: 1rem;
        }}
        .message {{
            border-radius: 12px;
            padding: 12px 18px;
            margin: 10px 0;
            max-width: 80%;
            font-size: 16px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.05);
        }}
        .user-msg {{
            background-color: #e8f5e9;
            color: #1b5e20;
            text-align: right;
            margin-left: auto;
        }}
        .bot-msg {{
            background-color: #fdfdfd;
            color: #2e4e1f;
            border-left: 4px solid #81c784;
            text-align: left;
            margin-right: auto;
        }}
        .stChatInputContainer input {{
            border-radius: 20px;
            padding: 12px;
            border: 1px solid #c5e1a5;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background
set_bg("background.jpg")  # Replace with actual background image path

# ====== LangChain Setup ======

# Chat memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(
        k=2, memory_key="chat_history", return_messages=True
    )

# Vector DB and embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = Chroma(persist_directory="my_chroma_store", embedding_function=embeddings)
db_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# Prompt template
prompt_template = """
<s>[INST]
You are AgroSphere, a professional AI agricultural assistant. Your goal is to provide clear, reliable, and technically sound responses using appropriate agricultural terminology wherever necessary.

Instructions:
- Base your answers strictly on the provided CONTEXT and your agricultural knowledge.
- Use agronomic or farming terms (e.g., "powdery mildew" instead of "white plant fungus") when relevant, but ensure explanations remain concise and understandable.
- Limit answers to **1–2 sentences** maximum.
- Always end with the disclaimer: 
  “Thank you. Happy to help you!”

If the question is outside your knowledge or CONTEXT, respond with:
“I’m sorry, I don’t have enough information to answer that. Please consult an agricultural expert.”

CONTEXT: {context}

CHAT HISTORY: {chat_history}

USER QUESTION: {question}

YOUR ANSWER:
</s>[INST]
"""

prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question', 'chat_history'])

# LLM
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# QA Chain
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=st.session_state.memory,
    retriever=db_retriever,
    combine_docs_chain_kwargs={'prompt': prompt}
)

# ====== Streamlit UI ======

st.markdown("<h1>🌿 AgroSphere—Your Smart Agricultural Companion</h1>", unsafe_allow_html=True)


# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat display area
chat_container = st.container()
input_container = st.container()

# Show chat messages (older to newer) with icons
with chat_container:
    for sender, msg in st.session_state.chat_history:
        if sender == "User":
            st.markdown(
                f"<div class='message user-msg'>"
                f"<span style='font-size:20px;'>👨‍🌾</span> <strong>User:</strong><br>{msg}"
                f"</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='message bot-msg'>"
                f"<span style='font-size:20px;'>🌿</span> <strong>AgroSphere:</strong><br>{msg}"
                f"</div>",
                unsafe_allow_html=True
            )

# Input field pinned at the bottom
with input_container:
    user_input = st.chat_input("Ask your question related to agriculture here...")

# Process input
if user_input:
    with st.spinner("🤖 AgroSphere is thinking..."):
        result = qa.invoke(input=user_input)
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("AgroSphere", result["answer"]))
        st.rerun()

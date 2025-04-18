from student_councellor.tools import StoriesTool, CommentsTool, ContentTool  
import asyncio 
from PIL import Image
import streamlit as st 
from langchain.agents.agent_types import AgentType 
from langchain.agents.initialize import initialize_agent
from langchain_community.chat_models.openai import ChatOpenAI 
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory 
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder

# Get API key from Streamlit secrets
api_key = st.secrets.get("OPENAI_API_KEY")

if api_key is None:
    raise ValueError(
        "API key not found. Please set the OPENAI_API_KEY environment variable." 
    ) 

# Update page configuration with a generic title and favicon
st.set_page_config(
    page_title="AI Career Counselor",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar: add content about the app along with contact details
st.sidebar.markdown(
    """
    ## About the App
    Welcome to the **AI Career Counselor**! This virtual tool assists students in exploring potential career paths, identifying their strengths, and making informed academic and professional decisions. 
      
    **Features:**
    - Answers queries on top colleges, courses, and educational paths.
    - Provides networking strategies and insights on continuous learning.
    - Integrates multiple AI models and agents to deliver comprehensive guidance.
      
    For more details or to view the source code, visit the [Repository](https://github.com/alsaif1431/AI-Student-Councellor).
      
    ---
      
    ## Contact Us
    - [LinkedIn](https://www.linkedin.com/in/saif-pasha-59643b197/)
    - [GitHub](https://github.com/alsaif1431)
    """
)

async def generate_response(question):
    result = await open_ai_agent.arun(question)
    return result

st.title("AI Career Counselor 👩🏻‍🏫")
stop = False

if api_key:
    success_message_html = """
    <span style='color:green; font-weight:bold;'>
        ✅ Powering the Chatbot using Groq's 
        <a href='https://console.groq.com' target='_blank'>Llama 3.3 model</a>!
    </span>
    """
    st.markdown(success_message_html, unsafe_allow_html=True)
    openai_api_key = api_key
else:
    openai_api_key = st.text_input("Enter your API_KEY: ", type="password")
    if not openai_api_key:
        st.warning("Please, enter your API_KEY", icon="⚠️")
        stop = True
    else:
        st.success("Ask the AI career counselor for guidance!", icon="👉")

st.markdown(
    """
    # *Ask me about* :
    1. **Top colleges in your state.**
    2. **Top courses to pursue based on your academics.**
    3. **What educational and certification paths should I consider for career advancement?**
    4. **What networking strategies can I employ to build a strong professional network?**
    5. **What is the importance of continuous learning in today's evolving job landscape?**
    """
)

if stop:
    st.stop()

tools = [StoriesTool(), CommentsTool(), ContentTool()]
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs, return_messages=True)

system_message = SystemMessage(
    content="""
        You are an expert student counselor who will guide and
        assist students in their career paths.

        Based on the user question, suggest the best resources and insights 
        after performing relevant Google searches.

        Your sole purpose is to assist students in making the best decisions 
        for their careers. Provide specific, precise, and truthful answers in markdown format.
        
        If a user greets you, simply greet back with a short message like "Thanks for asking".
        
        If asked your name, respond with "AI career counselor" and remember to say "Thanks for asking" at the end of your answer.
        
        Always return the source link of the answer at the end and avoid duplicate links.
    """
)

if len(msgs.messages) == 0:
    msgs.add_ai_message(
        "Hello there, I am the AI Career Counselor. How can I help you?"
    )

llm = ChatOpenAI()
agent_kwargs = {
    "system_message": system_message,
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="history")],
}
open_ai_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    agent_kwargs=agent_kwargs,
    verbose=True,
    memory=memory,
)

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input(disabled=not openai_api_key):
    st.chat_message("human").write(prompt)
    with st.spinner("Thinking and analyzing ..."):
        response = asyncio.run(generate_response(prompt))
        st.chat_message("ai").write(response)

# Footer with generic information
footer_html = """
<div style="text-align: center; margin: 0px;">
    <p>
        © 2024. All rights reserved.
    </p>
</div>
"""

footer_css = """
<style>
.footer {
    position: fixed;
    z-index: 1000;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    padding: 10px 0;
}
</style>
"""

footer = f"{footer_css}<div class='footer'>{footer_html}</div>"
st.markdown(footer, unsafe_allow_html=True)

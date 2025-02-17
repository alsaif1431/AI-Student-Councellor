from student_councellor.tools import StoriesTool,CommentsTool,ContentTool
import asyncio
from PIL import Image
import streamlit as st
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory import StreamlitChatMessageHistory
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder
# from langchain_openai import ChatOpenAI

api_key = st.secrets["OPENAI_API_KEY"]

if api_key is None:
    raise ValueError(
        "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

favicon = Image.open("favicon.png")

st.set_page_config(
    page_title="GenAI Demo | Trigent AXLR8 Labs",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Logo
logo_html = """
<style>
    [data-testid="stSidebarNav"] {
        background-image: url(https://trigent.com/wp-content/uploads/Trigent_Axlr8_Labs.png);
        background-repeat: no-repeat;
        background-position: 20px 20px;
        background-size: 80%;
    }
</style>
"""
st.sidebar.markdown(logo_html, unsafe_allow_html=True)


async def generate_response(question):
    result = await open_ai_agent.arun(question)
    return result

st.title("Ai carrer councellor 👩🏻‍🏫")
stop = False

if api_key:
    success_message_html = """
    <span style='color:green; font-weight:bold;'>✅ Powering the Chatbot using Open AI's 
    <a href='https://platform.openai.com/docs/models/gpt-3-5' target='_blank'>gpt-3.5-turbo-0613 model</a>!</span>
    """

    # Display the success message with the link
    st.markdown(success_message_html, unsafe_allow_html=True)
    openai_api_key = api_key
else:
    openai_api_key = st.text_input(
        'Enter your OPENAI_API_KEY: ', type='password')
    if not openai_api_key:
        st.warning('Please, enter your OPENAI_API_KEY', icon='⚠️')
        stop = True
    else:
        st.success('Ask Ai career councellor about guidance!', icon='👉')


st.markdown("""
# *Ask me about* :
1. **Top colleges in your state.**
2. **Top courses to pursue based on your academics.**
3. **What educational and certification paths should I consider for career advancement?**
4. **What networking strategies can I employ to build a strong professional network?**
5. **What is the importance of continuous learning in today's evolving job landscape?**

""")



if stop:
    st.stop()


tools = [StoriesTool(), CommentsTool(), ContentTool()]
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs, return_messages=True)

system_message = SystemMessage(content="""
        You are an expert student counselor who will guide and
        assist students in their career paths.

        Remember Based on the user question, you will suggest them the best 
        from the Google searches after searching it n the web first.

        You will never dissatisfy user.

        Remember that your sole purpose is to assist students in making 
        the best decisions for their careers.

        Be specific and precise in your response.
        Always be truthful in your answers as it is a matter of student's careers.

        Remember to give the answer in a markdown format and do not overwrite the answer.

        If the user greets you just greet him normally and do not include
        anything apart from greeting like "Thanks for asking".

        If the user asks for your name, always reply with "AI career counselor".
        Remeber to say "Thanks for asking" at the end of the answer.

        Remember to return the source link of the answer at the end and don't add
        duplicate sources link.
""")

if len(msgs.messages) == 0:
    msgs.add_ai_message(
        "Hello there, I am the Ai Career councellor. How can I help you?")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613",
                 openai_api_key=openai_api_key)
agent_kwargs = {
    "system_message": system_message,
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="history")]
}
open_ai_agent = initialize_agent(tools,
                                 llm,
                                 agent=AgentType.OPENAI_FUNCTIONS,
                                 agent_kwargs=agent_kwargs,
                                 verbose=True,
                                 memory=memory
                                 )

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)


if prompt := st.chat_input(disabled=not openai_api_key):
    st.chat_message("human").write(prompt)
    with st.spinner("Thinking and analyzing ..."):
        response = asyncio.run(generate_response(prompt))
        st.chat_message("ai").write(response)

# Footer
footer_html = """
<div style="text-align: right; margin-right: 10%;">
    <p>
        Copyright © 2024, Trigent Software, Inc. All rights reserved. | 
        <a href="https://www.facebook.com/TrigentSoftware/" target="_blank">Facebook</a> |
        <a href="https://www.linkedin.com/company/trigent-software/" target="_blank">LinkedIn</a> |
        <a href="https://www.twitter.com/trigentsoftware/" target="_blank">Twitter</a> |
        <a href="https://www.youtube.com/channel/UCNhAbLhnkeVvV6MBFUZ8hOw" target="_blank">YouTube</a>
    </p>
</div>
"""

# Custom CSS to make the footer sticky
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
}
</style>
"""


footer = f"{footer_css}<div class='footer'>{footer_html}</div>"

# Rendering the footer
st.markdown(footer, unsafe_allow_html=True)
import os

from dotenv import load_dotenv
import streamlit as st

from hindsight_client import Hindsight
from groq import Groq

from ingest_gmail import ingest_emails


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

BANK_ID = "enterprise-knowledge"


# ============================================================
# CONNECT SERVICES
# ============================================================

@st.cache_resource
def connect_services():

    hindsight_client = Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=os.getenv("HINDSIGHT_API_KEY")
    )

    groq_client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    return hindsight_client, groq_client


hindsight_client, groq_client = connect_services()


# ============================================================
# AGENT
# ============================================================

def ask_agent(question):

    # --------------------------------------------------------
    # STEP 1: SYNC NEW GMAIL DATA
    # --------------------------------------------------------

    try:

        with st.status(
            "🔄 Syncing new enterprise emails...",
            expanded=False
        ):

            new_emails = ingest_emails()

        if new_emails > 0:

            st.success(
                f"📧 Synced {new_emails} new email(s) into enterprise memory."
            )

        else:

            st.info(
                "📧 No new enterprise emails found."
            )

    except Exception as e:

        st.warning(
            f"Gmail sync skipped: {e}"
        )


    # --------------------------------------------------------
    # STEP 2: RECALL FROM HINDSIGHT
    # --------------------------------------------------------

    try:

        result = hindsight_client.recall(
            bank_id=BANK_ID,
            query=question
        )

    except Exception as e:

        raise Exception(
            f"Hindsight recall failed: {e}"
        )


    # --------------------------------------------------------
    # STEP 3: EXTRACT MEMORY TEXT
    # --------------------------------------------------------

    memories = []

    if hasattr(result, "results"):

        for item in result.results:

            if hasattr(item, "text"):

                memories.append(item.text)

    elif isinstance(result, list):

        for item in result:

            if hasattr(item, "text"):

                memories.append(item.text)

            elif isinstance(item, dict) and "text" in item:

                memories.append(item["text"])


    # --------------------------------------------------------
    # STEP 4: NO MEMORY FOUND
    # --------------------------------------------------------

    if not memories:

        return "I don't have that information in the enterprise memory."


    # --------------------------------------------------------
    # STEP 5: BUILD CONTEXT
    # --------------------------------------------------------

    context = "\n\n--- MEMORY ---\n\n".join(memories)


    # --------------------------------------------------------
    # STEP 6: ASK GROQ
    # --------------------------------------------------------

    prompt = f"""
You are an Enterprise Knowledge Agent.

Answer the user's question using ONLY the information
contained in the retrieved enterprise memories below.

STRICT FACTUAL GROUNDING RULES:

- Use only facts explicitly stated in the memories.
- Do not invent information.
- Do not infer names, numbers, dates, events, or relationships.
- Preserve numbers exactly as stated.
- Do not combine unrelated memories to create a new fact.
- If the memories say something was NOT detected, do not
  convert that into a positive event or numerical count.
- If the answer is not explicitly supported by the memories,
  say:

"I don't have that information in the enterprise memory."

Keep the answer concise and professional.

Retrieved enterprise memories:

{context}

User question:

{question}
"""


    response = groq_client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": "You are a factual enterprise knowledge assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )


    return response.choices[0].message.content


# ============================================================
# STREAMLIT UI
# ============================================================

st.set_page_config(
    page_title="Enterprise Knowledge Agent",
    page_icon="🧠",
    layout="centered"
)


st.title("🧠 Enterprise Knowledge Agent")

st.caption(
    "An AI agent that continuously learns from enterprise information "
    "using Gmail, Groq, and Hindsight memory."
)


# ============================================================
# STATUS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Memory",
        "Persistent",
        "Hindsight"
    )

with col2:

    st.metric(
        "Data Source",
        "Gmail",
        "Connected"
    )

with col3:

    st.metric(
        "AI Engine",
        "Groq",
        "Connected"
    )


st.divider()


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask about projects, people, tasks, decisions, issues..."
)


if question:

    # Show user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # Generate agent response

    with st.chat_message("assistant"):

        with st.spinner("🧠 Checking enterprise memory..."):

            try:

                answer = ask_agent(question)

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                error_message = f"Agent error: {e}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🧠 Agent")

    st.write(
        "This agent continuously synchronizes new Gmail "
        "information into persistent enterprise memory."
    )

    st.divider()

    st.subheader("Capabilities")

    st.write("📧 Gmail ingestion")
    st.write("🔍 Semantic email filtering")
    st.write("🧠 Enterprise memory")
    st.write("🤖 LLM fact extraction")
    st.write("💬 Natural language questions")

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()
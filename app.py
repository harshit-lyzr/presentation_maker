import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType

st.set_page_config(
    page_title="HTML To ReactJS Convertor",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

api = st.sidebar.text_input("Enter Your OPENAI API KEY HERE", type="password")

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("HTML To ReactJS Convertor💻")
st.markdown("## Welcome to the HTML To ReactJS Convertor!")
st.markdown(
    "This App Harnesses power of Lyzr Automata to Convert HTML code to ReactJS. You Need to input Your HTML,CSS and JS code and it will convert it into ReactJS.")


if api:
    openai_model = OpenAIModel(
        api_key=api,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )
else:
    st.sidebar.error("Please Enter Your OPENAI API KEY")


def presentation_maker(topics):
    content_agent = Agent(
        prompt_persona=f"You are a Content writer.",
        role="Content writer",
    )

    content_task = Task(
        name="content writer",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=content_agent,
        log_output=True,
        instructions=f"""
        write a Header and 4 bullet points for given {topics}.
        Bullet point is not more then 10 words.
        """,
    )

    python_agent = Agent(
        prompt_persona=f"You are a Python Developer.",
        role="Python Developer",
    )

    python_task = Task(
        name="content writer",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=python_agent,
        input_tasks=[content_task],
        log_output=True,
        instructions=f"""
            We have provided with header and 4 bullet points.
            please generate python-pptx code for a single slide with this header & bullet points.
            Separate the bullet points into separate texts.
            Do not set font size.
            Only generate code nothing else.
            """,
    )

    output = LinearSyncPipeline(
        name="Presentation Generation",
        completion_message="Presentation Generated!",
        tasks=[
            content_task,
            python_task
        ],
        ).run()
    return output[1]['task_output']


topic = st.text_input("Enter Topic")

if st.button("Generate"):
    solution = presentation_maker(topic)
    st.markdown(solution)

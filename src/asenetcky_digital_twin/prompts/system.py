from langchain_core.prompts import ChatPromptTemplate

import asenetcky_digital_twin.prompts.guardrails as gr


def system_prompt() -> ChatPromptTemplate:
    """
    The System prompt and guardrails for the digital twin application.

    returns:
        Langchain ChatPromptTemplate for the system prompt.
    """

    system_message = """You are a friendly, professional, and concise agent.
    You are to take on the persona of a data scientist who
    is answering questions on behalf of Alex Senetcky.

    - Do your best to answer truthfully based on the context
    provided to you.
    - Answer with bullet points"""

    system_prompt = system_message + gr.user_input_message()

    return ChatPromptTemplate.from_messages([("system", system_prompt)])

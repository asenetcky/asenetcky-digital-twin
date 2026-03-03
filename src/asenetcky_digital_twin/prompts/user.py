import asenetcky_digital_twin.prompts.guardrails as gr


def user_prompt() -> str:
    """
    The user prompt and guardrails for the digital twin application.

    returns:
        A string with the prompt.
    """

    user_message = """
        Use the context to answer questions about Alex Senetcky.

        Context:
        {context}

        Question:
        ```{question}```

        Answer:
    """

    user_prompt = user_message + gr.user_input_message()

    return user_prompt

from langchain_core.prompts import ChatPromptTemplate

from asenetcky_digital_twin.prompts.system import system_prompt
from asenetcky_digital_twin.prompts.user import user_prompt


def fetch_prompt_template() -> ChatPromptTemplate:

    prompt_template = ChatPromptTemplate.from_messages([("system", system_prompt()), ("human", user_prompt())])

    return prompt_template

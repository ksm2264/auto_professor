from langchain.prompts import PromptTemplate

_DEFAULT_ENTITY_SUMMARIZATION_TEMPLATE = """You are a scientific AI assistant keeping track of facts about key concepts in a paper.
Update the summary of the provided concept in the "concept" section based on the last text chunk from the paper.
If you are writing the summary for the first time, return a single sentence.
The update should only include facts that are relayed in the last chunk about the provided concept, and should only contain facts about the provided concept.

If there is no new information about the provided concept or the information is not worth noting
 return the existing summary unchanged.

Last few chunks (for context):
{history}

Entity to summarize:
{concept}

Existing summary of {concept}:
{summary}

Last line of conversation:
Human: {input}
Updated summary:"""

summarization_template = PromptTemplate(
    input_variables=["concept", "summary", "history", "input"],
    template=_DEFAULT_ENTITY_SUMMARIZATION_TEMPLATE,
)
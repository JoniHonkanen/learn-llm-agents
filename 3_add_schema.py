import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv

#This example add schema to the LLM output

# .env file is used to store the api key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Initialize the language model
# use dotnenv to load OPENAI_API_KEY api key
llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-4o-mini",
)

# Create a prompt template, topic is a variable
FUNNY_LLM_PROMPT = ChatPromptTemplate.from_template(
    """
    You are the funniest person in the world, a comedian, a joker. You make up jokes about every topic.
    Topic: {topic}                                                      
    """
)


# Create a Pydantic model for the prompt
# Reason of this is to structure the output of the LLM
class FunnySchema(BaseModel):
    topic: str = Field(
        description="The topic of the joke",
    )
    joke: str = Field(
        description="The joke",
    )
    rating: int = Field(
        description="The rating of the joke, from 1 to 10 (bigger is funnuer)",
    )
    rating_reason: str = Field(
        description="Why the joke is rated this way",
    )


# Use created schema to structure the output
structured_llm = llm.with_structured_output(FunnySchema)
prompt = FUNNY_LLM_PROMPT.format(topic="Hello World")
# Invoke the LLM with a prompt and get the structured output
res = structured_llm.invoke(prompt)

# Print the whole structured output
print(f"{res}\n")
# Print the structured output fields (from FunnySchema)
print(res.topic)
print(res.joke)
print(res.rating)
print(res.rating_reason)

# langchain_helper.py
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def generate_blog_titles(topic: str, adjective: str):
    if not topic or not topic.strip():
        raise ValueError("Topic must be a non-empty string.")
    if not adjective or not adjective.strip():
        raise ValueError("Adjective/type must be a non-empty string.")

    llm = ChatGroq(
        model="qwen/qwen3-32b",
        temperature=0.7
    ) 

    prompt_template = PromptTemplate(
        input_variables=["topic", "adjective"],
        template="Suggest three {adjective} blog post titles about {topic}."
    )

    chain = prompt_template | llm | StrOutputParser()

    response = chain.invoke({"topic": topic, "adjective": adjective})

    # 🧹 Remove hidden reasoning block
    response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

    return response


if __name__ == "__main__":
    user_topic = input("Enter a topic: ").strip()
    user_adjective = input("What kind of titles? (e.g. creative, academic, funny): ").strip()

    print("\nGenerated Titles (raw LLM output):\n")
    print(generate_blog_titles(user_topic, user_adjective))


 
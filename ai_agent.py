from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider=="Groq":
        llm = ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm = ChatOpenAI(model=llm_id)
    
    tools = [TavilySearch(max_results=2)] if allow_search else []

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{messages}")
    ])

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt
    )

    state = {"messages": query}
    response = agent.invoke(state)

    messages = response.get("messages", [])
    for m in reversed(messages):
        if isinstance(m, AIMessage) and m.content:
            return m.content
    return "⚠️ No AI response found"


# Example usage
query = "Tell me about concerts that are going to happen in india in 2025"
result = get_response_from_ai_agent(
    llm_id="llama-3.3-70b-versatile",
    query=query,
    allow_search=True,
    system_prompt="Act as a friendly AI chatbot",
    provider="Groq"
)

print("✅ AI Answer:", result)

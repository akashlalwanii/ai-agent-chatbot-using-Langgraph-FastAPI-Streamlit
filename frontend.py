#  step1: setup UI with streamlit (model provider, model, system prompt,websearch, query)
import streamlit as st

st.set_page_config(page_title = "Langgraph Agent UI",layout = "centered")
st.title("AI Chatbot Agents")
st.write("Create & Interact with AI Agents!")  #will show as a description

system_prompt = st.text_area("Define your AI Agent: ", height = 70, placeholder = "Type your system prompt here.")
# the above line will give the character or role to our agent

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Provider:", ("Groq","OpenAI"))

if provider == 'Groq':
    selected_model = st.selectbox("Select Groq Model: ", MODEL_NAMES_GROQ)
elif provider == 'OpenAI':
    selected_model = st.selectbox('Select OpenAI Model: ', MODEL_NAMES_OPENAI) 

allow_web_search = st.checkbox("Allow Web Search")


user_query = st.text_area("Enter your query: ", height = 150, placeholder = "Ask Anything!")

API_URL = "http://127.0.0.1:9999/chat"     #http local pr jo chat end point hai udhar request bejhkr usse interact krna hai
if st.button("Ask Agent!"):
    if user_query.strip():
        # step2: Connect with backend via URL
        import requests

        payload = {    "model_name" : selected_model,
                        "model_provider" : provider,
                        "system_prompt" : system_prompt,
                        "messages" :  [user_query],
                        "allow_search": allow_web_search 
                  }
        
        response =requests.post(API_URL,json=payload)
        #get response from backend and store here
        if response.status_code == 200:
            response_data = response.json()
          

            if "error" in response_data:
                st.error(response_data["error"])
            else:         
                st.subheader("Agent Response")
                st.markdown(f"**Final Response:** {response_data['answer'] if isinstance(response_data, dict) else response_data}")
        else:
            st.error(f"Backend error: {response.status_code}")
                

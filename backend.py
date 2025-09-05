# STEP 1: SETUP PYDANTIC MODEL (SCHEMA VALIDATION)

from pydantic import BaseModel
from typing import List
#typing is an inbuilt library 

# below is data contract or pydantic model 
class RequestState(BaseModel):
    model_name : str
    model_provider : str
    system_prompt : str
    messages : List[str] 
    allow_search: bool


# STEP 2: SETUP AI AGENT FROM FRONT END REQUEST
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

ALLOWED_MODELS_NAMES = ["gpt-4o-mini","llama-3.3-70b-versatile"]

app = FastAPI(title="Langgraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    try:
        if request.model_name not in ALLOWED_MODELS_NAMES:
            return {"error": "Invalid Model Name. Kindly select a valid AI model"}
        
        response = get_response_from_ai_agent(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt,
            request.model_provider
        )

        return {"answer": response}
    except Exception as e:
        # log error in console + return JSON
        print("❌ Backend Exception:", str(e))
        return {"error": f"Backend crashed: {str(e)}"}


# Step 3: RUN APP AND EXPLORE SWAGGER UI DOCS
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host ="127.0.0.1",port = 9999)


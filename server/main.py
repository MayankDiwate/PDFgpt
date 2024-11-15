from endpoints import upload, ask_question
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from env import CLIENT_URL

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],        
)

@app.get('/')
def root():
    return {"status": "API is running"}

# Register the routers
app.include_router(upload.router, tags=["upload"])
app.include_router(ask_question.router, tags=["ask_question"])


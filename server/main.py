from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import upload, ask_question
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5175",
    "https://pdf-gpt-client.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173"
]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


from fastapi import APIRouter
from .endpoints import upload_pdf, ask_question

app_router = APIRouter()

# Route for /upload
app_router.post("/upload")(upload_pdf)

# Route for /ask
app_router.post("/ask")(ask_question)
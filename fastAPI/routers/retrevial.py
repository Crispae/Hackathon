from fastapi import APIRouter
from fastAPI.models.retrevial import RetrevialRequest, RetrevialResponse
from fastAPI.services.faiss_db import DenseSearchFAISS
import os
from dotenv import load_dotenv

load_dotenv()

retrevial_router = APIRouter()
PIXTRAL_API_KEY = os.getenv("MIXTRAL_API_KEY")


## Instansiating the reterival database
db = DenseSearchFAISS(
    embedding_model="mistral-embed",
    api_key=PIXTRAL_API_KEY,
    dimension=1024,
    base_path=r"C:\Users\saurav\OneDrive - URV\Escritorio\Hackathon\images",
    prefix="fashion_image",
    suffix="jpg",
)


@retrevial_router.post("/retrevial", response_model=RetrevialResponse)
async def retrevial(query: RetrevialRequest):
    request_data = query.model_dump()

    ## Exract prompt
    prompt = request_data.get("prompt")

    ## Search in the database
    response = db.search(query=prompt, k=30, encoded=True)

    return {"response": response}

from fastapi import APIRouter
from fastAPI.models.completition import CompletitionRequest, CompletitionResponse
from fastAPI.services.pix import Pixtral
import os
from dotenv import load_dotenv


load_dotenv()


completition_router = APIRouter()


PIXTRAL_API_KEY = os.getenv("MIXTRAL_API_KEY")
MODEL_NAME = "pixtral-12b-2409"

PISTRAL_MODEL = Pixtral(api_key=PIXTRAL_API_KEY, model_name=MODEL_NAME)


@completition_router.post("/completition", response_model=CompletitionResponse)
async def completition(prompt: CompletitionRequest):
    """
    Handles the completion of description of provided image for similarity ranking

    """
    request_data = prompt.model_dump()

    prompt = request_data.get("prompt")
    image_encoding = request_data.get("image_encoding")

    response = PISTRAL_MODEL.complete(
        prompt=prompt, image_path=None, image_base46_encoding=image_encoding
    )

    ## Just send the message from response

    response = response.dict()["choices"][0]["message"]

    return {"response": response}

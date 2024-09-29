from pydantic import BaseModel
from typing import Dict, Optional


class CompletitionRequest(BaseModel):
    """

    Handles the generation of description of provided image for similarity ranking


    """

    prompt: str
    image_encoding: str


class CompletitionResponse(BaseModel):
    response: Optional[Dict]  # Dict, or change according to what response should be

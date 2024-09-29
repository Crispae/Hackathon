from pydantic import BaseModel
from typing import List, Any, Dict


class RetrevialRequest(BaseModel):
    prompt: str


class RetrevialResponse(BaseModel):
    response: List[Dict[str, Any]]

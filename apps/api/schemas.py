from pydantic import BaseModel, Field


class SentimentRequest(BaseModel):
    text: str = Field(..., example="This movie was fantastic!")


class SentimentResponse(BaseModel):
    label: str
    confidence: float
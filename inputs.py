from typing import List

from pydantic import BaseModel, Field, validator, HttpUrl


class NewTransaction(BaseModel):
    sender: str = Field(..., max_length=1024, min_length=1)
    recipient: str = Field(..., max_length=1024, min_length=1)
    amount: int = Field(..., ge=1)

    @validator('sender', 'recipient')
    def validate_sender(cls, value):
        if value == '0':
            raise ValueError("You can't use this sender/recipient identifier")
        return value


class NewNodes(BaseModel):
    nodes: List[HttpUrl]

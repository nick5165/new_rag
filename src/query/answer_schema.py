from pydantic import BaseModel, Field
from typing import List, Optional

class Articles(BaseModel):
    article: str = Field(
        ...,
        description = 'A quote of an article from the Labour Code of the Russian Federation in Russian.'
    )
    explanation: str = Field(
        ...,
        description = 'A simple explanation of the content of the article in Russian.'
    )
    subparagraphs: str = Field(
        ...,
        description = 'List of subparagraphs of the article in Russian if any.'
    )

class Topic(BaseModel):
    topic: str = Field(
        ...,
        description = 'A labor law topic relevant to the user’s query in Russian.'
    )
    description: str = Field(
        ...,
        description = 'A short description of a topic from labor law in Russian'
    )
    laws: List[Articles] = Field(
        ...,
        description = "A list of articles related to the user's query."
    )
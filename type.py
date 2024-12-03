from typing import TypedDict

class Paper(TypedDict):
    title: str
    link: str
    description: str
    tags: list[str]



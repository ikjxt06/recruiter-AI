from pydantic import BaseModel


class JobDescriptionCreate(BaseModel):
    title: str
    description: str


class JobDescriptionRead(BaseModel):
    id: int
    title: str
    description: str
    required_skills: list[str]
    preferred_skills: list[str]
    experience_requirements: dict

    class Config:
        from_attributes = True

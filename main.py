from typing import List

from fastapi import FastAPI, Form
from pydantic import BaseModel, computed_field, Field, ConfigDict, HttpUrl
import uuid

app = FastAPI()


class Photo(BaseModel):
    url: HttpUrl

class Starship(BaseModel):
    id: str = Field(default_factory=lambda: f"schorle-{uuid.uuid4()}", exclude=True)
    name: str
    price: float
    discount: float | None
    photo: List[Photo | None]
    model_config = ConfigDict(json_schema_extra={
            "example": {
                "name": "X-wing",
                "price": 100000,
                "discount": 10
            }
        })
    @computed_field
    @property
    def total(self) -> float:
        return self.price - (self.price * self.discount / 100)
class Jedi(BaseModel):
    id: str = Field(default_factory=lambda: f"schorle-{uuid.uuid4()}", exclude=True)
    name: str
    home_world: str
    model_config = ConfigDict(json_schema_extra={
            "example": {
                "name": "Luke Skywalker",
                "home_world": "Tatooine"
            }
        })

@app.post("/addStarship")
async def add_starship(starship: Starship):
    return {
        "starship_id": starship.id,
        "starship": starship
    }

@app.post("/purchase")
async def purchase(starship: Starship, jedi: Jedi):
    return {
        "starship": starship,
        "jedi": jedi
    }

@app.post("/signin")
def login(email:str = Form(...), password: str = Form(...)):
    return {"email": email}

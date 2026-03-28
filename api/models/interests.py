from pydantic import BaseModel, Field
from typing import List, Optional

class Food(BaseModel):
    dietary_restrictions: List[str] = Field(default_factory=list, description="e.g. Vegetarian, Keto, Gluten-Free or allergies")
    favorite_cuisines: List[str] = Field(default_factory=list, description="e.g. Italian, Thai, Vegan")
    going_out: Optional[str] = Field(None, description="How often they eat out or order in")
    cooking: Optional[str] = Field(None, description="Whether they like to cook and what they like to make")

class Sports(BaseModel):
    active_sports: List[str] = Field(default_factory=list, description="Sports the user actually plays")
    spectator_sports: List[str] = Field(default_factory=list, description="Teams or leagues they watch")

class Music(BaseModel):
    genres: List[str] = Field(default_factory=list)
    instruments: List[str] = Field(default_factory=list, description="Instruments the user plays")

class Movies(BaseModel):
    genres: List[str] = Field(default_factory=list)
    favorite_films: List[str] = Field(default_factory=list)
    movie_enthusiast: Optional[str] = Field(None, description="Whether they consider themselves a movie buff or casual viewer")

class Fitness(BaseModel):
    activities: List[str] = Field(default_factory=list, description="e.g. CrossFit, Yoga, Running")
    frequency: Optional[str] = Field(None, description="How often they exercise")

class Travel(BaseModel):
    destinations: List[str] = Field(default_factory=list, description="Places visited or bucket list")
    style: Optional[str] = Field(None, description="e.g. Backpacking, Luxury, Solo")

class Art(BaseModel):
    creating: List[str] = Field(default_factory=list, description="Types of art they create, if any")
    appreciating: List[str] = Field(default_factory=list, description="Types of art they enjoy")

class Interests(BaseModel):
    food: Optional[Food] = None
    sports: Optional[Sports] = None
    music: Optional[Music] = None
    movies: Optional[Movies] = None
    fitness: Optional[Fitness] = None
    travel: Optional[Travel] = None
    art: Optional[Art] = None
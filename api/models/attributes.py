from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class LoveLanguage(str, Enum):
    ACTS = "Acts of Service"
    GIFT = "Receiving Gifts"
    QUALITY = "Quality Time"
    WORDS = "Words of Affirmation"
    TOUCH = "Physical Touch"
    OTHER = "Other"

class Mbti(str, Enum):
    ISTJ = "ISTJ"
    ISFJ = "ISFJ"
    INFJ = "INFJ"
    INTJ = "INTJ"
    ISTP = "ISTP"
    ISFP = "ISFP"
    INFP = "INFP"
    INTP = "INTP"
    ESTP = "ESTP"
    ESFP = "ESFP"
    ENFP = "ENFP"
    ENTP = "ENTP"
    ESTJ = "ESTJ"
    ESFJ = "ESFJ"
    ENFJ = "ENFJ"
    ENTJ = "ENTJ"
    OTHER = "Other"

class AstrologicalSign(str, Enum):
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"
    UNKNOWN = "Unknown"


class Background(BaseModel):
    education: Optional[str] = Field(None, description="User's education background")
    work: Optional[str] = Field(None, description="User's work background")
    culture: Optional[str] = Field(None, description="User's cultural background")
    lived_in: Optional[str] = Field(None, description="Places the user has lived in")
    religion: Optional[str] = Field(None, description="User's religious beliefs")
    family: Optional[str] = Field(None, description="User's family background")

class Lifestyle(BaseModel):
    daily_routine: Optional[str] = Field(None, description="User's daily routine")
    personality_type: Optional[str] = Field(None, description="User's personality type")
    political_views: Optional[str] = Field(None, description="User's political views")
    active_lifestyle: Optional[str] = Field(None, description="User's level of physical activity")
    social_life: Optional[str] = Field(None, description="User's social life and what they like to do with friends")

class Personality(BaseModel):
    traits: Optional[str] = Field(None, description="User's personality traits")
    love_language: Optional[List[LoveLanguage]] = Field(None, description="User's love languages, up to 2")
    communication_style: Optional[str] = Field(None, description="User's communication style")
    humor: Optional[str] = Field(None, description="User's sense of humor")
    values: Optional[str] = Field(None, description="User's core values")
    mbti: Optional[Mbti] = Field(None, description="User's MBTI personality type")
    astrology: Optional[AstrologicalSign] = Field(None, description="User's astrological sign")
    @field_validator('love_languages')
    @classmethod
    def limit_languages(cls, v: List[LoveLanguage]) -> List[LoveLanguage]:
        if len(v) > 2:
            raise ValueError('Please provide no more than 2 love languages')
        return v


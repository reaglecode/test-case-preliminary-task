from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, ValidationError, field_validator, ConfigDict, confloat

from typing import Optional
from datetime import date

from .const import TABLE_NAME

# Define the base model class
Base = declarative_base()


# Define the model
class VantaaOpenApplications(Base):
    # TODO: do we need testing for this?
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    field = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    job_key = Column(String, nullable=False)
    address = Column(String, nullable=False)
    longitude_wgs84 = Column(Float, nullable=False)
    latitude_wgs84 = Column(Float, nullable=False)
    application_end_date = Column(Date, nullable=True)
    link = Column(String, nullable=False)


class OpenApplication(BaseModel):
    model_config = ConfigDict(extra='ignore')  # this is for the columns received but we are not storing them in the database.

    id: int
    ammattiala: str
    tyotehtava: str
    tyoavain: str
    osoite: str
    # These constraints are to make sure data is at least within bounding box of Vantaa
    x: confloat(gt=24.7462358484138747, lt=25.1930682902584984, strict=True)
    y: confloat(gt=60.2372175528625178, lt=60.4012548544924215, strict=True)
    haku_paattyy_pvm: Optional[date]
    linkki: str

    @field_validator('haku_paattyy_pvm', mode='before')
    def validate_date(cls, val):
        if isinstance(val, str):
            try:
                parsed_date = date.fromisoformat(val)
                return parsed_date
            except ValueError:
                raise ValidationError(
                    f"'{val}' is not a valid date. Please provide a date in ISO format."
                )
        if val is None:
            return None
        else:
            raise ValueError(f"Input must be either a date object or a valid date string, got {type(val)} instead.")

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class MotionContext(StrEnum):
    UNSET = "0"
    SEDENTARY = "1"
    ACTIVE = "2"


class HealthData(BaseModel):
    type: str = Field(
        alias="type",
        title="Type",
        description="Type of health data",
        examples=["HKQuantityTypeIdentifierHeartRate"],
    )
    source_name: str = Field(
        alias="sourceName",
        title="Source Name",
        description="Name of the source",
        examples=["Apple Watch"],
    )
    source_version: str | None = Field(
        default=None,
        alias="sourceVersion",
        title="Source Version",
        description="Version of the source",
        examples=[None, "10.2", "11.0.1"],
    )
    unit: str = Field(
        alias="unit",
        title="Unit",
        description="Unit of the health data",
        examples=["count/min", "kcal", "%"],
    )
    creation_date: datetime = Field(
        alias="creationDate",
        title="Creation Date",
        description="Date of creation",
        examples=["2021-01-01 00:00:00 +0200"],
    )
    start_date: datetime = Field(
        alias="startDate",
        title="Start Date",
        description="Date of measurement start",
        examples=["2021-01-01 00:00:00 +0200"],
    )
    end_date: datetime = Field(
        alias="endDate",
        title="End Date",
        description="Date of measurement end",
        examples=["2021-01-01 00:00:00 +0200"],
    )
    value: int | float = Field(
        alias="value",
        title="Value",
        description="Value of the health data",
        examples=[60, 120, 15.5],
    )

    @field_validator("creation_date", "start_date", "end_date", mode="before")
    @classmethod
    def check_date(cls, v: str) -> datetime:
        return datetime.strptime(v, "%Y-%m-%d %H:%M:%S %z")

    @field_validator("value", mode="before")
    @classmethod
    def str_to_numeric(cls, v) -> int | float:
        if type(v) is str:
            try:
                return int(v)
            except ValueError:
                return float(v)
        return v


class HeartRateData(HealthData):
    device: str = Field(title="Device", description="Device used for measurement")
    motion_context: str = Field(
        alias="motionContext",
        title="Motion Context",
        description="Context of motion (e.g. sedentary, active, unset)",
        examples=["Unset", "Sedentary", "Active"],
    )

    @field_validator("motion_context", mode="before")
    @classmethod
    def check_motion_context(cls, v: str) -> str:
        return MotionContext(v).name.lower().capitalize()

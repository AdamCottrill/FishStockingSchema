from typing import Annotated, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, BeforeValidator





def StockingEventFactory(AgencyEnum,
LakeEnum,
StateProvinceEnum,
StatDistEnum,
Grid10Enum,
StockingMethodEnum,
SpcEnum,
StrainEnum,
LifeStageEnum,
ClipEnum,
MarkEnum,
TagTypeEnum,
MortalityEnum,
HatcheryEnum
):
    """A factory function that returns a pydantic validator/scheam for
    StockingEvent Records using the current lookup values."""



    class StockingEvent(BaseModel):

        stocking_id: Optional[int] = Field(alias="GLFSD_Stock_ID")
        agency_stocking_id: Optional[str] = Field(alias="Your_Agency_Stock_ID",  coerce_numbers_to_str=True)
        agency: AgencyEnum = Field(alias="AGENCY")
        lake: LakeEnum = Field(alias="LAKE")
        state_province: StateProvinceEnum = Field(alias="STATE_PROV")
        stat_dist: StatDistEnum = Field(alias="STAT_DIST")
        ls_management: Optional[str] = Field(alias="LS_MGMT")
        grid10: Grid10Enum = Field(alias="GRID_10MIN", coerce_numbers_to_str=True)
        location_primary: str = Field(alias="LOCATION_PRIMARY")
        location_secondary: str = Field(alias="LOCATION_SECONDARY")
        latitude: float = Field(alias="LATITUDE")
        longitude: float = Field(alias="LONGITUDE")
        year: int = Field(alias="YEAR")
        month: int = Field(alias="MONTH", ge=1, le=12)
        day: int = Field(alias="DAY", ge=1, le=31)
        stock_method: StockingMethodEnum = Field(alias="STOCK_METHOD")
        species: SpcEnum = Field(alias="SPECIES")
        strain: StrainEnum = Field(alias="STRAIN")
        year_class: int = Field(alias="YEAR-CLASS")
        life_stage: LifeStageEnum = Field(alias="LIFE_STAGE")
        age_months: int = Field(alias="AGE_MONTHS", ge=0)
        clipc: str = Field(alias="CLIP")
        clip_efficiency: Optional[float] = Field(alias="CLIP_EFFICIENCY", ge=0, le=100)
        physchem_mark: Optional[str] = Field(alias="PHYS-CHEM_MARK")
        tag_type: Optional[TagTypeEnum] = Field(alias="TAG_TYPE")
        cwt_number: Optional[str] = Field(alias="CWT_Number")
        tag_retention: Optional[float] = Field(alias="TAG_RETENTION", ge=0, le=100)
        mean_length_mm: Optional[float] = Field(alias="MEAN_LENGTH_MM", ge=1)
        total_weight: Optional[float] = Field(alias="TOTAL_WEIGHT_KG", ge=0.1)
        stocking_mortality: MortalityEnum = Field(alias="STOCKING_MORTALITY")
        lot_code: Optional[str] = Field(alias="LOT_CODE", coerce_numbers_to_str=True)
        hatchery: HatcheryEnum = Field(alias="HATCHERY")
        number_stocked: int = Field(alias="NUMBER_STOCKED", ge=1)
        notes: Optional[str] = Field(alias="NOTES")


    return StockingEvent

# ensure that yyyy-mm-dd is a valid date (e.g. not April 31)

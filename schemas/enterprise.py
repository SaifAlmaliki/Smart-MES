from pydantic import BaseModel, Field
from typing import Optional

# Enterprise Schema
class EnterpriseBase(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the enterprise")
    disabled: bool = Field(default=False, description="Indicates if the enterprise is disabled")

class EnterpriseCreate(EnterpriseBase):
    pass

class EnterpriseUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    disabled: Optional[bool] = Field(None)

class EnterpriseOut(EnterpriseBase):
    id: int = Field(..., description="ID of the enterprise")

    class Config:
        orm_mode = True


# Site Schema
class SiteBase(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the site")
    parent_id: int = Field(..., description="ID of the parent enterprise", alias="enterprise_id")
    disabled: bool = Field(default=False, description="Indicates if the site is disabled")

class SiteCreate(SiteBase):
    class Config:
        allow_population_by_field_name = True

class SiteUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    parent_id: Optional[int] = Field(None, description="ID of the parent enterprise", alias="enterprise_id")
    disabled: Optional[bool] = Field(None)

    class Config:
        allow_population_by_field_name = True

class SiteOut(SiteBase):
    id: int = Field(..., description="ID of the site")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# Area Schema
class AreaBase(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the area")
    parent_id: int = Field(..., description="ID of the parent site", alias="site_id")
    disabled: bool = Field(default=False, description="Indicates if the area is disabled")

class AreaCreate(AreaBase):
    class Config:
        allow_population_by_field_name = True

class AreaUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    parent_id: Optional[int] = Field(None, description="ID of the parent site", alias="site_id")
    disabled: Optional[bool] = Field(None)

    class Config:
        allow_population_by_field_name = True

class AreaOut(AreaBase):
    id: int = Field(..., description="ID of the area")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# Line Schema
class LineBase(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the production line")
    parent_id: int = Field(..., description="ID of the parent area", alias="area_id")
    disabled: bool = Field(default=False, description="Indicates if the line is disabled")

class LineCreate(LineBase):
    class Config:
        allow_population_by_field_name = True

class LineUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    parent_id: Optional[int] = Field(None, description="ID of the parent area", alias="area_id")
    disabled: Optional[bool] = Field(None)

    class Config:
        allow_population_by_field_name = True

class LineOut(LineBase):
    id: int = Field(..., description="ID of the production line")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# Cell Schema
class CellBase(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the cell")
    parent_id: int = Field(..., description="ID of the parent line", alias="line_id")
    disabled: bool = Field(default=False, description="Indicates if the cell is disabled")

class CellCreate(CellBase):
    class Config:
        allow_population_by_field_name = True

class CellUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    parent_id: Optional[int] = Field(None, description="ID of the parent line", alias="line_id")
    disabled: Optional[bool] = Field(None)

    class Config:
        allow_population_by_field_name = True

class CellOut(CellBase):
    id: int = Field(..., description="ID of the cell")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

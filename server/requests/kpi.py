from pydantic import BaseModel, validator
from typing import List
from .helper import check_string_helper, check_float_helper


class KpiRequest(BaseModel):
    id: str
    name: str
    value: float
    symbol: str
    executive_staff: List[str] | str
    lower_bound: float
    upper_bound: float

    @validator('id')
    def check_string_id(cls, value):
        return check_string_helper(value=value, error_message='Id must be string')

    @validator('name')
    def check_string_name(cls, value):
        return check_string_helper(value=value, error_message='Name must be string')

    @validator('value')
    def check_float_value(cls, value):
        return check_float_helper(value=value, error_message='Value must be float')

    @validator('symbol')
    def check_string_symbol(cls, value):
        return check_string_helper(value=value, error_message='Symbol must be float')

    @validator('lower_bound')
    def check_float_lower_bound(cls, value):
        return check_float_helper(value=value, error_message='Lower bound must be float')

    @validator('upper_bound')
    def check_float_upper_bound(cls, value):
        return check_float_helper(value=value, error_message='Upper bound must be float')

    @validator("executive_staff")
    def validate_executive_staff(cls, v):
        if isinstance(v, str):
            v = [v]
        if not all(isinstance(item, str) for item in v):
            raise ValueError(
                "executive_staff must contain only strings or a single string")
        return v


class KpiConditionRequest(BaseModel):
    id: str
    post_condition: List[str]

    @validator('post_condition', each_item=True)
    def check_string_post_condition(cls, value):
        return check_string_helper(
            value=value, error_message='All items in post_condition must be strings')

    @validator('id')
    def check_string_id(cls, value):
        return check_string_helper(value=value, error_message='Id must be string')

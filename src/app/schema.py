from typing import List

from pydantic import BaseModel, validator

from .models import DataVector
from .services import get_column_distincts

VECTORS_ITEMS_ATTRS = ("date_", "val_", "type_")


class VectorDataItem(BaseModel):
    date: str
    value: float


class VectorData(BaseModel):
    datatype_x: str
    datatype_y: str
    dataset_x: List[VectorDataItem]
    dataset_y: List[VectorDataItem]

    def _make_dicts(self, datatype, type_name):
        item_cols = [attr + type_name for attr in VECTORS_ITEMS_ATTRS]
        result = []
        for item in self.dataset_x:
            full_vector_item = (item.date, item.value, datatype)
            vector_item_dataset = dict(zip(item_cols, full_vector_item))
            result.append(vector_item_dataset)
        return result

    def to_dicts(self):
        dicts_x = self._make_dicts(self.datatype_x, "x")
        dicts_y = self._make_dicts(self.datatype_y, "y")
        return dicts_x, dicts_y


class VectorRecord(BaseModel):
    user_id: int
    data: VectorData


class Correlation(BaseModel):
    value: float
    p_value: float


class VectorFromRequest(BaseModel):
    user_id: int
    datatype_x: str
    datatype_y: str

    @validator("user_id")
    def validate_user_id(cls, new_user_id):
        unique_user_ids = get_column_distincts(DataVector.user_id)
        if new_user_id not in unique_user_ids:
            raise ValueError(f"User with {new_user_id} doesn't exists!")
        return new_user_id

    @validator("datatype_x", "datatype_y")
    def validate_datatype(cls, new_datatype):
        unique_datatypes_x = get_column_distincts(DataVector.datatype_x)
        unique_datatypes_y = get_column_distincts(DataVector.datatype_y)
        unique_datatypes = tuple(unique_datatypes_y) + tuple(unique_datatypes_x)

        if new_datatype not in unique_datatypes:
            raise ValueError(f"Datatype '{new_datatype} doesn't exists!")

        return new_datatype


class VectorDBReturn(BaseModel):
    user_id: int
    datatype_x: str
    datatype_y: str
    correlation: Correlation

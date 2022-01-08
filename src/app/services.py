from itertools import chain

import pandas as pd
from scipy import stats
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from .config import DB_URL
from .models import DataVector

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


def find_correlation(x, y, date_for_filter, round_to: int = 2):
    dataset_x, dataset_y = pd.DataFrame(x), pd.DataFrame(y)
    full_dataset = pd.concat([dataset_x, dataset_y], axis=1)

    date_mask_x = full_dataset["date_x"] == date_for_filter
    date_mask_y = full_dataset["date_y"] == date_for_filter
    by_date = full_dataset[date_mask_x & date_mask_y]

    datax, datay = by_date["val_x"], by_date["val_y"]
    correlation, p_value = stats.pearsonr(datax, datay)

    rounded_correlation = round(correlation, round_to)
    rounded_p_value = round(p_value, round_to)
    return rounded_correlation, rounded_p_value


def save_vectors_correlation(data_vector):
    with Session() as session:
        session.add(data_vector)
        session.commit()


def get_correlation(user_id, datatype_x, datatype_y):
    and_filter = and_(*[
        DataVector.user_id == user_id,
        DataVector.datatype_x == datatype_x,
        DataVector.datatype_y == datatype_y
    ])

    with Session() as session:
        return session.query(DataVector).filter(and_filter)[-1]


def get_column_distincts(columns, return_whole=True):
    with Session() as session:
        column_distincts = session.query(columns).distinct()

    if not return_whole:
        return column_distincts
    return chain.from_iterable(column_distincts)

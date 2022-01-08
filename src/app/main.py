from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .models import DataVector
from .schema import VectorRecord, Correlation, VectorDBReturn, VectorFromRequest
from .services import find_correlation, save_vectors_correlation, get_correlation

app = FastAPI()


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exception: ValueError):
    why_fail = exception.errors()[0].get('msg', '')
    return JSONResponse(status_code=400, content={"message": why_fail})


@app.on_event("shutdown")
def some():
    pass


@app.get("/test")
def test():
    return {"msg": "ok"}


@app.post("/calculate")
def compute_correlation(vectors_record: VectorRecord, filter_date: str):
    xs, ys = vectors_record.data.to_dicts()
    correlation, p_value = find_correlation(x=xs, y=ys, date_for_filter=filter_date)

    vector = DataVector(
        user_id=vectors_record.user_id,
        datatype_x=vectors_record.data.datatype_x,
        datatype_y=vectors_record.data.datatype_y,
        by_date_computed=filter_date,
        correlation_value=correlation,
        p_value=p_value
    )
    save_vectors_correlation(vector)

    return {
        "msg": "Data has been saved successfully!",
        "corr": {"corr": correlation, 'p_val': p_value},
    }


@app.get("/correlation")
def get_vector_correlation(user_id: int, datatype_x: str, datatype_y: str):
    vector_request = VectorFromRequest(user_id=user_id, datatype_x=datatype_x, datatype_y=datatype_y)

    correlation_db = get_correlation(
        user_id=vector_request.user_id,
        datatype_x=vector_request.datatype_x,
        datatype_y=vector_request.datatype_y
    )

    vector_to_return = VectorDBReturn(
        user_id=correlation_db.user_id,
        datatype_x=correlation_db.datatype_x,
        datatype_y=correlation_db.datatype_y,
        correlation=Correlation(
            value=correlation_db.correlation_value,
            p_value=correlation_db.p_value
        )

    )

    return vector_to_return

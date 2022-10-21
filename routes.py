from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Kimono, KimonoDTO

router = APIRouter()

@router.get("/", response_description="List all kimonos", response_model=List[Kimono])
def list_books(request: Request):
    kimonos = list(request.app.database["kimonos"].find(limit=100))
    return kimonos

# @router.get("/{id}", response_description="Get a single book by id", response_model=Book)
# def find_book(id: str, request: Request):
#     if (book := request.app.database["books"].find_one({"_id": id})) is not None:
#         return book
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

@router.post("/", response_description="Create a new kimono", status_code=status.HTTP_201_CREATED, response_model=Kimono)
def create_kimono(request: Request, kimono: Kimono = Body(...)):
    kimono = jsonable_encoder(kimono)
    new_kimono = request.app.database["kimonos"].insert_one(kimono)
    created_kimono = request.app.database["kimonos"].find_one(
        {"_id": new_kimono.inserted_id}
    )

    return created_kimono
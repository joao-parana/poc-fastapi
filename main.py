from datetime import datetime
import logging as logger
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Shape(BaseModel):
    item_name: str
    no_of_sides: int
    id: int

shapes = [
    {"item_name": "Triangle", "no_of_sides": 3, "id": 1},
    {"item_name": "Square", "no_of_sides": 4, "id": 2}
]

logger.basicConfig(
    filename='mylog.log', encoding='utf-8', level=logger.INFO)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print('Shape list:', shapes)
    logger.info("\n" + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + 
                " - Application starts")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("\n" +
                datetime.now().strftime('%d/%m/%Y %H:%M:%S') + 
                    " - Application shutdown")

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/shapes")
async def get_shapes():
    return shapes

@app.get("/shapes/{shape_id}")
async def get_shape_by_id(shape_id: int):
    for shape in shapes:
        if shape['id'] == shape_id:
            return shape
    
    # If shape doesn't exists I will throw HTTPException
    raise HTTPException(status_code=404, detail=f"No shape with id {shape_id} found")

@app.post("/shapes")
async def post_shape(shape: Shape):
    shapes.append(shape.dict())
    print('Updated list:', shapes)
    return shape

@app.put("/shapes/{shape_id}")
async def update_shape(shape_id: int, shape: Shape):
    for my_shape in shapes:
        if my_shape["id"] == shape_id:
            my_shape["item_name"] = shape.item_name
            my_shape["no_of_sides"] = shape.no_of_sides
            print('Updated list:', shapes)
            return my_shape
    raise HTTPException(status_code=404, detail=f"No shape with id {shape_id} found")


@app.put("/shapes/upsert/{shape_id}")
async def update_shape(shape_id: int, shape: Shape):
    for my_shape in shapes:
        if my_shape["id"] == shape_id:
            print('The shape already exist. I will update it !')
            my_shape["item_name"] = shape.item_name
            my_shape["no_of_sides"] = shape.no_of_sides
            print('Updated list:', shapes)
            return my_shape
            
    print('The shape doesn\'t exist. I will insert it !')
    shapes.append(shape.dict())
    print('Updated list:', shapes)
    return shape

@app.delete("/shapes/{shape_id}")
async def delete_shape(shape_id: int):
    # delete element using the command: del shapes[index]
    index: int = 0;
    for my_shape in shapes:
        if my_shape["id"] == shape_id:
            del shapes[index]
            print('Updated list:', shapes)
            return {"OK": True}
        index = index + 1
    raise HTTPException(status_code=404, 
                        detail=f"No shape with id: {shape_id} exists")

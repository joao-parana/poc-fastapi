# fastapi

## Install

```bash
pip3 install fastapi
pip3 install uvicorn
pip3 install httpie
pip3 install pydantic
```

You can see all dependencies in [requirements.txt](requirements.txt).

## Testing:

```bash
uvicorn main:app --host "0.0.0.0" --port 8000 --reload
```

In another Terminal:

```bash
http http://127.0.0.1:8000/
```

You will see something like this:

```txt
HTTP/1.1 200 OK
content-length: 25
content-type: application/json
date: Sun, 28 Aug 2022 18:06:38 GMT
server: uvicorn

{
    "message": "Hello world"
}
```

## The source code

See bellow our simple example of FastAPI App

```python
from fastapi import FastAPI, HTTPException

shapes = [
    {"item_name": "Triangle", "no_of_sides": 3, "id": 1},
    {"item_name": "Square", "no_of_sides": 4, "id": 2}
]

app = FastAPI()

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
    
    # If shape doesn't exists I will raise an HTTPException
    raise HTTPException(status_code=404, 
                        detail=f"No shape with id {shape_id} found")
```

Can be tested with HTTPie:

```bash
http http://127.0.0.1:8000/shapes/2
```

```txt
HTTP/1.1 200 OK
content-length: 45
content-type: application/json
date: Sun, 28 Aug 2022 18:51:30 GMT
server: uvicorn

{
    "id": 2,
    "item_name": "Square",
    "no_of_sides": 4
}
```

### Adding new feature (add Shape to list) using pydantic

To add one new Shape using FastAI use post HTTP method:

```python
@app.post("/shapes")
async def post_shape(shape: Shape):
    shapes.append(shape.dict())
    print('Updated list:', shapes) # for simple DEBUG
    return shape
```

But for this we need **pydantic**

```python
from pydantic import BaseModel

class Shape(BaseModel):
    name: str
    no_of_sides: int
    id: int
```

Now we can test on Swagger interface or in Terminal:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/shapes' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Hexagon",
    "no_of_sides": 6,
    "id": 9
}'
```

which returns:

```txt
{"name":"Hexagon","no_of_sides":6,"id":9}
```

and we can see in the **uvicorn** LOG:

```txt
INFO:     127.0.0.1:59374 - "POST /shapes HTTP/1.1" 200 OK
Updated list: [{'item_name': 'Triangle', 'no_of_sides': 3, 'id': 1}, {'item_name': 'Square', 'no_of_sides': 4, 'id': 2}, {'name': 'Hexagon', 'no_of_sides': 6, 'id': 9}]
INFO:     127.0.0.1:59402 - "POST /shapes HTTP/1.1" 200 OK
```

The **HTTPie** makes it easy to add Shape objects using the POST HTTP method.

```bash
http post 127.0.0.1:8000/shapes item_name=Octogan no_of_sides=8 id=15
```

```txt
HTTP/1.1 200 OK
content-length: 47
content-type: application/json
date: Sun, 28 Aug 2022 21:06:42 GMT
server: uvicorn

{
    "id": 15,
    "item_name": "Octogan",
    "no_of_sides": 8
}
```

### PUT and DELETE

See [https://realpython.com/lessons/fastapi-put-delete-requests/](https://realpython.com/lessons/fastapi-put-delete-requests/) for example.

The PUT method is used to Update shape

```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/shapes/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "item_name": "Triangulo",
  "no_of_sides": 3,
  "id": 1
}'
```

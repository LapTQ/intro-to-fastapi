from typing import Annotated
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from enum import Enum
import numpy as np
import cv2


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# ================== Path Parameters ==================
# Order matters
# When creating path operations, you can find situations where you have a fixed path.
# Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# By inheriting from `int` the API docs will be able to know that the values (1,2,3) must be of type int and will be able to render correctly.
class Color(int, Enum):
    r = 1
    g = 2
    b = 3

@app.get("/color/{color}") # insert the color code here (hmm :-/ ...)
async def get_color(color: Color):
    if color is Color.r:
        return {"color_name": color.name, "message": "Red here"}

    if color.value == 2:
        return {"color_name": color.name, "message": "Green here"}

    return {"color_name": color.name, "message": "Blue here"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
# so you would need a leading `/` in the path: http://127.0.0.1:8000/files//hello/world.txt


# ================== Query Parameters ==================
# When you declare other function parameters that are not part of the path parameters, 
# they are automatically interpreted as "query" parameters.
@app.get("/random")
async def random(min: int = 0, max: int = 10):
    return {"random_number": np.random.randint(min, max)}
# As query parameters are not a fixed part of a path, they can be optional and can have default values.

# But when you want to make a query parameter required (not optional), you can just not declare any default value:
@app.get("/random2")
async def random2(min: int, max: int = 3):
    return {"random_number": np.random.randint(min, max)}


# ================ Request Body ================
# When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.
# Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time.
class ShowRequest(BaseModel):
    url: str
    n_frames: int = 100     # optional, the same as query parameter


@app.post("/show")
async def show(show_request: ShowRequest):
    if show_request.url == '0':
        show_request.url = 0
    cap = cv2.VideoCapture(show_request.url)
    for i in range(show_request.n_frames):
        ret, frame = cap.read()
        if ret:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    return show_request

@app.post("/show/{scale}")
async def show_scale(show_request: ShowRequest, scale: float):
    # do similarly...
    request_dict = show_request.model_dump()
    request_dict.update({'scale': scale})
    return request_dict

# ================ Validate query parameters ==================
@app.get("/hello")
async def hello_query(name: Annotated[str | None, Query(max_length=10)] = None):
    return {"message": "Hello " + (name or "World")}

# ================ Validate path parameters ==================
@app.get("/choose_number/{num}")
async def choose_number(num: Annotated[int, Path(ge=10)]):
    return {"message": "You chose " + num}
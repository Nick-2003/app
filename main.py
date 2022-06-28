from fastapi import FastAPI, Response, status, HTTPException # FastAPI provides all functionality for API
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
from random import randrange

app = FastAPI() 
# Instance of class FastAPI named app; main point of interaction to create all API

# Path operation
@app.get("/login") # Decorator turns function below into path operation; method passes in HTTP method to be used
# ("/") -> Route path; path after specific domain name of API, 
                     # references path required to go to in URL to access function below
def login_user(): # Function
    return {"message": "Welcome to the API"} # Data sent back to user

@app.get("/") 
def login_user(): # Function
    return {"message": "Greetings, mortals"}

# async def read_root(): # Only require "async" for asynchrounous tasks (e.g. Making API call)
#     return {"message": "Hello There"}

# Need to check password and database
# FastAPI will automatically convert to json

# title str, content str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # If published value is not provided, default to True
    rating: Optional[int] = None # Value is completely optional to fill in, default to None, 
                                 # and will be invalid if value is not an int

# @app.post("/create")
# def make_post(payLoad: dict = Body(...)): # Will extract all fields from given Body(...) 
#                                           # to be converted to python dictionary dict and stored 
                                            # into payLoad
#     return {"new_post": f"title: {payLoad['title']}, content: {payLoad['content']}"}

# Sample posts
my_posts = [{"title": "post1", "content": "cont1", "id": 1}, 
            {"title": "post2", "content": "cont2", "id": 2}] 
            # Array to contain posts in the form of dictionaries; includes samples

# Retrieve all posts
@app.get("/posts") 
def get_posts():
    return {"data": my_posts}

# Make new post
@app.post("/posts", status_code=status.HTTP_201_CREATED) # Status code for creating new post
def create_post(post: Post): # Reference Post pydantic model and save it as a variable new_post
    # Will display error if at least one of the categories does not fit the data type
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 9999999999999999999999999999999999999) # Need to make it such that multiple posts cannot have the same ID
    my_posts.append(post_dict) # Convert pydantic model into dictionary, then add to my_posts
    return {"data": post_dict}

# Retrieve 1 post
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# @app.get("/posts/Hello") # DO NOT PLACE ANY FORM OF @app.get("/posts/...") AFTER @app.get("/posts/{id}") , as ... will be treated as an id
# def get_posts():
#     return {"Hello"}

@app.get("/posts/{id}") 
def get_post(id: int, response: Response): # Validation on id being an integer; will give 422 error if fail
    post = find_post(id) 
    # find_post(id) will have an id in the form of a string without get_post(id: int), 
    # would need to use post = find_post(int(id))
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with ID {id} was not found") # Gives both 404 and message
        # response.status_code = status.HTTP_404_NOT_FOUND 
        # return {"message": f"Post with ID {id} was not found"}
    return {"post_detail": post}

# Delete post
def find_index_post(id):
    for i, p in enumerate(my_posts):
         if p["id"] == id:
             return i

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id) # Find index in array with required ID
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with ID {id} was not found")
    my_posts.pop(index)
    return {"message": "Post deleted"}

# Update post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id) # Find index in array with required ID
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with ID {id} was not found")
    post_dict = post.dict()
    post_dict["id"] = id # Same ID
    my_posts[index] = post_dict # Replace old post with new one
    return {"data": post_dict}


from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from .. database import engine, get_db

# app = FastAPI()
router = APIRouter(prefix='/posts',
                   tags=['Posts'])
# class Test(BaseModel):
#     user_id: str
#     name: str
#     marks: int
    
@router.get('/', response_model=List[schemas.Post])
# def get_posts(data:Test):
def get_posts(db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, search:Optional[str]= ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts =cursor.fetchall()
    # print(type(posts))
    print(f"{current_user.id=}")
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    print(f"{current_user}")
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()


# def find_post(id):
#     for p in my_posts:
#         if p["id"]==id:
#             return p

# @router.get('/posts/latest')
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]  # Safely access the last post
#     return {"post detail": post}

@router.get('/{id}')
def get_post(id:int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    post = db.query(models.Post).filter(models.Post.id==id).first() #finds the matching post then return it
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with {id} not found")
    return {"message": post}
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    # test_post = cursor.fetchone()
    # if not test_post:
    #     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
    #                         detail= f"post with {id} not found")
    # print(test_post)
    # return test_post
    
    
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
    #                         detail= f"post with {id} not found")
        
    # return {"post detail": post}
    
    # post = db.query(models.Post).filter(models.Post.id==id).all()   #will keep finding posts with same id even if one post with that id is found

# def find_post_index(id):
#     for index, p in enumerate(my_posts):
#         if p["id"]==id:
#             return index
        
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if deleted_post==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no index found')
    
    # return deleted_post
    
    
    # index = find_post_index(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no index found')
    # my_posts.pop(index)
    # return {"message": f"post {id} deleted successfully"}
    

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()
    return post_query.first()
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='not found post')
    # return updated_post
    
    
    # print(post)
    # index = find_post_index(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='not found post')
    # post_dict = post.model_dump()
    # print(type(post_dict))
    # print(post_dict)
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    # return  {"data": post_dict}
    
from typing import Optional

from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publishing_year: int

    def __init__(self,id,title,author,description,rating,publishing_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publishing_year = publishing_year
class BookRequest(BaseModel):
    id: Optional[int] = Field(title= 'id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1,max_length=100)
    rating: int=Field(gt=0,lt=6)
    publishing_year: int=Field(gt=1998, lt=2024)

    class Config:
        schema_extra = {
            'example': {
                'title': 'A New Book',
                'author': 'Author of this book',
                'description': "A beautiful Book",
                'rating': 5,
                'publishing_year': 2012
            }
        }


BOOKS=[
    Book(1,"That Sick Saturday Night","Arindam Halder","a great book", 4, 2011),
    Book(2,"Memory HOW TO DEVELOP", "William Walker Atkinson", "a nice book", 4, 2012),
    Book(3,"Do It Today", "Darius Foroux", "a amazing book", 5, 2014),
    Book(4,"HP1", "Author 1", "book description", 2, 2018),
    Book(5,"HP2", "Author 2", "book description", 3, 2021),
    Book(6,"HP#", "Author 3", "book description", 1, 2023)
]

def find_book_id(book: Book):
    if len(BOOKS)>0:
        book.id=BOOKS[-1].id+1
    else:
        book.id=1
    return book


@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/books_by_rating/",status_code=status.HTTP_200_OK)
async def books_by_rating(book_rating: int= Query(gt=0,lt=6)):
    books_by_rating=[]
    for book in BOOKS:
        if book.rating==book_rating:
            books_by_rating.append(book)
    return books_by_rating

@app.get("/books/books_by_publishing_year/",status_code=status.HTTP_200_OK)
async def books_by_published_year(published_year: int= Query(gt=1998, lt=2024)):
    books_to_return=[]
    for book in BOOKS:
        if book.publishing_year==published_year:
            books_to_return.append(book)
    return books_to_return
@app.post("/books/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book=Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))

@app.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    flag = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book
            flag = True
    if flag==False:
        raise HTTPException (status_code=404, detail='Item not found')
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int= Path(gt=0)):
    flag=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            flag=True
            break
    if flag==False:
        raise HTTPException (status_code=404, detail='Item not found')

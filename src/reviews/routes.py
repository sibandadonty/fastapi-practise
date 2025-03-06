from fastapi import APIRouter, Depends
from src.auth.dependencies import get_current_user
from src.books.schemas import BookDetailsModel
from src.db.models import User
from src.reviews.schemas import CreateReviewModel
from src.reviews.services import ReviewsService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session


review_router = APIRouter()
review_services = ReviewsService()

@review_router.post("/book/{book_uid}") #, response_model=BookDetailsModel)
async def create_book_review(
    book_uid: str,
    review_data: CreateReviewModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)):

    review = await review_services.create_book_review(
        current_user.email,
        book_uid,
        review_data,
        session
    )
    print("review data: ", review)
    return review



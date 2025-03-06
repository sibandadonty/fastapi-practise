import logging
from src.reviews.schemas import CreateReviewModel
from fastapi import HTTPException, status
from src.auth.services import AuthServices
from src.books.services import BookServices
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.models import Review

books_service = BookServices()
auth_service = AuthServices()

def not_found_exp(message: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message
    )

class ReviewsService:
    async def create_book_review(
            self, 
            user_email:str,
            book_uid: str,
            review_data: CreateReviewModel,
            session: AsyncSession):
        try:
            book = await books_service.get_book(book_uid, session)
            user = await auth_service.get_user_by_email(user_email, session)
       
            if not book:
                not_found_exp("Book not found")

            if not user:
                not_found_exp("User not found")

            review_data_dict = review_data.model_dump()
            
            new_review = Review(
                **review_data_dict
            )
            
            new_review.book = book
            new_review.user = user

            session.add(new_review)
            await session.commit()
            await session.refresh(new_review)
            print("new review: ", new_review)
            return new_review

        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ooops something went wrong"
            )
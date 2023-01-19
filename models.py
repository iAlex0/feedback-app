from sqlalchemy import Column,  Integer, String, Text
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    customer = Column(String(200), nullable=False, unique=True)
    dealer = Column(String(200), nullable=False)
    rating = Column(Integer, nullable=False)
    comments = Column(Text(), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from database import Base
from schemas import RoleEnum

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=False)
    password = Column(String, nullable=False)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.READER)
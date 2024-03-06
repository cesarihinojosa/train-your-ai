from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, mapped_column
from os import path

def create_database(db_name):
    engine = create_engine(f"sqlite:///database/{db_name}", echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column("user_id", Integer, primary_key=True)
    first_name = Column("first_name", String)
    last_initial = Column("last_initial", CHAR)
    grade = Column("grade", Integer)
    ai = relationship("AI", back_populates="user")

    def __init__(self, first_name, last_initial, grade):
        self.first_name = first_name
        self.last_initial = last_initial
        self.grade = grade

    def __repr__(self):
        return f"({self.id}) ({self.first_name}) ({self.last_initial}) ({self.grade})"
    
class AI(Base):
    __tablename__ = "ai"

    ai_id = Column("ai_id", Integer, primary_key=True)
    high_score = Column("high_score", Integer)
    average_score = Column("average_score", Integer) #TODO:maybe change to float
    eat_apple = Column("eat_apple", Integer)
    stay_alive = Column("stay_alive", Integer)
    dies = Column("dies", Integer)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    user = relationship("User", back_populates = "ai")

    def __init__(self, high_score, average_score, eat_apple, stay_alive, dies, user_id):
        self.high_score = high_score
        self.average_score = average_score
        self.eat_apple = eat_apple
        self.stay_alive = stay_alive
        self.dies = dies
        self.user_id = user_id
    
    def __repr__(self):
        return f"({self.ai_id}) ({self.high_score}) ({self.average_score}) ({self.eat_apple}) ({self.stay_alive}) ({self.dies}) ({self.user_id})"


User.ai = relationship("AI", order_by = AI.ai_id, back_populates = "user")
session = create_database("tyai.db")

def add_user(user): #TODO: How to handle edge case of duplicates
    session.add(user)
    session.commit()

def get_user_id(first_name, last_initial, grade):
    return session.query(User).filter(
        User.first_name.like(first_name),
        User.last_initial.like(last_initial),
        User.grade == grade
    ).first().user_id

def get_user_by_id(id):
    return User.query.get(id)

def query_all_users():
    return session.query(User).all()

def add_ai(ai):
    session.add(ai)
    session.commit()

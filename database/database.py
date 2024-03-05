from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column("user_id", Integer, primary_key=True)
    first_name = Column("first_name", String)
    last_initial = Column("last_initial", CHAR)
    grade = Column("grade", Integer)

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
    user_id = Column(Integer, ForeignKey("user.user_id"))

    def __init__(self, high_score, average_score, eat_apple, stay_alive, dies, user_id):
        self.high_score = high_score
        self.average_score = average_score
        self.eat_apple = eat_apple
        self.stay_alive = stay_alive
        self.dies = dies
        self.user_id = user_id
    
    def __repr__(self):
        return f"({self.ai_id}) ({self.high_score}) ({self.average_score}) ({self.eat_apple}) ({self.stay_alive}) ({self.dies}) ({self.user_id})"

engine = create_engine("sqlite:///database/tyai.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_user(first_name, last_initial, grade):
    user = User(first_name, last_initial, grade)
    session.add(user)
    session.commit()

def query_all_users():
    return session.query(User).all()
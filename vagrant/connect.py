from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

def connect(database):
	engine = create_engine(database)
	Base.metadata.bind=engine
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	return session
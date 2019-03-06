from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date,Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from config import DB_URL

from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

engine = create_engine(DB_URL, echo=False, connect_args={'check_same_thread':False})
Base = declarative_base()

def get_db_session(engine): 
    Session = sessionmaker(bind=engine)
    session=Session()
    return session

session=get_db_session(engine)

#create table classes 
class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return "<Country(name={}, code={},id={})>".\
        format(self.name, self.code, self.id)

class Index(Base):
    __tablename__ = 'index'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return "<Index(name={},id={})>".format(self.name, self.id)
    
class Index_value(Base):
    __tablename__ = 'index_value'
    #autoincrement is automatically set to true for a primary key
    id = Column(Integer, primary_key=True)
    value = Column(Float)
    year=Column(Integer)
    index_id = Column(Integer, ForeignKey('index.id'))
    country_id=Column(Integer, ForeignKey('country.id'))
    def __repr__(self):
        return "<Index_value(value={}, year={}, country_id={}, index_id={})>".\
        format(self.value, self.year,self.country_id, self.id)

class Indicator(Base):
    __tablename__ = 'indicator'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    index_id=Column(Integer, ForeignKey('index.id'))
    def __repr__(self):
        return "<Indicator(name={},id={})>".format(self.name, self.id)
    
class Indicator_value(Base):
    __tablename__ = 'indicator_value'
    #autoincrement is automatically set to true for a primary key
    id = Column(Integer, primary_key=True)
    value = Column(Float)
    year=Column(Integer)
    index_id = Column(Integer, ForeignKey('indicator.id'))
    country_id=Column(Integer, ForeignKey('country.id'))
    def __repr__(self):
        return "<Inicator_value(value={}, year={},country_id={}, index_id={})>".\
        format(self.name, self.id)

if __name__ == '__main__':
  Base.metadata.create_all(engine)

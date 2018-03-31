from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///sqlalchemy_example.db')
Session = sessionmaker(bind=engine)
session = Session()


class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    imdbid = Column(String(10))
    title = Column(String(100), nullable=False)
    poster = Column(String(200))
    rating = Column(Float(1))
    genre = Column(String(50))
    cast = Column(String(300))
    directors = Column(String(50))
    comments = Column(String(200))

    def __init__(self, title, imdbid='' , poster='', rating=0.0 , genre='', cast='', directors='', comments='no comments'):
        self.title = title
        self.imdbid = imdbid
        self.poster = poster
        self.rating = rating
        self.genre = genre
        self.cast = cast
        self.directors = directors
        self.comments = comments

    def __repr__(self):
        return 'Movie(title="{title}", imdbid="{imdbid}", poster="{poster}", rating={rating}, genre="{genre}",' \
               'cast="{cast}", directors="{directors}", comments="{comments}" '.format(**vars(self))

    @property
    def info(self):
        return 'Movie title: {title}, imdb ID: {imdbid}, poster: {poster}, rating:{rating}, genre: {genre}, ' \
               'cast: {cast}, directors: {directors}, comments: {comments}'.format(**vars(self))


Base.metadata.create_all(engine)

if __name__ == '__main__':
    pass
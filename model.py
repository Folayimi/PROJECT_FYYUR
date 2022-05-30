from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(), nullable=True)  
    Venue_Show = db.relationship('Show', backref="venueS", lazy=True) 
    
    def __repr__(self):
      return f'<Venue id:{self.id} name:{self.name} city:{self.city} state:{self.state} address:{self.address} phone:{self.phone} genres: {self.genres} image_link:{self.image_link} facebook_link:{self.facebook_link} website_link:{self.website_link} seeking_talent:{self.seeking_talent} seeking_description:{self.seeking_description}>'  
    

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)    
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(), nullable=False)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), nullable=True) 
    Artist_Show = db.relationship('Show', backref="artistS", lazy=True)      
    
    def __repr__(self):
      return f'<Artist id:{self.id} name:{self.name} city:{self.city} state:{self.state} phone:{self.phone} genres: {self.genres} image_link:{self.image_link} facebook_link:{self.facebook_link} website_link:{self.website_link} seeking_venue:{self.seeking_venue} seeking_description:{self.seeking_description}>'   

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
class Show(db.Model):
    __tablename__ = 'show'
    
    id = db.Column(db.Integer, primary_key=True)    
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)    
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)        
    start_time = db.Column(db.String(), nullable = False )
    
    def __repr__(self):
      return f'<Show id:{self.id} artist_id:{self.artist_id} venue_id={self.venue_id} start_time={self.start_time}>'      
    

db.create_all()
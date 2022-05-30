#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request,abort,Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from model import *
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
    

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate


#     # TODO: implement any missing fields, as a database migration using Flask-Migrate
    

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

def generate_upcoming_data(data):      
  upcoming_show =[]    
  present_time = str(datetime.today())    
  show_data = Show.query.filter_by(venue_id=data.id).all()  
  for showD in show_data:            
    if showD.start_time > present_time:
      active_Artist = Artist.query.get(showD.artist_id)
      upcomingData = {
        "artist_id":active_Artist.id,
        "artist_name":active_Artist.name,
        "artist_image_link":active_Artist.image_link,
        "start_time":showD.start_time
      }
      upcoming_show.append(upcomingData)  
  value = len(upcoming_show)
  return value


@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  venueData = Venue.query.all()
  record = []
  datas =[]        
  for data1 in venueData:    
    cities = []
    firstCity = Venue.query.filter_by( city = data1.city , state =data1.state).all()
    recordData={
      "city":data1.city,
      "state":data1.state
    }
    if recordData in record:
      break
    else:
      record.append(recordData)  
      
    value = generate_upcoming_data(data1)    
    for f in firstCity: 
      city = {
        'id':f.id,
        'name':f.name,
        'num_upcoming_shows':value
      }  
      cities.append(city)
      
    data = {
      "city":data1.city,
      "state":data1.state,
      "venues": cities}
    datas.append(data)  
  return render_template('pages/venues.html', areas=datas);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  venue_data = Venue.query.all()
  finalData =[]        
  for data in venue_data:
    past_show = []
    upcoming_show =[]
    present_show = []
    present_time = str(datetime.today())    
    show_data = Show.query.filter_by(venue_id=data.id)
    for showD in show_data:      
      if showD.start_time < present_time:
        active_Artist = Artist.query.get(showD.artist_id)
        pastData = {
          "artist_id":active_Artist.id,
          "artist_name":active_Artist.name,
          "artist_image_link":active_Artist.image_link,
          "start_time":showD.start_time
        }
        past_show.append(pastData)
      elif showD.start_time > present_time:
        active_Artist = Artist.query.get(showD.artist_id)
        upcomingData = {
          "artist_id":active_Artist.id,
          "artist_name":active_Artist.name,
          "artist_image_link":active_Artist.image_link,
          "start_time":showD.start_time
        }
        upcoming_show.append(upcomingData)
      else:
        active_Artist = Artist.query.get(showD.artist_id)
        presentData = {
          "artist_id":active_Artist.id,
          "artist_name":active_Artist.name,
          "artist_image_link":active_Artist.image_link,
          "start_time":showD.start_time
        }
        present_show.append(presentData)    
        
    dataItem ={
      "id": data.id,
      "name":data.name,
      "genres":data.genres,
      "city":data.city,
      "state":data.state,
      "phone":data.phone,
      "website":data.website_link,
      "facebook_link":data.facebook_link,
      "seeking_talent":data.seeking_talent,
      "seeking_description":data.seeking_description,
      "image_link":data.image_link,
      "past_shows": past_show,
      "upcoming_shows": upcoming_show,
      "past_shows_count": len(past_show),
      "upcoming_shows_count": len(upcoming_show),
    }
    finalData.append(dataItem)
  
  data = list(filter(lambda d: d['id'] == venue_id, finalData))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  form = VenueForm()
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  Id = Venue.query.all()
  Id_Length = len(Id)
  
  Error = False
  try:      
      new_data = Venue(
        id = Id_Length+1,
        name=form.name.data, 
        city = form.city.data,
        state = form.state.data,
        address = form.address.data,
        phone = form.phone.data,
        genres = form.genres.data,
        image_link = form.image_link.data,
        facebook_link = form.facebook_link.data,
        website_link = form.website_link.data,
        seeking_talent = form.seeking_talent.data,
        seeking_description = form.seeking_description.data
        ) 
      db.session.add(new_data)
      db.session.commit()
  except:
      Error = True
      db.session.rollback()
  finally:
      db.session.close() 
  if Error == True:      
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  else:
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
      deletedV = Venue.query.filter_by(id == venue_id)
      deletedV.detlete()
      db.session.commit()
  except:            
      db.session.rollback()      
      flash("An Error Occured While Deleting ")
  finally:
      db.session.close()   

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for(index))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  
  artist_data = Artist.query.all()
  datas =[]
  for d in artist_data:
    data={
      "id": d.id,
      "name": d.name
    }
    datas.append(data)
  
  return render_template('pages/artists.html', artists=datas)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 3,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
    
  artist_data = Artist.query.all()
  finalData =[]    
  for data in artist_data:
    past_show = []
    upcoming_show =[]
    present_show = []
    present_time = str(datetime.today())    
    show_data = Show.query.filter_by(artist_id=data.id)
    for showD in show_data:      
      if showD.start_time < present_time:
        active_Venue = Venue.query.get(showD.venue_id)
        pastData = {
          "venue_id":active_Venue.id,
          "venue_name":active_Venue.name,
          "venue_image_link":active_Venue.image_link,
          "start_time":showD.start_time
        }
        past_show.append(pastData)
      elif showD.start_time > present_time:
        active_Venue = Venue.query.get(showD.venue_id)
        upcomingData = {
          "venue_id":active_Venue.id,
          "venue_name":active_Venue.name,
          "venue_image_link":active_Venue.image_link,
          "start_time":showD.start_time
        }
        upcoming_show.append(upcomingData)
      else:
        active_Venue = Venue.query.get(showD.venue_id)
        presentData = {
          "venue_id":active_Venue.id,
          "venue_name":active_Venue.name,
          "venue_image_link":active_Venue.image_link,
          "start_time":showD.start_time
        }
        present_show.append(presentData)
        
    dataItem ={
      "id": data.id,
      "name":data.name,
      "genres":data.genres,
      "city":data.city,
      "state":data.state,
      "phone":data.phone,
      "website":data.website_link,
      "facebook_link":data.facebook_link,
      "seeking_venue":data.seeking_venue,
      "seeking_description":data.seeking_description,
      "image_link":data.image_link,
      "past_shows": past_show,
      "upcoming_shows": upcoming_show,
      "past_shows_count": len(past_show),
      "upcoming_shows_count": len(upcoming_show),
    }
    finalData.append(dataItem)
    
  data = list(filter(lambda d: d['id'] == artist_id, finalData))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()       
  artist={
    "id": artist_id,
    "name": form.name.data,
    "genres": form.genres.data,
    "city": form.city.data,
    "state": form.state.data,
    "phone": form.phone.data,
    "website": form.website_link.data,
    "facebook_link": form.facebook_link.data,
    "seeking_venue": form.seeking_venue.data,
    "seeking_description": form.seeking_description.data,
    "image_link": form.image_link.data
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  form = ArtistForm()
  Error = False
  try:      
      stuff = Artist.query.get(artist_id)             
      stuff.name = form.name.data
      stuff.city = form.city.data
      stuff.state = form.state.data
      stuff.phone = form.phone.data
      stuff.genres = form.genres.data
      stuff.image_link = form.image_link.data
      stuff.facebook_link = form.facebook_link.data
      stuff.website_link = form.website_link.data
      stuff.seeking_venue = form.seeking_venue.data
      stuff.seeking_description = form.seeking_description.data
      
      db.session.commit()
  except:
      Error = True
      db.session.rollback()
  finally:
      db.session.close() 
  if Error == True:      
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be placed.')
      flash('Make sure you put in the correct Data for each input! links should begin with https or http')      
  else:
      flash('Artist ' + request.form['name'] + ' was successfully Placed!')      
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": venue_id,
    "name": form.name.data,
    "genres": form.genres.data,
    "address": form.address.data,
    "city": form.city.data,
    "state": form.state.data,
    "phone": form.phone.data,
    "website": form.website_link.data,
    "facebook_link": form.facebook_link.data,
    "seeking_talent": form.seeking_talent.data,
    "seeking_description": form.seeking_description.data,
    "image_link": form.image_link.data
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  Error = False
  try:      
      stuff = Venue.query.get(venue_id)             
      stuff.name = form.name.data
      stuff.city = form.city.data
      stuff.state = form.state.data
      stuff.address = form.address.data
      stuff.phone = form.phone.data
      stuff.genres = form.genres.data
      stuff.image_link = form.image_link.data
      stuff.facebook_link = form.facebook_link.data   
      stuff.website_link = form.website_link.data
      stuff.seeking_talent = form.seeking_talent.data
      stuff.seeking_description = form.seeking_description.data
      
      db.session.commit()
  except:
      Error = True
      db.session.rollback()
  finally:
      db.session.close() 
  if Error == True:      
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be placed.')
      flash('Make sure you put in the correct Data for each input! links should begin with https or http')      
  else:
      flash('Venue ' + request.form['name'] + ' was successfully Placed!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  form = ArtistForm()
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  
  Id = Artist.query.all()
  Id_Length = len(Id)
  Error = False
  try:
      new_data = Artist(
        id = Id_Length+1,
        name=form.name.data, 
        city = form.city.data,
        state = form.state.data,        
        phone = form.phone.data,
        genres = form.genres.data,
        image_link = form.image_link.data,
        facebook_link = form.facebook_link.data,
        website_link = form.website_link.data,
        seeking_venue = form.seeking_venue.data,
        seeking_description = form.seeking_description.data
        ) 
      db.session.add(new_data)
      db.session.commit()
  except:
      Error = True
      db.session.rollback()
  finally:
      db.session.close() 
  if Error == True:      
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  
  show_data = Show.query.all()
  finalData =[]  
  
  for data in show_data:    
    active_Artist =  Artist.query.get(data.artist_id)
    active_Venue = Venue.query.get(data.venue_id)
    dataItem ={
      "venue_id": data.venue_id,
      "venue_name":active_Venue.name,
      "artist_id":data.artist_id,
      "artist_name":active_Artist.name,
      "artist_image_link":active_Artist.image_link,      
      "start_time":data.start_time
    }
    finalData.append(dataItem)
  
  return render_template('pages/shows.html', shows=finalData)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead 
  form = ShowForm() 
  # on successful db insert, flash success  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  Error = False
  try:
      show_data = Show( 
        artist_id = form.artist_id.data,
        venue_id = form.venue_id.data,
        start_time = form.start_time.data
      )
      active_Artist =  Artist.query.get(form.artist_id.data)
      active_Venue = Venue.query.get(form.venue_id.data)
      show_data.venueS = active_Venue
      show_data.artistS = active_Artist   
      db.session.add(show_data)
      db.session.commit()
  except:
      Error = True
      db.session.rollback()
  finally:
      db.session.close()
  if Error == True:
      flash('An error occurred. Show could not be listed.')
  else:
      flash('Show was successfully listed!')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

from datetime import datetime
from flask import flash
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL
import re

def is_phone_validated(number):
    """ Special types on numbers to be considered such as:
    (international numbers) +(234)123456789
    (no spacing)            1234567890 
    (dot separator)         123.456.7890
    (dash separator)        123-456-7890 
    (space separator)       123 456 7890 
    Patterns:    
    """   
    
    pattern = '^([+]?[(]?[0-9]{1,3}?[)]?)?\(?([0-9]{3,4})\)?[\-\.\ ]?([0-9]{3,4})[\-\.\ ]?([0-9]{4})$'    
    phone_format = re.compile(pattern)
    if phone_format.match(number):
        return True

def is_facebook_validated(facebook_url):
    """
        Checks for the https or http or ftp characters
        in the url and made sure it follows the patterns:
        "https://www.facebook.com/username"
        "http://www.facebook.com/username"
        "ftp://www.facebook.com/username"
    
    Note: i didnt't make use of the ? wild character because the 
    link has a fixed format!
    """
    pattern = '^(https|http|ftp)\:([\/]{2})([w]{3})\.(facebook)\.(com)[\/]([a-zA-Z0-9]|.)+$'
    facebook_format = re.compile(pattern)
    if facebook_format.match(facebook_url):
        return True
    else:
        return False

def is_image_validated(image_url):
    
    """
        Checks for the https or http or ftp characters
        in the url and made sure it follows the patterns:
        "https://www.address.jpg"
        "https://www.address.jpeg"
        "https://www.address.png"
        "https://www.address.webp"
        "https://www.address.gif"
        "https://www.address.bmp"
    
    Note: i didnt't make use of the ? wild character because the 
    link has a fixed format!
    """
    
    pattern = '^(https|http|ftp)\:([\/]{2})([a-zA-Z0-9]|.)+\.(jpg|jpeg|png|webp|gif|bmp)+$'
    image_format = re.compile(pattern)
    if image_format.match(image_url):
        return True
    else:
        return False

def is_website_validated(website_url):
    
    """
        Checks for the https or http or ftp characters
        in the url and made sure it follows the patterns:
        
        "https://www.address.host"        
    
    Note: i didnt't make use of the ? wild character because the 
    link has a fixed format!
    """
    
    pattern = '^(https|http|ftp)\:([\/]{2})([a-zA-Z0-9]|.)+$'
    website_format = re.compile(pattern)
    if website_format.match(website_url):
        return True
    else:
        return False
    
def is_date_valid(date_pattern):
    """
        Ensures The date format is fixed to the pattern
        Example -> 2022-06-03 06:41:41
    """    
    pattern = '^([0-9]{4})\-[0-1][0-9]\-[0-3][0-9]\ [0-2][0-9]\:[0-6][0-9]\:[0-6][0-9]'
    date_format=re.compile(pattern)
    if date_format.match(date_pattern):
        return True
    else:
        return False
    


class ShowForm(Form):
    def validate_date_time(self):
        if not is_date_valid(str(self.start_time.data)) == True:            
            return False
        else: 
            return True
        
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    
    def validate_venue(self):                      
        if not is_phone_validated(self.phone.data) == True:   
            self.phone.errors.append('Invalid phone.')         
            return False        
        elif not is_facebook_validated(self.facebook_link.data) == True:
            self.facebook_link.errors.append('Invalid facebook address.')
            return False
        elif not is_image_validated(self.image_link.data) == True:
            self.image_link.errors.append('Invalid Image Url.')
            return False
        elif not is_website_validated(self.website_link.data) == True:
            self.website_link.errors.append('Invalid Website Url.')
            return False   
        else:            
            return True                    
    
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],                
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(Form):
               
    def validate_artist(self):                      
        if not is_phone_validated(self.phone.data) == True:   
            self.phone.errors.append('Invalid phone.')         
            return False        
        elif not is_facebook_validated(self.facebook_link.data) == True:
            self.facebook_link.errors.append('Invalid facebook address.')
            return False
        elif not is_image_validated(self.image_link.data) == True:
            self.image_link.errors.append('Invalid Image Url.')
            return False
        elif not is_website_validated(self.website_link.data) == True:
            self.website_link.errors.append('Invalid Website Url.')
            return False   
        else:            
            return True    
    
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )    
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for phone 
        'phone', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
     )

    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )


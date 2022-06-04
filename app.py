from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose, AdminIndexView, form
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList, ValidationError, DateField, SelectField
from wtforms.validators import InputRequired, Length, AnyOf, Email, Regexp, EqualTo, Optional
from werkzeug.security import generate_password_hash, check_password_hash
import os
from jinja2 import Markup
import json
import random
import string
from flask_mail import Mail, Message

import subprocess

# logic borrowed from external source (1)
basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(basedir, 'static')
# end logic borrowed

# Temporary load of environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder='static')

'''
####################################################################################################
################################ Config Settings ###################################################
####################################################################################################
'''

app.config.from_envvar('APP_CONFIG')

# mail_settings = {
#    "MAIL_SERVER": 'smtp.gmail.com',
#    "MAIL_PORT": 465,
#    "MAIL_USE_TLS": False,
#    "MAIL_USE_SSL": True,
#    "MAIL_USERNAME": '<gmail address>',
#    "MAIL_PASSWORD": '<password to gmail account>'
# }

# app.config.update(mail_settings)
mail = Mail(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///<database name>.db'
# app.config['SECRET_KEY'] = '<your secret key>'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['TESTING'] = True
# app.config['WTF_CSRF_ENABLED'] = True
# app.config['WTF_CSRF_TIME_LIMIT'] = 3600


# instantiate sqlalchemy db
db = SQLAlchemy(app)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


admin = Admin(app, template_mode='bootstrap4')
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


'''
####################################################################################################
################### Database Schema (Defined for SQLAlchemy) #######################################
####################################################################################################
'''

class User(db.Model, UserMixin):
    '''
    SQLAlchemy table class: User
    Registered table name: user
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50))
    user_role = db.Column(db.String(10), nullable=False, server_default='user')
    user_email = db.Column(db.String(256), nullable=True)
    password_reset = db.Column(db.String(256), nullable=False, server_default='False')

    # Relationships:
    reviews = db.relationship('Reviews', backref='user', lazy='dynamic')
    user_details = db.relationship('UserDetails', backref='user', lazy='dynamic')

    def __repr__(self):
        return '%r' % (self.username)


class UserDetails(db.Model, UserMixin):
    '''
    SQLAlchemy table class: UserDetails
    Registered table name: user_details
    '''
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256), nullable=True)
    last_name = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(256), nullable=True)
    phone = db.Column(db.String(256), nullable=True)
    addr = db.Column(db.String(256), nullable=True)
    city = db.Column(db.String(256), nullable=True)
    state = db.Column(db.String(256), nullable=True)
    country = db.Column(db.String(256), nullable=True)
    zip = db.Column(db.String(256), nullable=True)
    cc_type = db.Column(db.String(20), nullable=True)
    cc_num = db.Column(db.String(256), nullable=True)
    sec_num = db.Column(db.Integer, nullable=True)

    # Relationships:
    reviews = db.relationship('Reviews', backref='user_details', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '%r' % (self.first_name)


class Book(db.Model):
    '''
    SQLAlchemy table class: Book
    Registered table name: book
    '''
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(256), nullable=False)
    publisher = db.Column(db.String(256), nullable=False)
    language = db.Column(db.String(256), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False)
    isbn = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(2048), nullable=False)
    sample = db.Column(db.String(4096), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image_uploads.id'))
    audio_id = db.Column(db.Integer, db.ForeignKey('audio_samples.id'))

    # Relationships:
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'))
    book_status_id = db.Column(db.Integer, db.ForeignKey('book_status.book_status_id'))
    book = db.relationship('Reviews', backref='book', lazy='dynamic')
    book_order_item = db.relationship('BookOrderItem', backref='book', lazy='dynamic')

    def __repr__(self):
        return '%r' % (self.title)


class ImageUploads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    path = db.Column(db.String(256), unique=True)
    user = db.relationship('Book', backref='image_uploads', lazy='dynamic')

    def __repr__(self):
        return self.name

class AudioSamples(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    path = db.Column(db.String(256), unique=True)
    user = db.relationship('Book', backref='audio_samples', lazy='dynamic')

    def __repr(self):
        return self.name

class Genre(db.Model):
    '''
    SQLAlchemy table class: Genre
    Registered table name: genre
    '''
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_desc = db.Column(db.String(100), nullable=False)
    book = db.relationship('Book', backref='genre', lazy='dynamic')

    def __repr__(self):
        return '%r' % (self.genre_desc)


class BookStatus(db.Model):
    '''
    SQLAlchemy table class: BookStatus
    Registered table name: book_status
    '''
    book_status_id = db.Column(db.Integer, primary_key=True)
    status_desc = db.Column(db.String(512), nullable=False)
    book = db.relationship('Book', backref='book_status', lazy='dynamic')

    def __repr__(self):
        return '%r' % (self.status_desc)


class Reviews(db.Model):
    '''
    SQLAlchemy table class: Reviews
    Registered table name: reviews
    '''
    review_id = db.Column(db.Integer, primary_key=True)
    review_desc = db.Column(db.String(512), nullable=False)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    user_details_id = db.Column(db.Integer, db.ForeignKey('user_details.id'))

    def __repr__(self):
        return '%r' % (self.review_id)


class BookOrder(db.Model):
    '''
    SQLAlchemy table class: BookOrder
    Registered table name: book_order
    '''
    order_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    addr = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(100), nullable=False)
    cc_type = db.Column(db.String(20), nullable=False)
    cc_num = db.Column(db.String(256), nullable=False)
    sec_num = db.Column(db.Integer, nullable=False)
    order_status = db.Column(db.String(20), nullable=False)

    book_order_item = db.relationship('BookOrderItem', backref='book_order', lazy='dynamic')


class BookOrderItem(db.Model):
    '''
    SQLAlchemy table class: BookOrderItem
    Registered table name: book_order_item
    '''
    boi_id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer)
    # Relationships
    order_id = db.Column(db.Integer, db.ForeignKey('book_order.order_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))


'''
####################################################################################################
################################# Customize Admin Table Views ######################################
####################################################################################################

Choose additional view attributes to add to each base view class (defined above) per the Flask-Admin
documentation link:
- https://flask-admin.readthedocs.io/en/latest/api/mod_contrib_sqla/
- https://flask-admin.readthedocs.io/en/latest/api/mod_model/#flask_admin.model.BaseModelView

'''

# Customize User Table View in Admin
class UserView(ModelView):
    '''
    Add View Attributes to class: User
    ----------------------------------
    Pick attributes from Flask-Admin docs.

    '''
    column_searchable_list = ('username', 'password', 'user_role')
    column_filters = ('username', 'password', 'user_role')
    column_exclude_list = []
    column_display_pk = True
    column_default_sort = 'username'
    export_types = ['csv', 'xlsx', 'json', 'xls', 'yaml', 'html', 'pandas']
    can_export = True

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method='sha256')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('noauth'))


# Customize UserDetails Table View in Admin
class UserDetailsView(ModelView):
    '''
    Add View Attributes to class: UserDetails
    ----------------------------------
    Pick attributes from Flask-Admin docs.

    '''
    column_searchable_list = ('first_name', 'last_name', 'email', 'phone', 'addr', 'city', 'state', 'country', 'zip', 'cc_type', 'cc_num', 'sec_num')
    column_filters = ('first_name', 'last_name', 'email', 'phone', 'addr', 'city', 'state', 'country', 'zip', 'cc_type', 'cc_num', 'sec_num')
    column_exclude_list = []
    column_display_pk = True
    column_default_sort = 'last_name'
    export_types = ['csv', 'xlsx', 'json', 'xls', 'yaml', 'html', 'pandas']
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('noauth'))


# customize Book Table View in Admin
class BookView(ModelView):
    '''
    Add View Attributes to class: Book
    ----------------------------------
    Pick attributes from Flask-Admin docs.

    '''
    column_searchable_list = ('title', 'author', 'publisher', 'language', 'pages', 'publish_date', 'isbn', 'price', 'description')
    column_filters = ('title', 'author', 'publisher', 'language', 'pages', 'publish_date', 'isbn', 'price', 'description')
    column_exclude_list = ['language', 'description', 'pages', 'publish_date', 'sample']
    export_types = ['csv', 'xlsx', 'json', 'xls', 'yaml', 'html', 'pandas']
    can_export = True
    page_size = 6

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('noauth'))

    def _list_thumbnail(view, context, model, name):
        if not model.image or not model.image.path:
            return ''

        return Markup(
            '<img src="%s">' %
            url_for('static',
                    filename=form.thumbgen_filename(model.image.path))
        )

    column_formatters = {
        'image': _list_thumbnail
    }

    edit_template = 'edit_user.html'


class ImageUploadsView(ModelView):
    page_size = 6

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('noauth'))

    # Method is borrowed from external source (1)
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup(
            '<img src="%s">' %
            url_for('static',
                    filename=form.thumbgen_filename(model.path))
        )

    column_formatters = {
        'path': _list_thumbnail
    }

    form_extra_fields = {
        'path': form.ImageUploadField(
            'Image', base_path=file_path, thumbnail_size=(100, 100, True))
    }



# customize BookStatus View Table in Admin
class BookStatusView(ModelView):
    '''
    Add View Attributes to class: BookStatus
    ----------------------------------------
    Pick attributes from Flask-Admin docs.

    '''
    column_searchable_list = ('status_desc', )
    column_filters = ('status_desc', )
    column_exclude_list = []
    column_display_pk = True
    export_types = ['csv', 'xlsx', 'json', 'xls', 'yaml', 'html', 'pandas']
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('noauth'))


# customize Reviews Table in Admin
class ReviewsView(ModelView):
    '''
    Add View Attributes to class: Reviews
    -------------------------------------
    Pick attributes from Flask-Admin docs.

    '''
    column_searchable_list = ('review_desc', )
    column_filters = ('review_desc', )
    column_exclude_list = []
    column_display_pk = True
    export_types = ['csv', 'xlsx', 'json', 'xls', 'yaml', 'html', 'pandas']
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('noauth'))


# customize BookOrder Table View in Admin
class BookOrderView(ModelView):
    '''
    Add View Attributes to class: BookOrder
    ---------------------------------------
    Pick attributes from Flask-Admin docs.

    '''
    column_searchable_list = ('first_name', 'last_name', 'email', 'phone', 'addr', 'city', 'state', 'country', 'cc_type', 'order_status')
    column_filters = ('first_name', 'last_name', 'email', 'phone', 'addr', 'city', 'state', 'country', 'cc_type', 'order_status')
    column_exclude_list = []
    column_display_pk = True
    export_types = ['csv', 'xlsx', 'json', 'xls', 'yaml', 'html', 'pandas']
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('noauth'))


# customize BookOrderItem Table View in Admin
class BookOrderItemView(ModelView):
    '''
    Add View Attributes to class: BookOrderItem
    -------------------------------------------
    Pick attributes from Flask-Admin docs.

    '''
    column_searchable_list = ('qty', )
    column_filters = ('qty', )
    column_exclude_list = []
    column_display_pk = True
    export_types = ['csv', 'xlsx', 'json', 'xls', 'yaml', 'html', 'pandas']
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('noauth'))


# customize Genre Table View in Admin
class GenreView(ModelView):
    '''
    Add View Attributes to class: Genre
    -----------------------------------
    Pick attributes from Flask-Admin docs.

    '''
    column_searchable_list = ('genre_desc', )
    column_filters = ('genre_desc', )
    column_exclude_list = []
    column_display_pk = True
    export_types = ['csv', 'xlsx', 'json', 'xls', 'yaml', 'html', 'pandas']
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('noauth'))


class LogoutAdminView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('logout'))


'''
####################################################################################################
########################### Modified Admin View ####################################################
####################################################################################################

The modified views (above) are now added to the application.

'''

admin.add_view(UserView(User, db.session))
admin.add_view(UserDetailsView(UserDetails, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(BookStatusView(BookStatus, db.session))
admin.add_view(ReviewsView(Reviews, db.session))
admin.add_view(BookOrderView(BookOrder, db.session))
admin.add_view(BookOrderItemView(BookOrderItem, db.session))
admin.add_view(GenreView(Genre, db.session))

admin.add_view(ImageUploadsView(ImageUploads, db.session))
admin.add_view(LogoutAdminView(name='Logout', endpoint='logout'))

'''
####################################################################################################
########################### Authentication Helper Classes ##########################################
####################################################################################################

These are classes used to aid in authentication.

'''
class AuthLoginForm(FlaskForm):
    username = StringField(label='Username', validators=[InputRequired('You must enter a Username'), Length(min=5, max=25, message='Username must be between 5 and 25 chars.')])
    password = PasswordField('password', validators=[InputRequired('Password: @ least 1 digit, @ least 1 upper-case char, @ least 1 lower-case char, @ least 1 special char.'), Length(min=8, max=25, message='Password must be 8 to 25 chars long.'), Regexp('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$', message='Regex does not match.')])
    remember_me = BooleanField()


class AuthRegForm(FlaskForm):
    email = StringField('email', validators=[InputRequired('You must enter an email'), Email(message='You must enter a valid email format')])
    username = StringField(label='username', validators=[InputRequired('You must enter a Username'), Length(min=5, max=25, message='Username must be between 5 and 25 chars.')])
    password = PasswordField('password', validators=[InputRequired('Password: @ least 1 digit, @ least 1 upper-case char, @ least 1 lower-case char, @ least 1 special char.'), Length(min=8, max=25, message='Password must be 8 to 25 chars long.'), Regexp('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$', message='Regex does not match.')])
    check_password = PasswordField('check_password', validators=[InputRequired('Password: @ least 1 digit, @ least 1 upper-case char, @ least 1 lower-case char, @ least 1 special char.'), Length(min=8, max=25, message='Password must be 8 to 25 chars long.'), Regexp('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$', message='Regex does not match.'), EqualTo('password', message='Your password entries must match each other.')])


class UserDetailsUpdateForm(FlaskForm):
    first_name = StringField('first_name', validators=[Optional(),Length(min=0, max=50, message='Username must be between 0 and 150 chars.'),Regexp('^[a-zA-Z]+$', message='Regex does not match. String only.')])
    last_name = StringField('last_name', validators=[Optional(),Length(min=0, max=50, message='Username must be between 0 and 150 chars.'),Regexp('^[a-zA-Z]+$', message='Regex does not match. String only.')])
    email = StringField('email', validators=[Optional(), Email(message='You must enter a valid email format')])
    phone = StringField('phone', validators=[Optional(),Length(min=0, max=50, message='Phone Number format: ###-###-####'),Regexp('^(\d{3})-(\d{3})-(\d{4})$', message='Regex does not match. Phone Number Format: ###-###-####.')])
    addr = StringField('addr', validators=[Optional(),Length(min=0, max=50, message='Address format: Alphanumeric'),Regexp('^\d+\s[A-z]+\s[A-z]+', message='Regex does not match. Address Format: Alpha numeric.')])
    city = StringField('city', validators=[Optional(),Length(min=0, max=50, message='City name must be between 0 and 150 chars.'),Regexp('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', message='Regex does not match. String only.')])
    state = SelectField('state', validators=[Optional()], choices=[('AL', 'AL'),('AK', 'AK'),('AZ', 'AZ'),('AR', 'AR'),('CA', 'CA'),('CO', 'CO'),('CT', 'CT'),('DE', 'DE'),('FL', 'FL'),('GA', 'GA'),('HI', 'HI'),('ID', 'ID'),('IL', 'IL'),('IN', 'IN'),('IA', 'IA'),('KS', 'KS'),('KY', 'KY'),('LA', 'LA'),('ME', 'ME'),('MD', 'MD'),('MA', 'MA'),('MI', 'MI'),('MN', 'MN'),('MS', 'MS'),('MO', 'MO'),('MT', 'MT'),('NE', 'NE'),('NV', 'NV'),('NH', 'NH'),('NJ', 'NJ'),('NM', 'NM'),('NY', 'NY'),('NC', 'NC'),('ND', 'ND'),('OH', 'OH'),('OK', 'OK'),('OR', 'OR'),('PA', 'PA'),('RI', 'RI'),('SC', 'SC'),('SD', 'SD'),('TN', 'TN'),('TX', 'TX'),('UT', 'UT'),('VT', 'VT'),('VA', 'VA'),('WA', 'WA'),('WV', 'WV'),('WI', 'WI'),('WY', 'WY')])
    zip_code = IntegerField('zip', validators=[Optional()])
    country = SelectField('country', validators=[Optional()], choices=[('Afghanistan', 'Afghanistan'),('Albania', 'Albania'),('Algeria', 'Algeria'),('Andorra', 'Andorra'),('Angola', 'Angola'),('Antigua and Barbuda', 'Antigua and Barbuda'),('Argentina', 'Argentina'),('Armenia', 'Armenia'),('Australia', 'Australia'),('Austria', 'Austria'),('Azerbaijan', 'Azerbaijan'),('Bahamas', 'Bahamas'),('Bahrain', 'Bahrain'),('Bangladesh', 'Bangladesh'),('Barbados', 'Barbados'),('Belarus', 'Belarus'),('Belgium', 'Belgium'),('Belize', 'Belize'),('Benin', 'Benin'),('Bhutan', 'Bhutan'),('Bolivia', 'Bolivia'),('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),('Botswana', 'Botswana'),('Brazil', 'Brazil'),('Brunei', 'Brunei'),('Bulgaria', 'Bulgaria'),('Burkina Faso', 'Burkina Faso'),('Burundi', 'Burundi'),('Côte d\'Ivoire', 'Côte d\'Ivoire'),('Cabo Verde', 'Cabo Verde'),('Cambodia', 'Cambodia'),('Cameroon', 'Cameroon'),('Canada', 'Canada'),('Central African Republic', 'Central African Republic'),('Chad', 'Chad'),('Chile', 'Chile'),('China', 'China'),('Colombia', 'Colombia'),('Comoros', 'Comoros'),('Costa Rica', 'Costa Rica'),('Croatia', 'Croatia'),('Cuba', 'Cuba'),('Cyprus', 'Cyprus'),('Czech Republic', 'Czech Republic'),('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),('Denmark', 'Denmark'),('Djibouti', 'Djibouti'),('Dominica', 'Dominica'),('Dominican Republic', 'Dominican Republic'),('East Timor', 'East Timor'), ('Ecuador', 'Ecuador'),('Egypt', 'Egypt'),('El Salvador', 'El Salvador'),('Equatorial Guinea', 'Equatorial Guinea'),('Eritrea', 'Eritrea'),('Estonia', 'Estonia'),('Eswatini (fmr. "Swaziland")', 'Eswatini (fmr. "Swaziland")'),('Ethiopia', 'Ethiopia'),('Fiji', 'Fiji'),('Finland', 'Finland'),('France', 'France'),('Gabon', 'Gabon'),('Gambia', 'Gambia'),('Georgia', 'Georgia'),('Germany', 'Germany'),('Ghana', 'Ghana'),('Greece', 'Greece'),('Grenada', 'Grenada'),('Guatemala', 'Guatemala'),('Guinea', 'Guinea'),('Guinea-Bissau', 'Guinea-Bissau'),('Guyana', 'Guyana'),('Haiti', 'Haiti'),('Holy See', 'Holy See'),('Honduras', 'Honduras'),('Hungary', 'Hungary'),('Iceland', 'Iceland'),('India', 'India'),('Indonesia', 'Indonesia'),('Iran', 'Iran'),('Iraq', 'Iraq'),('Ireland', 'Ireland'),('Israel', 'Israel'),('Italy', 'Italy'),('Ivory Coast', 'Ivory Coast'), ('Jamaica', 'Jamaica'),('Japan', 'Japan'),('Jordan', 'Jordan'),('Kazakhstan', 'Kazakhstan'),('Kenya', 'Kenya'),('Kiribati', 'Kiribati'),('North Korea', 'North Korea'), ('South Korea', 'South Korea'), ('Kosovo', 'Kosovo'), ('Kuwait', 'Kuwait'),('Kyrgyzstan', 'Kyrgyzstan'),('Laos', 'Laos'),('Latvia', 'Latvia'),('Lebanon', 'Lebanon'),('Lesotho', 'Lesotho'),('Liberia', 'Liberia'),('Libya', 'Libya'),('Liechtenstein', 'Liechtenstein'),('Lithuania', 'Lithuania'),('Luxembourg', 'Luxembourg'),('Macedonia', 'Macedonia'),('Madagascar', 'Madagascar'),('Malawi', 'Malawi'),('Malaysia', 'Malaysia'),('Maldives', 'Maldives'),('Mali', 'Mali'),('Malta', 'Malta'),('Marshall Islands', 'Marshall Islands'),('Mauritania', 'Mauritania'),('Mauritius', 'Mauritius'),('Mexico', 'Mexico'),('Micronesia', 'Micronesia'),('Moldova', 'Moldova'),('Monaco', 'Monaco'),('Mongolia', 'Mongolia'),('Montenegro', 'Montenegro'),('Morocco', 'Morocco'),('Mozambique', 'Mozambique'),('Myanmar', 'Myanmar'),('Namibia', 'Namibia'),('Nauru', 'Nauru'),('Nepal', 'Nepal'),('Netherlands', 'Netherlands'),('New Zealand', 'New Zealand'),('Nicaragua', 'Nicaragua'),('Niger', 'Niger'),('Nigeria', 'Nigeria'),('Norway', 'Norway'),('Oman', 'Oman'),('Pakistan', 'Pakistan'),('Palau', 'Palau'),('Panama', 'Panama'),('Papua New Guinea', 'Papua New Guinea'),('Paraguay', 'Paraguay'),('Peru', 'Peru'),('Philippines', 'Philippines'),('Poland', 'Poland'),('Portugal', 'Portugal'),('Qatar', 'Qatar'),('Romania', 'Romania'),('Russian Federation', 'Russian Federation'),('Rwanda', 'Rwanda'),('St Kitts &amp; Nevis', 'St Kitts &amp; Nevis'),('St Lucia', 'St Lucia'),('Saint Vincent &amp; the Grenadines', 'Saint Vincent &amp; the Grenadines'),('Samoa', 'Samoa'),('San Marino', 'San Marino'),('Sao Tome &amp; Principe', 'Sao Tome &amp; Principe'),('Saudi Arabia', 'Saudi Arabia'),('Senegal', 'Senegal'),('Serbia', 'Serbia'),('Seychelles', 'Seychelles'),('Sierra Leone', 'Sierra Leone'),('Singapore', 'Singapore'),('Slovakia', 'Slovakia'),('Slovenia', 'Slovenia'),('Solomon Islands', 'Solomon Islands'),('Somalia', 'Somalia'),('South Africa', 'South Africa'),('South Sudan', 'South Sudan'),('Spain', 'Spain'),('Sri Lanka', 'Sri Lanka'),('Sudan', 'Sudan'),('Suriname', 'Suriname'),('Swaziland', 'Swaziland'),('Sweden', 'Sweden'),('Switzerland', 'Switzerland'),('Syria', 'Syria'),('Taiwan', 'Taiwan'),('Tajikistan', 'Tajikistan'),('Tanzania', 'Tanzania'),('Thailand', 'Thailand'),('Togo', 'Togo'),('Tonga', 'Tonga'),('Trinidad &amp; Tobago', 'Trinidad &amp; Tobago'),('Tunisia', 'Tunisia'),('Turkey', 'Turkey'),('Turkmenistan', 'Turkmenistan'),('Tuvalu', 'Tuvalu'),('Uganda', 'Uganda'),('Ukraine', 'Ukraine'),('United Arab Emirates', 'United Arab Emirates'),('United Kingdom', 'United Kingdom'),('United States', 'United States'),('Uruguay', 'Uruguay'),('Uzbekistan', 'Uzbekistan'),('Vanuatu', 'Vanuatu'),('Vatican City', 'Vatican City'),('Venezuela', 'Venezuela'),('Vietnam', 'Vietnam'), ('Yemen', 'Yemen'),('Zambia', 'Zambia'),('Zimbabwe', 'Zimbabwe')])
    cc_type = SelectField('cc_type', validators=[Optional()], choices=[('VISA', 'VISA'),('MASTER CARD', 'MASTER CARD'),('AMEX', 'AMEX'),('DISCOVER', 'DISCOVER'), ('PREPAID', 'PREPAID')])
    cc_num = StringField('cc_num', validators=[Optional(),Length(min=0, max=20, message='Credit Card Number format: ####-####-####-####'),Regexp('^(\d{4})-(\d{4})-(\d{4})-(\d{4})$', message='Regex does not match. Credit Card Number Format: ####-####-####-####.')])
    sec_num = StringField('sec_num', validators=[Optional(),Length(min=3, max=4, message='Security Numbre format: ###'),Regexp('^(\d{3})', message='Regex does not match. Security Number Format: ###(#).')])

# Form for checkout
class CheckoutForm(FlaskForm):
    first_name = StringField('first_name', validators=[InputRequired('You must enter in a first name.'),Length(min=0, max=50, message='Username must be between 0 and 150 chars.'),Regexp('^[a-zA-Z]+$', message='Regex does not match. String only.')])
    last_name = StringField('last_name', validators=[InputRequired('You must enter in a last name.'),Length(min=0, max=50, message='Username must be between 0 and 150 chars.'),Regexp('^[a-zA-Z]+$', message='Regex does not match. String only.')])
    email = StringField('email', validators=[InputRequired('You must enter in a valid email.'), Email(message='You must enter a valid email format')])
    phone = StringField('phone', validators=[Optional(),Length(min=0, max=50, message='Phone Number format: ###-###-####'),Regexp('^(\d{3})-(\d{3})-(\d{4})$', message='Regex does not match. Phone Number Format: ###-###-####.')])
    addr = StringField('addr', validators=[InputRequired('You must enter in a valid address.'),Length(min=0, max=50, message='Address format: Alphanumeric'),Regexp('^\d+\s[A-z]+\s[A-z]+', message='Regex does not match. Address Format: Alpha numeric.')])
    city = StringField('city', validators=[InputRequired('You must enter in a valid city.'),Length(min=0, max=50, message='City name must be between 0 and 150 chars.'),Regexp('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', message='Regex does not match. String only.')])
    state = SelectField('state', validators=[InputRequired('You must select a valid state.')], choices=[('AL', 'AL'),('AK', 'AK'),('AZ', 'AZ'),('AR', 'AR'),('CA', 'CA'),('CO', 'CO'),('CT', 'CT'),('DE', 'DE'),('FL', 'FL'),('GA', 'GA'),('HI', 'HI'),('ID', 'ID'),('IL', 'IL'),('IN', 'IN'),('IA', 'IA'),('KS', 'KS'),('KY', 'KY'),('LA', 'LA'),('ME', 'ME'),('MD', 'MD'),('MA', 'MA'),('MI', 'MI'),('MN', 'MN'),('MS', 'MS'),('MO', 'MO'),('MT', 'MT'),('NE', 'NE'),('NV', 'NV'),('NH', 'NH'),('NJ', 'NJ'),('NM', 'NM'),('NY', 'NY'),('NC', 'NC'),('ND', 'ND'),('OH', 'OH'),('OK', 'OK'),('OR', 'OR'),('PA', 'PA'),('RI', 'RI'),('SC', 'SC'),('SD', 'SD'),('TN', 'TN'),('TX', 'TX'),('UT', 'UT'),('VT', 'VT'),('VA', 'VA'),('WA', 'WA'),('WV', 'WV'),('WI', 'WI'),('WY', 'WY')])
    zip_code = IntegerField('zip', validators=[InputRequired('You must enter in a valid zip code.')])
    country = SelectField('country', validators=[InputRequired('You must select a valid country.')], choices=[('Afghanistan', 'Afghanistan'),('Albania', 'Albania'),('Algeria', 'Algeria'),('Andorra', 'Andorra'),('Angola', 'Angola'),('Antigua and Barbuda', 'Antigua and Barbuda'),('Argentina', 'Argentina'),('Armenia', 'Armenia'),('Australia', 'Australia'),('Austria', 'Austria'),('Azerbaijan', 'Azerbaijan'),('Bahamas', 'Bahamas'),('Bahrain', 'Bahrain'),('Bangladesh', 'Bangladesh'),('Barbados', 'Barbados'),('Belarus', 'Belarus'),('Belgium', 'Belgium'),('Belize', 'Belize'),('Benin', 'Benin'),('Bhutan', 'Bhutan'),('Bolivia', 'Bolivia'),('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),('Botswana', 'Botswana'),('Brazil', 'Brazil'),('Brunei', 'Brunei'),('Bulgaria', 'Bulgaria'),('Burkina Faso', 'Burkina Faso'),('Burundi', 'Burundi'),('Côte d\'Ivoire', 'Côte d\'Ivoire'),('Cabo Verde', 'Cabo Verde'),('Cambodia', 'Cambodia'),('Cameroon', 'Cameroon'),('Canada', 'Canada'),('Central African Republic', 'Central African Republic'),('Chad', 'Chad'),('Chile', 'Chile'),('China', 'China'),('Colombia', 'Colombia'),('Comoros', 'Comoros'),('Costa Rica', 'Costa Rica'),('Croatia', 'Croatia'),('Cuba', 'Cuba'),('Cyprus', 'Cyprus'),('Czech Republic', 'Czech Republic'),('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),('Denmark', 'Denmark'),('Djibouti', 'Djibouti'),('Dominica', 'Dominica'),('Dominican Republic', 'Dominican Republic'),('East Timor', 'East Timor'), ('Ecuador', 'Ecuador'),('Egypt', 'Egypt'),('El Salvador', 'El Salvador'),('Equatorial Guinea', 'Equatorial Guinea'),('Eritrea', 'Eritrea'),('Estonia', 'Estonia'),('Eswatini (fmr. "Swaziland")', 'Eswatini (fmr. "Swaziland")'),('Ethiopia', 'Ethiopia'),('Fiji', 'Fiji'),('Finland', 'Finland'),('France', 'France'),('Gabon', 'Gabon'),('Gambia', 'Gambia'),('Georgia', 'Georgia'),('Germany', 'Germany'),('Ghana', 'Ghana'),('Greece', 'Greece'),('Grenada', 'Grenada'),('Guatemala', 'Guatemala'),('Guinea', 'Guinea'),('Guinea-Bissau', 'Guinea-Bissau'),('Guyana', 'Guyana'),('Haiti', 'Haiti'),('Holy See', 'Holy See'),('Honduras', 'Honduras'),('Hungary', 'Hungary'),('Iceland', 'Iceland'),('India', 'India'),('Indonesia', 'Indonesia'),('Iran', 'Iran'),('Iraq', 'Iraq'),('Ireland', 'Ireland'),('Israel', 'Israel'),('Italy', 'Italy'),('Ivory Coast', 'Ivory Coast'), ('Jamaica', 'Jamaica'),('Japan', 'Japan'),('Jordan', 'Jordan'),('Kazakhstan', 'Kazakhstan'),('Kenya', 'Kenya'),('Kiribati', 'Kiribati'),('North Korea', 'North Korea'), ('South Korea', 'South Korea'), ('Kosovo', 'Kosovo'), ('Kuwait', 'Kuwait'),('Kyrgyzstan', 'Kyrgyzstan'),('Laos', 'Laos'),('Latvia', 'Latvia'),('Lebanon', 'Lebanon'),('Lesotho', 'Lesotho'),('Liberia', 'Liberia'),('Libya', 'Libya'),('Liechtenstein', 'Liechtenstein'),('Lithuania', 'Lithuania'),('Luxembourg', 'Luxembourg'),('Macedonia', 'Macedonia'),('Madagascar', 'Madagascar'),('Malawi', 'Malawi'),('Malaysia', 'Malaysia'),('Maldives', 'Maldives'),('Mali', 'Mali'),('Malta', 'Malta'),('Marshall Islands', 'Marshall Islands'),('Mauritania', 'Mauritania'),('Mauritius', 'Mauritius'),('Mexico', 'Mexico'),('Micronesia', 'Micronesia'),('Moldova', 'Moldova'),('Monaco', 'Monaco'),('Mongolia', 'Mongolia'),('Montenegro', 'Montenegro'),('Morocco', 'Morocco'),('Mozambique', 'Mozambique'),('Myanmar', 'Myanmar'),('Namibia', 'Namibia'),('Nauru', 'Nauru'),('Nepal', 'Nepal'),('Netherlands', 'Netherlands'),('New Zealand', 'New Zealand'),('Nicaragua', 'Nicaragua'),('Niger', 'Niger'),('Nigeria', 'Nigeria'),('Norway', 'Norway'),('Oman', 'Oman'),('Pakistan', 'Pakistan'),('Palau', 'Palau'),('Panama', 'Panama'),('Papua New Guinea', 'Papua New Guinea'),('Paraguay', 'Paraguay'),('Peru', 'Peru'),('Philippines', 'Philippines'),('Poland', 'Poland'),('Portugal', 'Portugal'),('Qatar', 'Qatar'),('Romania', 'Romania'),('Russian Federation', 'Russian Federation'),('Rwanda', 'Rwanda'),('St Kitts &amp; Nevis', 'St Kitts &amp; Nevis'),('St Lucia', 'St Lucia'),('Saint Vincent &amp; the Grenadines', 'Saint Vincent &amp; the Grenadines'),('Samoa', 'Samoa'),('San Marino', 'San Marino'),('Sao Tome &amp; Principe', 'Sao Tome &amp; Principe'),('Saudi Arabia', 'Saudi Arabia'),('Senegal', 'Senegal'),('Serbia', 'Serbia'),('Seychelles', 'Seychelles'),('Sierra Leone', 'Sierra Leone'),('Singapore', 'Singapore'),('Slovakia', 'Slovakia'),('Slovenia', 'Slovenia'),('Solomon Islands', 'Solomon Islands'),('Somalia', 'Somalia'),('South Africa', 'South Africa'),('South Sudan', 'South Sudan'),('Spain', 'Spain'),('Sri Lanka', 'Sri Lanka'),('Sudan', 'Sudan'),('Suriname', 'Suriname'),('Swaziland', 'Swaziland'),('Sweden', 'Sweden'),('Switzerland', 'Switzerland'),('Syria', 'Syria'),('Taiwan', 'Taiwan'),('Tajikistan', 'Tajikistan'),('Tanzania', 'Tanzania'),('Thailand', 'Thailand'),('Togo', 'Togo'),('Tonga', 'Tonga'),('Trinidad &amp; Tobago', 'Trinidad &amp; Tobago'),('Tunisia', 'Tunisia'),('Turkey', 'Turkey'),('Turkmenistan', 'Turkmenistan'),('Tuvalu', 'Tuvalu'),('Uganda', 'Uganda'),('Ukraine', 'Ukraine'),('United Arab Emirates', 'United Arab Emirates'),('United Kingdom', 'United Kingdom'),('United States', 'United States'),('Uruguay', 'Uruguay'),('Uzbekistan', 'Uzbekistan'),('Vanuatu', 'Vanuatu'),('Vatican City', 'Vatican City'),('Venezuela', 'Venezuela'),('Vietnam', 'Vietnam'), ('Yemen', 'Yemen'),('Zambia', 'Zambia'),('Zimbabwe', 'Zimbabwe')])
    cc_type = SelectField('cc_type', validators=[InputRequired('You must select a valid credit card type.')], choices=[('VISA', 'VISA'),('MASTER CARD', 'MASTER CARD'),('AMEX', 'AMEX'),('DISCOVER', 'DISCOVER'), ('PREPAID', 'PREPAID')])
    cc_num = StringField('cc_num', validators=[InputRequired('You must enter in a valid credit card number.'),Length(min=0, max=20, message='Credit Card Number format: ####-####-####-####'),Regexp('^(\d{4})-(\d{4})-(\d{4})-(\d{4})$', message='Regex does not match. Credit Card Number Format: ####-####-####-####.')])
    sec_num = StringField('sec_num', validators=[InputRequired('You must enter in a valid security number.'),Length(min=3, max=4, message='Security Numbre format: ###'),Regexp('^(\d{3})', message='Regex does not match. Security Number Format: ###(#).')])


class ForgotPWForm(FlaskForm):
    email = StringField('email', validators=[InputRequired('You must enter an email'), Email(message='You must enter a valid email format')])


class ResetPWForm(FlaskForm):
    username = StringField(label='username', validators=[InputRequired('You must enter a Username'), Length(min=5, max=25, message='Username must be between 5 and 25 chars.')])
    password = PasswordField('password', validators=[InputRequired('Password: @ least 1 digit, @ least 1 upper-case char, @ least 1 lower-case char, @ least 1 special char.'), Length(min=8, max=25, message='Password must be 8 to 25 chars long.'), Regexp('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$', message='Regex does not match.')])
    check_password = PasswordField('check_password', validators=[InputRequired('Password: @ least 1 digit, @ least 1 upper-case char, @ least 1 lower-case char, @ least 1 special char.'), Length(min=8, max=25, message='Password must be 8 to 25 chars long.'), Regexp('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$', message='Regex does not match.'), EqualTo('password', message='Your password entries must match each other.')])


'''
##############################################################################################################
################################# HELPER FUNCTIONS ###########################################################
##############################################################################################################
'''
def temp_pw_generator():
    upper_case = random.choice(string.ascii_letters).upper()
    lower_case_chars = ''
    numbers = ''
    for each in range(4):
        lower_case_chars += random.choice(string.ascii_letters).lower()

    for each in range(3):
        numbers += random.choice(string.digits)

    special_char = '@'
    temp_pw = upper_case + lower_case_chars + numbers + special_char
    return temp_pw


'''
####################################################################################################
################################# Routes ###########################################################
####################################################################################################

These are the routes defined for the Where Is My Book? Application.

'''


@app.route('/profile')
@login_required
def profile():
    return f'<h1>You are in the protected profile of: User ID: {current_user.id}, Username: {current_user.username}</h1>'


@app.route('/checkadmin')
@login_required
def checkadmin():
    if current_user.is_authenticated and current_user.user_role != 'Admin':
        return '<h1>You are logged in but you are NOT admin.</h1>'
    return '<h1>You are logged in AND you are admin'


@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = AuthRegForm()

    if reg_form.validate_on_submit():
        email = reg_form.email.data
        username = reg_form.username.data
        password = reg_form.password.data
        check_password = reg_form.check_password.data
        print(f'The returned email: {email}')
        print(f'The returned username: {username}')
        print(f'The returned password: {password}')
        print(f'The returned password: {check_password}')
        # hash the validated password
        password_hashed = generate_password_hash(password, method='sha256')
        # create database entry
        new_user = User(username=username, password=password_hashed, user_role='user', user_email=email)
        # insert new user into database
        db.session.add(new_user)
        # commit transaction to database
        db.session.commit()
        # locate the new user in the database
        located_user = User.query.filter_by(username=username).first()
        # log them in
        login_user(located_user, remember=False)
        # After login it goes to a route but we can have a simple confirmation page (we have to decide)
        return redirect(url_for('new_user'))
    return render_template('registration.html', reg_form=reg_form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    forgot_pw_form = ForgotPWForm()
    # POST
    if forgot_pw_form.validate_on_submit():
        # collect data from the forgot password form
        valid_email = forgot_pw_form.email.data
        # look up the user in the database
        verify_user = User.query.filter_by(user_email=valid_email).first()
        print(f"User found for email recovery: {verify_user}")
        # if the user can be found via unique email
        if verify_user:
            # generate a temp pw
            temp_pw = temp_pw_generator()
            # reset the current user's pw with temp pw AND set password_reset = True
            print(f"verified user's password before change: {verify_user.password}")
            password_hashed = generate_password_hash(temp_pw, method='sha256')
            verify_user.password = password_hashed
            print(f"verified user's password after change: {verify_user.password}")
            # change password_reset to True
            verify_user.password_reset = 'True'
            db.session.commit()

            pw_reset_instructions = f'''
            #### PASSWORD RESET ####

            Please login with these credentials:
            Username: {verify_user.username}
            Temporary Password: {temp_pw}

            Note:
            -------
            When you login with your temporary password. There will be a "Reset Username/Password" tab in the navigation.
            You are required to reset your username and/or password once you activate recovery. If you feel
            like browsing or continuing to use the temporary password for now, you may. The "Reset Username/Password" tab
            will remain in the navigation until you reset the password. Feel free to do it anytime you wish.
            Happy shopping.
            '''
            # send an email to the user with temp pw
            with mail.connect() as conn:
                msg = Message(subject="CPSC 462 - Group 8 Project: Password Recovery", sender=app.config.get("MAIL_USERNAME"), recipients=[valid_email], body=pw_reset_instructions)
                conn.send(msg)
            return redirect(url_for('login'))
    # GET
    return render_template('forgot_password.html', forgot_pw_form=forgot_pw_form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    reset_pw_form = ResetPWForm()
    # POST
    if reset_pw_form.validate_on_submit():
        # get current user object
        found_user = User.query.filter_by(username=current_user.username).first()
        found_user.username = reset_pw_form.username.data
        password_hashed = generate_password_hash(reset_pw_form.password.data, method='sha256')
        found_user.password = password_hashed
        # set password_reset back to false
        found_user.password_reset = 'False'
        db.session.commit()

        return render_template('reset_confirm.html')

    # GET
    return render_template('reset_password.html', reset_pw_form=reset_pw_form)

@app.route('/new_user')
def new_user():
    # user was automatically logged in after successful registration via /register route
    return render_template('new_user_page.html', current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = AuthLoginForm()

    if login_form.validate_on_submit():
        # query database to verify username
        username = login_form.username.data
        print(f'The returned username: {username}')
        password = login_form.password.data
        print(f'The returned password: {password}')
        remember_me = login_form.remember_me.data
        print(f'Remember Me Value: {remember_me}')
        verify_user = User.query.filter_by(username=username).first()

        # if valid username is found
        if verify_user != None:
            db_pw_hash = verify_user.password
            print(f'Database pw hash: {db_pw_hash}')
            print('DEBUG: username is valid')
            # compare DB password hash to hashed user login password
            if check_password_hash(db_pw_hash, password):
                login_user(verify_user, remember=remember_me)
            else:
                return render_template('login.html', login_form=login_form, success=False)
        else:
            return redirect(url_for('noexist'))


        if 'next' in session and session['next']:
            if is_safe_url(session['next']):
                return redirect(session['next'])

        # if that does not work, redirect to home page (if nothing in session).
        return redirect(url_for('index'))

    # get route tried to go to but could not because of not being logged in.
    session['next'] = request.args.get('next')
    # GET request
    return render_template('login.html', login_form=login_form, success=None)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/noexist')
def noexist():
    return render_template('no_exist.html')


@app.route('/noauth')
def noauth():
    return render_template('error_no_auth.html')


@app.route('/_image-url')
def _get_image_url():
    img_id = request.args.get('img_id')
    img = ImageUploads.query.get(img_id)
    if img is None:
        response = jsonify(status='not found')
        return response
    return jsonify(img_path=img.path, status='ok')


@app.route('/account', methods=['GET', 'POST', 'PUT'])
def account():
    # if user is not logged in
    if not current_user.is_authenticated:
        return render_template('error_no_auth.html')

    # if user is logged in:
    update_form = UserDetailsUpdateForm()

    current_user_id = current_user.id
    found_user = UserDetails.query.filter(UserDetails.id == current_user_id).first()

    # if the form is validated and the user has no details entered
    if update_form.validate_on_submit() and found_user == None:
        print('The user update form validated successfully.')
        # query database to verify username
        first_name = update_form.first_name.data
        last_name = update_form.last_name.data
        email = update_form.email.data
        phone = update_form.phone.data
        addr = update_form.addr.data
        city = update_form.city.data
        state = update_form.state.data
        country = update_form.country.data
        zip_code = update_form.zip_code.data
        cc_type = update_form.cc_type.data

        # fetch logged in user id
        logged_in_user_id = current_user.id
        print(logged_in_user_id)
        # create database entry with correct id of logged in user
        update_user_details = UserDetails(id=logged_in_user_id, first_name=first_name, last_name=last_name, email=email, phone=phone, addr=addr, city=city, state=state, zip=zip_code, country=country, cc_type=cc_type)
        print(update_user_details)
        #add the row
        db.session.add(update_user_details)
        # commit transaction to database
        db.session.commit()
        #redirect to account, so it shows current data in the database for that user
        return redirect(url_for('account'))

    #else if user has a details row, then just perform an update
    elif update_form.validate_on_submit() and found_user != None:
        # just add the fields that need updating
        if update_form.first_name.data != '':
            found_user.first_name = update_form.first_name.data
        if update_form.last_name.data != '':
            found_user.last_name = update_form.last_name.data
        if update_form.email.data != '':
            found_user.email = update_form.email.data
        if update_form.phone.data != '':
            found_user.phone = update_form.phone.data
        if update_form.addr.data != '':
            found_user.addr = update_form.addr.data
        if update_form.city.data != '':
            found_user.city = update_form.city.data
        if update_form.state.data != '':
            found_user.state = update_form.state.data
        if update_form.zip_code.data != None:
            found_user.zip = update_form.zip_code.data
        if update_form.country.data != '':
            found_user.country = update_form.country.data
        if update_form.cc_type.data != '':
            found_user.cc_type = update_form.cc_type.data
        # after all edits are made, commit to database
        db.session.commit()

    #GET: serve the template with current_user object
    return render_template('user_details_update.html', current_user=current_user, update_form=update_form, found_user=found_user)


#################### STORE API #######################
import pugsql

queries = pugsql.module('store_queries/')
queries.connect(app.config['SQLALCHEMY_DATABASE_URI'])

##### ADDITIONAL CART RELATED FUNCTIONS #####
class CartManager:
    @staticmethod
    def createCart():
        session['cart'] = dict()
        session.modified = True

    @staticmethod
    def addItem(itemID, quantity):
        if itemID not in session['cart']:
            session['cart'][itemID] = 0
        session['cart'][itemID] += quantity
        session.modified = True

    @staticmethod
    def updateItem(itemID, quantity):
        if itemID in session['cart']:
            if quantity > 0:
                session['cart'][itemID] = quantity
            else:
                session['cart'].pop(itemID)
            session.modified = True

    @staticmethod
    def getBookIDsInCart():
        book_ids = []
        for key in session['cart']:
            app.logger.info("book id key:" + key)
            book_ids.append(key)
        return book_ids

    @staticmethod
    def getBookQuantity(itemID):
        if itemID not in session['cart']:
            return 0
        return session['cart'][itemID]

    @staticmethod
    def getBookQuantities():
        return session['cart']

    @staticmethod
    def clearCart():
        session['cart'] = dict()
        session.modified = True

####### ROUTES #######

#### STORE ROUTES
# demo route to demonstrate Bootstrap 4 card usage
@app.route('/', methods=['GET', 'POST'])
def index():
    all_books = list(queries.get_all_books_and_statuses_and_genres())
    editors_books = list(queries.get_all_books_w_images_by_status_with_genres(status="Editor's Choice"))
    most_popular = list(queries.get_all_books_w_images_by_status_with_genres(status="Most Popular"))
    monthly_specials = list(queries.get_all_books_w_images_by_status_with_genres(status="Monthly Specials"))
    scifi_books = list(queries.get_all_books_w_images_by_genre_with_statuses(genre="Sci-Fi"))
    return render_template('index.html', all_books=all_books, editors_books=editors_books, most_popular=most_popular, monthly_specials=monthly_specials, scifi_books=scifi_books)


@app.route('/book/<int:book_id>', methods=['GET'])
def getbook(book_id):
    book = queries.get_book_by_id(book_id=book_id)
    audiosample = book['audio_id']

    # If no audio sample, create audio sample
    if audiosample == None:
        text = """
        <speak>
        <amazon:domain name="conversational">
        """ + book['sample'] + """
        </amazon:domain>
        </speak>
        """

        arguments = [
                "python",
                "../tts/tts.py",
                "-t",
                text,
                "-f",
                book['title'] + "_v3"
        ]
        cp = subprocess.run(arguments)

        if cp.returncode == 0:
            audio_id = queries.create_audio_entry(name=(book['title'] + "_audio_v3"), path=("audio/"+ book['title']+"_v3.mp3"))
            queries.set_audio_id(book_id=book_id, audio_id=audio_id)
            audiosample = queries.get_audio_sample(audio_id=book['audio_id'])
    else:
        audiosample = queries.get_audio_sample(audio_id=book['audio_id'])

    if book == None:
        return "Book not found!"
    reviews = list(queries.get_book_reviews(book_id=book_id))
    return render_template('store_templates/book.html', book=book, reviews=reviews, current_user=current_user, audiosample=audiosample)


@app.route('/book/<int:book_id>/newreview', methods=['POST'])
@login_required
def addReview(book_id):
    if current_user.is_authenticated:

        book = queries.get_book_by_id(book_id=book_id)
        if book == None:
            return "Invalid Request!"

        review = request.form['review']
        if len(review) > 0:
            app.logger.info("posted this review:" + review)
            queries.add_new_book_review(book_id=book_id, user_id=current_user.id, review=review)
    return redirect(url_for('getbook', book_id=book_id))

@app.route('/book/search')
def search():
    # Need to make this so that we create the table only every once in a while.
    queries.delete_vbook_table()
    queries.create_vbook_table()
    queries.populate_vbook_table()

    # Extract search parameters
    searchString = ""
    genreFilters = list()
    priceFilters = list()

    # Get genres for selection
    genres = list(queries.get_all_genres())
    books = None

    for filter in request.args:
        if 'search' in filter:
            for token in request.args[filter].split(' '):
                if token.isalnum():
                    searchString += token + '* AND '
            if len(searchString) > 5:
                searchString = searchString[:-5]
            #return searchString
        elif 'genre' in filter:
            genreFilters.append(request.args[filter])
        elif 'price' in filter:
            values = request.args[filter].split('-')
            if len(values) < 2 and values[0] == '5':
                priceFilters.append(0)
            for value in values:
                priceFilters.append(int(value))
            if len(values) < 2 and values[0] == '30':
                priceFilters.append(999999999)

    # query for book ids based on filters
    book_ids = set()
    if len(priceFilters) > 0:
        for i in range(0, len(priceFilters), 2):
            result = queries.fts_bids_by_p(minBound=priceFilters[i], maxBound=priceFilters[i+1])
            book_ids.update(set({r['book_id'] for r in result}))
    if len(genreFilters) > 0:
        result = queries.fts_bids_by_g(genre_ids=genreFilters)
        if len(book_ids) > 0:
            book_ids = book_ids.intersection(set({r['book_id'] for r in result}))
        else:
            book_ids.update(set({r['book_id'] for r in result}))

    # Set book id filters
    fts_bids = ''
    for id in book_ids:
        if len(fts_bids) > 0:
            fts_bids += ' OR '
        fts_bids += str(id)

    # Create fts5 match query
    query = ''
    if len(searchString) > 1:
        query += '( ' + searchString + ' )'
    if len(fts_bids) > 0:
        if len(query) > 1:
            query += ' AND '
        query += '( book_id : (' + fts_bids + ') )'

    # Execute query
    if(len(query) > 1):
        books = queries.fts5_search(query_string=query)

    # Render page
    return render_template('store_templates/search_results.html', books=books, genres=genres)

@app.route('/cart/<int:book_id>/newitem', methods=['POST'])
def addItemToCart(book_id):
    quantity = request.form['quantity']
    if 'cart' not in session:
        CartManager.createCart()

    # Need to validate book id and quantity
    book = queries.get_book_by_id(book_id=book_id)
    if book == None:
        return "Book not found!"

    if int(quantity) <= 0:
        return "Invalid Quantity!"

    CartManager.addItem(str(book_id), int(quantity))
    totalQuantity = CartManager.getBookQuantity(str(book_id))
    return render_template('store_templates/add_to_cart_confirmation.html', quantity=quantity, book=book, totalQuantity=totalQuantity)

@app.route('/cart', methods=['GET', 'POST'])
def manageCart():
    if request.method == 'POST':
        for key in request.form:
            CartManager.updateItem(key, int(request.form[key]))
    if 'cart' in session and len(session['cart']) > 0:
        book_ids = CartManager.getBookIDsInCart()
        quantitiesById = CartManager.getBookQuantities()
        booksInCart = list(queries.get_books_by_ids(book_ids=book_ids))

        # set accumulator to collect order summary values
        summary_values = {'total_books':0, 'cumulative_bf_tax':0.0, 'cumulative_tax': 0.0, 'cumulative_after_tax': 0.0}

        for book in booksInCart:
            book['quantity'] = quantitiesById[str(book['book_id'])]
            # add to summary book quantity
            summary_values['total_books'] += book['quantity']

            book['total_price_before_tax'] = book['quantity'] * book['price']
            # add to summary cumulative total price before tax
            summary_values['cumulative_bf_tax'] += book['total_price_before_tax']

            book['tax'] = book['total_price_before_tax'] * 0.07
            # add to summary cumulative total tax
            summary_values['cumulative_tax'] += book['tax']

            book['total_price_after_tax'] = book['total_price_before_tax'] + book['tax']
            # add to summary cumulative total after tax
            summary_values['cumulative_after_tax'] += book['total_price_after_tax']
        return render_template('store_templates/cart.html', booksInCart=booksInCart, summary_values=summary_values)
    return render_template('store_templates/empty_cart.html')

# Temporary suggestion for fixing the issue of needing to sign in to purchase a book
class DetailsManager:
    @staticmethod
    def createDetails():
        session['details'] = dict()
        session['details']['isSet'] = False
        session.modified = True

    @staticmethod
    def putValue(key, value):
        if key not in session['details']:
            session['details'][key] = '?'
        session['details'][key] = value
        session.modified = True

    @staticmethod
    def setByUser(user):
        session['details']['first_name'] = user.first_name
        session['details']['last_name'] = user.last_name
        session['details']['email'] = user.email
        session['details']['phone'] = user.phone
        session['details']['addr'] = user.addr
        session['details']['city'] = user.city
        session['details']['state'] = user.state
        session['details']['country'] = user.country
        session['details']['zip'] = user.zip
        session['details']['cc_type'] = user.cc_type
        session['details']['cc_num'] = user.cc_num
        session['details']['sec_num'] = user.sec_num
        session['details']['isSet'] = True
        session.modified = True

    @staticmethod
    def isSet():
        if 'details' in session:
            return session['details']['isSet']
        return False

    @staticmethod
    def setIsSet(val):
        if 'details' in session:
            session['details']['isSet'] = val

    @staticmethod
    def getValue(key, value):
        for key in session['details']:
            app.logger.info("book id key:" + key)
            return session['details'][key]
        return None

    @staticmethod
    def getAll():
        if 'details' in session:
            if session['details']['isSet']:
                return session['details']
        return None

    @staticmethod
    def hasDetailsInstance():
        return 'details' in session

    @staticmethod
    def clearDetails():
        session['details'] = dict()
        session['details']['isSet'] = False
        session.modified = True

    @staticmethod
    def commitToDatabase(userID):
        if 'details' in session:
            user_details = UserDetails.query.filter(UserDetails.id == userID).first()
            if user_details == None:
                # create database entry with correct id of logged in user
                update_user_details = UserDetails(
                    user_id=userID,
                    first_name=session['details']['first_name'],
                    last_name=session['details']['last_name'],
                    email=session['details']['email'],
                    phone=session['details']['phone'],
                    addr=session['details']['addr'],
                    city=session['details']['city'],
                    state=session['details']['state'],
                    zip=session['details']['zip'],
                    country=session['details']['country'],
                    cc_type=session['details']['cc_type'],
                    cc_num=session['details']['cc_num'],
                    sec_num=session['details']['sec_num']
                )
                #add the row
                db.session.add(update_user_details)
            else:
                user_details.first_name=session['details']['first_name']
                user_details.last_name=session['details']['last_name']
                user_details.email=session['details']['email']
                user_details.phone=session['details']['phone']
                user_details.addr=session['details']['addr']
                user_details.city=session['details']['city']
                user_details.state=session['details']['state']
                user_details.zip=session['details']['zip']
                user_details.country=session['details']['country']
                user_details.cc_type=session['details']['cc_type']
                user_details.cc_num=session['details']['cc_num']
                user_details.sec_num=session['details']['sec_num']
            db.session.commit()

@app.route('/checkout', methods=['GET', 'POST', 'PUT'])
def checkout():
    # Declarations
    update_form = CheckoutForm()
    found_user = None

    # Initializations
    if not DetailsManager.hasDetailsInstance():
        DetailsManager.createDetails()

    if current_user.is_authenticated:
        current_user_id = current_user.id
        user_details = UserDetails.query.filter(UserDetails.id == current_user_id).first()
        if user_details != None:
            DetailsManager.setByUser(user_details)

    found_user = DetailsManager.getAll()

    # Submissions
    # if the form is validated and the user has no details entered
    if update_form.validate_on_submit() and found_user == None:
        print('The user update form validated successfully.')
        # query database to verify username
        DetailsManager.putValue('first_name', update_form.first_name.data)
        DetailsManager.putValue('last_name', update_form.last_name.data)
        DetailsManager.putValue('email', update_form.email.data)
        DetailsManager.putValue('phone', update_form.phone.data)
        DetailsManager.putValue('addr', update_form.addr.data)
        DetailsManager.putValue('city', update_form.city.data)
        DetailsManager.putValue('state', update_form.state.data)
        DetailsManager.putValue('country', update_form.country.data)
        DetailsManager.putValue('zip', update_form.zip_code.data)
        DetailsManager.putValue('cc_type', update_form.cc_type.data)
        DetailsManager.putValue('cc_num', update_form.cc_num.data)
        DetailsManager.putValue('sec_num', update_form.sec_num.data)
        DetailsManager.setIsSet(True)
        if current_user.is_authenticated:
            DetailsManager.commitToDatabase(current_user.id)
        return redirect(url_for('confirmation'))
    elif update_form.validate_on_submit() and found_user != None:
        # just add the fields that need updating
        if update_form.first_name.data != '':
            DetailsManager.putValue('first_name', update_form.first_name.data)
        if update_form.last_name.data != '':
            DetailsManager.putValue('last_name', update_form.last_name.data)
        if update_form.email.data != '':
            DetailsManager.putValue('email', update_form.email.data)
        if update_form.phone.data != '':
             DetailsManager.putValue('phone', update_form.phone.data)
        if update_form.addr.data != '':
            DetailsManager.putValue('addr', update_form.addr.data)
        if update_form.city.data != '':
            DetailsManager.putValue('city', update_form.city.data)
        if update_form.state.data != '':
            DetailsManager.putValue('state', update_form.state.data)
        if update_form.zip_code.data != None:
            DetailsManager.putValue('zip', update_form.zip_code.data)
        if update_form.country.data != '':
            DetailsManager.putValue('country', update_form.country.data)
        if update_form.cc_type.data != '':
            DetailsManager.putValue('cc_type', update_form.cc_type.data)
        if update_form.cc_num.data != '':
            DetailsManager.putValue('cc_num', update_form.cc_num.data)
        if update_form.sec_num.data != '':
            DetailsManager.putValue('sec_num', update_form.sec_num.data)
        # after all edits are made, commit to database
        if current_user.is_authenticated:
            DetailsManager.commitToDatabase(current_user.id)
        return redirect(url_for('confirmation'))

    # Prepare cart details
    booksInCart = list()
    if 'cart' in session and len(session['cart']) > 0:
        book_ids = CartManager.getBookIDsInCart()
        quantitiesById = CartManager.getBookQuantities()
        booksInCart = list(queries.get_books_by_ids(book_ids=book_ids))

        summary_values = {'total_books':0, 'cumulative_bf_tax':0.0, 'cumulative_tax': 0.0, 'cumulative_after_tax': 0.0, 'grand_total_plus_shipping':0.0}
        for book in booksInCart:
            book['quantity'] = quantitiesById[str(book['book_id'])]
            # add to summary book quantity
            summary_values['total_books'] += book['quantity']

            book['total_price_before_tax'] = book['quantity'] * book['price']
            # add to summary cumulative total price before tax
            summary_values['cumulative_bf_tax'] += book['total_price_before_tax']

            book['tax'] = book['total_price_before_tax'] * 0.07
            # add to summary cumulative total tax
            summary_values['cumulative_tax'] += book['tax']

            book['total_price_after_tax'] = book['total_price_before_tax'] + book['tax']
            # add to summary cumulative total after tax
            summary_values['cumulative_after_tax'] += book['total_price_after_tax']

        summary_values['grand_total_plus_shipping'] = (summary_values['cumulative_after_tax'] + 8.0)

    return render_template('store_templates/checkout.html', current_user=current_user, update_form=update_form, found_user=found_user, booksInCart=booksInCart, summary_values=summary_values)

@app.route('/confirmation')
def confirmation():
    if not DetailsManager.hasDetailsInstance() or not DetailsManager.isSet():
        return "Missing user details for order."

    if 'cart' not in session or len(session['cart']) <= 0:
        return "Error placing order. Cart not found."

    found_user = DetailsManager.getAll()

    # Add order to the book orders table
    order = queries.add_new_book_order(
        first_name=found_user['first_name'],
        last_name=found_user['last_name'],
        email=found_user['email'],
        phone=found_user['phone'],
        addr=found_user['addr'],
        city=found_user['city'],
        state=found_user['state'],
        country=found_user['country'],
        zip=found_user['zip'],
        cc_type=found_user['cc_type'],
        cc_num=found_user['cc_num'],
        sec_num=found_user['sec_num'],
        order_status="Order Placed."
    )

    book_ids = CartManager.getBookIDsInCart()
    quantitiesById = CartManager.getBookQuantities()

    for book_id in book_ids:
        queries.add_new_book_order_item(
            qty=quantitiesById[str(book_id)],
            order_id=order,
            book_id=book_id
        )

    # Order Confirmation message to email customer

    # Summary:
    booksInCart = list()
    if 'cart' in session and len(session['cart']) > 0:
        book_ids = CartManager.getBookIDsInCart()
        quantitiesById = CartManager.getBookQuantities()
        booksInCart = list(queries.get_books_by_ids(book_ids=book_ids))

        summary_values = {'total_books':0, 'cumulative_bf_tax':0.0, 'cumulative_tax': 0.0, 'cumulative_after_tax': 0.0, 'grand_total_plus_shipping':0.0}
        for book in booksInCart:
            book['quantity'] = quantitiesById[str(book['book_id'])]
            # add to summary book quantity
            summary_values['total_books'] += book['quantity']

            book['total_price_before_tax'] = book['quantity'] * book['price']
            # add to summary cumulative total price before tax
            summary_values['cumulative_bf_tax'] += book['total_price_before_tax']

            book['tax'] = book['total_price_before_tax'] * 0.07
            # add to summary cumulative total tax
            summary_values['cumulative_tax'] += book['tax']

            book['total_price_after_tax'] = book['total_price_before_tax'] + book['tax']
            # add to summary cumulative total after tax
            summary_values['cumulative_after_tax'] += book['total_price_after_tax']

        summary_values['grand_total_plus_shipping'] = (summary_values['cumulative_after_tax'] + 8.0)

    #########################
    ordered_books='\n'
    for book in booksInCart:
        ordered_books += book['title'] + '  for  ' + '  $' + str(book['price']) + ' each ' + '  Qty:  ' + str(book['quantity']) + '\n'

    order_confirm_msg = f'''
    \nOrder Confirmation:
    ------------------------
    \nYour order has been submitted. You should receive your order within 4 business days.
    \nOrder Summary:
    ------------------------
    \nTotal Books: {summary_values['total_books']}
    \nPrice Before Tax: ${format(summary_values['cumulative_bf_tax'], ".2f")}
    \nTax: + ${format(summary_values['cumulative_tax'], ".2f")}
    \nPrice After Tax: ${format(summary_values['cumulative_after_tax'], ".2f")}
    \nGrand Total (plus shipping): ${format(summary_values['grand_total_plus_shipping'], ".2f")}

    \nOrdered Items:
    ------------------------
    {ordered_books}
    '''
    # send an email to customer to confirm order
    with mail.connect() as conn:
        msg = Message(subject="CPSC 462 - Group 8 Project: Order Confirmation", sender=app.config.get("MAIL_USERNAME"), recipients=[found_user['email']], body=order_confirm_msg)
        conn.send(msg)
    # END email order confirmation section

    # Clear cart
    CartManager.clearCart()

    # Show success
    return render_template('store_templates/confirmation.html')


@app.route('/about', methods=['GET', 'POST'])
def about():


    return render_template('about.html')

'''
####################################################################################################
################################# Application Gateway ##############################################
####################################################################################################

Run the application.
REMEMBER: Comment this out so you can run: flask run
'''
# if __name__ == '__main__':
#   app.run(debug=True)

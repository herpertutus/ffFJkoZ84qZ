
from sqlite3 import Date
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, TelField, DateField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp


#creates the login information
class LoginForm(FlaskForm):
    username=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    username= StringField("User Name", validators=[InputRequired(),
                                                   Length(min= 0, max= 20, message="Username is too long")])
    email = StringField("Email Address", validators=[InputRequired(),
                                                     Email("Please enter a valid email"),
                                                     Length(min= 0, max= 35, message="Please enter a valid email")])
    phnumber = TelField("Phone Number", validators=[InputRequired(),
                                                    Length(min= 10, max= 10, message="Enter valid phone number"),
                                                    Regexp(r'\d+',message="Must be a digit")])
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", [InputRequired(),
                                          EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Submit")

class CreateEventForm(FlaskForm):
    name = StringField("Event Name", validators=[InputRequired()])
    speaker = StringField("Event Speaker", validators=[InputRequired()])
    tickets = IntegerField("Available Tickets", validators=[InputRequired()])
    price = IntegerField("Ticket Price", validators=[InputRequired()])
    category = SelectField("Event Category", choices=[('mathcategory','math'), ('sciencecategory','science'), ('technologycategory','technology'), ('socialcategory','social'), ('businesscategory','business')], validators=[InputRequired()])
    status = SelectField("Event Category", choices=[('Unpublished'), ('Open'), ('Closed')], validators=[InputRequired()])
    description = TextAreaField("Event Description", validators=[InputRequired(), Length(min=0, max= 200, message="description is too long")])
    date = StringField("Event Date", validators=[InputRequired()])
    image = StringField("Event Image URL", [InputRequired()])
    submit = SubmitField("Submit")

class PurchaseForm(FlaskForm):
    tickets = IntegerField("Ticket Quantity", validators=[InputRequired()])
    submit = SubmitField("Submit")
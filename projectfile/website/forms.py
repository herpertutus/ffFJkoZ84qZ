
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, TelField
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
    submit = SubmitField("Register")


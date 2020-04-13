from flask import render_template,flash,redirect,request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User,Volunteer,NGO,Donations

class LoginForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired()])
	password=StringField('Password',validators=[DataRequired()])
	remember_me=BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class LoginFormNgo(FlaskForm):
	orgname=StringField('Organization name',validators=[DataRequired()])
	password=StringField('Password',validators=[DataRequired()])
	remember_me=BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegFormNgo(FlaskForm):
    orgname=StringField('Organization Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    field_of_work=StringField('Field of Work',validators=[DataRequired()])
    about=StringField('About the Organization',validators=[DataRequired()])
    submit = SubmitField('Register')
    def validate_username(self,orgname):
        ngo=NGO.query.filter_by(orgname=orgname.data).first()
        if ngo is not None:
            raise ValidationError('Please use a different name for your organization.')

    def validate_email(self, email):
        org_email=NGO.query.filter_by(email=email.data).first()
        if org_email is not None:
            raise ValidationError('Please use a different email address.')
    	

class RegFormV(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    about = StringField('About You',validators=[DataRequired()])
    related_with=StringField('Affiliated Organization',validators=[DataRequired()])
    submit = SubmitField('Register')
    def validate_username(self, username):
        vol = Volunteer.query.filter_by(uname=username.data).first()
        if vol is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Volunteer.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
    def validate_affiliation(self,related_with):
        org=NGO.query.filter_by(orgname=related_with.data).first()
        if org is not None:
            raise ValidationError('Please enter a valid organization name.')
    	

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class DonationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    orgname=StringField('Organization name', validators=[DataRequired()])
    amount=IntegerField('Amount', validators=[DataRequired()])
    submit=SubmitField('Donate')
    
    def validate_username(self, username):
        usern=User.query.filter_by(username=username.data).first()
        userm=Volunteer.query.filter_by(uname=username.data).first()
        if usern is None and userm is None:
            raise ValidationError('No such user.')
    
    def validate_orgname(self, orgname):
        orgn=NGO.query.filter_by(orgname=orgname.data).first()
        if orgn is None:
            raise ValidationError('No such organization.')


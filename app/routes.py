from flask import render_template,flash,redirect,request
from app import app
from app.forms import LoginForm,LoginFormNgo,RegistrationForm,RegFormV,RegFormNgo,DonationForm
from app import db
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Volunteer,NGO,Donations
from werkzeug.urls import url_parse
from flask_socketio import SocketIO
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
socketio=SocketIO(app)
bot=ChatBot("Beku", storage_adapter="chatterbot.storage.SQLStorageAdapter")
#bot=ChatterBotCorpusTrainer(ebot)

#bot.set_trainer(ListTrainer)
ebot=ListTrainer(bot)
ebot.train(['What is your name?', 'My name is Beku'])
ebot.train(['What is your name', 'My name is Beku'])
ebot.train(['what is your name?', 'My name is Beku'])
ebot.train(['what is your name', 'My name is Beku'])
ebot.train(['Who are you?', 'I am a bot' ])
ebot.train(['who are you?', 'I am a bot' ])
ebot.train(['Who are you', 'I am a bot' ])
ebot.train(['who are you', 'I am a bot' ])
ebot.train(['Who created you?', 'I am created by the team at Beku'])
ebot.train(['who created you?', 'I am created by the team at Beku'])
ebot.train(['who created you', 'I am created by the team at Beku'])
ebot.train(['why are you here','I am here to help you :)'])
ebot.train(['Why are you here','I am here to help you :)'])
ebot.train(['Why are you here?','I am here to help you :)'])
ebot.train(['What are the steps to help around here?','You can go through our portfolio,gallery,etc to get an idea of the kind of work that we do.You can then login to donate or join as a volunteer as well.You can also start your own fundraiser. :D'])
ebot.train(['how can i help around here?','You can go through our portfolio,gallery,etc to get an idea of the kind of work that we do.You can then login to donate or join as a volunteer as well.You can also start your own fundraiser. :D'])
ebot.train(['what kind of work do you do','You can go through our portfolio,gallery,etc to get an idea of the kind of work that we do'])
ebot.train(['What kind of work do you do?','You can go through our portfolio,gallery,etc to get an idea of the kind of work that we do'])
ebot.train(['how do I donate?','Click on the donate now button,choose the organisation that you want to donate to and donate!'])
ebot.train(['how do i donate?','Click on the donate now button,choose the organisation that you want to donate to and donate!'])
ebot.train(['how do i donate','Click on the donate now button,choose the organisation that you want to donate to and donate!'])
ebot.train(['How do I donate?','Click on the donate now button,choose the organisation that you want to donate to and donate!'])
ebot.train(['How do i join as a volunteer?','Just register yourself as a volunteer and choose the orgainsation that you want to work with :)'])
ebot.train(['how do i join as a volunteer?','Just register yourself as a volunteer and choose the orgainsation that you want to work with :)'])
ebot.train(['how do i join as a volunteer','Just register yourself as a volunteer and choose the orgainsation that you want to work with :)'])
ebot.train(['What is your cause about?','Our aim is to bring people closer to the ngos by providing a platform for doing this seamlessly'])
ebot.train(['what is your cause about','Our aim is to bring people closer to the ngos by providing a platform for doing this seamlessly and help more people.'])
ebot.train("chatterbot.corpus.english")

@app.route('/')
@app.route('/index')
#@login_required
def index():
    #user = {'username': 'Anjali'}
    return render_template('index.html', title='Home')


@app.route('/login',methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect('/index')
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect('/login')
		#set_current_user(user)
		login_user(user,remember=form.remember_me.data)	
		next_page=request.args.get('next')
		if not next_page or url_parse(next_page).netloc!="":
			next_page="/index"
			
		#flash('Login requested for user {},remember_me={}'.format(form.username.data,form.remember_me.data))
		print("ASSA",current_user.username)
		return redirect(next_page)
		
	return render_template('login.html',form=form)




@app.route('/login_v',methods=["GET","POST"])
def loginv():
	if current_user.is_authenticated:
		return redirect('/index')
	form=LoginForm()
	if form.validate_on_submit():
		user=Volunteer.query.filter_by(uname=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			flash('Are you a registered user?')
			return redirect('/login_v')
		#set_current_user(user)
		login_user(user,remember=form.remember_me.data)	
		next_page=request.args.get('next')
		if not next_page or url_parse(next_page).netloc!="":
			next_page="/index"
			
		#flash('Login requested for user {},remember_me={}'.format(form.username.data,form.remember_me.data))
		return redirect(next_page)
		
	return render_template('loginv.html',form=form)



@app.route('/login_ngo',methods=["GET","POST"])
def loginngo():
	if current_user.is_authenticated:
		return redirect('/index')
	form=LoginFormNgo()
	if form.validate_on_submit():
		ngo=NGO.query.filter_by(orgname=form.orgname.data).first()
		if ngo is None or not ngo.check_password(form.password.data):
			flash('Invalid organization name')
			flash('Are you a registered organization')
			return redirect('/login_ngo')
		login_user(ngo,remember=form.remember_me.data)
		next_page=request.args.get('next')
		if not next_page or url_parse(next_page).netloc!="":
			next_page="/index"
		
		return redirect(next_page)

	return render_template('loginngo.html',form=form)


		

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/index')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/index')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)



@app.route('/registervol', methods=['GET', 'POST'])
def registervol():
    if current_user.is_authenticated:
        return redirect('/index')
    form = RegFormV()
    if form.validate_on_submit():
        user = Volunteer(uname=form.username.data, email=form.email.data,about=form.about.data,related_with=form.related_with.data)
        user.set_password(form.password.data)
	
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered Volunteer!')
        return redirect('/login_v')
    return render_template('register_vol.html', title='Register_Vol', form=form)


@app.route('/registerngo',methods=['GET','POST'])
def registerngo():
    if current_user.is_authenticated:
        return redirect('/index')
    form = RegFormNgo()
    if form.validate_on_submit():
        ngo=NGO(orgname=form.orgname.data, email=form.email.data,field_of_work=form.field_of_work.data,about=form.about.data)
        ngo.set_password(form.password.data)
	
        db.session.add(ngo)
        db.session.commit()
        flash('Congratulations, you are now a registered organization!')
        return redirect('/login_ngo')
    return render_template('register_ngo.html', title='Register_Ngo', form=form)

@app.route('/vol/<username>')
def vol(username):
	user = Volunteer.query.filter_by(uname=username).first_or_404()
	return render_template('vol.html',user=user)


@app.route('/ngo/<orgname>')
def ngo(orgname):
	user=NGO.query.filter_by(orgname=orgname).first_or_404()
	return render_template('ngo.html',user=user) 

@login_required
@app.route('/donate',methods=['GET','POST'])
def donate():
 form = DonationForm()
 if form.validate_on_submit():
        donation=Donations(username=form.username.data, orgname=form.orgname.data,amount=form.amount.data)
	
        db.session.add(donation)
        db.session.commit()
        flash('Congratulations, you have donated successfully.')
        return redirect('/donate')
 return render_template('donate.html', title='Donate', form=form)


@app.route('/chat')
def chat():
    #if current_user.is_authenticated:
    flash('Welcome to chat support!')
    return render_template('chat.html')
    #else:
    
    #return redirect('/index')
@app.route("/get")
def get_bot_response():
	userText=request.args.get('msg')
	return str(bot.get_response(userText))

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)




@app.route('/about')
def about():
	
	return render_template('about.html',title='About us')
@app.route('/causes')
def causes():
	
	return render_template('causes.html',title='Causes')
@app.route('/portfolio')
def portfolio():
	
	return render_template('portfolio.html',title='Portfolio')

@app.route('/multistage')
def ms():
	
	return render_template('multistage.html',title='gallery')


'''
@app.route('/news')
def news():
'''	



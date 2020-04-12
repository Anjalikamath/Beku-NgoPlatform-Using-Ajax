from app import app
from app.models import User
from app import db

@app.shell_context_processor 
def msc():
	return {'db':db,'User':User}


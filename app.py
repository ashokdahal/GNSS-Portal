from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, TextField, RadioField, SelectField, FileField, IntegerField, DateField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired
import os,sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from incelery import make_celery
from celery import chain
from random import *
from flask import send_from_directory
from werkzeug import secure_filename
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from dateutil.parser import parse


app = Flask(__name__)
app.debug=True

app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['CELERY_BROKER_URL']='amqp://localhost//'
app.config['CELERY_RESULT_BACKEND']='db+postgresql://postgres:admin@localhost/GNSSportal'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/GNSSportal'


# app.config['SECRET_KEY'] = 'Thisisasecret!'
# app.config['CELERY_BROKER_URL']='amqp://SHt1Xvhb:pnQe-0wfCf7dpU2IFXJMFShYjcZSgIpR@small-fiver-23.bigwig.lshift.net:10123/FlGJwZfbz4TR'
# app.config['CELERY_RESULT_BACKEND']='db+postgres://yzfijjubjpijdv:f9420c6b9add8c5509e78ba977492671fe9f2bf9b62e91daeb67ffed6dfd665f@ec2-54-163-246-193.compute-1.amazonaws.com:5432/dhcbl58v8ifst'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yzfijjubjpijdv:f9420c6b9add8c5509e78ba977492671fe9f2bf9b62e91daeb67ffed6dfd665f@ec2-54-163-246-193.compute-1.amazonaws.com:5432/dhcbl58v8ifst'

db = SQLAlchemy(app)
celery = make_celery(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(APP_ROOT)
ALLOWED_EXTENSIONS_NAV = re.compile(r"(\d{2}(n|nav)$)|([\d{2}]*(nav)$)")
ALLOWED_EXTENSIONS_OBS = re.compile(r"(\d{2}(o|d|obs)$)|([\d{2}]*(obs)$)") 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_filename(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def allowed_filename_NAV(filename):
    return '.' in filename and \
        bool(ALLOWED_EXTENSIONS_NAV.match(filename.rsplit('.', 1)[1].lower()))

def allowed_filename_OBS(filename):
    return '.' in filename and \
        bool(ALLOWED_EXTENSIONS_OBS.match(filename.rsplit('.', 1)[1].lower()))        

class cors_Data(db.Model):
    id=db.Column(db.Integer)
    interval = db.Column(db.String(80))
    lat = db.Column(db.String(120))
    lon = db.Column(db.String(120))
    earliest_d = db.Column(db.DateTime(80))
    latest_dat = db.Column(db.DateTime(80))
    Name = db.Column(db.String(500))
    stnID = db.Column(db.String(6), primary_key=True)
    def __repr__(self):
        return self.stnID
    def __init__(self, id, interval, lat, lon, earliest_d, latest_dat, Name, stnID):
    	self.id = id
    	self.interval = interval
    	self.lat = lat    
    	self.lon = lon
    	self.earliest_d = earliest_d
    	self.latest_dat = latest_dat 
    	self.Name = Name
    	self.stnID=stnID

def choice_query():
	x= cors_Data.query
	return x.stnID

def manipDate(date):
	mylist = []
	mylist.append(date)
	dt = str(mylist[0])
	stripDate=datetime.strptime(dt,'%Y-%m-%d')
	# 1. Day of Year 2. Year Without century 3. Year With Century
	return stripDate.strftime('%j'), stripDate.strftime('%y'), stripDate.strftime('%Y')

def ftplink(date,filetype,station):
	# DOY:=  Day of Year 
	# YWC:=  Year With century 
	# YWOC:= Year Without Century
	DOY, YWOC, YWC = manipDate(date)
	fileName=station.lower()+DOY+'0.'+YWOC+'d.Z'
	fileLink='ftp://data-out.unavco.org/pub/rinex/'+filetype+'/'+YWC+'/'+DOY+'/'+fileName
	return fileLink

def writefiles(startDate,enddate,filetype,station):
    filename = 'Download'+str(randint(10000, 99999))+'.txt'
    file = open(filename,"w+")
    while (startDate <= enddate):
        file.write(ftplink(startDate,filetype,station)+"\n")
        startDate += timedelta(days=1)
    file.close()
    return filename


class My1Form(FlaskForm):
    email = EmailField('Email',[validators.InputRequired(), validators.Email()])
    fileBase = FileField('Base OBS file:',validators=[InputRequired()])
    fileObsRover= FileField('Rover OBS file:',validators=[InputRequired()])
    fileNavRover= FileField('Rover NAV file:',validators=[InputRequired()])
    Name = TextField('Name',validators=[InputRequired()])
    ema = IntegerField('Elevation mask angle',[validators.InputRequired(), validators.NumberRange(min=0, max=89)])
    frq = RadioField('Frequecies', default='option1', choices=[('1', 'L1'), ('2', 'L1 and L2'), ('3', 'L1, L2 and L5')],validators=[InputRequired()])
    pmode = SelectField('Positioning mode', choices=[('1', 'DGPS/DGNSS'), ('2', 'Kinematic'), ('3', 'Static Positioning')],validators=[InputRequired()])

class My2Form(FlaskForm):
    semail = EmailField('Email',[validators.InputRequired(), validators.Email()])    
    sfileObsRover= FileField('Rover OBS file:',validators=[InputRequired()])
    sfileNavRover= FileField('Rover NAV file:',validators=[InputRequired()])
    sName = TextField('Name',validators=[InputRequired()])
    sema = IntegerField('Elevation mask angle',[validators.InputRequired(), validators.NumberRange(min=0, max=89)])
    sfrq = RadioField('Frequecies', default='option1',choices=[('1', 'L1'), ('2', 'L1 and L2'), ('3', 'L1, L2 and L5')], validators=[InputRequired()])

class My3Form(FlaskForm):
    # station = SelectField('Station ID', choices=[('1', 'STPA'), ('2', 'CMB'), ('3', 'BKK')], validators=[InputRequired()])
    station = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label='stnID',validators=[InputRequired()])
    email = EmailField('Email', [validators.InputRequired(), validators.Email()])
    Name = TextField('Name', validators=[InputRequired()])
    startDate = DateField('Start Date (YYYY-MM-DD)',format='%Y-%m-%d',validators=[InputRequired()])
    endDate = DateField('End Date (YYYY-MM-DD)',format='%Y-%m-%d',validators=[InputRequired()])
    FileType = RadioField('File type', default='obs', choices=[('obs', 'obs'), ('nav', 'nav'), ('meteo', 'meteo')], validators=[InputRequired()])
        


# To find type of the variable  type(variable)

@app.route('/')
def index():
    return render_template('index.php')

@app.route('/test')
def test():
    return render_template('test.html')    

@app.route('/download.php', methods=['GET', 'POST'])
def download():
    download = My3Form()
    download.station.query = cors_Data.query.filter(cors_Data.id>0)
    strstnID=str(download.station.data) # Convert Station ID to String Form
    if request.method == 'POST':
	    if download.validate_on_submit():
                global startDBstring
    	    	startDateUser=download.startDate.data
    	    	endDateUser=download.endDate.data          
                startDB=cors_Data.query.filter(cors_Data.stnID==strstnID).first().earliest_d
                endDB=cors_Data.query.filter(cors_Data.stnID==strstnID).first().latest_dat
                startDBstring=str(startDB)
                endDBstring=str(endDB)
                emailAdd=download.email.data
                errorMessage='Data Only available for '+strstnID+ ' from '+startDBstring+' to '+endDBstring
                if ((startDB<startDateUser) and (endDB>endDateUser) and (startDateUser<endDateUser)):
                    a=writefiles(startDateUser,endDateUser,download.FileType.data,strstnID)
                    chain(emailfile.s(a,emailAdd),deletefile.s()).apply_async()
                    return render_template('downloadResult.html',email=emailAdd, Name=download.Name.data, station=strstnID,startDateUser=startDateUser, startDateDb=startDB, FileType=download.FileType.data,endDateUser=endDateUser, endDateDb=endDB)
                else:
                    return render_template('download.php', error=errorMessage, download=download)
    return render_template('download.php', download=download)



@app.route('/SPP.php', methods=['GET', 'POST'])
def SPP():
    SPP = My2Form()
    if request.method == 'POST':
        if SPP.validate_on_submit():
            submitted_file1 = request.files['sfileObsRover'] 
            submitted_file2 = request.files['sfileNavRover']
            a=submitted_file1.filename
            c=submitted_file2.filename
            selevation=str(SPP.sema.data)
            sFreq=SPP.sfrq.data
            emailAdd=SPP.semail.data

            if (submitted_file1 and allowed_filename_OBS(submitted_file1.filename) and submitted_file2 and allowed_filename_NAV(submitted_file2.filename)):
                filename1 = secure_filename(submitted_file1.filename)
                submitted_file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
                filename2 = secure_filename(submitted_file2.filename)
                submitted_file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))                
                chain(processSPP.s(selevation,a,c), emailfile.s(emailAdd), deletefile.s()).apply_async()
                return render_template('results.html', email=emailAdd, Name=SPP.sName.data, ema=selevation, frq=sFreq, pmode='Single Point Positioning')
            elif submitted_file1 and allowed_filename_OBS(submitted_file1.filename):
                return render_template('SPP.php',errorNav='errorNav',SPP=SPP)
            elif submitted_file2 and allowed_filename_NAV(submitted_file2.filename):
                return render_template('SPP.php',errorObs='errorObs',SPP=SPP)
            else:
                return render_template('SPP.php',errorObs='errorObs',errorNav='errorNav',SPP=SPP)

    return render_template('SPP.php',SPP=SPP)



@app.route('/rtk.php')
def rtk():
    return render_template('rtk.php')    

@app.route('/pp.php', methods=['GET', 'POST'])
def pp():
    pp = My1Form()
    if request.method == 'POST':
        if pp.validate_on_submit():
            submitted_file1 = request.files['fileBase']
            submitted_file2 = request.files['fileObsRover']
            submitted_file3 = request.files['fileNavRover']
            
            a=submitted_file1.filename
            b=submitted_file2.filename
            c=submitted_file3.filename
            
            Name=pp.Name.data
            elevation=str(pp.ema.data)
            Freq=pp.frq.data
            posMode=pp.pmode.data
            emailAdd=pp.email.data

            if ((submitted_file1 and allowed_filename_OBS(submitted_file1.filename)) and (submitted_file2 and allowed_filename_OBS(submitted_file2.filename)) and (submitted_file3 and allowed_filename_NAV(submitted_file3.filename))):
                filename1 = secure_filename(submitted_file1.filename)
                submitted_file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
                filename2 = secure_filename(submitted_file2.filename)
                submitted_file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
                filename3 = secure_filename(submitted_file3.filename)
                submitted_file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3)) 
                chain(processPP.s(posMode,Freq,elevation,a,b,c), emailfile.s(emailAdd), deletefile.s()).apply_async()
                return render_template('results.html', email=pp.email.data, Name=pp.Name.data, ema=elevation, frq=Freq, pmode=posMode, fileBase=a)
            else:
                return render_template('pp.php',errors='Please check the Base station and Rover stations data',pp=pp)

    return render_template('pp.php', pp=pp)    

@app.route('/aboutus.php')
def aboutus():
    return render_template('aboutus.php')

@app.route('/gic.php')
def gic():
    return render_template('gic.php')    


@celery.task(name='app.processPP')
def processPP(a,b,c,d,e,f):
    x = str(randint(10000, 99999))+'.pos'
    command='rnx2rtkp -p '+a+' -f '+b+' -m '+c+' -n -o '+x+' '+d+' '+e+' '+f
    os.system(command)
    os.remove(d)
    os.remove(e)
    os.remove(f)
    return x

@celery.task(name='app.processSPP')
def processSPP(selevation,a,c):
    y = str(randint(10000, 99999))+'.pos'
    command='rnx2rtkp -p 0 -m '+selevation+' -n -o '+y+' '+a+' '+c
    os.system(command)
    os.remove(a)
    os.remove(c)
    return y    

@celery.task(name='app.deletefile')
def deletefile(fileDel):
    os.remove(fileDel)
    return 'File Deleted Successfully'

@celery.task(name='app.emailfile')
def emailfile(attachmentFile,recipientemail):  
    email_user = 'gnssportal@gmail.com'
    email_password = 'GICstaff'


    subject = 'subject'
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = recipientemail
    msg['Subject'] = subject
    extension = os.path.splitext(attachmentFile)[1]

    if extension=='.pos':
        body = 'This is your Post-Processed position file'
    else:
        body = 'Please open the attachment for download links'

    msg.attach(MIMEText(body,'plain'))
    attachment  =open(attachmentFile,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+attachmentFile)

    msg.attach(part)
    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)

    server.sendmail(email_user,recipientemail,text)
    server.quit()
    return attachmentFile      

if __name__=="__main__":
    app.run() 






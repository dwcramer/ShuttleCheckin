__author__ = 'craig.vyvial'

from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import render_template
from flask import url_for
from flask import escape
from flask.ext.sqlalchemy import SQLAlchemy

from datetime import date
from datetime import timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shuttle.db'
db = SQLAlchemy(app)


class Shuttle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(60), nullable=False)

    def __init__(self,capacity,name):
        self.capacity=capacity
        self.name=name

    def __repr__(self):
        return '<Shuttle %r>' % self.name

class Tripconfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    week_day = db.Column(db.Integer, nullable=False)
    returnTrip = db.Column(db.String(5), nullable=True)
    
    shuttle_id = db.Column(db.Integer, db.ForeignKey('shuttle.id'))
    shuttle = db.relationship('Shuttle')
    pickuppoint = db.relationship("Pickuppoint", backref='pickuppoint')
   
    def __init__(self, name,week_day,returnTrip,shuttle):
        self.name = name
        self.week_day=week_day
        self.returnTrip=returnTrip
        
        self.shuttle=shuttle

class Pickuppoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(50), nullable=False)
    depart_time = db.Column(db.Integer, nullable=False)

    tripconfig_id = db.Column(db.Integer, db.ForeignKey('tripconfig.id'))
    tripconfig = db.relationship('Tripconfig')

    def __init__(self, origin, depart_time, tripconfig):
        self.origin=origin
        self.depart_time=depart_time
        self.tripconfig=tripconfig

class Currenttrip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    tripconfig_id = db.Column(db.Integer, db.ForeignKey('tripconfig.id'))
    tripconfig = db.relationship('Tripconfig')
    
    rackercheckin = db.relationship("Rackercheckin", backref='Rackercheckin')
    rackerreserve = db.relationship("Rackerreserve", backref='Rackerreserve')

    def __init__(self, date, tripconfig):
        self.date = date
        self.tripconfig = tripconfig

class Racker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(10), nullable=True)

    def __init__(self,username,name='',phone=''):
        self.username = username
        self.name=name
        self.phone=phone

class Rackercheckin(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    currenttrip_id = db.Column(db.Integer, db.ForeignKey('currenttrip.id'))
    #checkInactualshuttleleg = db.relationship('CheckInactualshuttleleg')
    racker_id = db.Column(db.Integer,db.ForeignKey('racker.id'))
    racker =  db.relationship('Racker')

    def __init__(self, currenttrip_id, racker_id):
        self.currenttrip_id = currenttrip_id
        self.racker_id = racker_id

class Rackerreserve(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    currenttrip_id = db.Column(db.Integer, db.ForeignKey('currenttrip.id'))
    #checkInactualshuttleleg = db.relationship('CheckInactualshuttleleg')
    racker_id = db.Column(db.Integer,db.ForeignKey('racker.id'))
    racker =  db.relationship('Racker')

    def __init__(self, currenttrip_id, racker):
        self.currenttrip_id = currenttrip_id
        self.racker = racker

class ShuttleView():
    def __init__(self,totalCheckin, totalReserves, capacity,departtime,origin,id,returnTrip):
        self.totalCheckin = totalCheckin
        self.totalReserves = totalReserves
        self.capacity = capacity
        self.departtime = departtime
        self.origin = origin
        self.id = id
        self.returnTrip = returnTrip
        return
    
class TestClass():
    def testTrip(self):
        currenttripid = Currenttrip.query.filter_by(date=date.today()).all()
        to_san = []
        for f in range(0,len(currenttripid)):
            pickuppoint = currenttripid[f].tripconfig.pickuppoint
            rackercheckin = currenttripid[f].rackercheckin
            
            for h in range(0,len(rackercheckin)):
                print rackercheckin[h].racker_id
                
            print currenttripid[f].tripconfig.shuttle.capacity
            for g in range(0, len(pickuppoint)):
                to_san.append(ShuttleView(currenttripid[f].tripconfig.shuttle.capacity,pickuppoint[g].depart_time,pickuppoint[g].origin,currenttripid[f].id))
        
        
        for j in range(0, len(to_san)):
            shuttleView = to_san[j]
            print shuttleView.departtime, shuttleView.origin
        return

@app.route('/checkins', methods=['GET', 'POST'])
def check_ins():
    if request.method == 'POST':
        racker = session['racker']
        racker.name=request.form['name']
        racker.phone=request.form['phone']
        db.session.add(racker)

        checkInShuttleId = request.form['depart']
        reserveShuttleId = request.form['return']

        currentCheckin = Rackercheckin(checkInShuttleId,racker.id)
            
        db.session.add(currentCheckin)
#    The call below should be removed. The current trip ids could be saved in the database and should not be queried every time
        currenttripid = Currenttrip.query.filter_by(date=date.today()).all()
        
        currentReserve = None
        
        for currentTrip in currenttripid :
            rackerReserveList = currentTrip.rackerreserve
            for rackerReserve in rackerReserveList:
                if rackerReserve.racker.id == racker.id:
                    currentReserve = rackerReserve
                    break
        
        if currentReserve is None:
            currentReserve = Rackerreserve(reserveShuttleId,racker)
        else:
            currentReserve.currenttrip_id = reserveShuttleId
        
        db.session.add(currentReserve)
        db.session.commit()
        
        rackerid = Rackercheckin.query.filter_by(currenttrip_id=reserveShuttleId).all()
        return render_template('history.html',rackerIds=rackerid)
    else:
        print (request.form['name'])
        shuttle = {'shuttle 1':'test'}
        return render_template('checkin.html', shuttle=shuttle)

@app.route('/')
@app.route('/main',methods=['GET'])
def index():
    if 'username' in session:
        username = escape(session['username'])
        racker = Racker.query.filter_by(username=username).all()
        if racker == []:
            racker = Racker(username)
            db.session.add(racker)
            db.session.commit()
        else:
            racker = racker[0]

        session['racker']=racker

        currenttripid = Currenttrip.query.filter_by(date=date.today()).all()
        to_san = []
#        currentTime = datetime
        for f in range(0,len(currenttripid)):
            capacity = currenttripid[f].tripconfig.shuttle.capacity
            rackercheckin = currenttripid[f].rackercheckin
            totalCheckin = len(rackercheckin)
            rackerreserves = currenttripid[f].rackerreserve
            totalReserves = len(rackerreserves)
            pickuppoint = currenttripid[f].tripconfig.pickuppoint
            for g in range(0, len(pickuppoint)):
                to_san.append(ShuttleView(totalCheckin,totalReserves, capacity,pickuppoint[g].depart_time,pickuppoint[g].origin,currenttripid[f].id,pickuppoint[g].tripconfig.returnTrip))
        return render_template('shuttle.html', racker=racker, to_san=to_san)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == "admin":
            session['username'] = username
            session['password'] = password
        return redirect(url_for('index'))
    return redirect(url_for('static', filename='login.html'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/history')
def history():
    currenttrip = Currenttrip.query.filter_by(date=date.today()).all()
    return render_template('history.html',currenttrip=currenttrip)

@app.route('/driver', methods=['GET', 'POST'])

def driver():
    currenttrip = Currenttrip.query.filter_by(date=date.today()).all()
    if request.method == 'GET':
        return render_template('driver.html', currenttrip=currenttrip)

# A better way would be to get the list of racker who reserved but have checked in already by sql instead of data manipulation in python code
    if request.method == 'POST':    
        action = request.form['bSubmit']
        if action == 'listCheckin':
            currenttrip_id = request.form['depart']
            session['currenttripId']=currenttrip_id
        else:
# The rackerId is part of the submit button value
            currenttrip_id = session['currenttripId']
            rackerCheckin = Rackercheckin(currenttrip_id,action)
            db.session.add(rackerCheckin)
            db.session.commit()
        
    rackerReserve = Rackerreserve.query.filter_by(currenttrip_id=currenttrip_id).all()
    rackerCheckin = Rackercheckin.query.filter_by(currenttrip_id=currenttrip_id).all()
    checkedInList = []
    reserveFilteredList = []
    
    for racker in rackerCheckin:
        checkedInList.append(racker.racker_id)
    
    for racker in rackerReserve:
        if racker.racker_id not in checkedInList:
            reserveFilteredList.append(racker)
    
    return render_template('driver.html',currenttrip=currenttrip, rackerReserves=reserveFilteredList,rackerCheckins=rackerCheckin)

  
def rackerList(currenttrip_id,currenttrip):
    rackerReserve = Rackerreserve.query.filter_by(currenttrip_id=currenttrip_id).all()
    rackerCheckin = Rackercheckin.query.filter_by(currenttrip_id=currenttrip_id).all()
    checkedInList = []
    reserveFilteredList = []
    
    for racker in rackerCheckin:
        checkedInList.append(racker.racker_id)
    
    for racker in rackerReserve:
        if racker.racker_id not in checkedInList:
            reserveFilteredList.append(racker)
    
    return render_template('driver.html',currenttrip=currenttrip, rackerReserves=reserveFilteredList,rackerCheckins=rackerCheckin)
    
class RackerList():
    def __init__(self,name,phone,status):
        self.name = name
        self.phone = phone
        self.status = status
        self.id = id
        return

# set the secret key.  keep this really secret:
app.secret_key = '\x0c\xe2\x83*\xe3MK\xf3\x9c\xe9\x16\xf7Bv\xe5\xf2\x17)\x05\x1a2\x91\xcc\xe8'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


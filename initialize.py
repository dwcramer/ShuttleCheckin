#!/usr/bin/env python

from shuttle import db, Shuttle, Tripconfig, Pickuppoint, Currenttrip, Racker, Rackerreserve,Rackercheckin
from datetime import date

# WARNING! Drops all tables!
db.drop_all()

# Following will create the DB.
db.create_all()

aus = 'Austin Office'
spm = 'Southpark Meadows'
castle = 'Castle'

# Populate the shuttle table
shuttle_big = Shuttle(30, 'Big')
shuttle_small = Shuttle(15, 'Small')
db.session.add(shuttle_big)
db.session.add(shuttle_small)

aus_morning_early_tripconfig = Tripconfig("Austin Morning Early Shuttle",'MTWTF',shuttle_big)
aus_morning_late_tripconfig = Tripconfig("Austin Morning Late Shuttle",'TWT',shuttle_small)
aus_evening_early_tripconfig = Tripconfig("Austin Evening Early Shuttle",'MTWTF',shuttle_big)
aus_evening_late_tripconfig = Tripconfig("Austin Evening Late Shuttle",'TWT',shuttle_small)

db.session.add(aus_morning_early_tripconfig)
db.session.add(aus_morning_late_tripconfig)
db.session.add(aus_evening_early_tripconfig)
db.session.add(aus_evening_late_tripconfig)

db.session.commit()

# Populate shuttle_leg table

# Minutes since midnight
time0715 = '7:15 AM'
time0730 = '7:30 AM'
time0745 = '7:45 AM'
time0800 = '8:00 AM'
time0900 = '9:00 AM'
time0915 = '9:15 AM'

time1600 = '4:00 PM'
time1715 = '5:15 PM'
time1745 = '5:45 PM'
time1830 = '6:30 PM'
time1900 = '7:00 PM'

aus_early_pickuppoint=Pickuppoint(aus,time0715,aus_morning_early_tripconfig)
spm_early_pickuppoint=Pickuppoint(spm,time0745,aus_morning_early_tripconfig)

aus_late_pickuppoint=Pickuppoint(aus,time0730,aus_morning_late_tripconfig)
spm_late_pickuppoint=Pickuppoint(spm,time0800,aus_morning_late_tripconfig)

castle_early_pickuppoint=Pickuppoint(castle,time1600,aus_evening_early_tripconfig)
castle_late_pickuppoint=Pickuppoint(castle,time1715,aus_evening_late_tripconfig)

db.session.add(aus_early_pickuppoint)
db.session.add(spm_early_pickuppoint)
db.session.add(aus_late_pickuppoint)
db.session.add(spm_late_pickuppoint)
db.session.add(castle_early_pickuppoint)
db.session.add(castle_late_pickuppoint)

db.session.commit()

aus_morning_early_currenttrip = Currenttrip(date.today(),aus_morning_early_tripconfig)
aus_morning_late_currenttrip = Currenttrip(date.today(),aus_morning_late_tripconfig)
aus_evening_evening_currenttrip = Currenttrip(date.today(),aus_evening_early_tripconfig)
aus_evening_late_currenttrip = Currenttrip(date.today(),aus_evening_late_tripconfig)

db.session.add(aus_morning_early_currenttrip)
db.session.add(aus_morning_late_currenttrip)
db.session.add(aus_evening_evening_currenttrip)
db.session.add(aus_evening_late_currenttrip)

db.session.commit()

#actual_shuttle_leg1 = Actualshuttleleg.query.filter_by(shuttleleg_id=aus_spm_early_shuttleleg.id).first()

"""
racker = Racker('raj.patel','rajesh.patel','123.123.1232')
db.session.add(racker)
db.session.commit()

rackerCheckin=Rackercheckin(aus_early_currenttrip.id,racker)
db.session.add(rackerCheckin)
db.session.commit()

rackerReserve=Rackerreserve(aus_late_currenttrip.id,racker)
db.session.add(rackerReserve) 
db.session.commit()"""
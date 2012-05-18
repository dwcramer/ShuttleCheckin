#!/usr/bin/env python

from shuttle import db, Shuttle, ShuttleLeg

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
db.session.commit()

# Populate shuttle_leg table

# Minutes since midnight
time0715 = 7 * 60 + 15
time0730 = 7 * 60 + 30 
time0745 = 7 * 60 + 45
time0800 = 8 * 60

time1600 = 16 * 60
time1715 = 17 * 60 + 15

for d in range(5):
    from_aus_0715 = ShuttleLeg(aus, castle, time0715, None, d, shuttle_big)
    from_spm_0745 = ShuttleLeg(spm, castle, time0745, None, d, shuttle_big)
    from_cas_1600 = ShuttleLeg(castle, aus, time1600, None, d, shuttle_big)
    db.session.add(from_aus_0715)
    db.session.add(from_spm_0745)
    db.session.add(from_cas_1600)
    db.session.commit()

for d in range(1, 4):
    from_aus_0730 = ShuttleLeg(aus, castle, time0730, None, d, shuttle_small)
    from_spm_0800 = ShuttleLeg(spm, castle, time0800, None, d, shuttle_small)
    from_cas_1715 = ShuttleLeg(castle, aus, time1715, None, d, shuttle_small)
    db.session.add(from_aus_0730)
    db.session.add(from_cas_1715)
    db.session.commit()

"""
Do the following to reconstitute datetime object based on minutes since midnight

>> from datetime import datetime, date, time, timedelta
>> d = date.today()
>> t = time(0, 0)
>> datetime.combine(d, t) + timedelta(minutes=435)
datetime.datetime(2012, 5, 18, 7, 15)
"""
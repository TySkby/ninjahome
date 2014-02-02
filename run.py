import datetime
from flask import Flask
from ninja.api import NinjaAPI
from ninja import devices

import secrets

# Instantiate our Flask application
app = Flask(__name__)
app.debug = True

# Instantiate a client to the Ninja Blocks API
api = NinjaAPI(secrets.ACCESS_TOKEN)

# Some GUIDS we'll be using
GUIDS = {
    'wemo': secrets.LIVING_ROOM_WEMO_GUID
}

# TODO: Make this better :P
# This just prevents the sample backdoor_triggered() function from continuously turning on the WeMo
TRIGGERS_OCCURRED = {
    'backdoor': False,
}

# Define various states for our home.  Eventually this will be moved out somewhere else and actually utilized
STATES = ['home', 'away', 'asleep']


@app.route('/backdoor', methods=['POST'])
def backdoor_triggered():
    """ Just temporary, but to illustrate the concept...
        When the backdoor opens within a specified range of time (when I get home from work),
        turn on the living room light (Belkin WeMo relay)
    """
    now = datetime.datetime.now()
    active_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    if TRIGGERS_OCCURRED['backdoor'] is False:
        if now.strftime('%a') in active_days:
            if now.hour < 5 or now.hour > 17:
                wemo = api.getDevice(GUIDS['wemo'])
                wemo.turn_on()
                TRIGGERS_OCCURRED['backdoor'] = True
    return 'Received'


if __name__ == '__main__':
    app.run('0.0.0.0')

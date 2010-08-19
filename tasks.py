from datetime import datetime, timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import *
from utils import *


stale_session_timeout = timedelta(minutes = 2)


class SessionTaskHandler(webapp.RequestHandler):

    def get(self):
        expired_sessions = RoomList.all().filter("last_seen <", datetime.now() - stale_session_timeout)
        for session in expired_sessions:
            leave_room(session=session)


application = webapp.WSGIApplication([(r'/tasks/session', SessionTaskHandler),
                                      ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
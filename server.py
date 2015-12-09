import os

from flask.ext.script import Manager
from config import config
from app import create_app

CONFIGNAME = os.environ.get('APP_CONFIG', 'default')
app = create_app(CONFIGNAME)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()

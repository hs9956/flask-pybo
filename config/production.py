from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR,'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY=b'c\xf0\\\xee\x98j\xc5\xee\xc0;|7\x8fu\x15\xd1'
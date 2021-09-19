from flask import Blueprint, url_for
from werkzeug.utils import redirect

from pybo.models import Question

# Blueprint(블루프린트의 이름, 모듈명, URL 프리픽스)
# __name__ = 해당 파일의 이름 (즉, main_views)
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
	return "Hello, Pybo!"

@bp.route('/')
def index():
	return redirect(url_for('question._list'))
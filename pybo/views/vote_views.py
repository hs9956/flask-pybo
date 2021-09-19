from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer, question_voter, answer_voter
from pybo.views.auth_views import login_required

bp = Blueprint('vote', __name__, url_prefix="/vote")

@bp.route('/question/<int:question_id>')
@login_required
def question(question_id):
	_question = Question.query.get_or_404(question_id)
	vote_already = db.session.query(question_voter).filter(question_voter.c.user_id==g.user.id, question_voter.c.question_id==question_id)
	if g.user == _question.user:
		flash('본인이 작성한 글은 추천할 수 없습니다.')
	elif vote_already.all():
		vote_already.delete() # 이미 존재하는 경우 좋아요 취소
		db.session.commit()
	
	else:
		_question.voter.append(g.user) # 좋아요 기록
		db.session.commit()
	return redirect('{}#vote_question'.format(url_for('question.detail', question_id = question_id)))

@bp.route('/answer/<int:answer_id>')
@login_required
def answer(answer_id):
	_answer = Answer.query.get_or_404(answer_id)
	vote_already = db.session.query(answer_voter).filter(answer_voter.c.user_id==g.user.id, answer_voter.c.answer_id==answer_id)
	if g.user == _answer.user:
		flash('본인이 작성한 글은 추천할 수 없습니다.')
	elif vote_already.all():
		vote_already.delete() # 이미 존재하는 경우 좋아요 취소
		db.session.commit()
	
	else:
		_answer.voter.append(g.user) # 좋아요 기록
		db.session.commit()
	return redirect('{}#vote_answer_{}'.format(url_for('question.detail', question_id = _answer.question.id),answer_id))

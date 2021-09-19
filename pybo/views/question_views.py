from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash, make_response
from werkzeug.utils import redirect
from .. import db #pybo/__init__.py의 db 객체 load
from pybo.models import Question, Answer, User, question_voter
from ..forms import QuestionForm, AnswerForm
from sqlalchemy import func

from .answer_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/setcookie', methods=["GET", "POST"])
def setcookie():
	if request.method == "POST":
		page = request.form["page"]
		ss = request.form["ss"]
		kw = request.form["kw"]
		so = request.form["so"]
		
		res = make_response(redirect(url_for('main.index')))
		res.set_cookie("page", page)
		res.set_cookie("ss", ss)
		res.set_cookie("kw", kw)
		res.set_cookie("so", so)

	return res

@bp.route('/list/')
def _list():
	clear = request.args.get('clear', type=int, default=0)
	if clear == 1:
		res = make_response(redirect(url_for('main.index')))
		res.set_cookie("page", '1')
		res.set_cookie("ss", 'qs')
		res.set_cookie("kw", '')
		res.set_cookie("so", 'rc')
		return res

	page = request.cookies.get('page') # default=1
	if page: page = int(page)
	ss = request.cookies.get('ss') # default='qs'
	kw = request.cookies.get('kw') # default=''
	so = request.cookies.get('so') # default='rc'

	#print("page : {}".format(page))
	#print("ss : {}".format(ss))
	#print("kw : {}".format(kw))
	#print("so : {}".format(so))

	if so=="rm": #recommend
		sub_query= db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')).group_by(question_voter.c.question_id).subquery()
		question_list = Question.query.outerjoin(sub_query, Question.id==sub_query.c.question_id).order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
	elif so=="po": #popular
		sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')).group_by(Answer.question_id).subquery()
		question_list = Question.query.outerjoin(sub_query, Question.id==sub_query.c.question_id).order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
	else: #최근순(recent)
		question_list = Question.query.order_by(Question.create_date.desc())

	if kw: #검색 내용에 따라 조회 내역 재작성
		search = '%%{}%%'.format(kw)
		sub_query = db.session.query(Answer.question_id, Answer.content, User.username).join(User, Answer.user_id==User.id).subquery()
		question_list = question_list.join(User).outerjoin(sub_query, sub_query.c.question_id==Question.id)

		if ss=="qc":
			question_list=question_list.filter(Question.content.ilike(search)).distinct() #질문 내용
		elif ss=="qu":
			question_list=question_list.filter(User.username.ilike(search)).distinct() #질문 작성자
		elif ss=="ac":
			question_list=question_list.filter(sub_query.c.content.ilike(search)).distinct() #답변 내용
		elif ss=="au":
			question_list=question_list.filter(sub_query.c.username.ilike(search)).distinct() #답변 작성자
		else:
			question_list=question_list.filter(Question.subject.ilike(search)).distinct() #질문 제목

	question_list=question_list.paginate(page, per_page=10) #Pagination 객체 생성
	return render_template('question/question_list.html', question_list = question_list, page=page, ss=ss, kw=kw, so=so)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
	form = AnswerForm()
	question=Question.query.get_or_404(question_id)
	return render_template('question/question_detail.html',question=question, form=form)

@bp.route('/create/', methods=('GET','POST'))
@login_required
def create():
	form = QuestionForm()
	if request.method=="POST" and form.validate_on_submit():
		question=Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
		db.session.add(question)
		db.session.commit()
		return redirect(url_for('main.index'))
	return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>/', methods=("GET","POST"))
@login_required
def modify(question_id):
	question=Question.query.get_or_404(question_id)
	if g.user != question.user:
		flash('수정권한이 없습니다.')
		return redirect(url_for('question.detail', question_id=question_id))
	if request.method=="POST":
		form = QuestionForm()
		if form.validate_on_submit():
			form.populate_obj(question)
			question.modify_date=datetime.now()
			db.session.commit()
			return redirect(url_for('question.detail', question_id=question_id))
	form = QuestionForm(obj=question)
	return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>/')
@login_required
def delete(question_id):
	question=Question.query.get_or_404(question_id)
	if g.user != question.user:
		flash('삭제권한이 없습니다.')
		return redirect(url_for('question.detail', question_id=question_id))
	else:
		db.session.delete(question)
		db.session.commit()
		return redirect(url_for('question._list'))
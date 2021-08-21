from flask import Flask, render_template, redirect, request, jsonify, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
from models import *
from flask_bcrypt import Bcrypt



db = SQLAlchemy()

bp = Blueprint('main', __name__)
bcrypt = Bcrypt()

# home
@bp.route('/', methods=["GET"])
def home():
    books = Book.query.all()

    if session['login'] is not None:
        user = User.query.filter(User.email == session['login']).first()
        return render_template('main.html', books=books, user=user)
    else:
        return render_template('main.html', books=books)

# 회원가입
@bp.route('/register', methods=["GET", "Post"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        email = request.form['email']
        name = request.form['name']
        password = request.form['pwd'] #ajax에서 넘어오는 데이터의 key값을 넣어줘야함

        pw_hash = bcrypt.generate_password_hash(password)

        # 이미 등록된 사용자인지 검사
        user = User.query.filter(User.email == email).first()
        if user is not None:
            return jsonify({"result": "email_check"})
        # 비밀번호 자릿수 검사
        if len(password) < 8:
            return jsonify({"result": "pw_check"})

        # 위 검사를 통과 했으므로 유저 생성
        user = User(email, name, pw_hash)
        db.session.add(user)
        db.session.commit()

        return jsonify({"result": "success"})

# 로그인
@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['pwd']

        user = User.query.filter(User.email == email).first()

        if user is not None:
            if bcrypt.check_password_hash(user.password, password):
                session['login'] = user.email
                return jsonify({"result": "success"})
            else:
                return jsonify({"result": "fail"})
        else:
            return jsonify({"result": "noUser"})

#로그아웃    
@bp.route('/logout')
def logout():
    session['login'] = None
    return redirect('/')

# 대여하기 
@bp.route('/borrow', methods=["PATCH"])
def borrow():
    book_id = request.form['book_id']

    book = db.session.query(Book).filter(Book.id == book_id).first()
    
    if 'login' not in session:
        return jsonify({"result": "login_fail"})
    else:
        if session['login'] is None:
            return jsonify({"result": "login_fail"})
        else:
            if book.quantity > 0:
                book.quantity -= 1 
                user_book = User_Book(session['login'], book_id)
                db.session.add(user_book)
                db.session.commit()
                return jsonify({"result": "success"})
            else: 
                return jsonify({"result": "fail"})
    

# 책 상세 페이지
@bp.route('/book/<int:book_id>', methods=["GET"])
def book_info(book_id):
    book = Book.query.filter(Book.id == book_id).first()

    if 'login' not in session:
        return render_template('book.html', book=book)
    else:
        if session['login'] is None:
            return render_template('book.html', book=book)
        else:
            user = User.query.filter(User.email == session['login']).first()
            return render_template('book.html', book=book, user=user)

    return render_template('book.html', book=book)

from flask import Flask, render_template, redirect, request, jsonify, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from models import *
from flask_bcrypt import Bcrypt



db = SQLAlchemy()

bp = Blueprint('main', __name__)
bcrypt = Bcrypt()

# home
@bp.route('/', methods=["GET"])
def home():
    books = Book.query.all()
    
    if 'login' not in session:
        return render_template('main.html', books=books)

    if session['login'] is not None:
        user = db.session.query(User).filter(User.email == session['login']).first()
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
        user = db.session.query(User).filter(User.email == email).first()
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

        user = db.session.query(User).filter(User.email == email).first()

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
    session.clear()
    return redirect('/')

# 대여하기 
@bp.route('/borrow', methods=["PATCH"])
def borrow():
    book_id = request.form['book_id']

    book = db.session.query(Book).filter(Book.id == book_id).first()
    book_title = book.title
    
    if 'login' not in session:
        return jsonify({"result": "login_fail"})
    else:
        if session['login'] is None:
            return jsonify({"result": "login_fail"})
        else:
            if book.quantity > 0:
                book.quantity -= 1 
                user_book = User_Book(session['login'], book_id, book_title)
                db.session.add(user_book)
                db.session.commit()
                return jsonify({"result": "success"})
            else: 
                return jsonify({"result": "fail"})

# 대여기록
@bp.route('/borrowed_books', methods=["GET"])
def show_borrowed_books():
    user = db.session.query(User).filter(User.email == session['login']).first()

    borrowed_books = db.session.query(User_Book).filter(User_Book.user_email == user.email).all()
    
    return render_template('borrowed_books.html', borrowed_books=borrowed_books, user=user)

# 반납하기
@bp.route('/return_book', methods=["PATCH"])
def return_book():
    rent_id = request.form['id']
    borrowed_book = db.session.query(User_Book).filter(User_Book.id == rent_id).first()
    book = db.session.query(Book).filter(Book.id == borrowed_book.book_id).first()
    book.quantity += 1
    db.session.delete(borrowed_book)
    db.session.commit()

    return jsonify({"result": "success"})

# 책 상세 페이지
@bp.route('/book/<int:book_id>', methods=["GET"])
def book_info(book_id):
    book = db.session.query(Book).filter(Book.id == book_id).first()
    
    reviews = db.session.query(Review).filter(Review.book_id == book_id).order_by(Review.posted_at.desc()).all()

    if 'login' not in session:
        return render_template('book.html', book=book, reviews=reviews)

    if session['login'] is None:
        return render_template('book.html', book=book, reviews=reviews)

    user = db.session.query(User).filter(User.email == session['login']).first()
    return render_template('book.html', book=book, reviews=reviews, user=user)

# 리뷰 작성 페이지
@bp.route('/review/<int:book_id>', methods=["POST"])
def post_review(book_id):
    rating = int(request.form['rating'])
    content = request.form['content']
    user_email = session['login']
    book_id = book_id
    # 리뷰 데이터 추가
    review = Review(user_email, book_id, rating, content)
    db.session.add(review)
    db.session.commit()
    # rating 평균 구하고 book의 rating 수정
    reviews = db.session.query(Review).filter(Review.book_id == book_id).all()
    sum = 0
    for review in reviews:
        sum += review.rating
    avg_rating = round(sum / len(reviews))

    book = db.session.query(Book).filter(Book.id == book_id).first()
    book.rating = avg_rating
    db.session.commit()
    
    return jsonify({"result": 'success'})

# 리뷰 삭제
@bp.route('/delete_review/<int:book_id>/<int:review_id>', methods=["DELETE"])
def delete_review(book_id, review_id):
    review = db.session.query(Review).filter(Review.id == review_id).first()
    book = db.session.query(Book).filter(Book.id == book_id).first()

    if review.user_email != session['login']:
        return jsonify({"result": "user_error"})
    elif review.book_id != book.id:
        return jsonify({"reuslt": "fail"})
    else:
        db.session.delete(review)
        db.session.commit()
        # rating 평균 구하고 book의 rating 수정
        reviews = db.session.query(Review).filter(Review.book_id == book_id).all()
        sum = 0
        avg_rating = 0
        for review in reviews:
            sum += review.rating
            if len(reviews) > 0:
                avg_rating = round(sum / len(reviews))


        book = db.session.query(Book).filter(Book.id == book_id).first()
        book.rating = avg_rating
        db.session.commit()

        return jsonify({"result": "success"})


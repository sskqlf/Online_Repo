from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션 암호화를 위한 비밀키
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# 데이터베이스 초기화 함수
def initialize_database():
    if not os.path.exists("users.db"):
        db.create_all()
        print("데이터베이스가 초기화되었습니다.")

# 홈 페이지
@app.route("/")
def home():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
        return render_template("index.html", user=user.username)
    return render_template("index.html", user=None)

# 회원가입 페이지
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("이미 존재하는 사용자 이름입니다.")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password, method="sha256")
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("회원가입이 완료되었습니다. 로그인 해주세요!")
        return redirect(url_for("login"))

    return render_template("signup.html")

# 로그인 페이지
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("로그인 성공!")
            return redirect(url_for("drawing_app"))  # 로그인 성공 시 그림판으로 이동
        else:
            flash("잘못된 사용자 이름 또는 비밀번호입니다.")
            return redirect(url_for("login"))

    return render_template("login.html")

# 로그아웃
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("로그아웃되었습니다.")
    return redirect(url_for("home"))

# 그림판 앱
@app.route("/drawing")
def drawing_app():
    if "user_id" not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for("login"))
    return render_template("drawing.html")

if __name__ == "__main__":
    initialize_database()  # 애플리케이션 실행 시 데이터베이스 초기화
    app.run(debug=True)

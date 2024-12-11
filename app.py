from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from io import BytesIO
from PIL import Image

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션 암호화를 위한 비밀키
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Drawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    filename = db.Column(db.String(150), nullable=False)

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

        # 비밀번호 해싱
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
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
            return redirect(url_for("home"))  # 로그인 성공 시 홈 페이지로 이동
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

# 그림판 페이지
@app.route("/drawing", methods=["GET", "POST"])
def drawing():
    if "user_id" not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for("login"))

    if request.method == "POST":
        # 파일 저장 처리
        if "drawing" in request.files:
            file = request.files["drawing"]
            if file.filename != "":
                user_id = session["user_id"]
                filename = f"user_{user_id}_{file.filename}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)

                # 데이터베이스에 저장
                with open(filepath, "rb") as f:
                    image_data = f.read()
                drawing = Drawing(user_id=user_id, image_data=image_data, filename=filename)
                db.session.add(drawing)
                db.session.commit()

                flash("그림이 저장되었습니다!")
                return redirect(url_for("drawing"))

    return render_template("drawing.html")

# 그림 다운로드
@app.route("/download/<int:drawing_id>")
def download_drawing(drawing_id):
    if "user_id" not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for("login"))

    drawing = Drawing.query.filter_by(id=drawing_id, user_id=session["user_id"]).first()
    if not drawing:
        flash("해당 그림을 찾을 수 없습니다.")
        return redirect(url_for("drawing"))

    return send_file(BytesIO(drawing.image_data), mimetype="image/png", as_attachment=True, download_name=drawing.filename)

if __name__ == "__main__":
    # 애플리케이션 컨텍스트 내에서 데이터베이스 초기화
    with app.app_context():
        db.create_all()
        print("데이터베이스가 초기화되었습니다.")

    # Flask 애플리케이션 실행
    app.run(host="0.0.0.0", port=5000, debug=True)

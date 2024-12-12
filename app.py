from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from io import BytesIO

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Drawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    filename = db.Column(db.String(150), nullable=False)

@app.route("/")
def home():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
        images = Drawing.query.filter_by(user_id=session["user_id"]).all()
        return render_template("index.html", user=user.username, images=images)
    return render_template("index.html", user=None, images=[])

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("이미 존재하는 사용자 이름입니다.")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("회원가입이 완료되었습니다. 로그인 해주세요!")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("로그인 성공!")
            return redirect(url_for("home"))
        else:
            flash("잘못된 사용자 이름 또는 비밀번호입니다.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("로그아웃되었습니다.")
    return redirect(url_for("home"))

@app.route("/upload_image", methods=["POST"])
def upload_image():
    if "user_id" not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for("login"))

    if "image" in request.files:
        file = request.files["image"]
        if file.filename != "":
            user_id = session["user_id"]
            filename = f"user_{user_id}_{file.filename}"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            with open(filepath, "rb") as f:
                image_data = f.read()
            drawing = Drawing(user_id=user_id, image_data=image_data, filename=filename)
            db.session.add(drawing)
            db.session.commit()

            flash("이미지가 업로드되었습니다!")
            return redirect(url_for("home"))
    flash("이미지 업로드에 실패했습니다.")
    return redirect(url_for("home"))

@app.route("/image/<int:image_id>")
def display_image(image_id):
    if "user_id" not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for("login"))

    drawing = Drawing.query.filter_by(id=image_id, user_id=session["user_id"]).first()
    if not drawing:
        flash("이미지를 찾을 수 없습니다.")
        return redirect(url_for("home"))

    return send_file(BytesIO(drawing.image_data), mimetype="image/png")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("데이터베이스가 초기화되었습니다.")
    app.run(host="0.0.0.0", port=5000, debug=True)

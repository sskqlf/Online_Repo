from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 사용자 데이터 (데모용)
users = {}

# 라우트
@app.route("/")
def home():
    if "user_id" in session:
        return render_template("index.html")
    flash("로그인하세요.")
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user_id"] = username
            flash("로그인 성공!")
            return redirect(url_for("home"))
        flash("잘못된 사용자 이름 또는 비밀번호입니다.")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            flash("이미 존재하는 사용자 이름입니다.")
            return redirect(url_for("signup"))
        users[username] = password
        flash("회원가입 성공! 로그인하세요.")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("로그아웃되었습니다.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

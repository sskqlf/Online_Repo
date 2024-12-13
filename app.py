from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"
BASE_UPLOAD_FOLDER = "uploads"
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)

# 사용자 데이터 (데모용)
users = {}

# 라우트
@app.route("/")
def home():
    if "user_id" in session:
        user_folder = os.path.join(BASE_UPLOAD_FOLDER, session["user_id"])
        files = os.listdir(user_folder) if os.path.exists(user_folder) else []
        return render_template("index.html", files=files)
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
        # 사용자 이름으로 폴더 생성
        user_folder = os.path.join(BASE_UPLOAD_FOLDER, username)
        os.makedirs(user_folder, exist_ok=True)
        flash("회원가입 성공! 로그인하세요.")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("로그아웃되었습니다.")
    return redirect(url_for("login"))

@app.route("/upload", methods=["POST"])
def upload_file():
    if "user_id" not in session:
        flash("로그인 후 파일을 업로드할 수 있습니다.")
        return redirect(url_for("login"))

    if "file" not in request.files:
        flash("파일이 선택되지 않았습니다.")
        return redirect(url_for("home"))

    file = request.files["file"]
    if file.filename == "":
        flash("파일 이름이 없습니다.")
        return redirect(url_for("home"))

    user_folder = os.path.join(BASE_UPLOAD_FOLDER, session["user_id"])
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, file.filename)
    file.save(file_path)
    flash("파일이 성공적으로 업로드되었습니다.")
    return redirect(url_for("home"))

@app.route("/download/<filename>")
def download_file(filename):
    if "user_id" not in session:
        flash("로그인 후 파일을 다운로드할 수 있습니다.")
        return redirect(url_for("login"))

    user_folder = os.path.join(BASE_UPLOAD_FOLDER, session["user_id"])
    return send_from_directory(user_folder, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

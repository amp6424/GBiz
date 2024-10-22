# importing needed modules
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from user_management import User
from brand_management import BrandRegistration
from content_management import ContentDataManagement
from chatbot import ChatBot
from image_generation import PostGenerator

app = Flask(__name__)
app.secret_key = "shss!thisissecretkey."

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user" not in session:
        session["user"] = False
        session["username"] = ""
    if session["user"] == False:
        if request.method == "GET":
            return render_template("signup.html")
        elif request.method == "POST":
            user = User()
            username = request.form.get("username")
            password = request.form.get("password")
            if user.signup(username, password):
                session["user"] = True
                session["username"] = username
                user.close_connection()
                return redirect(url_for('brand_registration'))
            else:
                session["user"] = False
                session["username"] = ""
                user.close_connection()
                return redirect(url_for('signup'))
    else:
        return redirect(url_for("landing"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" not in session:
        session["user"] = False
        session["username"] = ""
    if session["user"] == False:
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            user = User()
            username = request.form.get("username")
            password = request.form.get("password")
            if user.login(username, password):
                session["user"] = True
                session["username"] = username
                user.close_connection()
                return redirect(url_for('brand_registration'))
            else:
                session["user"] = False
                session["username"] = ""
                user.close_connection()
                return redirect(url_for('login'))
    else:
        return redirect(url_for("landing"))

@app.route('/logout')
def logout():
    if "user" in session:
        session["user"] = False
        session["username"] = ""
    return redirect(url_for("landing"))

@app.route('/brandregistration', methods=["GET", "POST"])
def brand_registration():
    if "user" in session and session["user"] == True:
        if request.method == "GET":
            return render_template("brand_registration.html")
        elif request.method == "POST":
            brand_name = request.form.get("brand_name")
            brand_tagline = request.form.get("brand_tagline")
            industry = request.form.get("industry")
            brand_description = request.form.get("brand_description")
            primary_color = request.form.get("primary_color")
            secondary_color = request.form.get("secondary_color")
            complementary_color = request.form.get("complementary_color")
            brand_keywords = request.form.get("brand_keywords")

            brand_registration = BrandRegistration()
            user = User()
            uuid = user.get_user_uuid(session["username"])
            brand_registration.add_data(uuid, brand_name, brand_tagline, industry, brand_description,
                    primary_color, secondary_color, complementary_color, brand_keywords)
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for("signup"))

@app.route('/dashboard')
def dashboard():
    if session["user"] == True and session["username"] != "":
        return render_template("dashboard.html")
    else:
        return redirect(url_for("landing"))

@app.route('/insights')
def insights():
    if session["user"] == True and session["username"] != "":
        return render_template("insights.html")
    else:
        return redirect(url_for("landing"))

@app.route('/chatbot', methods=["GET", "POST"])
def chatbot():
    if session["user"] == True and session["username"] != "":
        if request.method == "GET":
            return render_template("chatbot.html", response="")
        elif request.method == "POST":
            cb = ChatBot()
            username = session["username"]
            prompt = request.form.get('prompt')
            response = cb.chat(username, prompt)
            return render_template("chatbot.html", response=response['response'])
    else:
        return redirect(url_for("landing"))
    
@app.route("/imageCreation", methods=["POST"])
def imageCreation():
    if request.method == "POST":
        print("world")
        prompt = request.form.get('prompt')
        print(prompt)
        post = PostGenerator(prompt)
        print("hello")
        return render_template("image_creation.html", imgpath=post.generated)
    
@app.route("/profile")
def profile():
    return render_template("profilepage.html")

if __name__ == "__main__":
    app.run(debug=True)

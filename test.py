"--> IMPORTING NECESSART MODULE AND LIBRARIES <--"

from flask import Flask, render_template, request, session, redirect, flash

"""
Flask - to create an app object using this class
render_template - to fetch the template and return it to the browser with necessary variables from the backend
request - to get the data from the client
session - to store data in the session
redirect - to redirect the user to a different route
flash - to display a message to the user
"""
import json  # to reuse variables used in the code
from flask_mail import (
    Mail,
)  # to send mail using flask from our browser for notification purposes
from flask_sqlalchemy import SQLAlchemy  # to authorise our backend with the database
from datetime import datetime  # to use it in time purposes
import math  # for performing calculations

# to upload our files we import the following modules and libraries
import os  # to interact with the os of admin and/or user
from werkzeug.utils import (
    secure_filename,
)  # for the privacy of the files uploaded in our website


# opening the json file in read mode and...
with open("config.json", "r") as c:
    params = json.load(c)["params"]  # storing the value in a variable named params

wn = params[
    "websitename"
]  # storing the name of the website from the params in a new var called wn


# creating an object using the Flask class
app = Flask(__name__)

app.secret_key = "super-secret-key"  # storing the
app.config["UPLOAD_FOLDER"] = params[
    "upload_location"
]  # storing the uplaod location in this variable


"--> configuring mail to get update <--"
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT="465",
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params["gmail-user"],
    MAIL_PASSWORD=params["gmail_password"],
)
mail = Mail(app)


"--> DATABASE <--"
# connecting our database to mysql database (we can use any other database sql)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/kalker_chipa"
# syntax: app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
"""
Hence we've no username so, username is root. 
Hence we don't have a password so password is ignored or blank)
"""

# initialising the database by creating an object using the SQLAlchemy class
db = SQLAlchemy(app)


# creating a database class (OOP Concept) of Contacts & Posts, aligning with the localadmin database
# (EXACTLY THE SEM IS DATABASE WE CREATED IN http://localhost/phpmyadmin/)
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    tagline = db.Column(db.String(25), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)


"--> BACKEND CODE <--"


@app.route("/")  # the pipeline where it'll be routing
def home():

    # displaying flash messaged using this codes
    flash("Hello noobie motherfucker what the fuck is up!!!", "primary")
    flash("Start fucking your brains up from here...", "success")

    posts = (
        Posts.query.filter_by().all()
    )  # fetching all the fucking post using this line

    last = math.ceil(
        len(posts) / int(params["no_of_posts"])
    )  # finding the last page using this line
    # first we count the number of total posts using len(post)
    # then we divide the number of total posts using the number of posts present in per page i.e. no_of_post = 5
    # thus we obtain our total desired number of pages. We did the ceil fucntion to avoid fractions hecne page number can't be a irrational

    page_number = request.args.get(
        "page"
    )  # fetching the page number using this line. And this thing will always be a string
    # Our web page url is string. So we convert the page number into integer for calculation puposes

    if not str(
        page_number
    ).isnumeric():  # verifying if the page number is numeric value or not
        page_number = 1  # we'll assign a value in case the page number ain't numeric

    page_num = int(page_number)
    # the number of posts that we want to display in per page without LOOSING TRACK by using slicing
    posts = posts[
        (page_num - 1)
        * int(params["no_of_posts"]) : (page_num - 1)
        * int(params["no_of_posts"])
        + int(params["no_of_posts"])
    ]

    if page_num == 1:  # if we're on the first page then...
        prev = "#"  # the previous button will return nothing hence the post before the first page don't even exist
        next = "/?page=" + str(
            page_num + 1
        )  # the next page will be page + 1. We did so and also type casted the value back to string hence url is always a string

    # if we are on our last page then...
    elif page_num == last:
        prev = "/?page=" + str(
            page_num - 1
        )  # prev page before the last page is page - 1
        next = "#"  # no page after last page

    # what if we land in the middle of our webpage
    else:
        prev = "/?page=" + str(page_num - 1)
        next = "/?page=" + str(page_num + 1)

    return render_template(
        "index.html", params=params, posts=posts, prev=prev, next=next
    )


# the above lines are the most important lines of all time in flask web development. specially the return one


@app.route("/dashboard", methods=["GET", "POST"])
# GET is default keyword to fetch the url (can be found in terminal)
# POST is used to send data to the server to perform some operation


def dashboard():

    if (
        "user" in session and session["user"] == params["admin_user"]
    ):  # verifying if admin is already logged in or not
        post = (
            Posts.query.all()
        )  # if logged in then admin can see all posts from his dashboard
        return render_template(
            "admin.html", params=params, posts=post
        )  # we'll pass all the posts & params in frontend

    if request.method == "POST":  # if admin isn't logged in then he have to sign in
        useremail = request.form.get(
            "email"
        )  # fetching the email from the form in login.html.
        userpass = request.form.get(
            "pass"
        )  # fetching the email from the form in login.html.
        # have written name = email and name = pass in the login.html. This is the varible name used in login.html to store our data

        if (
            useremail == params["admin_user"] and userpass == params["admin_pass"]
        ):  # matching data with username & password stored in json
            session["user"] = useremail  # setting the session for the user
            post = Posts.query.all()
            return render_template("admin.html", params=params, posts=post)

    else:  # if pass & username don't match in that case lol
        return render_template(
            "login.html", params=params
        )  # we'll send back to the login page once again for privacy


@app.route("/logout")
def logout():
    session.pop("user")  # ending the session for the user
    return redirect("/dashboard")


# http://127.0.0.1:5000/post/first-post
# we want to show the slug hence we wrote this shit in app.route()
@app.route("/post/<string:post_slug>", methods=["GET"])
# post_slug is a varible.
# according to the syntax of flask if we use any variable in app.route then we've to pass it in the fucntion as well
def post_route(post_slug):
    p = Posts.query.filter_by(slug=post_slug).first()  # fetching our post
    # it means go to Post and perform a query which will filter by slug = post_slug
    return render_template("post.html", params=params, post=p)


# http://127.0.0.1:5000/edit/1
@app.route("/edit/<string:sno>", methods=["GET", "POST"])
def edit(sno):
    if "user" in session and session["user"] == params["admin_user"]:
        if request.method == "POST":
            box_title = request.form.get("title")
            tline = request.form.get("tline")
            slug = request.form.get("slug")
            content = request.form.get("content")
            img_file = request.form.get("img_file")
            date = datetime.now()

            if sno == "0":
                post = Posts(
                    title=box_title,
                    slug=slug,
                    content=content,
                    tagline=tline,
                    img_file=img_file,
                    date=date,
                )
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.tagline = tline
                post.slug = slug
                post.content = content
                post.img_file = img_file
                post.date = date
                db.session.commit()
                return redirect(f"/dashboard")

    post = Posts.query.filter_by(sno=sno).first()
    return render_template("edit.html", params=params, sno=sno, post=post)


@app.route("/uploader", methods=["GET", "POST"])
def uploader():
    if (
        "user" in session and session["user"] == params["admin_user"]
    ):  # if the user is logged in then he/she can upload the file
        if (
            request.method == "POST"
        ):  # the user must request the post instead of typing the url manually in the browser
            f = request.files[
                "file1"
            ]  # will fetch the file from the admin panel which is named as file1 and store it in f var
            f.save(
                os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename))
            )  # then we'll save the file here
            return "Uploaded successfully!"  # returning a success  message bro


@app.route("/delete/<string:sno>", methods=["GET", "POST"])
def delete(sno):
    if (
        "user" in session and session["user"] == params["admin_user"]
    ):  # only if the user is logged in then he/she can delete the post
        post = Posts.query.filter_by(
            sno=sno
        ).first()  # fetching the post that we want to delte
        db.session.delete(post)  # deletion code
        db.session.commit()  # confirming that we want to delte using code
    return redirect("/dashboard")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # fetch data from the front end to the backend
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        # adding the data from backend to the database
        entry = Contacts(
            name=name, phone_num=phone, msg=message, date=datetime.now(), email=email
        )
        # values on the left will align with phpadmin's table's column name and right will match the name of the variable that's used above
        # didn't include sno hence that will automatically increasng and date will be the current date

        db.session.add(entry)
        db.session.commit()

        # after comitting we'll send a notification via mail in the following process
        # mail.send_message('New message from ' + name,
        # sender = email,
        # recipients = params["gmail-user"],
        # body = message,
        # )
        flash("Thanks for your fucking feedback. Now back to brainrot!")
    return render_template("contact.html", params=params)


@app.route("/about")
def about():
    return render_template("about.html", params=params)


@app.route("/test")
def test():
    return render_template("test.html", params=params)


if __name__ == "__main__":
    app.run(debug=True)

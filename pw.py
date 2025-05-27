from flask import Flask, render_template, request, session, redirect, flash
import json
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import math
import os
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import pymysql
import random
import bcrypt

with open("config.json", "r") as c:
    params = json.load(c)["params"]

app = Flask(__name__)

app.secret_key = "super-secret-key"
# app.config['UPLOAD_FOLDER'] = params['upload_location']

app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME="uchhassaha46@gmail.com",
    MAIL_PASSWORD="ksoz qsde qypk doyg",
)
mail = Mail(app)


def create_database_if_not_exists():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",  # your root password (IF ANY)
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS uchhas")
    connection.close()


create_database_if_not_exists()

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root@localhost/uchhas"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)
app.jinja_env.globals.update(getattr=getattr)


# Define your models
class Resume(db.Model):
    __tablename__ = "resume"
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(25), nullable=False)
    degree = db.Column(db.String(250), nullable=False)
    institute = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1500), nullable=False)


class Certificates(db.Model):
    __tablename__ = "certificates"
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    url = db.Column(db.String(5000), nullable=False)


class XP(db.Model):
    __tablename__ = "xp"
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=False)


class Contacts(db.Model):
    __tablename__ = "contacts"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    num = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    msg = db.Column(db.String(1500), nullable=False)
    date = db.Column(db.String(13), nullable=True)


class Services(db.Model):
    __tablename__ = "services"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    image_file = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(100), nullable=True)


class Skills(db.Model):
    __tablename__ = "skills"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    percentage = db.Column(db.String(500), nullable=False)


class Language(db.Model):
    __tablename__ = "language"
    sno = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(250), nullable=False)
    percentage = db.Column(db.String(20), nullable=False)


class Projects(db.Model):
    __tablename__ = "projects"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(2000), nullable=False)
    img_file = db.Column(db.String(500), nullable=False)


class CV(db.Model):
    __tablename__ = "cv"
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5250), nullable=False)
    file = db.Column(db.String(1000), nullable=False)


with app.app_context():
    db.create_all()

    # Seed Projects if none exist
    if not Projects.query.first():
        print("Seeding Projects...")
        projects = [
            Projects(
                name="TextUtils",
                category="Django Web development",
                url="https://github.com/Uchhas007/Text-Utils.git",
                img_file="images/project - txtutils.jpg",
            ),
            Projects(
                name="Snake Game",
                category="Game Development using Pygame",
                url="https://github.com/Uchhas007/Snake-Game.git",
                img_file="images/project snake game.png",
            ),
            Projects(
                name="Drizzler",
                category="Django Web Development",
                url="https://github.com/Uchhas007/Drizzler.git",
                img_file="images/project drizzler.jpg",
            ),
            Projects(
                name="Ami Bolsi",
                category="Flask Web Development",
                url="https://github.com/Uchhas007/ami-bolsi.git",
                img_file="images/project ami bolsi.jpg",
            ),
        ]
        db.session.add_all(projects)
        db.session.commit()
        print("Projects seeded successfully.")

    # Seed Services if none exist
    if not Services.query.first():
        print("Seeding Services...")
        services = [
            Services(
                name="Back-End Web Development in Django and/or Flask",
                image_file="images/backend.jpg",
                date="2025-05-28",
            ),
            Services(
                name="Database Management using MySQL, SQL Lite, and SQL Server",
                image_file="images/dbm.jpg",
                date="2025-05-28",
            ),
            Services(
                name="Software Engineering",
                image_file="images/software engineering.jpg",
                date="2025-05-28",
            ),
            Services(
                name="Machine Learning", image_file="images/ml.jpg", date="2025-05-28"
            ),
        ]
        db.session.add_all(services)
        db.session.commit()
        print("Services seeded successfully.")

    # Seed XP (Experience) if none exist
    if not XP.query.first():
        print("Seeding Experience...")
        experiences = [
            XP(
                date="07/2019 - 04/2021",
                name="Joint Secretary (Day Shift)",
                platform="Remians Art Club - Dhaka Residential Model College",
                description="As the Joint Secretary of the Remians Art Club, I coordinated events, mentored junior members, and organized art exhibitions to foster creativity.",
            ),
            XP(
                date="06/2023 - 02/2024",
                name="Apprentice",
                platform="Robotics Club of BRAC University",
                description="As an apprentice in the Finance and Marketing department, I supported event budgeting and promoted club activities through digital platforms.",
            ),
            XP(
                date="02/2024 - 08/2024",
                name="Junior Executive",
                platform="Robotics Club of BRAC University",
                description="As a Junior Executive in Finance and Marketing at the Robotics Club, I led sponsorship outreach and managed budgeting for tech events.",
            ),
            XP(
                date="05/2024 - 06/2024",
                name="Campus Ambassador",
                platform="G17 Global",
                description="As a Campus Ambassador for the G17 - Bangladesh, I promoted the organization's mission, engaged students in SDG initiatives, and facilitated campus events.",
            ),
            XP(
                date="06/2024 - 04/2025",
                name="Campus Director",
                platform="G17 Global",
                description="As the Campus Director for G17 – Bangladesh at BRAC University, I led SDG-related campaigns, coordinated student involvement, and strengthened partnerships.",
            ),
            XP(
                date="04/2025 - 05/2025",
                name="Machine Learning Intern",
                platform="CodSoft",
                description="I developed customized algorithms to enable critical business insights and collaborated on predictive analytics solutions using Python and ML frameworks.",
            ),
            XP(
                date="04/2025 - 06/2025",
                name="Machine Learning Intern",
                platform="CodeAlpha",
                description="I designed and implemented customized machine learning models to solve classification problems and improved model accuracy through iterative testing.",
            ),
        ]
        db.session.add_all(experiences)
        db.session.commit()
        print("Experience seeded successfully.")

    if not Language.query.first():
        print("Seeding Languages...")
        languages = [
            Language(lang="Bengali", percentage="97"),
            Language(lang="English", percentage="95"),
        ]
        db.session.add_all(languages)
        db.session.commit()
        print("Languages seeded successfully.")

    # Seed Skills if none exist
    if not Skills.query.first():
        print("Seeding Skills...")
        skills = [
            Skills(name="Python", percentage="90"),
            Skills(name="Java", percentage="65"),
            Skills(name="HTML, CSS and JS", percentage="70"),
            Skills(name="Bootstrap", percentage="95"),
            Skills(name="Database management using MySQL", percentage="90"),
            Skills(name="Database management using SQL Server", percentage="90"),
            Skills(name="Back End Web Development using Flask", percentage="90"),
            Skills(name="Back End Web Development using Django", percentage="90"),
            Skills(name="Machine Learning", percentage="75"),
        ]
        db.session.add_all(skills)
        db.session.commit()
        print("Skills seeded successfully")

    # Seed CV file if none exists
    if not CV.query.first():
        print("Seeding CV...")
        cv_entry = CV(
            title="Uchhas Saha - Resume", file="files/Uchhas Saha - Resume.pdf"
        )
        db.session.add(cv_entry)
        db.session.commit()
        print("CV seeded successfully.")

    # Seed Certificates if none exist
    if not Certificates.query.first():
        print("Seeding Certificates...")
        certificates = [
            Certificates(
                date="09/2024 - Present",
                name="Python (Basic) Certificate",
                platform="HackerRank",
                description="Certified in Python fundamentals including Scalar types, Conditionals, Loops, Functions, and Built-in Methods.",
                url="https://www.hackerrank.com/certificates/iframe/679",
            ),
            Certificates(
                date="09/2024 - Present",
                name="Java (Basic) Certificate",
                platform="HackerRank",
                description="Covered core Java topics such as classes, data structures, and OOP fundamentals.",
                url="https://www.hackerrank.com/certificates/iframe/d36",
            ),
            Certificates(
                date="09/2024 - Present",
                name="Problem Solving (Basic)",
                platform="HackerRank",
                description="Achieved certification covering fundamental Data Structures and Algorithms.",
                url="https://www.hackerrank.com/certificates/iframe/2d2",
            ),
            Certificates(
                date="09/2024 - Present",
                name="Problem Solving (Intermediate)",
                platform="HackerRank",
                description="Achieved certification covering Data Structures (e.g., Stacks, Queues) and Algorithm design patterns.",
                url="https://www.hackerrank.com/certificates/iframe/696",
            ),
            Certificates(
                date="02/2025 - Present",
                name="Second Runner's Up at Hult - On Campus Program",
                platform="HULT",
                description="Launched our own sustainable and eco-friendly business initiative as part of a team competition.",
                url="instagram",
            ),
            Certificates(
                date="03/2025 - Present",
                name="Introduction of SQL",
                platform="DataCamp",
                description="Achieved certification covering basic SQL Commands such as SELECT, WHERE, and JOIN.",
                url="https://www.datacamp.com/completed/statement-of-accomplishment",
            ),
            Certificates(
                date="04/2025 - Present",
                name="Introduction to SQL Server",
                platform="DataCamp",
                description="Achieved certification covering SQL Server-specific syntax and commands.",
                url="https://www.datacamp.com/completed/statement-of-accomplishment",
            ),
            Certificates(
                date="05/2025 - Present",
                name="SQL (Basic) Certificate",
                platform="HackerRank",
                description="Achieved certification covering basic SQL Commands and query operations.",
                url="https://www.hackerrank.com/certificates/iframe/e2c",
            ),
            Certificates(
                date="05/2025 - Present",
                name="SQL (Intermediate) Certificate",
                platform="HackerRank",
                description="Achieved certification covering advanced SQL Commands including subqueries, joins, and aggregations.",
                url="https://www.hackerrank.com/certificates/iframe/9d8",
            ),
            Certificates(
                date="05/2025 - Present",
                name="Software Engineer",
                platform="HackerRank",
                description="Achieved certification covering advanced topics like system design, coding assessments, and OOP.",
                url="https://www.hackerrank.com/certificates/iframe/84b",
            ),
            Certificates(
                date="05/2025 - Present",
                name="Software Engineer Intern",
                platform="HackerRank",
                description="Achieved certification covering intern topics like version control, debugging, and productivity tools.",
                url="https://www.hackerrank.com/certificates/iframe/35d",
            ),
        ]
        db.session.add_all(certificates)
        db.session.commit()
        print("Certificates seeded successfully.")


# backend
@app.route("/")
def home():
    return render_template("home.html", params=params)


@app.route("/resume")
def resume():
    resume = Resume.query.all()
    cert = Certificates.query.all()
    return render_template("resume.html", params=params, r=resume, c=cert)


@app.route("/services")
def services():
    service = Services.query.all()
    xp = XP.query.all()
    return render_template("services.html", params=params, s=service, e=xp)


@app.route("/skills")
def skills():
    skill = Skills.query.all()
    lang = Language.query.all()
    return render_template("skills.html", params=params, skills=skill, lang=lang)


@app.route("/projects")
def projects():
    project = Projects.query.all()
    return render_template("projects.html", params=params, p=project)


@app.route("/blog")
def myblog():
    return render_template("blog.html", params=params)


@app.route("/about")
def about():
    cv = CV.query.order_by(CV.sno.desc()).first()
    return render_template("about.html", params=params, cv=cv)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        cont = request.form.get("num")
        email = request.form.get("email")
        sub = request.form.get("subject")
        message = request.form.get("msg")
        entry = Contacts(
            name=name,
            num=cont,
            email=email,
            subject=sub,
            msg=message,
            date=datetime.now(),
        )

        db.session.add(entry)
        db.session.commit()

        # mail.send_message('New message from ' + name,
        # sender = email,
        # recipients = params["gmail-user"],
        # body = message,

        flash("Thanks for contacting us. I will get back to you soon!!!")
    return render_template("contact.html", params=params)


# Administration
@app.route("/admin/", methods=["GET", "POST"])
def admin():
    if "user" in session and session["user"] == params["admin"]:
        resume = Resume.query.all()
        contacts = Contacts.query.all()
        services = Services.query.all()
        skills = Skills.query.all()
        projects = Projects.query.all()

        return render_template(
            "admin.html",
            params=params,
            r=resume,
            c=contacts,
            services=services,
            skills=skills,
            p=projects,
        )

    if request.method == "POST":
        useremail = request.form.get("email")
        userpass = request.form.get("pass")

        if useremail == params["admin"] and userpass == params["pass"]:
            session["user"] = useremail
            resume = Resume.query.all()
            contacts = Contacts.query.all()
            services = Services.query.all()
            skills = Skills.query.all()
            projects = Projects.query.all()

            return render_template(
                "admin.html",
                params=params,
                r=resume,
                c=contacts,
                services=services,
                skills=skills,
                p=projects,
            )

    else:
        return render_template("login.html", params=params)


@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/admin")


@app.route("/admin/contacts", methods=["GET", "POST"])
def adminContacts():
    if "user" in session and session["user"] == params["admin"]:
        contacts = Contacts.query.all()
        return render_template("adc.html", params=params, c=contacts)
    else:
        return render_template("login.html", params=params)


@app.route("/admin/projects", methods=["GET", "POST"])
def adminProjects():
    if "user" in session and session["user"] == params["admin"]:
        projects = Projects.query.all()
        return render_template("adp.html", params=params, c=projects)
    else:
        return render_template("login.html", params=params)


@app.route("/admin/resume", methods=["GET", "POST"])
def adminResume():
    if "user" in session and session["user"] == params["admin"]:
        resume = Resume.query.all()
        return render_template("adr.html", params=params, c=resume)
    else:
        return render_template("login.html", params=params)


@app.route("/admin/services", methods=["GET", "POST"])
def adminServices():
    if "user" in session and session["user"] == params["admin"]:
        services = Services.query.all()
        return render_template("adse.html", params=params, c=services)
    else:
        return render_template("login.html", params=params)


@app.route("/admin/skills", methods=["GET", "POST"])
def adminSkills():
    if "user" in session and session["user"] == params["admin"]:
        skills = Skills.query.all()
        return render_template("adsk.html", params=params, c=skills)
    else:
        return render_template("login.html", params=params)


# http://127.0.0.1:5000/Resume/first-Resume
# @app.route("/Resume/<string:Resume_slug>", methods=['GET'])
# def Resume_route(Resume_slug):
#     p = Resume.query.filter_by(slug=Resume_slug).first()
#     return render_template('Resume.html', params=params, Resume = p)

# http://127.0.0.1:5000/admin/contacts/edit/1
# @app.route("/admin/contacts/edit/<string:sno>" , methods=['GET', 'POST'])
# def edit(sno):
#     if "user" in session and session['user']==params['admin']:
#         if request.method=="POST":
#             name = request.form.get('name')
#             num = request.form.get('num')
#             email = request.form.get('email')
#             sub = request.form.get('subject')
#             msg = request.form.get('msg')
#             date = datetime.now()

#             if sno == "0":
#                 return render_template('404.html', params=params)
#             else:
#                 c = Contacts.query.filter_by(sno=(sno)).first()
#                 c.name = name
#                 c.num = num
#                 c.email = email
#                 c.subject = sub
#                 c.msg = msg
#                 c.date = date
#                 db.session.commit()
#                 return redirect(f'/admin')

#     c = Contacts.query.filter_by(sno=sno).first()
#     return render_template('edit.html', params=params, sno = sno, contact = c)

model_map = {
    "contacts": Contacts,
    "projects": Projects,
    "skills": Skills,
    "services": Services,
    "resume": Resume,
}


@app.route("/admin/<table>/edit/<string:sno>", methods=["GET", "POST"])
def edit_dynamic(table, sno):
    if "user" in session and session["user"] == params["admin"]:
        model = model_map.get(table)
        if not model:
            return render_template("404.html", params=params)

        record = model.query.filter_by(sno=sno).first()
        if not record:
            return render_template("404.html", params=params)

        if request.method == "POST":
            for field in record.__dict__:
                if field not in ["_sa_instance_state", "sno", "date"]:
                    setattr(record, field, request.form.get(field))

            if hasattr(record, "date"):
                record.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.session.commit()

            return redirect(f"/admin/{table}")

        return render_template(
            "nedit.html", record=record, table=table, sno=sno, params=params
        )

    return redirect("/login")


# @app.route("/uploader" , methods=['GET', 'Resume'])
# def uploader():
#     if "user" in session and session['user']==params['admin_user']:
#         if request.method=='Resume':
#             f = request.files['file1']
#             f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
#             return "Uploaded successfully!"


@app.route("/uploader/<string:table>", methods=["GET", "POST"])
def uploader(table):
    if "user" in session and session["user"] == params["admin_user"]:
        if request.method == "POST":
            if "file" not in request.files:
                return "No file part, bro."

            file = request.files["file"]
            if file.filename == "":
                return "No file selected. You kidding?"

            if file:
                filename = secure_filename(file.filename)
                upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(upload_path)

                return f"File uploaded successfully to '{upload_path}' for table '{table}' 😎"

        return f"<h1>Upload something for table '{table}'</h1>"
    return redirect("/login")


@app.route("/admin/<table>/delete/<string:sno>", methods=["GET", "Resume"])
def delete(table, sno):
    if "user" in session and session["user"] == params["admin_user"]:
        model = model_map.get(table)
        if not model:
            return render_template("404.html", params=params)

        record = model.query.filter_by(sno=sno).first()
        if not record:
            return render_template("404.html", params=params)

        db.session.delete(record)
        db.session.commit()

    return redirect(f"/admin/{table}")


# tester
@app.route("/test")
def test():
    return render_template("test.html", params=params)


if __name__ == "__main__":
    app.run(debug=True)

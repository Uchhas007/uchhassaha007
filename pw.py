from flask import Flask, render_template, request, session, redirect, flash
import json 
from flask_mail import Mail 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math
import os
from werkzeug.utils import secure_filename
import secrets
import os
from dotenv import load_dotenv


with open('config.json', 'r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)

s  = (secrets.token_hex(32))

# Load .env file
load_dotenv()

# Set secret key from .env
app.secret_key = os.getenv("SECRET_KEY")

# app.secret_key = 'super-secret-key'

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/uchhas' 
db = SQLAlchemy(app)

class Resume(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(25), nullable=False)
    degree = db.Column(db.String(250), nullable=False)
    institute = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1500), nullable=False)

class Certificates(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    url = db.Column(db.String(5000), nullable=False)

class XP(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=False)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    num = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    msg = db.Column(db.String(1500), nullable=False)
    date = db.Column(db.String(13), nullable=True)

class Services(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    image_file = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(100), nullable=True)  

class Skills(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    percentage = db.Column(db.String(500), nullable=False)  

class Language(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(250), nullable=False)
    percentage = db.Column(db.String(20), nullable=False)  

class Projects(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(1000), nullable=False)    
    url = db.Column(db.String(2000), nullable=False)
    img_file = db.Column(db.String(500), nullable=False)

class CV(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5250), nullable=False)
    file = db.Column(db.String(1000), nullable=False) 

# backend 
@app.route('/')  
def home():
    return render_template('home.html', params=params) 

@app.route('/resume')  
def resume():
    resume = Resume.query.all()
    cert = Certificates.query.all()
    return render_template('resume.html', params=params, r = resume, c = cert)

@app.route('/services')  
def services():
    service = Services.query.all()
    xp = XP.query.all()
    return render_template('services.html', params=params, s = service, e = xp)

@app.route('/skills')  
def skills():
    skill = Skills.query.all()
    lang = Language.query.all()
    return render_template('skills.html', params=params, skills = skill, lang = lang)

@app.route('/projects')  
def projects():
    project = Projects.query.all()
    return render_template('projects.html', params=params, p = project)

@app.route('/blog')  
def myblog():
    return render_template('blog.html', params=params)

@app.route('/about')  
def about():
    cv = CV.query.order_by(CV.sno.desc()).first()
    return render_template('about.html', params=params, cv = cv)


@app.route('/contact', methods=['GET', 'POST'])  
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        cont = request.form.get('num')
        email = request.form.get('email')
        sub = request.form.get('subject')
        message = request.form.get('msg')
        entry = Contacts(name = name, num = cont, email = email, subject = sub, msg = message, date = datetime.now())
        
        db.session.add(entry)
        db.session.commit()

        # mail.send_message('New message from ' + name,
        # sender = email,
        # recipients = params["gmail-user"],
        # body = message,

        flash('Thanks for contacting us. I will get back to you soon!!!')    
    return render_template('contact.html', params = params)



# Administration
@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if "user" in session and session['user'] == params['admin']:
        resume = Resume.query.all()
        contacts = Contacts.query.all()
        services = Services.query.all()
        skills = Skills.query.all()
        projects = Projects.query.all()

        return render_template("admin.html", params = params, r = resume, c = contacts, services = services, skills = skills, p = projects)

    if request.method == "POST":
        useremail = request.form.get("email") 
        userpass = request.form.get("pass")

        if useremail == params['admin'] and userpass == params['pass']:
            session['user'] = useremail
            resume = Resume.query.all()
            contacts = Contacts.query.all()
            services = Services.query.all()
            skills = Skills.query.all()
            projects = Projects.query.all()

            return render_template("admin.html", params = params, r = resume, c = contacts, services = services, skills = skills, p = projects)
        
    else:
        return render_template("login.html", params = params) 

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/admin')

@app.route('/admin/contacts', methods=['GET', 'POST'])
def adminContacts():
    if "user" in session and session['user'] == params['admin']:
        contacts = Contacts.query.all()
        return render_template("adc.html", params = params, c = contacts)
    else:
        return render_template("login.html", params = params)

@app.route('/admin/projects', methods=['GET', 'POST'])
def adminProjects():
    if "user" in session and session['user'] == params['admin']:
        projects = Projects.query.all()
        return render_template("adp.html", params = params, c = projects)
    else:
        return render_template("login.html", params = params)

@app.route('/admin/resume', methods=['GET', 'POST'])
def adminResume():
    if "user" in session and session['user'] == params['admin']:
        resume = Resume.query.all()
        return render_template("adr.html", params = params, c = resume)
    else:
        return render_template("login.html", params = params)
    
@app.route('/admin/services', methods=['GET', 'POST'])
def adminServices():
    if "user" in session and session['user'] == params['admin']:
        services = Services.query.all()
        return render_template("adse.html", params = params, c = services)
    else:
        return render_template("login.html", params = params)

@app.route('/admin/skills', methods=['GET', 'POST'])
def adminSkills():
    if "user" in session and session['user'] == params['admin']:
        skills = Skills.query.all()
        return render_template("adsk.html", params = params, c = skills)
    else:
        return render_template("login.html", params = params)


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
    "resume": Resume
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
            
            if hasattr(record, 'date'):
                record.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.commit()
            
            return redirect(f"/admin/{table}")

        return render_template("nedit.html", record=record, table = table, sno=sno, params=params)

    return redirect("/login")

# @app.route("/uploader" , methods=['GET', 'Resume'])
# def uploader():
#     if "user" in session and session['user']==params['admin_user']:  
#         if request.method=='Resume': 
#             f = request.files['file1']
#             f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))  
#             return "Uploaded successfully!" 

@app.route("/uploader/<string:table>", methods=['GET', 'POST'])
def uploader(table):
    if "user" in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            if 'file' not in request.files:
                return "No file part, bro."

            file = request.files['file']
            if file.filename == '':
                return "No file selected. You kidding?"

            if file:
                filename = secure_filename(file.filename)
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                
                return f"File uploaded successfully to '{upload_path}' for table '{table}' 😎"

        return f"<h1>Upload something for table '{table}'</h1>"
    return redirect('/login')

@app.route("/admin/<table>/delete/<string:sno>" , methods=['GET', 'Resume'])
def delete(table, sno):
    if "user" in session and session['user']==params['admin_user']:
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
@app.route('/test')  
def test():
    return render_template('test.html', params=params)


if __name__ == '__main__':
    app.run(debug=True)
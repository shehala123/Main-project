import os
from flask import *
from werkzeug.utils import secure_filename

from src.dbconnection import *

import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail



app = Flask(__name__)
app.secret_key='aa'

# mail=Mail(app)
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'Insightblind364@gmail.com'
# app.config['MAIL_PASSWORD'] = 'mails2020'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
import functools

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('log.html')
        return func()

    return secure_function

@app.route('/')
def login():
    return render_template("index.html")

@app.route('/log')
def log():
    return render_template("log.html")

@app.route('/homepage')
def homepage():
    return render_template("HOMEPAGE ADMIN.html")

@app.route('/Caretaker_registration')
def Caretaker_registration():
    return render_template("caretaker registration.html")
@app.route('/view & approve caretaker')
@login_required
def viewapprove_caretaker():
    qry="SELECT `care_registration`. *, `login`.`usertype`,DATE_FORMAT(Dob,'%d-%m-%Y') FROM`care_registration` JOIN `login` ON `login`.`login_id` = `care_registration`.`login_id` WHERE`login`.`usertype` = 'Pending'"
    res=selectall(qry)
    return render_template("view & approve caretaker.html",val=res)
@app.route('/Accept_caretaker')
@login_required
def accept_caretaker():
    id=request.args.get('id')
    qry="UPDATE `login` SET `usertype`='caretaker' WHERE `login_id`=%s"
    iud(qry,str(id))
    return '''<script>alert("Admin Accepted  you are registration!");
           window.location='/'</script>'''

@app.route('/Reject_caretaker')
@login_required
def reject_caretaker():
    id = request.args.get('id')
    qry = "UPDATE `login` SET `usertype`='reject' WHERE `login_id`=%s"
    iud(qry, str(id))
    return '''<script>alert("Admin Rejected you are registration ");
           window.location='/'</script>'''

@app.route('/care_homepage')
@login_required
def care_homepage():
    loginID = session['lid']
    qry = "SELECT Fname,Lname FROM  `care_registration` WHERE `login_id`= %s "
    res = selectone(qry, loginID)
    name = res[0]+" "+res[1]
    return render_template("care homepage.html",name=name)


@app.route('/loginform',methods=['POST'])
def loginform():
    uname = request.form['textfield']
    password = request.form['textfield2']
    qry = "select*from login where username = %s and password= %s"
    val=(uname,password)
    res=selectone(qry,val)
    if res is None:
        return '''<script>alert("Invalid username and password");
        window.location='/'</script>'''
    elif res[3]=='admin':
        session['lid']=res[0]
        return redirect('/homepage')

    elif res[3]=='caretaker':
        session['lid'] = res[0]
        return redirect('/care_homepage')
    else:
        return '''<script>alert("Invalid username and password");
                window.location='/'</script>'''

@app.route('/care_registration',methods=['post'])
@login_required
def care_registration():
    Fname = request.form['textfield']
    Lname = request.form['textfield2']
    Gender = request.form['radiobutton']
    DOB = request.form['textfield3']
    Place= request.form['textfield4']
    Post = request.form['textfield5']
    Pin = request.form['textfield6']
    Phone = request.form['textfield7']
    Email = request.form['textfield8']
    Username= request.form['textfield9']
    Password = request.form['textfield10']
    conf_password = request.form['textfield11']
    if Password != conf_password:
        return '''<script>alert("Password must match!");
        history.back()  
        </script>'''

    qry1 ="insert into login values(Null,%s,%s,'Pending')"
    val =(Username,Password)
    id=iud(qry1,val)
    qry2 = "insert into care_registration values(Null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'Pending')"
    val2=(str(id),Fname,Lname,Gender,DOB,Place,Post,Pin,Phone,Email)
    iud(qry2,val2)
    return '''<script>alert("Registration Succesfull!");
           window.location='/'</script>'''


@app.route('/profile_update')
@login_required
def profile_update():
    lid=session['lid']
    qry="SELECT * ,DATE_FORMAT(Dob,'%d-%m-%Y') FROM `care_registration` WHERE `login_id`='"+str(lid)+"'"
    res=selectone1(qry)
    return render_template("update_profile.html",val=res)

@app.route('/update',methods=['post'])
@login_required
def update():
    Fname = request.form['textfield']
    Lname = request.form['textfield2']
    Gender = request.form['radiobutton']
    DOB = request.form['textfield3']
    Place = request.form['textfield4']
    Post = request.form['textfield5']
    Pin = request.form['textfield6']
    Phone = request.form['textfield7']
    Email = request.form['textfield8']

    qry="UPDATE `care_registration` SET `Fname`=%s,`Lname`=%s,`Gender`=%s,`Dob`=%s,`Place`=%s,`Post`=%s,`Pin`=%s,`Phone`=%s,`Email`=%s WHERE `login_id`=%s"
    val=(Fname,Lname,Gender,DOB,Place,Post,Pin,Phone,Email,session['lid'])
    iud(qry,val)


    return '''<script>alert("Profile Updated Succesfully!");
               window.location='/profile_update'</script>'''

@app.route('/blind_registration', methods=['post','get'])
@login_required
def blind_reg():
    return render_template("blind_registration.html")



@app.route('/blind_index')
@login_required
def blind_ind():
    return render_template("blindmanageindex.html")



@app.route('/add_blinds',methods=['post'])
@login_required
def blind_add():
    Fname = request.form['textfield2']
    Lname = request.form['textfield']
    Gender = request.form['radiobutton']
    DOB = request.form['textfield4']
    Place = request.form['textfield5']
    Post = request.form['textfield6']
    Pin = request.form['textfield7']
    Phone = request.form['textfield8']
    IMEI=request.form['textfield9']
    qry="INSERT INTO `blind_reg` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(Fname,Lname,Gender,DOB,Place,Post,Pin,Phone,IMEI,session['lid'])
    iud(qry,val)
    return '''<script>alert('Registration Succesfull!');window.location='/view_blind'</script>'''

@app.route('/view_blind')
@login_required
def view_blinds():

    qry="select blind_reg.*,DATE_FORMAT(Dob,'%d-%m-%Y') from blind_reg where C_id='"+str(session['lid'])+"'"
    # res=selectall2(qry,session['lid'])
    res=selectall(qry)
    print(res,"============================================")
    return render_template("blind.html",val=res)

# @app.route('/', methods=['post'])
# def profile_update():
#     return render_template("update_profile.html")

@app.route('/view approved caretaker')
@login_required
def approvedcaretaker():
    qry="SELECT `care_registration`. *, `login`.`usertype`,DATE_FORMAT(care_registration.Dob,'%d-%m-%Y')FROM`care_registration` JOIN `login` ON `login`.`login_id` = `care_registration`.`login_id` WHERE`login`.`usertype` = 'caretaker'"
    res=selectall(qry)
    return render_template("view approved caretaker.html",val=res)





@app.route('/viewblinds')
@login_required
def viewblinds():
    qry="SELECT * FROM `care_registration` WHERE `Status`='accepted'"
    res=selectall(qry)
    # qry="SELECT blind_reg.*,`care_registration`.`Fname`,`care_registration`.`Lname` FROM blind_reg JOIN `care_registration` ON `blind_reg`.`C_id`=`care_registration`.`login_id`"
    # res=selectall(qry)
    qry1 = "SELECT *,DATE_FORMAT(Dob,'%d-%m-%Y')FROM `blind_reg`"
    res1 = selectall(qry1)
    return render_template("view_blinds.html",val=res,v=res1)



@app.route('/add_familiar',methods=['post'])
@login_required

def addfamiliar():
    qry="SELECT * FROM `blind_reg` WHERE `C_id`=%s"
    res=selectall2(qry,session['lid'])


    return render_template("Add_familiar_person.html",val=res)

@app.route('/view_familiar')
@login_required
def viewfamilar():

    qry="SELECT `blind_reg`.* FROM `blind_reg` WHERE `C_id`=%s"
    res=selectall2(qry,session['lid'])


    return render_template("view_familiar.html",val=res)




@app.route('/view_familiar1',methods=['post'])
@login_required
def viewfamilar1():
    blind = request.form['select']
    qry="SELECT `blind_reg`.* FROM `blind_reg` WHERE `C_id`=%s"
    res=selectall2(qry,session['lid'])
    qry = "SELECT `familiar_person`.* FROM `familiar_person` WHERE `B_id`=%s "
    res1 = selectall2(qry,blind)
    return render_template("view_familiar.html",val=res,val1=res1,s=blind)








@app.route('/add_familiar1',methods=['post'])
@login_required
def addfamiliar1():
    BlindName = request.form['select']
    Name = request.form['textfield']
    Image = request.files['file']
    img=secure_filename(Image.filename)
    Image.save(os.path.join("static/familiar person",img))
    relation = request.form['textfield2']

    qry = "INSERT INTO `familiar_person` VALUES(NULL,%s,%s,%s,%s)"
    val = (BlindName ,Name, img, relation)
    iud(qry, val)
    return redirect('/view_familiar')


@app.route('/editblind')
@login_required
def edit_blind():
    id=request.args.get('id')
    session['eid']=id
    q="SELECT * FROM `blind_reg` WHERE `B_id`=%s"
    res=selectone(q,id)
    return render_template("editblind.html",val=res)


@app.route('/updateblind',methods=["post"])
@login_required
def update_blind():
    Fname = request.form['textfield2']
    Lname = request.form['textfield']
    Gender = request.form['radiobutton']
    DOB = request.form['textfield4']
    Place = request.form['textfield5']
    Post = request.form['textfield6']
    Pin = request.form['textfield7']
    Phone = request.form['textfield8']
    IMEI_NO = request.form['textfield9']
    qry = "UPDATE `blind_reg` SET `Fname`=%s,`Lname`=%s,`Gender`=%s,`Dob`=%s,`Place`=%s,`Post`=%s,`Pin`=%s,`Phone`=%s,`IMEI_NO`=%s WHERE `B_id`=%s"
    val = (Fname, Lname, Gender, DOB, Place, Post, Pin, Phone, IMEI_NO, session['eid'])
    iud(qry, val)
    return '''<script>alert('Update  Succesfull!');window.location='/view_blind'</script>'''




@app.route('/editfamiliar')
@login_required
def edit_familiar():
    qry = "SELECT * FROM `blind_reg` WHERE `C_id`=%s"
    res1 = selectall2(qry, session['lid'])

    id=request.args.get('id')
    session['fid']=id
    q="SELECT * FROM `familiar_person` WHERE `f_id`=%s"
    res=selectone(q,str(id))
    return render_template("editfamiliarperson.html",val=res,val1=res1)

@app.route('/updatefamiliar',methods=["post"])
@login_required
def update_familiar():
    try:
        BlindName = request.form['select']
        Name = request.form['textfield']
        Image = request.files['file']
        img = secure_filename(Image.filename)
        Image.save(os.path.join("static/familiar person", img))
        relation = request.form['textfield2']

        qry = "UPDATE `familiar_person` SET `B_id`=%s,`Name`=%s,`Image`=%s,`Relation`=%s WHERE `f_id`=%s"
        val = (BlindName,Name,img,relation,session['fid'])
        iud(qry, val)
        return redirect("view_familiar")
    except Exception as e:
        BlindName = request.form['select']
        Name = request.form['textfield']

        relation = request.form['textfield2']

        qry = "UPDATE `familiar_person` SET `B_id`=%s,`Name`=%s,`Relation`=%s WHERE `f_id`=%s"
        val = (BlindName, Name, relation, session['fid'])
        iud(qry,val)
        return redirect("view_familiar")

@app.route('/deletefamiliar')
@login_required
def delete_familiar():
    id=request.args.get('id')
    qry="DELETE FROM `familiar_person` WHERE f_id=%s"
    iud(qry,id)
    return '''<script>alert('DELETED!');window.location='/view_familiar'</script>'''


@app.route('/deleteblind')
@login_required
def delete_blind():
    id=request.args.get('id')
    qry="DELETE FROM `blind_reg` WHERE B_id=%s"
    iud(qry,id)
    return '''<script>alert('DELETED!');window.location='/view_blind'</script>'''

@app.route('/search_blinds',methods=["post"])
@login_required
def search_blinds():
    name=request.form['select']
    qry="SELECT * FROM `blind_reg` WHERE `C_id` = %s"
    res=selectall2(qry,name)
    qry1="SELECT * FROM `care_registration` WHERE `Status`='accepted'"
    res1=selectall(qry1)
    return render_template("view_blinds.html",v=res,val=res1,s=name)
@app.route('/viewreply')
@login_required
def viewreply():
    qry="select *,DATE_FORMAT(complaints.date,'%d-%m-%y') from complaints where care_id="+str(session['lid'])
    res=selectall(qry)

    return render_template("viewreply.html",val=res)


@app.route('/send_complaints',methods=["post"])
@login_required
def send_complaints():

    return render_template("Send_complaints.html")



@app.route('/send_comp',methods=["post"])
@login_required
def send_comp():
    complaint=request.form['textarea']
    qry="INSERT INTO `complaints`VALUES(NULL,%s,%s,CURDATE(),'pending')"
    val=(session['lid'],complaint)
    iud(qry,val)
    return '''<script>alert('SENDED!');window.location='/viewreply'</script>'''


@app.route('/location',methods=["post",'get'])
@login_required
def loc():
    qry="SELECT `blind_reg`.`Fname`,`Lname`,`location`.`Latitude`,`Longitude` FROM `location` JOIN `blind_reg` ON `blind_reg`.`B_id`=`location`.`B_id` WHERE `blind_reg`.`C_id`=%s"
    res=selectall2(qry,session['lid'])
    return render_template("location.html",val=res)

@app.route('/view')
@login_required
def view_com():
    qry= "SELECT `complaints`.* ,`care_registration`.`Fname`,`care_registration`.`Lname`,DATE_FORMAT(complaints.date,'%d-%m-%y') FROM `care_registration` JOIN `complaints` ON `care_registration`.`login_id`= `complaints`.`care_id` WHERE `complaints`.`reply`='pending'"
    res=selectall(qry)
    print(res,"==========================")
    return render_template("view_complints_admin.html",val=res)

@app.route('/send_reply')
@login_required
def send_reply():
    id=request.args.get('id')
    session['cid']=id
    return render_template("send_reply.html")

@app.route('/sending_reply',methods=['post'])
@login_required
def sending_reply():

    reply=request.form['textarea']
    qry="UPDATE `complaints` SET reply=%s WHERE `complaint_id`=%s"
    val=(reply,session['cid'])
    iud(qry,val)

    return redirect("view")

@app.route('/forgot')

def forgot():

    return render_template("forgot.html")

@app.route('/forgotpassword1',methods=['post'])

def forgotpassword1():
    print(request.form)
    try:
        print(request.form)
        email = request.form['textfield']
        print(email)
        qry = "SELECT `login`.`password` FROM `login` JOIN `care_registration` ON `login`.`login_id`=`care_registration`.`login_id` WHERE `care_registration`.`Email`=%s"
        s = selectone(qry, email)
        print(s, "=============")
        if s is None:
            return '''<script>alert('invalid!');window.location='/'</script>'''
        else:
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)
                gmail.ehlo()
                gmail.starttls()
                gmail.login('insightblind364@gmail.com', 'iuhjzrfyoembxhcs')
            except Exception as e:
                print("Couldn't setup email!!" + str(e))
            msg = MIMEText("Your new password is : " + str(s[0]))
            print(msg)
            msg['Subject'] = 'INSIGHT'
            msg['To'] = email
            msg['From'] = 'insightblind364@gmail.com'
            try:
                gmail.send_message(msg)
            except Exception as e:
                print("COULDN'T SEND EMAIL", str(e))
            return '''<script>alert("SEND"); window.location="/"</script>'''
    except:
        return '''<script>alert("PLEASE ENTER VALID DETAILS"); window.location="/"</script>'''



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/log')



app.run(debug=True)
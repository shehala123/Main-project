import os
from flask import *
from werkzeug.utils import secure_filename

from src.dbconnection import *
app = Flask(__name__)
app.secret_key='aa'
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
def viewapprove_caretaker():
    qry="SELECT `care_registration`. *, `login`.`usertype`FROM`care_registration` JOIN `login` ON `login`.`login_id` = `care_registration`.`login_id` WHERE`login`.`usertype` = 'Pending'"
    res=selectall(qry)
    return render_template("view & approve caretaker.html",val=res)
@app.route('/Accept_caretaker')
def accept_caretaker():
    id=request.args.get('id')
    qry="UPDATE `login` SET `usertype`='caretaker' WHERE `login_id`=%s"
    iud(qry,str(id))
    return '''<script>alert("Admin Accepted  you are registration!");
           window.location='/'</script>'''

@app.route('/Reject_caretaker')
def reject_caretaker():
    id = request.args.get('id')
    qry = "UPDATE `login` SET `usertype`='reject' WHERE `login_id`=%s"
    iud(qry, str(id))
    return '''<script>alert("Admin Rejected you are registration ");
           window.location='/'</script>'''

@app.route('/care_homepage')
def care_homepage():
    return render_template("care homepage.html")


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
def profile_update():
    lid=session['lid']
    qry="SELECT * FROM `care_registration` WHERE `login_id`=%s"
    res=selectone(qry,lid)
    return render_template("update_profile.html",val=res)

@app.route('/update',methods=['post'])
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
def blind_reg():
    return render_template("blind_registration.html")



@app.route('/blind_index')
def blind_ind():
    return render_template("blindmanageindex.html")



@app.route('/add_blinds',methods=['post'])
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
def view_blinds():
    qry="select * from blind_reg"
    res=selectall(qry)
    return render_template("blind.html",val=res)

# @app.route('/', methods=['post'])
# def profile_update():
#     return render_template("update_profile.html")

@app.route('/view approved caretaker')
def approvedcaretaker():
    qry="SELECT `care_registration`. *, `login`.`usertype`FROM`care_registration` JOIN `login` ON `login`.`login_id` = `care_registration`.`login_id` WHERE`login`.`usertype` = 'caretaker'"
    res=selectall(qry)
    return render_template("view approved caretaker.html",val=res)





@app.route('/viewblinds')
def viewblinds():
    qry="SELECT blind_reg.*,`care_registration`.`Fname`,`care_registration`.`Lname` FROM blind_reg JOIN `care_registration` ON `blind_reg`.`C_id`=`care_registration`.`login_id`"
    res=selectall(qry)
    return render_template("view_blinds.html",val=res)



@app.route('/add_familiar',methods=['post'])
def addfamiliar():
    qry="SELECT * FROM `blind_reg` WHERE `C_id`=%s"
    res=selectall2(qry,session['lid'])


    return render_template("Add_familiar_person.html",val=res)

@app.route('/view_familiar')
def viewfamilar():
    qry = "SELECT `blind_reg`.`Fname`,`blind_reg`.`Lname`,`familiar_person`.* FROM `familiar_person` JOIN `blind_reg` ON `blind_reg`.B_id=`familiar_person`.B_id"
    res = selectall(qry)
    return render_template("view_familiar.html",val=res)


@app.route('/add_familiar1',methods=['post'])
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
def edit_blind():
    id=request.args.get('id')
    session['eid']=id
    q="SELECT * FROM `blind_reg` WHERE `B_id`=%s"
    res=selectone(q,id)
    return render_template("editblind.html",val=res)


@app.route('/updateblind',methods=["post"])
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
def edit_familiar():
    qry = "SELECT * FROM `blind_reg` WHERE `C_id`=%s"
    res1 = selectall2(qry, session['lid'])

    id=request.args.get('id')
    session['fid']=id
    q="SELECT * FROM `familiar_person` WHERE `f_id`=%s"
    res=selectone(q,str(id))
    return render_template("editfamiliarperson.html",val=res,val1=res1)

@app.route('/updatefamiliar',methods=["post"])
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
def delete_familiar():
    id=request.args.get('id')
    qry="DELETE FROM `familiar_person` WHERE f_id=%s"
    iud(qry,id)
    return '''<script>alert('DELETED!');window.location='/view_familiar'</script>'''


@app.route('/deleteblind')
def delete_blind():
    id=request.args.get('id')
    qry="DELETE FROM `blind_reg` WHERE B_id=%s"
    iud(qry,id)
    return '''<script>alert('DELETED!');window.location='/view_blind'</script>'''



app.run(debug=True)
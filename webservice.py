import os
from flask import *
from src.recognize_face import rec_face_image
import cv2
from scipy.ndimage import rotate

from src.dbconnection import *
app = Flask(__name__)
from src.objectdetection import objdet
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
@app.route('/ip',methods=['post'])
def ip():
    ip=request.form['imei']
    print("imei",ip)
    qry="SELECT * FROM `blind_reg` WHERE `IMEI_NO`=%s"
    res=selectone(qry,ip)
    if res is None:
        return jsonify({'task': 'invalid'})
    else:

        return jsonify({'task':'success','id':res[0]})



@app.route('/capture',methods=['post'])
def capture():

    try:
        save_location = "static/identify.jpg"
        img = request.files['files']
        B_id = request.form['B_id']
        print("jhfh",B_id)
        # qry= "SELECT `B_id` FROM `blind_reg` WHERE `IMEI_NO`=%s"
        # res=selectone(qry,imei)
        # if res is not None:
        #     B_id=res[0]
        #     print(B_id)

        # print(imei)
        img.save(save_location)

        img = cv2.imread(save_location)
        print(type(img))
        try:
            img = rotate(img, 270)
            cv2.imwrite("ro.jpg", img)
        except Exception as e:
            print(e)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        print("ppppppppppppp", faces)
        print("lngthhhhhhhhhhh", len(faces))

        if len(faces) == 0:
            # results = objdet(save_location)
            results=objdet('ro.jpg')
            re = ', '.join(results) + " are in front of you"

            return jsonify({'task': re})
        else:
            import pymysql
            con = pymysql.connect(host="localhost", user="root", password="", port=3306, db="angel_eye")
            cmd = con.cursor()
            print("ppppppppppppppppppppppppp")
            cmd.execute("SELECT * FROM `familiar_person` where B_id='"+B_id+"'")
            s = cmd.fetchall()
            from src.encode_faces import enf

            enf("ro.jpg")
            for r in s:
                res = rec_face_image("static/familiar person/" + r[3])
                print("R", res)
                if res is not None:
                    print("GETTTTTTTTTTTTTTTTTTTTTTTTTTTTT", res)
                    cmd.execute("select * FROM `familiar_person` WHERE `Image`='" + str(res) + "'")
                    s = cmd.fetchone()
                    print(s)
                    print({'task': " " + s[2] + " is infront of you " + "relation is " + s[4]})
            return jsonify({'task': " " + s[2] + " is infront of you" + "relation is" + s[4]})




    except Exception as e:
        print(e)
        return jsonify({'task': "unknown person recognized"})
        return jsonify({'task': "unknown person recognized"})


@app.route('/getvolphone',methods=['post'])
def getvolphone():
    imei=request.form['IMEI_NO']
    qry="SELECT `care_registration`.`Phone` FROM `care_registration` WHERE `login_id` IN(SELECT `C_id` FROM `blind_reg` WHERE `IMEI_NO`=%s)"
    res=selectone(qry,imei)
    if res is not None:
        return jsonify({'volphone':res[0]})
    else:
        return jsonify({'volphone': "8590494466"})


app.run(host="0.0.0.0",port=5000)
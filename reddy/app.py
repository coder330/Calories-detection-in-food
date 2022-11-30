from flask import Flask, render_template, request, redirect, url_for
import os
import MySQLdb.cursors
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import preprocess_input
# best_model = h5py.file()
# base_model = load_model("C:\\Users\\Welcome\\OneDrive\\Desktop\\Projects\\IBM Project\\model\\model.pkl")
model = load_model("best_model.h5" )
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Sameonu07@"
app.config["MYSQL_DB"] = "food"
mysql = MySQL(app)
name = {0: 'burger',
 1: 'butter_naan',
 2: 'chai',
 3: 'chapati',
 4: 'chole_bhature',
 5: 'dal_makhani',
 6: 'dhokla',
 7: 'fried_rice',
 8: 'idli',
 9: 'jalebi',
 10: 'kaathi_rolls',
 11: 'kadai_paneer',
 12: 'kulfi',
 13: 'masala_dosa',
 14: 'momos',
 15: 'paani_puri',
 16: 'pakode',
 17: 'pav_bhaji',
 18: 'pizza',
 19: 'samosa'}
 

picture = os.path.join('static', 'image')
app.config["UPLOAD"] = picture
app.config["IMAGE"] = "C:\\Users\\Hari\\Desktop\\reddy\\static\\image"
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/home',methods=['POST', "GET"])
def index():
    if request.method=="POST":
        image = request.files['file']
        print(image)
        filename = secure_filename(image.filename)
        basdir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basdir, app.config["IMAGE"], filename))
        print(filename)
        disease_name = prediction("C:\\Users\\Hari\\Desktop\\reddy\\static\\image\\"+filename)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select protein, calories, carbohybrate, beta_carbohydrate, fastfood from nutrients where food_name =%s", [disease_name])
        foodDetails = cursor.fetchone()
        message = find_food_category(foodDetails.get('fastfood'))
#// details = "Product name : "+disease_name+"\n Protein:"+str(foodDetails.get('protein'))+" g\nCalories:"+str(foodDetails.get('calories'))+" g\nCarbohydrates: "+str(foodDetails.get('carbohydrates'))+" g\nFat:"+str(foodDetails.get('beta_carbohydrate'))+"g\n"+message
        product_name = disease_name
        protein = str(foodDetails.get('protein'))
        calories = str(foodDetails.get('calories'))
        carbohydrates = str(foodDetails.get('carbohydrates'))
        fat = str(foodDetails.get('beta_carbohydrate'))
        return render_template("report.html", filename = filename, disease_name = product_name, protein = protein, calories = calories, carbohybrate = carbohydrates, fat = fat, message = message)
    return render_template("predict.html")

@app.route("/diet", methods=['GET', 'POST'])
def diet():
    if request.method=="POST":
        gender = request.form['cropname']
        diet = request.form['diet_plan']
        if gender == 'male':
            if diet == 'normal':
                return render_template("report1.html",filename="OIP.jpg", diet = "Balance diet")
            elif diet == 'normal':
                return render_template("report1.html",filename="OIP.jpg", diet = "Weight loss diet")
            elif diet == 'normal':
                return render_template("report1.html",filename="OIP.jpg", diet = "Muscle gain diet")
            else:
                return render_template("report1.html",filename="OIP.jpg", diet = "Workout diet")
        else:
            if diet == 'normal':
                return render_template("report1.html",filename="OIP.jpg", diet = "Balance diet")
            elif diet == 'normal':
                return render_template("report1.html",filename="OIP.jpg", diet = "Weight loss diet")
            elif diet == 'normal':
                return render_template("report1.html",filename="OIP.jpg", diet = "Muscle gain diet")
            else:
                return render_template("report1.html",filename="OIP.jpg", diet = "Workout diet")
    return render_template("diet.html")
def prediction(path):
    img = load_img(path, target_size=(256,256))
    i = img_to_array(img)
    
    im = preprocess_input(i)
    img = np.expand_dims(im, axis = 0)
#     pred = base_model.predict(img)
    pred = np.argmax(model.predict(img))
    return name[pred]

def find_food_category(food_type):
    if(food_type==0):
        return "It is the healthy food. So it will not affect your diet"
    elif(food_type==1):
        return "It is the fast food. If you want to maintain your health say no to it."
    else:
        return "It also fast food. Eat as less you can."
if(__name__ == '__main__'):
    app.run(port=5000, debug=True)






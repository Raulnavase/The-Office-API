from flask import Flask, request, redirect, url_for, render_template, jsonify
from os import getenv
from dotenv import load_dotenv
from flask_mysqldb import MySQL

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = getenv('MYSQL_DB')
app.secret_key = getenv('SECRET_KEY')

mysql = MySQL(app)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_personaje', methods=['POST'])
def add_personaje():
    nombre = request.form['nombre'].capitalize()
    apellido = request.form['apellido'].capitalize()
    url_imagen = request.form['url_imagen']
    puesto = request.form['puesto'].capitalize()
    departamento = request.form['departamento'].capitalize()
    descripcion = request.form['descripcion'].capitalize()
    primera_aparicion = request.form['primera_aparicion'].capitalize()
    ultima_aparicion = request.form['ultima_aparicion'].capitalize()
    total_episodios = request.form['total_episodios']
    frase_iconica = request.form['frase_iconica'].capitalize()
    hobbie_principal = request.form['hobbie_principal'].capitalize()
    ciudad_origen = request.form['ciudad_origen'].capitalize()

    if nombre and apellido and url_imagen and puesto and departamento and descripcion and primera_aparicion and ultima_aparicion and total_episodios and frase_iconica and hobbie_principal and ciudad_origen:
        cursor = mysql.connection.cursor()
        
        sql = "INSERT INTO personajes (nombre, apellido, url_imagen, puesto, departamento, descripcion, primera_aparicion, ultima_aparicion, total_episodios, frase_iconica, hobbie_principal, ciudad_origen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        cursor.execute(sql, (nombre, apellido, url_imagen, puesto, departamento, descripcion, primera_aparicion, ultima_aparicion, 
        total_episodios, frase_iconica, hobbie_principal, ciudad_origen))
        
        mysql.connection.commit()
        
        cursor.close()

        return redirect(url_for('index'))
    

    return redirect(url_for('index'))



@app.route('/personajes', methods=['GET'])
def get_personajes():
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM personajes;"
    cursor.execute(sql)
    data = cursor.fetchall()
    personajes = []
    for row in data:
        personaje = {
            'id': row[0],
            'nombre': row[1], 
            'apellido': row[2], 
            'url_imagen': row[3], 
            'puesto': row[4], 
            'departamento': row[5], 
            'descripcion': row[6], 
            'primera_aparicion': row[7], 
            'ultima_aparicion': row[8], 
            'total_episodios': row[9], 
            'frase_iconica': row[10], 
            'hobbie_principal': row[11], 
            'ciudad_origen': row[12]
        }
        personajes.append(personaje)
    
    return jsonify(personajes)




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
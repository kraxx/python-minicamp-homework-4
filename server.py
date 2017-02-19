from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/movie', methods = ['POST'])
def newMovie():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    name = request.form['name']
    info = request.form['info']

    try:
        cursor.execute('INSERT INTO movies(name,info) VALUES (?,?)', (name, info))
        connection.commit()
        message = 'Successfully inserted into movies table'
    except:
        connection.rollback()
        message = 'There was an issue inserting the data'
    finally:
        connection.close()
        return message + '<a href="/"><p>Return home</p></a>'

@app.route('/movies')
def getMovies():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movies')
    movieList = cursor.fetchall()
    connection.close()
    return jsonify(movieList)

@app.route('/search', methods = ['GET'])
def search():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        name = (request.args.get('searchName'),)
        cursor.execute('SELECT * FROM movies WHERE name =?', name)
        connection.commit()
        data = cursor.fetchall()
    except:
        connection.rollback()
        data = 'Database search error'
    finally:
        return jsonify(data)
        connection.close()



app.run(debug = True)

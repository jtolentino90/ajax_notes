from flask import Flask, render_template, request, redirect, jsonify
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'notes_db')

@app.route('/')
def index():
	query = "SELECT * FROM notes"
	notes = mysql.query_db(query)
	return render_template('index.html', notes=notes)

@app.route('/create', methods=['POST'])
def create():
	notes = request.form
	query = "INSERT INTO notes(title, description) VALUES('{}', '{}')".format(notes['title'], notes['description'])
	mysql.query_db(query)
	return redirect('/')

@app.route('/update/<id>', methods=['POST'])
def update(id):
	try:
		note = request.form
		update_query = "UPDATE notes SET title = :title, description = :description, updated_at = NOW() WHERE id = :id"
		data = {
			'title': request.form['title'],
			'description': request.form['description'],
			'id': id,
			}
		mysql.query_db(update_query, data)
	except:
		description_query = "UPDATE notes SET descrjiption = :description, updated_at = NOW() WHERE id = :id"
		data = {
			'description': request.form['description'],
			'id': id,
			}
		mysql.query_db(description_query, data)
	select_query = "SELECT * FROM notes"
	notes = mysql.query_db(select_query)
	return redirect('/')

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
	delete_query = "DELETE FROM notes WHERE id = :id"
	data = { 'id': id }
	mysql.query_db(delete_query, data)
	select_query = "SELECT * FROM notes"
	notes = mysql.query_db(select_query)
	return redirect('/')
app.run(debug=True)

from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.client import Client


@app.route("/clients/new")
def create_client():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('add_client.html')

@app.route('/clients/new/process', methods=['POST'])
def process_client():
    if 'user_id' not in session:
        return redirect('/')
    
    if not Client.validate_client(request.form):
        return redirect('/clients/new')

    data = {
        'users_id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'diagnosis': request.form['diagnosis'],
        'goals': request.form['goals'],
        'address': request.form['address'],
        'medications': request.form['medications'],

    }
    Client.save(data)
    return redirect('/dashboard')

@app.route('/clients/<int:id>')
def view_client(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('client_view.html',client=Client.get_by_id({'id': id}))

@app.route('/clients/edit/<int:id>')
def edit_client(id):
    if 'user_id' not in session:
        return redirect('/')

    return render_template('client_edit.html',client=Client.get_by_id({'id': id}))

@app.route('/clients/edit/process/<int:id>', methods=['POST'])
def process_edit_client(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Client.validate_client(request.form):
        return redirect(f'/clients/edit/{id}') 

    data = {
        'id': id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'diagnosis': request.form['diagnosis'],
        'goals': request.form['goals'],
        'address': request.form['address'],
        'medications': request.form['medications'],
    }

    Client.update(data)
    return redirect('/dashboard')

@app.route('/clients/destroy/<int:id>')
def destroy_client(id):
    if 'user_id' not in session:
        return redirect('/')

    Client.destroy({'id':id})
    return redirect('/dashboard')





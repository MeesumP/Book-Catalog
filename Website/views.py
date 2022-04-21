from Website.models import Note, Book
from Website.auth import login
from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, db
import json

views = Blueprint("views", __name__)

@views.route('/', methods=["GET"])
def bookcatalog_page():
    books = Book.query.all()
    def make_objlink(title):
        return title.replace(' ', '-')
    return render_template('book-catalog.html', make_link=make_objlink, user=current_user, books=books)

@views.route('/home', methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note is too short", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added!", category="success")
        

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('add-book', methods=["GET", "POST"])
def addbook_page():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        shelf = request.form.get('shelf')
    
        try:
            new_book = Book(title=title, author=author, genre=genre, shelf=shelf)
            db.session.add(new_book)
            db.session.commit()
            flash("Book Added!", category="success")
        except:
            flash("Attempt Failed", category="error")

    return render_template('add-book.html', user=current_user)

@views.route('/delete-<booktitle>')
def delete_book(booktitle):
    def make_title(linkedTitle):
        return linkedTitle.replace('-', ' ')
    book_title = make_title(booktitle)
    book = Book.query.filter_by(title=book_title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect('/')
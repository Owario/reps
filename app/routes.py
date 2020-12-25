from datetime import datetime
from werkzeug.urls import url_parse
from app.models import User, Writer, Book, Comment, User_Book
from app.forms import LoginForm, RegistrationForm, NewBookForm, NewWriterForm
from app.forms import EditProfileForm, RatingForm, CommentForm, SearchForm
from app.forms import CategoryForm, CategoryUserForm, GenreForm, EditProfileModeratorForm
from config import GENRES
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request
from app import app, db


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    form = GenreForm()

    if form.validate_on_submit():
        page = 1
    else:
        page = request.args.get('page', 1, type=int)
    if form.validate_on_submit() and form.genre.data != 'все':

        books = Book.query.filter_by(genre=form.genre.data).order_by(Book.rating.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    else:
        books = Book.query.order_by(Book.rating.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=books.next_num) \
        if books.has_next else None
    prev_url = url_for('index', page=books.prev_num) \
        if books.has_prev else None
    return render_template('index.html', title='Home', books=books.items, form=form, GENRES=GENRES,
                           next_url=next_url, prev_url=prev_url)


@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        c = int(form.category.data)
        s = form.search.data
        if c == 0:  # автор
            writer = Writer.query.filter_by(name=s).first()
            if writer:
                return redirect(url_for('writer', writer_id=writer.id))
            else:
                return render_template('search.html', title="Поиск", form=form, err=True)
        elif c == 1:  # книга
            book = Book.query.filter_by(title=s).first()
            if book:
                return redirect(url_for('book', book_id=book.id))
            else:
                return render_template('search.html', title="Поиск", form=form, err=True)
        elif c == 2:  # комментарий
            user = User.query.filter_by(login=s).first()
            if user:
                return redirect(url_for('user', user_id=user.id))
            else:
                return render_template('search.html', title="Поиск", form=form, err=True)
    return render_template('search.html', title="Поиск", form=form, err=False)


@app.route('/user/<user_id>', methods=['GET', 'POST'])
@app.route('/user/<user_id>/', methods=['GET', 'POST'])
def user(user_id):
    user = User.query.get(int(user_id))
    if not user:
        return redirect(url_for('index'))

    form = CategoryUserForm()
    if form.validate_on_submit():
        page = 1
    else:
        page = request.args.get('page', 1, type=int)
    if form.validate_on_submit() and int(form.category.data) != 0:
        if int(form.category.data) == 4:
            books = Book.query.join(User_Book, User_Book.book_id == Book.id).join(User, User.id == User_Book.user_id).filter_by(
                id=user.id).order_by(Book.rating.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
        else:
            books = Book.query.join(User_Book, User_Book.book_id == Book.id).filter_by(category=form.category.data).join(User, User.id == User_Book.user_id).filter_by(
                id=user.id).order_by(Book.rating.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('user', user_id=user_id, page=books.next_num) \
            if books.has_next else None
        prev_url = url_for('user', user_id=user_id, page=books.prev_num) \
            if books.has_prev else None
        return render_template('user.html', title=user.login, user=user, books=books.items, GENRES=GENRES, form=form, next_url=next_url, prev_url=prev_url)

    comments = user.comments.order_by(Comment.datetime.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', user_id=user_id, page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('user', user_id=user_id, page=comments.prev_num) \
        if comments.has_prev else None

    return render_template('user.html', user=user, title=user.login, comments=comments.items, form=form, next_url=next_url, prev_url=prev_url)


@app.route('/book/<book_id>')
@app.route('/book/<book_id>/')
def book(book_id):
    book = Book.query.get(int(book_id))
    if not book:
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    comments = book.comments.order_by(Comment.datetime.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('book', book_id=book_id, page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('book',  book_id=book_id, page=comments.prev_num) \
        if comments.has_prev else None
    if current_user.is_anonymous:
        return render_template('book.html', title=book.title, book=book,
                               comments=comments.items, GENRES=GENRES, next_url=next_url, prev_url=prev_url)
    rating_form = RatingForm()
    comment_form = CommentForm()
    category_form = CategoryForm()
    return render_template('book.html', title=book.title, book=book, comments=comments.items,
                           rating_form=rating_form, comment_form=comment_form, category_form=category_form,
                           GENRES=GENRES, next_url=next_url, prev_url=prev_url)


@app.route('/writer/<writer_id>')
@app.route('/writer/<writer_id>/')
def writer(writer_id):
    writer = Writer.query.get(int(writer_id))
    if not writer:
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    books = writer.books.order_by(Book.rating.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('writer', writer_id=writer_id, page=books.next_num) \
        if books.has_next else None
    prev_url = url_for('writer', writer_id=writer_id, page=books.prev_num) \
        if books.has_prev else None
    return render_template('writer.html', title=writer.name, writer=writer, books=books.items, GENRES=GENRES,
                           next_url=next_url, prev_url=prev_url)


@app.route('/add_rating/<user_id>/<book_id>', methods=['GET', 'POST'])
@app.route('/add_rating/<user_id>/<book_id>/', methods=['GET', 'POST'])
@login_required
def add_rating(user_id, book_id):
    rating_form = RatingForm()
    comment_form = CommentForm()
    category_form = CategoryForm()
    book = Book.query.get(book_id)
    if rating_form.validate_on_submit():
        rating = float(rating_form.rating.data)
        ub = User_Book.query.filter_by(
            user_id=user_id, book_id=book_id).first()
        if ub:
            if ub.mark:
                # уже оценивал
                book.rating += (rating - ub.mark)/book.number_of_votes
            else:
                # ещё не оценивал
                if book.rating:

                    book.rating = book.number_of_votes / \
                        (book.number_of_votes+1)*(book.rating +
                                                  rating/book.number_of_votes)
                    book.number_of_votes += 1
                else:
                    book.rating = rating
                    book.number_of_votes = 1
            ub.mark = rating
            db.session.commit()
        else:
            ub = User_Book(user_id=user_id, book_id=book_id, mark=rating)
            if book.rating:
                book.rating = book.number_of_votes/(book.number_of_votes+1) *\
                    (book.rating + rating/book.number_of_votes)
                book.number_of_votes += 1
            else:
                book.rating = rating
                book.number_of_votes = 1
            db.session.add(ub)
            db.session.commit()
        return redirect(url_for('book', book_id=book_id))
    return render_template('book.html', title=book.title,
                           book=book, rating_form=rating_form, comment_form=comment_form, category_form=category_form)


@app.route('/add_comment/<user_id>/<book_id>', methods=['GET', 'POST'])
@app.route('/add_comment/<user_id>/<book_id>/', methods=['GET', 'POST'])
@login_required
def add_comment(user_id, book_id):
    rating_form = RatingForm()
    comment_form = CommentForm()
    category_form = CategoryForm()
    book = Book.query.get(book_id)

    if comment_form.validate_on_submit():
        comment = Comment(user_id=user_id, book_id=book_id,
                          text=comment_form.body.data, datetime=datetime.utcnow())
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('book', book_id=book_id))

    return render_template('book.html', title=book.title, GENRES=GENRES, book=book,
                           rating_form=rating_form, comment_form=comment_form, category_form=category_form)


@app.route('/add_category/<user_id>/<book_id>/', methods=['POST'])
@app.route('/add_category/<user_id>/<book_id>', methods=['POST'])
@login_required
def add_category(user_id, book_id):
    rating_form = RatingForm()
    comment_form = CommentForm()
    category_form = CategoryForm()
    book = Book.query.get(book_id)

    if category_form.validate_on_submit():
        ub = User_Book.query.filter_by(
            user_id=user_id, book_id=book_id).first()
        if ub:
            ub.category = category_form.category.data
        else:
            ub = User_Book(user_id=user_id, book_id=book_id,
                           category=category_form.category.data)
            db.session.add(ub)
        db.session.commit()
        return redirect(url_for('book', book_id=book_id))

    return render_template('book.html', title=book.title, GENRES=GENRES, book=book,
                           rating_form=rating_form, comment_form=comment_form, category_form=category_form)

# -------------------------------------------------------------------------------------------
# authentication
# -------------------------------------------------------------------------------------------


@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.username.data == 'admin':
            user = User(login=form.username.data, is_moderator=True)
        else:
            user = User(login=form.username.data, is_moderator=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@app.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.login = form.login.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', user_id=current_user.id))
    elif request.method == 'GET':
        form.login.data = current_user.login
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

# -------------------------------------------------------------------------------------------
# admin
# -------------------------------------------------------------------------------------------


@app.route('/add_book', methods=['GET', 'POST'])
@app.route('/add_book/', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_moderator:
        return redirect(url_for('index'))
    form = NewBookForm()
    if form.validate_on_submit():
        book = Book(writer_id=Writer.query.filter_by(name=form.author.data).first().id,
                    title=form.title.data, genre=form.genre.data)
        db.session.add(book)
        db.session.commit()
        flash(f'You\'ve added book  {form.title.data} by {form.author.data}')
        return redirect(url_for('add_book'))
    return render_template('add_book.html', title='add book', form=form)


@app.route('/delete_book/<book_id>')
@app.route('/delete_book/<book_id>/')
@login_required
def delete_book(book_id):
    if not current_user.is_moderator:
        return redirect(url_for('index'))
    book = Book.query.get(book_id)
    for ub in book.ub:
        db.session.delete(ub)
    for comment in book.comments:
        db.session.delete(comment)
    db.session.delete(book)
    db.session.commit()
    flash(f'You\'ve deleted book')
    return redirect(url_for('index'))


@app.route('/add_writer', methods=['GET', 'POST'])
@app.route('/add_writer/', methods=['GET', 'POST'])
@login_required
def add_writer():
    if not current_user.is_moderator:
        return redirect(url_for('index'))
    form = NewWriterForm()
    if form.validate_on_submit():
        writer = Writer(name=form.writer_name.data)
        db.session.add(writer)
        db.session.commit()
        flash(f'You\'ve added writer {form.writer_name.data}')
        return redirect(url_for('add_writer'))
    return render_template('add_writer.html', title='add writer', form=form)


@app.route('/delete_writer/<writer_id>', methods=['GET', 'POST'])
@app.route('/delete_writer/<writer_id>/', methods=['GET', 'POST'])
@login_required
def delete_writer(writer_id):
    if not current_user.is_moderator:
        return redirect(url_for('index'))
    writer = Writer.query.get(writer_id)
    for book in Book.query.filter_by(writer_id=writer.id):
        for ub in book.ub:
            db.session.delete(ub)
        for comment in book.comments:
            db.session.delete(comment)
        db.session.delete(book)
    db.session.delete(writer)
    db.session.commit()
    flash(f'You\'ve deleted writer')
    return redirect(url_for('index'))


@app.route('/edit_profile/<user_id>', methods=['GET', 'POST'])
@app.route('/edit_profile/<user_id>/', methods=['GET', 'POST'])
@login_required
def admin_edit_profile(user_id):
    if not current_user.is_moderator:
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    form = EditProfileModeratorForm()

    if form.validate_on_submit():
        if form.to_delete.data:
            ubs = User_Book.query.filter_by(user_id=user_id).all()
            for ub in ubs:
                db.session.delete(ub)
            comments = Comment.query.filter_by(user_id=user_id).all()
            for comment in comments:
                db.session.delete(comment)

            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('index'))
        user.about_me = form.about_me.data
        user.is_moderator = True if form.is_moderator.data == 'True' else False
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', user_id=user_id))
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
        return render_template('edit_profile.html', title='Edit Profile',
                               form=form)
    return redirect(url_for('user', user_id=user_id))
# -------------------------------------------------------------------------------------------

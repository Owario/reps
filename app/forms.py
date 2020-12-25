from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length
from app.models import User, Writer, Book
from config import GENRES


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(login=username.data).first()
        if user is not None:
            raise ValidationError('Этот логин занят!')


class EditProfileForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=300)])
    submit = SubmitField('Изменить')


class EditProfileModeratorForm(FlaskForm):
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=300)])
    is_moderator = RadioField('Это модератор?', choices=[
                              (True, 'ДА'), (False, 'нет')])
    to_delete = BooleanField('Удалить пользователя')
    submit = SubmitField('Изменить')


class NewWriterForm(FlaskForm):
    writer_name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Добавить')

    def validate_writer_name(self, writer_name):
        writer = Writer.query.filter_by(name=writer_name.data).first()
        if writer is not None:
            raise ValidationError('Этот писатель уже добавлен.')
        if len(writer_name.data) > 100:
            raise ValidationError('Имя слишком длинное.')


class NewBookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    submit = SubmitField('Добавить')

    def validate_title(self, title):
        writer = Writer.query.filter_by(name=self.author.data).first()
        if writer:
            book = Book.query.filter_by(
                title=title.data, writer_id=writer.id).first()
            if book is not None:
                raise ValidationError('Эта книга уже добавлена')
        if len(title.data) > 100:
            raise ValidationError('Название слишком длинное')

    def validate_author(self, author):
        writer = Writer.query.filter_by(name=author.data).first()
        if writer is None:
            raise ValidationError(
                'Такой автор не найден')

    def validate_genre(self, genre):
        if genre.data not in GENRES:
            l = list(GENRES.keys())
            raise ValidationError(f'Используйте правильное название жанра.\
        Одно из списка: \n {l}')


class RatingForm(FlaskForm):
    rating = SelectField('Оценить', choices=[(1, "1"), (2, "2"), (3, "3"), (
        4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), (9, "9"), (10, "10")])
    submit = SubmitField('Оценить')


class CommentForm(FlaskForm):
    body = TextAreaField('Оставьте комментарий:', validators=[
                         Length(min=10, max=300)])
    submit = SubmitField('Отправить')


class SearchForm(FlaskForm):
    category = SelectField('Категория поиска', validators=[DataRequired()], choices=[
                           (0, "Автор"), (1, "Книга"), (2, "Пользователь")])
    search = StringField('То, что хотите найти', validators=[
        DataRequired(), Length(max=100)])
    submit = SubmitField('Искать')


class CategoryForm(FlaskForm):
    category = SelectField('Список', validators=[DataRequired()], choices=[
                           (1, "Прочитал(а)"), (2, "Читаю"), (3, "Хочу прочитать"), (0, "Сбросить")])
    submit = SubmitField('Добавить')


class CategoryUserForm(FlaskForm):
    category = SelectField('Список', validators=[DataRequired()], choices=[
        (0, 'Комментарии'), (1, "Прочитал(а)"), (2, "Читает"), (3, "Хочет прочитать"), (4, "Все избранные книги")])
    submit = SubmitField('Искать')


class GenreForm(FlaskForm):
    items = list(GENRES.items())
    items.append(('все', 'все'))
    genre = SelectField('Жанр', validators=[DataRequired()], choices=items)
    submit = SubmitField('Искать')

from flask import g, url_for, redirect, request

from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from app import app, db
from models import Entry, Tag, User

class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (g.user.is_authenticated and g.user.is_admin()):
            return redirect(url_for('login', next=request.path))
        return self.render('admin/index.html')

class AdminAuthentication(object):
    def is_accessible(self):
        return g.user.is_authenticated and g.user.is_admin()

from wtforms.fields import SelectField  # At top of module.

class BaseModelView(AdminAuthentication, ModelView):
    pass

class SlugModelView(BaseModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(SlugModelView, self).on_model_change(form, model, is_created)

class EntryModelView(SlugModelView):
    _status_choices = [(choice, label) for choice, label in [
        (Entry.STATUS_PUBLIC, 'Public'),
        (Entry.STATUS_DRAFT, 'Draft'),
        (Entry.STATUS_DELETED, 'Deleted'),
    ]]

    column_choices = {
        'status': _status_choices,
    }

    column_filters = ['status', User.name, User.email, 'created_timestamp']

    column_list = ['title', 'status', 'author', 'tease', 'tag_list', 'created_timestamp']
    column_searchable_list = ['title', 'body']
    column_select_related_list = ['author']  # Efficient SELECT the author.

    form_args = {
        'status': {'choices': _status_choices, 'coerce': int}
    }
    form_columns = ['title', 'status', 'body', 'author', 'tags']
    form_overrides = {'status': SelectField}
    
    form_ajax_refs = {
        'author': {
            'fields': (User.name, User.email),
        },
    }

class TagModelView(SlugModelView):
    pass

from wtforms.fields import PasswordField

class UserModelView(SlugModelView):
    column_list = ['email', 'name', 'active', 'created_timestamp', 'admin']
    column_searchable_list = ['email', 'name']
    column_filters = ['active', 'created_timestamp', 'admin']

    form_columns = ['email', 'password', 'name', 'active', 'admin']
    form_extra_fields = {
        'password': PasswordField('New password'),
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = User.make_password(form.password.data)
        return super(UserModelView, self).on_model_change(form, model, is_created)

# Modifild file admin class
class BlogFileAdmin(AdminAuthentication, FileAdmin):
    pass

admin = Admin(app, 'Blog Admin', index_view=IndexView())  # Link app to admin extend
admin.add_view(EntryModelView(Entry, db.session))
admin.add_view(TagModelView(Tag, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(BlogFileAdmin(app.config['STATIC_DIR'], '/static', name='Static Files'))
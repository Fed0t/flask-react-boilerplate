from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database import db, User, Order, Company, Token, Webhook, Transaction, Role

from flask_security.utils import encrypt_password

admin_ui = Admin(name='GPSTrack Administrator',
                 template_mode='bootstrap3', url='/api/v1/admin')


class UserAdmin(ModelView):
    can_delete = False
    column_exclude_list = ['password', ]

    def on_model_change(self, form, model, is_created):
        new_password = encrypt_password(form.data['password'])
        model.password = new_password
        return super(UserAdmin, self).on_model_change(form, model, is_created)

    def update_model(self, form, model):
        return super(UserAdmin, self).update_model(form, model)

    def create_model(self, form):
        return super(UserAdmin, self).create_model(form)

    def delete_model(self, model):
        return super(UserAdmin, self).delete_model(model)

    pass


admin_ui.add_view(ModelView(Company, db.session))
admin_ui.add_view(ModelView(Order, db.session))
admin_ui.add_view(ModelView(Transaction, db.session))
admin_ui.add_view(ModelView(Webhook, db.session))

admin_ui.add_view(UserAdmin(User, db.session))
admin_ui.add_view(ModelView(Role, db.session))
admin_ui.add_view(ModelView(Token, db.session))
# admin_ui.add_view(ModelView(TokenBlocklist, db.session))

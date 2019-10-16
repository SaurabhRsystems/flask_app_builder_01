from flask import render_template, flash
#------for all models
from .models import *
#------for all forms
from .forms import *
#------for all apis
from .apis import *

from . import appbuilder, db

from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelRestApi, ModelView, MultipleView, MasterDetailView, \
    AppBuilder, BaseView, expose, has_access, SimpleFormView
from flask_appbuilder.widgets import ListThumbnail
from flask_appbuilder.fieldwidgets import Select2Widget

from flask_babel import lazy_gettext as _

from wtforms.ext.sqlalchemy.fields import QuerySelectField

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""
"""
    Application wide 404 error handler
"""


class MyView(BaseView):

    default_view = 'method1'

    @expose('/method1/')
    @has_access
    def method1(self):
        # do something with param1
        # and return to previous page or index
        return self.render_template('method3.html',
                            param1 = 'Hello')

    @expose('/method2/<string:param1>')
    @has_access
    def method2(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        return self.render_template('method3.html',
                            param1 = param1)
    
    @expose('/method3/<string:param1>')
    @has_access
    def method3(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        self.update_redirect()
        return self.render_template('method3.html',
                            param1 = param1)

class MyFormView(SimpleFormView):
    form = MyForm
    form_title = 'This is my first form view'
    message = 'My form submitted'

    def form_get(self, form):
        form.field1.data = 'This was prefilled'

    def form_post(self, form):
        # post process form
        flash(self.message, 'info')


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    label_columns = {'contact_group':'Contacts Group'}
    list_columns = ['name','personal_cellphone','birthday','contact_group']

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['name', 'address', 'contact_group']}
        ),
        (
            'Personal Info',
            {'fields': ['birthday', 'personal_phone', 'personal_cellphone'], 'expanded': False}
        ),
    ]

class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

class MultipleViewsExp(MultipleView):
    views = [GroupModelView, ContactModelView]

class GroupMasterView(MasterDetailView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

class PersonModelView(ModelView):
    datamodel = SQLAInterface(Person)

    list_widget = ListThumbnail

    label_columns = {'name':'Name','photo':'Photo','photo_img':'Photo', 'photo_img_thumbnail':'Photo'}
    list_columns = ['photo_img_thumbnail', 'name']
    show_columns = ['photo_img','name']


def department_query():
    return db.session.query(Department)
class EmployeeHistoryView(ModelView):
    datamodel = SQLAInterface(EmployeeHistory)
    list_columns = ['department', 'begin_date', 'end_date']

class EmployeeView(ModelView):
    datamodel = SQLAInterface(Employee)
    list_columns = ['full_name', 'department', 'employee_number']
    edit_form_extra_fields = {
        "department": QuerySelectField(
            "Department",
            query_factory=department_query,
            widget=Select2Widget(extra_classes="readonly"),
        )
    }

    related_views = [EmployeeHistoryView]
    show_template = 'appbuilder/general/model/show_cascade.html'

class FunctionView(ModelView):
    datamodel = SQLAInterface(Function)
    related_views = [EmployeeView]

class DepartmentView(ModelView):
    datamodel = SQLAInterface(Department)
    related_views = [EmployeeView]

class BenefitView(ModelView):
    datamodel = SQLAInterface(Benefit)
    related_views = [EmployeeView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']



@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )

db.create_all()

appbuilder.add_view(MyView, "Method1", category='My View')
appbuilder.add_link("Method2", href='/myview/method2/john', category='My View')
appbuilder.add_link("Method3", href='/myview/method3/john', category='My View')
appbuilder.add_view(MyFormView, "My form View", icon="fa-group", label=_('My form View'), category="My Forms", category_icon="fa-cogs")

appbuilder.add_view(GroupModelView, "List Groups", icon = "fa-folder-open-o", category = "Contacts", category_icon = "fa-envelope")
appbuilder.add_view(ContactModelView, "List Contacts", icon = "fa-envelope", category = "Contacts")
appbuilder.add_view(MultipleViewsExp, "Multiple Views", icon = "fa-envelope", category = "Contacts")
appbuilder.add_view(GroupMasterView, "Master  Views", icon = "fa-envelope", category = "Contacts")
appbuilder.add_view(PersonModelView, "Person Manager", icon="fa-group", label=_('PerMan - alt_name'),category="Person", category_icon="fa-cogs")

appbuilder.add_view(EmployeeView, "Employees", icon="fa-folder-open-o", category="Company")
appbuilder.add_separator("Company")
appbuilder.add_view(DepartmentView, "Departments", icon="fa-folder-open-o", category="Company")
appbuilder.add_view(FunctionView, "Functions", icon="fa-folder-open-o", category="Company")
appbuilder.add_view(BenefitView, "Benefits", icon="fa-folder-open-o", category="Company")
appbuilder.add_view_no_menu(EmployeeHistoryView, "EmployeeHistoryView")

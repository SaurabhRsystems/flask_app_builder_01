from flask import render_template, flash, g
#------for all models
from .models import *
#------for all forms
from .forms import *
#------for all apis
from .apis import *

from . import appbuilder, db

from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.actions import action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith
# If you're using Mongo Engine you should import filters like this, everything else is exactly the same
# from flask_appbuilder.models.mongoengine.filters import FilterStartsWith, FilterEqualFunction
from flask_appbuilder import ModelRestApi, ModelView, MultipleView, MasterDetailView, AppBuilder, BaseView, expose, has_access, SimpleFormView
from flask_appbuilder.widgets import ListThumbnail
from flask_appbuilder.fieldwidgets import Select2Widget, Select2AJAXWidget, BS3TextFieldWidget #not needed as not working01

from flask_babel import lazy_gettext as _
from flask_babel import gettext #not needed as not working01
from wtforms import TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import EqualTo



class BS3TextFieldROWidget(BS3TextFieldWidget):
    def __call__(self, field, **kwargs):
        kwargs['readonly'] = 'true'
        return super(BS3TextFieldROWidget, self).__call__(field, **kwargs)


# temporary
class ExampleView(ModelView):
    datamodel = SQLAInterface(ExampleModel)
    edit_form_extra_fields = {
        'field2': TextField('field2', widget=BS3TextFieldROWidget())
    }
 



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

class MyView2(ModelView):
    datamodel = SQLAInterface(MyModel)
    list_columns = ['name', 'my_custom']
    validators_columns = {
        'my_field1':[EqualTo('my_field2', message=gettext('fields must match'))]
    }

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
    # You can define individual filters for add,edit and search using \
    # add_form_quey_rel_fields, edit_form_query_rel_fields, search_form_query_rel_fields respectively\
    # it will show only fields with keyword
    add_form_query_rel_fields = {
        'contact_group': [['name', FilterStartsWith, 'c']],
        'gender': [['name', FilterStartsWith, 'M']]
        }
    add_form_extra_fields = {
        'contact_group1': AJAXSelectField(
                            'contact_group',
                            description='This will be populated with AJAX',
                            datamodel=datamodel,
                            col_name='contact_group',
                            widget=Select2AJAXWidget(endpoint='/contactmodelview/api/column/add/contact_group')
                         ),
    }

class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]
    #Base available permission are: can_add, can_edit, can_delete, can_list, can_show
    base_permissions = ['can_add','can_delete','can_list']

    @action("myaction","Do something on this record","Do you really want to?","fa-rocket")
    def myaction(self, item):
        """
            do something with the item record
        """
        return redirect(self.get_redirect())

    @action("myaction2","Do something on this record","Do you really want to?","fa-rocket")
    def myaction2(self, item):
        """
            do something with the item record
        """
        return redirect(self.get_redirect())

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket", single=False)
    def muldelete(self, items):
        '''single=False makes it only available in list view and not in show view'''
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())

    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket")
    def muldelete(self, items):
        '''removing single=False makes it available in list view and show view it should be able to manage single and multiple items'''
        if isinstance(items, list):
            self.datamodel.delete_all(items)
            self.update_redirect()
        else:
            self.datamodel.delete(items)
        return redirect(self.get_redirect())

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
    ## not working01
    # add_form_extra_fields = {
    #     'extra': TextField(gettext('Extra Field'),
    #     description=gettext('Extra Field description'),
    #     widget=BS3TextFieldWidget())
    # }

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



def get_user():
    return g.user
class MyModelView(ModelView):
    datamodel = SQLAInterface(MyModel)
    list_columns = ['name', 'my_custom']
    base_filters = [#['created_by', FilterEqualFunction, get_user],
                    ['name', FilterStartsWith, 'a']]
    base_order = ('name','desc')
    '''# You can pass extra Jinja2 arguments to your custom template, using extra_args property:
    extra_args = {'my_extra_arg':'SOMEVALUE'}
    show_template = 'my_show_template.html' '''
    '''# add custom form using wtform
    add_form = AddFormWTF'''
    
    add_columns = ['my_field1', 'my_field2']
    edit_columns = ['my_field1']




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
appbuilder.add_view(MyView2, "MyView2", category='My View 2')
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


appbuilder.add_view(MyModelView, "MyModelView", icon="fa-folder-open-o", category="Company")






# temporary 
appbuilder.add_view(ExampleView, "ExampleView", icon="fa-folder-open-o", category="Temporary")


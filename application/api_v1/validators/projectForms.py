from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired

from application.base.baseForm import BaseForm as Form

class ProjectForm(Form):
    project_id = IntegerField(validators=[DataRequired()])


class AddProjectForm(Form):
    project_name = StringField(validators=[DataRequired()])
    note = StringField()


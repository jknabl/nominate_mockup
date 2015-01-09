import wtforms
from flask.ext.wtf import Form
import start
import json

class NominateForm(Form):
  employee_id = wtforms.HiddenField("employee_id")
  your_name = wtforms.TextField('submitter_name')
  awesomeness = wtforms.TextAreaField('why_nominee_is_awesome')

# class InstitutionForm(wtforms.Form):
#   identifier = wtforms.StringField('Search by institution:')
#   institutions = json.loads(start.institutions)
#   label = wtforms.SelectField('Institution:', choices=institutions)
#   submit = wtforms.SubmitField('Search by Institution')

# class RegionForm(wtforms.Form):
#     identifier = wtforms.StringField('Search by region:')
#     regions = json.loads(start.regions)
#     label = wtforms.SelectField("Region:", choices=regions)
#     submit = wtforms.SubmitField('Search by Region')
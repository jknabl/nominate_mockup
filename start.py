import config
from flask import Flask, render_template, redirect, flash
from requests import get 
import json
import sqlite3
from flask import g
import forms

STAFF_EXPORT = config.URLS['staff_export']
DATABASE = '/Users/jknabl/Documents/code-projects/ccnomination/db.db'

app = Flask(__name__)

@app.route('/staff')
def staff():
  r = get(STAFF_EXPORT)
  init_db()
  returned = json.loads(r.text)
  return "hi"

@app.route('/regions')
def regions():
  r = query_db("SELECT region_name FROM staff_members")
  regions = []
  for reg in r:
    regions.append(reg['region_name'])
    print regions
  return json.dumps(list(set(regions)))

@app.route('/institutions')
def institutions():
  count = 0 
  r = query_db("SELECT institution_name FROM staff_members")
  #print r 
  institutions = []
  for inst in r:
    val = inst['institution_name']
    institutions.append(val)
    print institutions
  return json.dumps(list(set(institutions)))
  
def init_db():
  r = get(STAFF_EXPORT)
  returned = json.loads(r.text)
  #print returned
  for person in returned:
    #print person
    first_name = returned[person]['first_name']
    last_name = returned[person]['last_name']
    institution_name = returned[person]['institution_name']
    region_name = returned[person]['region_name']

    exists = query_db('select * from staff_members WHERE first_name=? AND \
    last_name=? AND institution_name=? AND region_name=?', 
    [first_name, last_name, institution_name, region_name])
    if exists is None:
      q = query_db('INSERT INTO staff_members VALUES (NULL, ?, ?, ?, ?)', 
        [first_name, last_name, institution_name, region_name])
      commit_db()
  # for staff in query_db('select * from staff_members'):
  #   print staff['first_name']
  return "hi"

@app.route('/')
def start():
  staff()
  return render_template('index.html')

@app.route('/full-list')
def full_employee_list_form():
  e = query_db('select * from staff_members')
  # for thing in e:
  #   print "thing is %s" % thing
  return render_template('all_employees_form.html', employees=e)

@app.route('/search-by-institution')
def search_by_institution_form():
  return render_template('institution_form.html')

@app.route('/search-by-region')
def search_by_region_form():
  return render_template('region_form.html')

@app.route('/nominate_form/<employee_id>', methods=['GET', 'POST'])
def nominate_form(employee_id):
  #send the employee info to the form to be populated.
  #then the form will pass it along to the function that actually 
  #persists the nomination in the DB.
  form = forms.NominateForm(csrf_enabled=False)
  e = query_db('select * from staff_members where id=?', [employee_id])[0]
  print e
  if form.validate_on_submit():
    flash('Nominated %s %s' % (e['first_name'], e['last_name']))
    # print form.your_name.data
    # print form.awesomeness.data
    q = query_db('INSERT INTO nominations VALUES (NULL, ?, ?, ?)', [e['id'], \
      form.your_name.data, form.awesomeness.data])
    commit_db()
    return redirect('/full-list')
  return render_template('nomination_form.html', employee=e, form=form)

@app.route('/nominate/<employee_id>', methods=['GET', 'POST'])
def nominate(employee_id):
  #persist in the DB, show confirmation.
  return ""



def commit_db():
  g.db.commit()

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
  g.db = connect_db()

@app.after_request
def after_request(response):
  g.db.close()
  return response

def query_db(query, args=(), one=False):
  cur = g.db.execute(query, args)
  rv = [dict((cur.description[idx][0], value)
    for idx, value in enumerate(row)) for row in cur.fetchall()]
  return (rv[0] if rv else None) if one else rv

if __name__ == '__main__':
  app.debug = True
  app.secret_key = "A secret"
  app.run()
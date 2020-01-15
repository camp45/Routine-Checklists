from flask import render_template

from cl_app import app

@app.route('/')
@app.route('/index')
def index():
    context = { 'check_lists': [
                    {'author': {'username': 'Brad'},
                    'title': 'Monday Chores',
                    'items': ['Take out trash', 'Test the app']
                    },
                    {
                    'author': {'username': 'Frank'},
                    'title': 'Pre Takeoff Checklist',
                    'items': ['Doors','Brakes', 'Flight Controls',
                              'Flight Instruments']
                    }
                ]
            }
    return render_template('index.html', context=context)


@app.route('/new')
def create_new_list():
    context = {'content':'This is the page to make a new checklist'}
    return render_template('new_list.html', context=context)

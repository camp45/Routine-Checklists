from cl_app import app, db
from cl_app.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

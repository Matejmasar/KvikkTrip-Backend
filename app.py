from sqlalchemy import text
from database import db
from app import app

db.init_app(app) 

with app.app_context():
    db.session.execute(text('CREATE EXTENSION IF NOT EXISTS postgis;'))
    db.session.commit()

with app.app_context():
    db.create_all()

''' Default route '''
@app.route('/')
def index():
    return "Kvikk Trip Backend"
            
if __name__ == '__main__':
    app.run(debug=True)
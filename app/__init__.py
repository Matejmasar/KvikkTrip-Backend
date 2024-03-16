from flask import Flask

app = Flask(__name__)
app.debug = True
from app.routes import location_routes, user_routes, event_routes, tag_routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:kvikktrip_password@dpg-cnevjqi1hbls738raqa0-a.frankfurt-postgres.render.com/kvikktrip'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

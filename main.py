from app import app, db
import admin  # This line is new, place after the app import 
import api
import models
import views

from entries.blueprint import entries  # add entries with blueprint
app.register_blueprint(entries, url_prefix='/entries')

if __name__ == '__main__':
    app.run()
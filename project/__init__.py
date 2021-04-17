from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from project.src.database.models import *

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_pyfile('./src/database/config_dev.cfg')
db.init_app(app)


if __name__ == '__main__':
    # app.run(port=5000)
    pass

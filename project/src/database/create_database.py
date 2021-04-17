from project import db, app
from models import FlatsBuy, FlatsRent, PricesBuy, PricesRent


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        pass
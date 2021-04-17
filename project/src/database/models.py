from sqlalchemy.ext.declarative import declarative_base
from project import db

Base = declarative_base()


class FlatsBuy(db.Model):
    __tablename__ = 'flats_buy'

    ad_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.String, nullable=False)
    date_scraped = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    seller = db.Column(db.String)
    property_type = db.Column(db.String)
    num_rooms = db.Column(db.Integer)
    num_bathrooms = db.Column(db.Integer)
    flat_area = db.Column(db.Integer, nullable=False)
    parking = db.Column(db.String)
    description = db.Column(db.String)
    page_address = db.Column(db.String)


class PricesBuy(db.Model):
    __tablename__ = 'prices_buy'

    price_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flat_id = db.Column(db.Integer, db.ForeignKey("flats_buy.ad_id"),
                        nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)
    price_flat = db.relationship('FlatsBuy')


class FlatsRent(db.Model):
    __tablename__ = 'flats_rent'

    ad_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.String, nullable=False)
    date_scraped = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    seller = db.Column(db.String)
    property_type = db.Column(db.String)
    num_rooms = db.Column(db.Integer)
    num_bathrooms = db.Column(db.Integer)
    flat_area = db.Column(db.Integer, nullable=False)
    parking = db.Column(db.String)
    description = db.Column(db.String)
    page_address = db.Column(db.String)
    smoking = db.Column(db.String)
    animals = db.Column(db.String)


class PricesRent(db.Model):
    __tablename__ = 'prices_rent'

    price_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flat_id = db.Column(db.Integer, db.ForeignKey("flats_rent.ad_id"),
                        nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)
    price_flat = db.relationship('FlatsRent')

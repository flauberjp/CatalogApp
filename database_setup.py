import os
import sys
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, schema,  or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database
from flask import url_for
from sqlalchemy.orm import sessionmaker

db_string = 'postgres://postgres:postgres@localhost:5432/ItemCatalogDb'

db = create_engine(db_string)
if not database_exists(db.url):
    create_database(db.url)

base = declarative_base()

class User(base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

class Category(base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'items': self.serialize_itemsFromThisCaregory
        }

    @property
    def serialize_itemsFromThisCaregory(self):
        items = session.query(Item).filter(Item.category_id == self.id)

        return [
            item.serialize for item in items
        ]


class Item(base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'category_id': self.category_id,
            'owner': self.serialize_owner_if_any
        }
    
    @property
    def serialize_owner_if_any(self):
        if (self.user is not None):
            return {
                'id': self.user.id,
                'name': self.user.name
            }
        else:
            return None

base.metadata.create_all(db)

Session = sessionmaker(db)
session = Session()

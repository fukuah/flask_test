from peewee import *


db = MySQLDatabase('webapp_test', user='root', password='RyugaWaga', host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField()
    password_hash = CharField()
    email = CharField()
    permissions = IntegerField()
    created_at = TimestampField()
    updated_at = TimestampField()


class UserBox(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    color = CharField()
    creator_id = IntegerField()
    created_at = TimestampField()
    updated_at = TimestampField()


class Item(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    count = IntegerField()
    box_id = IntegerField()
import sqlite3

class Contact:
    all = {}
    def __init__(self, name, phone, email=None, id= None):
        self.name = name
        self.phone = phone
        self.email = email

    def __repr__(self):
        return f"Contact(name={self.name}, phone={self.phone}, email={self.email})"
    
    @classmethod
    def create_table(cls):
        pass
    
    @classmethod
    def drop_table():
        pass
    
    def save(self):
        pass
    
    @classmethod
    def create(cls, name, phone, email=None):
        pass
    
    @classmethod
    def instance_from_db(cls):
        pass
    
    @classmethod
    def get_all(cls):
        pass
    
    
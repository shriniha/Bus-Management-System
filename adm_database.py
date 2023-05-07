import os

from deta import Deta


Deta_key="d0jxfrvb_hXSXb9XfUZLn5r2fgqKArwuUVb8368B4"

#initialize with project key

Deta=Deta(Deta_key)

#connect a database
db=Deta.Base("users_db")

def insert_user(username_adm,name_adm,password_adm):
    return db.put({"key":username_adm,"name":name_adm,"password":password_adm})



def fetch_all_users():
    res=db.fetch()
    return res.items

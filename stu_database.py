import os

from deta import Deta


Deta_key="d0jxfrvb_Fp7msm2uY7WLeh5Cq4ZvBme2s2r552zo"

#initialize with project key

Deta=Deta(Deta_key)

#connect a database
db=Deta.Base("stu_db")

def insert_user(username_adm,name_adm,password_adm):
    return db.put({"key":username_adm,"name":name_adm,"password":password_adm})



def fetch_all_users():
    res=db.fetch()
    return res.items

def insert_user(username,name,password):
    db.insert({
    "key": username,
    "name": name,
    "password": password
})

import psycopg2
import hashlib
import streamlit as st

host=st.secrets.db_credentials.host
user=st.secrets.db_credentials.user
password=st.secrets.db_credentials.password
db=st.secrets.db_credentials.database
port = st.secrets.db_credentials.database

def init_connection():
    return psycopg2.connect(database=db, user=user, password=password, host=host, port= port)

conn = init_connection()

cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS public."UserDetails"(id SERIAL PRIMARY KEY,username TEXT,email TEXT,password TEXT)')

def fetch_email(email):
    cur.execute('SELECT email FROM public."UserDetails" WHERE public."UserDetails".email=%s',(email,))
    data = cur.fetchone()
    return data

def add_user(username,email,password):
    cur.execute('INSERT INTO public."UserDetails" (username,email,password) VALUES(%s,%s,%s)',(username,email,password))
    conn.commit()

def email_login_check(email,password):
    try:
        cur.execute('SELECT * FROM public."UserDetails" WHERE public."UserDetails".email =%s AND public."UserDetails".password = %s',(email,password))
        data = cur.fetchone()
        return data
    except psycopg2.ProgrammingError as exc:
        print(exc.message)
        conn.rollback()
    # except psycopg2.InterfaceError as exc:
    #     print(exc.message)
    #     conn = psycopg2.connect(database="userdetails_1", user='pavan', password='Pavan1997', host='user-details.cl0dh5s6crch.us-east-1.rds.amazonaws.com', port= '5432')
    #     cursor = conn.cursor()


def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

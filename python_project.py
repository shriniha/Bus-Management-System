import streamlit as st

st.set_page_config(layout="wide")

import streamlit_authenticator as stauth
import matplotlib.pyplot as plt
import stu_database as db_stu
import adm_database as db
from PIL import Image
import piechart_stu_details
import os
from deta import Deta
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid,JsCode,GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import base64
import csv
import sqlite3
import uuid
import time





# Create or connect to SQLite3 databases
conn_students = sqlite3.connect('student_bus_detail.db')
c_students = conn_students.cursor()
conn_users = sqlite3.connect('user_details.db')
c_users = conn_users.cursor()




# Create student_bus_details table if it doesn't exist
c_students.execute('''CREATE TABLE IF NOT EXISTS student_bus_detail
                          (name text, roll_no text, dept text, bus_no text, gender text, year text, bus_route text, address text, stop text)''')
conn_students.commit()




# Create user_details table if it doesn't exist
c_users.execute('''CREATE TABLE IF NOT EXISTS user_details
                       (username text, password text, name text)''')
conn_users.commit()




# Define function to insert student bus details into database
def insert_student_bus_details(name, roll_no, dept, bus_no, gender, year, bus_route, address, stop):
    c_students.execute("INSERT INTO student_bus_detail VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, roll_no, dept, bus_no, gender, year, bus_route, address, stop))
    conn_students.commit()





# Define function to retrieve student bus details from database
def get_student_bus_detail(name):
    c_students.execute("SELECT * FROM student_bus_detail WHERE name=?", (name,))
    return c_students.fetchone()





# Define function to insert user login details into database
def insert_user_details(username, password, name):
    c_users.execute("INSERT INTO user_details VALUES (?, ?, ?)", (username, password, name))
    conn_users.commit()





# Define function to retrieve user login details from database
def get_user_details(username):
    c_users.execute("SELECT * FROM user_details WHERE username=?", (username,))
    return c_users.fetchone()





# Define a function to retrieve all students from the database
def get_students_details():
        c_students.execute("SELECT * FROM student_bus_detail")
        rows = c_students.fetchall()
        return rows





# Define a dictionary with default fees for each bus route
DEFAULT_FEES = {'1': 25000, '2': 24000, '3': 24500, '4': 23500, '5': 26000, '6': 25500}



# Define a function to create the database table
def create_table():
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 bus_route TEXT,
                 department TEXT,
                 year TEXT,
                 fee_paid INTEGER)''')
        conn.commit()
        conn.close()





        
# Define a function to add a student to the database
def add_student(name, route, dept, year, fee):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, bus_route, department, year, fee_paid) VALUES (?, ?, ?, ?, ?)",
                  (name, route, dept, year, fee))
        conn.commit()
        conn.close()





# Define a function to retrieve all students from the database
def get_students():
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        rows = c.fetchall()
        conn.close()
        return rows





# Define a function to update a student in the database
def update_student(id, name, route, dept, year, fee):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("UPDATE students SET name=?, bus_route=?, department=?, year=?, fee_paid=? WHERE id=?",
                  (name, route, dept, year, fee, id))
        conn.commit()
        conn.close()






def main_page():
        st.markdown('<h3 style="text-align:center;">Total Student Data Base</h3>', unsafe_allow_html=True)
        st.markdown('__________________________________________________________________________________________')

        Deta_key_st="d0jxfrvb_xccodCHMbedEGgEbPjPqVHbGumk4waaF"

        #initialize with project key

        Deta_st=Deta(Deta_key_st)

        #connect a database

        stdb=Deta_st.Base("st_db")

        def insert_user(total,first_yr,sec_yr,third_yr,fourth_yr):
                return stdb.put({"key":total,"first yr":first_yr,"second yr":sec_yr,"third yr":third_yr,"fourth yr":fourth_yr})

        insert_user("0","0","0","0","0")

        def fetch_all_st():
                stu=stdb.fetch()
                return stu.items

        st_num=fetch_all_st()
        st_dict=st_num[1]
        first_yr=st_dict["first yr"]
        sec_yr=st_dict["second yr"]
        third_yr=st_dict["third yr"]
        fourth_yr=st_dict["fourth yr"]




        # Pie chart, where the slices will be ordered and plotted counter-clockwise:

        labels = 'First yr', 'Second yr', 'Third yr', 'Fourth yr'
        sizes = [first_yr,sec_yr,third_yr,fourth_yr]
        explode = (0, 0, 0, 0)  # only "explode"
        print(sizes)

        fig1, ax1 = plt.subplots(figsize=(2,2))
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)





        
def route1():
        if "selected_rows" not in st.session_state:
                st.session_state.selected_rows = []

        @st.cache_data()
        def data_upload():
                df=pd.read_csv("Route1.csv")
                return df

        df=data_upload()

        gd=GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(editables=True,groupable=True)
        sel_mode=st.radio('Selection Type',options=['single','multiple'])
        gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
        gridoptions=gd.build()

        with st.form(key='add_form'):
                col1, col2, col3, col4, col5, col6,col7 = st.columns(7)

                with col1:
                        sno = st.text_input('S.No')

                with col2:
                        name = st.text_input('Name')

                with col3:
                        dept=st.text_input('Dept')

                with col4:
                        gender = st.selectbox('Gender', ['Male', 'Female'])

                with col5:
                        year = st.text_input('Year')

                with col6:
                        route = st.text_input('Route 1 (Stop)')

                with col7:
                        save_button = st.form_submit_button('Save')

                if save_button:
                        with open('Route1.csv', mode='a', newline='') as route1_file:
                                route1_writer = csv.writer(route1_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                route1_writer.writerow([sno,name, dept, gender,year,route])

                        st.success('Saved Successfully!')

        ag_grid = AgGrid(
                df,
                gridOptions=gridoptions,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                height=500,
                allow_unsafe_jscode=True,
                theme='alpine',
                selected_rows=st.session_state.selected_rows
                )







def route2():

        if "selected_rows" not in st.session_state:
                st.session_state.selected_rows = []

        @st.cache_data()
        def data_upload():
                df=pd.read_csv("Route2.csv")
                return df

        df=data_upload()

        gd=GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(editables=True,groupable=True)
        sel_mode=st.radio('Selection Type',options=['single','multiple'])
        gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
        gridoptions=gd.build()

        with st.form(key='add_form'):
                col1, col2, col3, col4, col5, col6,col7 = st.columns(7)

                with col1:
                        sno = st.text_input('S.No')

                with col2:
                        name = st.text_input('Name')

                with col3:
                        dept=st.text_input('Dept')

                with col4:
                        gender = st.selectbox('Gender', ['Male', 'Female'])

                with col5:
                        year = st.text_input('Year')

                with col6:
                        route = st.text_input('Route 2 (Stop)')

                with col7:
                        save_button = st.form_submit_button('Save')

                if save_button:
                        with open('Route2.csv', mode='a', newline='') as route1_file:
                                route1_writer = csv.writer(route1_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                route1_writer.writerow([sno,name, dept, gender,year,route])

                        st.success('Saved Successfully!')

        ag_grid = AgGrid(
                df,
                gridOptions=gridoptions,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                height=500,
                allow_unsafe_jscode=True,
                theme='alpine',
                selected_rows=st.session_state.selected_rows
                )







def route3():

        if "selected_rows" not in st.session_state:
                st.session_state.selected_rows = []

        @st.cache_data()
        def data_upload():
                df=pd.read_csv("Route3.csv")
                return df

        df=data_upload()

        gd=GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(editables=True,groupable=True)
        sel_mode=st.radio('Selection Type',options=['single','multiple'])
        gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
        gridoptions=gd.build()

        with st.form(key='add_form'):
                col1, col2, col3, col4, col5, col6,col7 = st.columns(7)

                with col1:
                        sno = st.text_input('S.No')

                with col2:
                        name = st.text_input('Name')

                with col3:
                        dept=st.text_input('Dept')

                with col4:
                        gender = st.selectbox('Gender', ['Male', 'Female'])

                with col5:
                        year = st.text_input('Year')

                with col6:
                        route = st.text_input('Route 3 (Stop)')

                with col7:
                        save_button = st.form_submit_button('Save')

                if save_button:
                        with open('Route3.csv', mode='a', newline='') as route1_file:
                                route1_writer = csv.writer(route1_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                route1_writer.writerow([sno,name, dept, gender,year,route])

                        st.success('Saved Successfully!')

        ag_grid = AgGrid(
                df,
                gridOptions=gridoptions,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                height=500,
                allow_unsafe_jscode=True,
                theme='alpine',
                selected_rows=st.session_state.selected_rows
                )







def route4():

        if "selected_rows" not in st.session_state:
                st.session_state.selected_rows = []

        @st.cache_data()
        def data_upload():
                df=pd.read_csv("Route4.csv")
                return df

        df=data_upload()

        gd=GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(editables=True,groupable=True)
        sel_mode=st.radio('Selection Type',options=['single','multiple'])
        gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
        gridoptions=gd.build()

        with st.form(key='add_form'):
                col1, col2, col3, col4, col5, col6,col7 = st.columns(7)

                with col1:
                        sno = st.text_input('S.No')

                with col2:
                        name = st.text_input('Name')

                with col3:
                        dept=st.text_input('Dept')

                with col4:
                        gender = st.selectbox('Gender', ['Male', 'Female'])

                with col5:
                        year = st.text_input('Year')

                with col6:
                        route = st.text_input('Route 4 (Stop)')

                with col7:
                        save_button = st.form_submit_button('Save')

                if save_button:
                        with open('Route4.csv', mode='a', newline='') as route1_file:
                                route1_writer = csv.writer(route1_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                route1_writer.writerow([sno,name, dept, gender,year,route])

                        st.success('Saved Successfully!')

        ag_grid = AgGrid(
                df,
                gridOptions=gridoptions,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                height=500,
                allow_unsafe_jscode=True,
                theme='alpine',
                selected_rows=st.session_state.selected_rows
                )







def route5():

        if "selected_rows" not in st.session_state:
                st.session_state.selected_rows = []

        @st.cache_data()
        def data_upload():
                df=pd.read_csv("Route5.csv")
                return df

        df=data_upload()

        gd=GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(editables=True,groupable=True)
        sel_mode=st.radio('Selection Type',options=['single','multiple'])
        gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
        gridoptions=gd.build()

        with st.form(key='add_form'):
                col1, col2, col3, col4, col5, col6,col7 = st.columns(7)

                with col1:
                        sno = st.text_input('S.No')

                with col2:
                        name = st.text_input('Name')

                with col3:
                        dept=st.text_input('Dept')

                with col4:
                        gender = st.selectbox('Gender', ['Male', 'Female'])

                with col5:
                        year = st.text_input('Year')

                with col6:
                        route = st.text_input('Route 5 (Stop)')

                with col7:
                        save_button = st.form_submit_button('Save')

                if save_button:
                        with open('Route5.csv', mode='a', newline='') as route1_file:
                                route1_writer = csv.writer(route1_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                route1_writer.writerow([sno,name, dept, gender,year,route])

                        st.success('Saved Successfully!')

        ag_grid = AgGrid(
                df,
                gridOptions=gridoptions,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                height=500,
                allow_unsafe_jscode=True,
                theme='alpine',
                selected_rows=st.session_state.selected_rows
                )







def add_stu():
        name = st.text_input("Name")
        roll_no = st.text_input("Roll No.")
        dept=st.text_input('Dept')
        bus_no = st.text_input("Bus No.")
        gender = st.selectbox('Gender', ['Male', 'Female'])
        year=st.text_input("Year")
        bus_route = st.selectbox('Bus Route', ['1', '2','3','4','5','6'])
        address = st.text_input("Address")
        stop = st.text_input("Stop")


        if st.button('ADD'):

                # Insert student bus details into database
                insert_student_bus_details(name, roll_no, dept, bus_no, gender, year, bus_route, address, stop)

                if bus_route==1:
                        with open('Route1.csv', mode='a', newline='') as route1_file:
                                route1_writer = csv.writer(route1_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                route1_writer.writerow([sno,name, dept, gender,year,bus_route])

                if bus_route==2:
                        with open('Route2.csv', mode='a', newline='') as route1_file:
                                route1_writer = csv.writer(route1_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                route1_writer.writerow([sno,name, dept, gender,year,bus_route])

                if bus_route==3:
                        with open('Route3.csv', mode='a', newline='') as route1_file:
                                route1_writer = csv.writer(route1_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                route1_writer.writerow([sno,name, dept, gender,year,bus_route])

                if bus_route==4:
                        with open('Route4.csv', mode='a', newline='') as route1_file:
                                route1_writer = csv.writer(route1_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                route1_writer.writerow([sno,name, dept, gender,year,bus_route])

                if bus_route==5:
                        with open('Route5.csv', mode='a', newline='') as route1_file:
                                route1_writer = csv.writer(route1_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                route1_writer.writerow([sno,name, dept, gender,year,bus_route])




                insert_user_details(roll_no,roll_no,name)

                db.insert_user(roll_no,name,roll_no)


                st.success("Student Added sucessfully")






# Define a function to search for student data in the database
def search_student_data(search_term):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        # Use a SQL query to search for the student data
        c.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search_term + '%',))
        results = c.fetchall()
        return results






def fee_details():

        st.subheader('Bus Fee Manager')

        # Create the database table if it doesn't exist
        create_table()

        # Retrieve all students from the database
        student_rows = get_students()

        # Convert the rows to a DataFrame for display
        student_data = pd.DataFrame(student_rows, columns=['ID', 'Name', 'Bus Route', 'Department', 'Year', 'Fee Paid'])

        # Calculate the remaining fee for each student
        student_data['Remaining Fee'] = student_data.apply(lambda row: DEFAULT_FEES.get(row['Bus Route'], 0) - row['Fee Paid'], axis=1)

        st.table(student_data)
    
        # Calculate the total amount of fees
        total_fees = student_data['Fee Paid'].sum()

        # Show the total amount of fees collected
        st.markdown(f'Total Fees Collected: Rupees {total_fees}')

        # Calculate the total remaining fees
        total_remaining_fees = student_data['Remaining Fee'].sum()

        # Show the total amount of fees collected
        st.markdown(f'Total Remaining Fees : Rupees {total_remaining_fees}')



        st.subheader('Search for Student Data')

        # Create a search bar for the user to enter a search term
        search_term = st.text_input('Enter student name')


        # Display the search results
        if search_term:
                st.write('Search Results')

                # Call the search_student_data() function to retrieve the results
                results = search_student_data(search_term)

                title=['ID','Name','Bus route','Dept','Year','Fee Paid']

                col1, col2 = st.columns(2)

                with col1:
                        for i in title:
                                st.write(i)


                with col2:

                        if len(results) == 0:
                                st.write('No results found.')

                        else:

                                for result in results:
                                        for i in result:
                                                st.markdown(i)
                                      




    
        # Add a form for users to edit student information
        with st.form(key='edit_student'):
            for index, row in student_data.iterrows():
                if st.checkbox(f"Edit Student {row['ID']}"):
                    edit_name = st.text_input('Name', value=row['Name'])
                    edit_route = st.selectbox('Bus Route', options=['1', '2', '3', '4', '5', '6'], index=int(row['Bus Route'])-1)
                    edit_dept = st.text_input('Department', value=row['Department'])
                    edit_year = st.text_input('Year', value=row['Year'])
                    edit_fee_paid = st.number_input('Fee Paid', value=row['Fee Paid'])

                    edit_default_fee = DEFAULT_FEES.get(edit_route, 0)
                    edit_remaining_fee = edit_default_fee - edit_fee_paid

                    if st.checkbox(f"Remove {row['ID']}"):
                        conn = sqlite3.connect('students.db')
                        c = conn.cursor()
                        c.execute("DELETE FROM student_bus_detail WHERE name=?", (row['ID'],))
                        conn.commit()
                        conn.close()

                        st.success(f'Student {row["ID"]} removed successfully!')

                    if st.form_submit_button(f"Update Student {row['ID']}"):
                        conn = sqlite3.connect('students.db')
                        c = conn.cursor()
                        c.execute("UPDATE students SET name=?, bus_route=?, department=?, year=?, fee_paid=? WHERE id=?",
                                  (edit_name, edit_route, edit_dept, edit_year, edit_fee_paid, row['ID']))
                        conn.commit()
                        conn.close()

                        st.success(f'Student {row["ID"]} updated successfully!')
            st.form_submit_button('Submit')


        # Add a form for users to input student information
        with st.form(key='add_student'):
            st.header('Add New Student')
            name = st.text_input('Name')
            route = st.selectbox('Bus Route', options=['1', '2', '3', '4', '5', '6'])
            dept = st.text_input('Department')
            year = st.text_input('Year')
            fee_paid = st.number_input('Fee Paid')

            # Calculate the remaining fee based on the default fee for the selected route
            default_fee = DEFAULT_FEES.get(route, 0)
            remaining_fee = default_fee - fee_paid

            submit_button = st.form_submit_button(label='Add Student')

            # If the form is submitted, add the student to the database
            if submit_button:
                add_student(name, route, dept, year, fee_paid)
                st.success('Student added successfully!')







# Define a function to search for student data in the database
def search_student_data1(search_term):
    # Use a SQL query to search for the student data
    c_students.execute("SELECT * FROM student_bus_detail WHERE name LIKE ?", ('%' + search_term + '%',))
    results = c_students.fetchall()
    return results






def student_data():

        # Retrieve all students from the database
        student_rows = get_students_details()

        # Convert the rows to a DataFrame for display
        student_data1 = pd.DataFrame(student_rows, columns=['Name','Roll No','Dept','Bus no','Gender','year', 'Bus Route', 'Address', 'Stop'])

        st.table(student_data1)

        st.subheader('Search for Student Data')

        # Create a search bar for the user to enter a search term
        search_term = st.text_input('Enter student name')


        # Display the search results
        if search_term:
                st.write('Search Results')

                # Call the search_student_data() function to retrieve the results
                results = search_student_data1(search_term)

                title=['Name','Roll No','Dept','Bus no','Gender','Year','Bus route','Address','Stop']

                col1, col2 = st.columns(2)

                with col1:
                        for i in title:
                                st.write(i)


                with col2:

                        if len(results) == 0:
                                st.write('No results found.')

                        else:

                                for result in results:
                                        for i in result:
                                                st.markdown(i)
                                      
                                        


        # Add a form for users to edit or remove student information
        with st.form(key='edit_student_details'):
            for index, row in student_data1.iterrows():
                if st.checkbox(f"Edit {row['Name']}",key=f"edit_{index}"):
                    edit_name = st.text_input('Name', value=row['Name'])
                    edit_roll_no = st.text_input('Roll No', value=row['Roll No'])
                    edit_dept = st.text_input('Dept', value=row['Dept'])
                    edit_bus_no = st.text_input('Bus no', value=row['Bus no'])
                    edit_gender = st.selectbox('Gender', options=['Male','Female'])
                    edit_year = st.text_input('Year', value=row['year'])
                    edit_route = st.selectbox('Bus Route', options=['1', '2', '3', '4', '5', '6'], index=int(row['Bus Route'])-1)
                    edit_address = st.text_input('Address', value=row['Address'])
                    edit_stop = st.text_input('Stop', value=row['Stop'])

                    # Add a remove button to remove the row
                    if st.checkbox(f"Remove {row['Name']}"):
                        conn = sqlite3.connect('student_bus_detail.db')
                        c = conn.cursor()
                        c.execute("DELETE FROM student_bus_detail WHERE name=?", (row['Name'],))
                        conn.commit()
                        conn.close()

                        st.success(f'Student {row["Name"]} removed successfully!')

                    # Add an update button to update the row
                    if st.form_submit_button(f"Update {row['Name']}"):
                        conn = sqlite3.connect('student_bus_detail.db')
                        c = conn.cursor()
                        c.execute("UPDATE student_bus_detail SET name=?,roll_no=?,dept=?,bus_no=?,gender=?,year=?, bus_route=?,address=?,stop=? WHERE name=?",
                                  (edit_name,edit_roll_no,edit_dept,edit_bus_no,edit_gender,edit_year, edit_route,edit_address,edit_stop, row['Name']))
                        conn.commit()
                        conn.close()

                        st.success(f'Student {row["Name"]} updated successfully!')

            st.form_submit_button('Submit')








def feedback_table():
                @st.cache_data
                def data_upload():
                        df=pd.read_csv("feedback_dup.csv")
                        return df

                df=data_upload()

                gd=GridOptionsBuilder.from_dataframe(df)
                gd.configure_pagination(enabled=True)
                gd.configure_default_column(editables=True,groupable=True)

                sel_mode=st.radio('Selection Type',options=['single','multiple'])

                gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
                gridoptions=gd.build()
                AgGrid(df,gridOptions=gridoptions,
                       update_mode=GridUpdateMode.SELECTION_CHANGED,
                       height=500,
                       allow_unsafe_jscode=True,
                       theme='alpine')









def generate_pdf_report(positive_feedback, negative_feedback, total_feedback, overall_satisfaction, punctuality_rating):
    pdf_file = BytesIO()
    doc = SimpleDocTemplate(pdf_file)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=18, textColor='navy')
    subtitle_style = ParagraphStyle('subtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, textColor='black')
    subtitle_style1 = ParagraphStyle('subtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, textColor='black',allign='right')

    #define report name
    report=Paragraph('REPORT ON BUS FACILITY FEEDBACK',title_style)

    
    # Define college logo and title
    logo_path = 'C:/Users/admin/OneDrive/Desktop/pspp project/Itechlogo.png'
    logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
    college_title = Paragraph('PSG INSTITUTE OF TECHNOLOGY AND APPLIED RESEARCH', title_style)
    
    
    # Define current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = Paragraph(f'Report generated on: {current_time}', subtitle_style)
    bus_admin = Paragraph('Transport officer', subtitle_style1)
    
    # Define feedback table
    data = [['Total Feedback', total_feedback],
            ['Positive Feedback', positive_feedback],
            ['Negative Feedback', negative_feedback],
            ['Overall Satisfaction', overall_satisfaction],
            ['Punctuality Rating', punctuality_rating]]
    table = Table(data, colWidths=[2*inch, 2*inch])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('FONTSIZE', (0, 0), (-1, 0), 14),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.grey)]))
    
    # Add elements to document
    elements = []
    elements.append(logo)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(college_title)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(report)
    elements.append(Spacer(1, 0.25*inch))
    elements.append(timestamp)
    elements.append(Spacer(1, 0.25*inch))
    elements.append(table)
    elements.append(Spacer(1,2*inch))
    elements.append(bus_admin)
    doc.build(elements)
    
    pdf_file.seek(0)
    return pdf_file








def generate_pdf_positive(positive_feedback, negative_feedback, total_feedback, overall_satisfaction, punctuality_rating,positive_feedback1,negative_feedback1):
    pdf_file = BytesIO()
    doc = SimpleDocTemplate(pdf_file)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=18, textColor='navy')
    subtitle_style = ParagraphStyle('subtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, textColor='black')
    subtitle_style1 = ParagraphStyle('subtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, textColor='black',allign='right')

    #define report name
    report=Paragraph('REPORT ON BUS FACILITY FEEDBACK',title_style)

    
    # Define college logo and title
    logo_path = 'C:/Users/admin/OneDrive/Desktop/pspp project/Itechlogo.png'
    logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
    college_title = Paragraph('PSG INSTITUTE OF TECHNOLOGY AND APPLIED RESEARCH', title_style)
    
    
    # Define current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = Paragraph(f'Report generated on: {current_time}', subtitle_style)
    bus_admin = Paragraph('Transport officer', subtitle_style1)
    
    # Define feedback table
    data = [['Total Feedback', total_feedback],
            ['Positive Feedback', positive_feedback],
            ['Negative Feedback', negative_feedback],
            ['Overall Satisfaction', overall_satisfaction],
            ['Punctuality Rating', punctuality_rating]]
    table = Table(data, colWidths=[2*inch, 2*inch])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('FONTSIZE', (0, 0), (-1, 0), 14),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.grey)]))


    # Define positive feedback section
    positive_feedback_header = Paragraph('Positive Feedback', subtitle_style)
    positive_feedback_str = positive_feedback1
    positive_feedback_paragraph = Paragraph(positive_feedback_str, styles['Normal'])

    
    # Add elements to document
    elements = []
    elements.append(logo)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(college_title)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(report)
    elements.append(Spacer(1, 0.25*inch))
    elements.append(timestamp)
    elements.append(Spacer(1, 0.25*inch))
    elements.append(table)
    elements.append(Spacer(1,2*inch))
    elements.append(positive_feedback_header)
    elements.append(Spacer(1, 0.25*inch))
    elements.append(positive_feedback_paragraph)
    elements.append(Spacer(1, 0.25*inch))
    elements.append(bus_admin)
    doc.build(elements)
    
    pdf_file.seek(0)
    return pdf_file








def generate_pdf_negative(positive_feedback, negative_feedback, total_feedback, overall_satisfaction, punctuality_rating,positive_feedback1,negative_feedback1):
    pdf_file = BytesIO()
    doc = SimpleDocTemplate(pdf_file)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=18, textColor='navy')
    subtitle_style = ParagraphStyle('subtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, textColor='black')
    subtitle_style1 = ParagraphStyle('subtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, textColor='black',allign='right')

    #define report name
    report=Paragraph('REPORT ON BUS FACILITY FEEDBACK',title_style)

    
    # Define college logo and title
    logo_path = 'C:/Users/admin/OneDrive/Desktop/pspp project/Itechlogo.png'
    logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
    college_title = Paragraph('PSG INSTITUTE OF TECHNOLOGY AND APPLIED RESEARCH', title_style)
    
    
    # Define current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = Paragraph(f'Report generated on: {current_time}', subtitle_style)
    bus_admin = Paragraph('Transport officer', subtitle_style1)
    
    # Define feedback table
    data = [['Total Feedback', total_feedback],
            ['Positive Feedback', positive_feedback],
            ['Negative Feedback', negative_feedback],
            ['Overall Satisfaction', overall_satisfaction],
            ['Punctuality Rating', punctuality_rating]]
    table = Table(data, colWidths=[2*inch, 2*inch])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('FONTSIZE', (0, 0), (-1, 0), 14),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.grey)]))


    # Define positive feedback section
    negative_feedback_header = Paragraph('Negative Feedback', subtitle_style)
    negative_feedback_str = negative_feedback1
    negative_feedback_paragraph = Paragraph(negative_feedback_str, styles['Normal'])

    
    # Add elements to document
    elements = []
    elements.append(logo)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(college_title)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(report)
    elements.append(Spacer(1, 0.25*inch))
    elements.append(timestamp)
    elements.append(Spacer(1, 0.25*inch))
    elements.append(table)
    elements.append(Spacer(1,2*inch))
    elements.append(negative_feedback_header)
    elements.append(Spacer(1, 0.25*inch))
    elements.append(negative_feedback_paragraph)
    elements.append(Spacer(1, 0.25*inch))
    elements.append(bus_admin)
    doc.build(elements)
    
    pdf_file.seek(0)
    return pdf_file







def feedback_adm():

        st.markdown('<h3 style="text-align:center;">FEEDBACK GIVEN BY STUDENT AND STAFF</h3>', unsafe_allow_html=True)

        feedback_table()
        
        if st.button("Generate Report"):
                feedback_df = pd.read_csv('feedback.csv', names=['name', 'email', 'feedback', 'overall_satisfaction', 'punctuality_rating'])
                feedback_df.fillna('', inplace=True)
                positive_feedback = feedback_df['feedback'].str.contains('good', case=False).sum()
                feedback1 = feedback_df['feedback']
                list1=[]
                for i in feedback1:
                        if "good" in i:
                                list1.append(i)
                positive_feedback1 = '\n'.join(list1)
                                
                negative_feedback = feedback_df['feedback'].str.contains('bad', case=False).sum()
                feedback2 = feedback_df['feedback']
                list2=[]
                for i in feedback2:
                        if "bad" in i:
                                list2.append(i)
                negative_feedback1='\n'.join(list2)
                
                total_feedback = feedback_df.shape[0]
                overall_satisfaction1 = feedback_df['overall_satisfaction'].astype(str).str.cat(sep='')
                overall_satisfaction2=overall_satisfaction1.split('.')
                overall_satisfaction3=0
                num1=0

                for s in overall_satisfaction2:
                        for j in s:
                                overall_satisfaction3+=int(s[int(j)])
                                num1+=1
                        overall_satisfaction=overall_satisfaction3//num1
                punctuality_rating1 = feedback_df['punctuality_rating'].astype(str).str.cat(sep='')
                punctuality_rating2=punctuality_rating1.split('.')
                punctuality_rating3=0
                num=0

                for i in punctuality_rating2:
                        for j in i:
                                punctuality_rating3+=int(i[int(j)])
                                num+=1
                punctuality_rating=punctuality_rating3//num

                st.markdown('Count of feedback Report')

                # Generate PDF report
                pdf_file = generate_pdf_report(positive_feedback, negative_feedback, total_feedback, overall_satisfaction, punctuality_rating)

                # Download PDF report
                b64 = base64.b64encode(pdf_file.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="report.pdf">Download PDF report</a>'
                st.markdown(href, unsafe_allow_html=True)


                st.markdown('Positive Feedback Report')
                # Generate PDF report
                pdf_file = generate_pdf_positive(positive_feedback, negative_feedback, total_feedback, overall_satisfaction, punctuality_rating,positive_feedback1,negative_feedback1)

                # Download PDF report
                b64 = base64.b64encode(pdf_file.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="report.pdf">Download PDF report</a>'
                st.markdown(href, unsafe_allow_html=True)


                st.markdown('Negative Feedback Report')
                # Generate PDF report
                pdf_file = generate_pdf_negative(positive_feedback, negative_feedback, total_feedback, overall_satisfaction, punctuality_rating,positive_feedback1,negative_feedback1)

                # Download PDF report
                b64 = base64.b64encode(pdf_file.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="report.pdf">Download PDF report</a>'
                st.markdown(href, unsafe_allow_html=True)

                
        







def admin_login():

        st.subheader('Admin')

        #load user authentication admin

        users=db.fetch_all_users()

        usernames_adm=[user["key"]for user in users]
        names_adm=[user["name"]for user in users]
        passwords_adm=[user["password"]for user in users]

        hashed_passwords_adm=stauth.Hasher(passwords_adm).generate()
        
        
        #loasd hashed passwords admin

        
        authenticator_adm=stauth.Authenticate(names_adm,usernames_adm,hashed_passwords_adm,"sales_dashboard_adm","1234")

        name_adm,authentication_status_adm,username_adm=authenticator_adm.login("login","main")


        if authentication_status_adm==False:
                st.error("username/password is incorrect")

        if authentication_status_adm==None:
                st.warning("Please enter your username and password")

        if authentication_status_adm==True:
                st.sidebar.title(f"Bus Data for :blue[{name_adm}]")

                page_names_to_funcs = {"MAIN PAGE": main_page,"ROUTE 1": route1,"ROUTE 2": route2,'ROUTE 3':route3,'ROUTE 4':route4,'ROUTE 5':route5,'Add Student':add_stu,'Student Data':student_data,'Fee Details':fee_details,'Feedback Review':feedback_adm}
                selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
                page_names_to_funcs[selected_page]()

                authenticator_adm.logout("logout","sidebar")







def Bus_request():
        st.header("BUS REQUEST")
        st.markdown('<p style="text-align:center;":>Staff\'s and student of same and different college who want to avail the college bus facility for a short period of time , Kindly send a msg over here and our Transport Officer will Contact you as soon as possible.</p>',unsafe_allow_html=True)

        Feedback="""
<form action="https://formsubmit.co/shriniha.pa@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your Email"required>
     <input type="text" name="Profession" placeholder="Professor/student"required>
     <input type="text" name="College" placeholder="Your College Name"required>
     <input type="text" name="Address" placeholder="Your Address"required>
     <textarea name="message" placeholder="Your Bus Request Message"></textarea>
     <button type="submit">Send</button>
</form>
"""
        st.markdown(Feedback,unsafe_allow_html=True)

        with open("style.css.txt")as f:
                st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)







def email_request():
        st.title("Email Sending")
        name=st.text_input("Name")
        email=st.text_input("Enter Your mail:")
        admin_email = 'shriniha.pa@gmail.com'
        msg=st.text_input('Enter your Message')
        if st.button('Send'):
                message = MIMEMultipart()
                message['From'] = 'shriniha.pa@gmail.com'
                message['To'] = admin_email
                message['Subject'] = 'New Mail from Student'
                body = f'Name: {name}\nEmail: {email}\nMessage: {msg}'
                message.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('shriniha.pa@gmail.com', 'krbypzcmwpopbmjh')
                server.sendmail('shriniha.pa@gmail.com', admin_email, message.as_string())
                server.quit()







def Feedback():
        st.title("Bus Facility Feedback")
        st.markdown('<p style="text-align:center;":>Kindly Provide your Feedback over here so that we could improve ourselves.</p>',unsafe_allow_html=True)

        name = st.text_input("Please enter your name:")
        email = st.text_input("Please enter your email:")

        feedback = st.text_area("Please provide your feedback:")
        overall_satisfaction = st.slider("Overall satisfaction (out of 10)", min_value=1, max_value=10, value=5)
        punctuality_rating  = st.slider("Punctuality rating", min_value=1, max_value=10, value=5)

        if st.button("Submit Feedback"):
                with open('feedback.csv', mode='a', newline='') as feedback_file:
                        feedback_writer = csv.writer(feedback_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        feedback_writer.writerow([name, email, feedback,overall_satisfaction,punctuality_rating])
                with open('feedback_dup.csv', mode='a', newline='') as feedback_file_dup:
                        feedback_writer = csv.writer(feedback_file_dup, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        feedback_writer.writerow([name, email, feedback,overall_satisfaction,punctuality_rating])

                st.success('Thank you for your feedback!')

                # Send email to admin

                admin_email = 'shriniha.pa@gmail.com'
                message = MIMEMultipart()
                message['From'] = 'shriniha.pa@gmail.com'
                message['To'] = admin_email
                message['Subject'] = 'New feedback submission'
                body = f'Name: {name}\nEmail: {email}\nFeedback: {feedback}\nOverall Satisfaction: {overall_satisfaction}\nPunctuality Rating: {punctuality_rating}'
                message.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('shriniha.pa@gmail.com', 'krbypzcmwpopbmjh')
                server.sendmail('shriniha.pa@gmail.com', admin_email, message.as_string())
                server.quit()






def route1_pdf():

        st.markdown('<span style="color: green;">DOWNLOAD THE DETAILS BELOW FOR ROUTE 1!</span>', unsafe_allow_html=True)

        # Read the PDF file into memory
        with open('R1', 'rb') as f:
                pdf_data = f.read()

        # Create a download button for the PDF file
        b64 = base64.b64encode(pdf_data).decode('utf-8')
        href = f'<a href="data:application/pdf;base64,{b64}" download="R1.pdf">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)






def route2_pdf():

        st.markdown('<span style="color: green;">DOWNLOAD THE DETAILS BELOW FOR ROUTE 2!</span>', unsafe_allow_html=True)
        
        # Read the PDF file into memory
        with open('R2.pdf', 'rb') as f:
                pdf_data = f.read()

        # Create a download button for the PDF file
        b64 = base64.b64encode(pdf_data).decode('utf-8')
        href = f'<a href="data:application/pdf;base64,{b64}" download="R2.pdf">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)







def route3_pdf():

        st.markdown('<span style="color: green;">DOWNLOAD THE DETAILS BELOW FOR ROUTE 3!</span>', unsafe_allow_html=True)
        
        # Read the PDF file into memory
        with open('R3.pdf', 'rb') as f:
                pdf_data = f.read()

        # Create a download button for the PDF file
        b64 = base64.b64encode(pdf_data).decode('utf-8')
        href = f'<a href="data:application/pdf;base64,{b64}" download="R3">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)





def route4_pdf():

        st.markdown('<span style="color: green;">DOWNLOAD THE DETAILS BELOW FOR ROUTE 4!</span>', unsafe_allow_html=True)
        
        # Read the PDF file into memory
        with open('R4.pdf', 'rb') as f:
                pdf_data = f.read()

        # Create a download button for the PDF file
        b64 = base64.b64encode(pdf_data).decode('utf-8')
        href = f'<a href="data:application/pdf;base64,{b64}" download="R4">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)





def route5_pdf():

        st.markdown('<span style="color: green;">DOWNLOAD THE DETAILS BELOW FOR ROUTE 5!</span>', unsafe_allow_html=True)
        
        # Read the PDF file into memory
        with open('R5.pdf', 'rb') as f:
                pdf_data = f.read()

        # Create a download button for the PDF file
        b64 = base64.b64encode(pdf_data).decode('utf-8')
        href = f'<a href="data:application/pdf;base64,{b64}" download="R5">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)






def route6_pdf():

        st.markdown('<span style="color: green;">DOWNLOAD THE DETAILS BELOW FOR ROUTE 6!</span>', unsafe_allow_html=True)
        
        # Read the PDF file into memory
        with open('R6.pdf', 'rb') as f:
                pdf_data = f.read()

        # Create a download button for the PDF file
        b64 = base64.b64encode(pdf_data).decode('utf-8')
        href = f'<a href="data:application/pdf;base64,{b64}" download="R6">Download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)







def your_data():
        st.subheader("Your bus details:")
        st.write(f"Name: {bus_details[0]}")
        st.write(f"Roll No.: {bus_details[1]}")
        st.write(f"Department.: {bus_details[2]}")
        st.write(f"Bus No.: {bus_details[3]}")
        st.write(f"Gender: {bus_details[4]}")
        st.write(f"Year: {bus_details[5]}")
        st.write(f"Bus Route: {bus_details[6]}")
        st.write(f"Address: {bus_details[7]}")
        st.write(f"Stop: {bus_details[8]}")







def more_details():
        st.markdown('<h3 style="text-align:center;">Select the Route</h3>', unsafe_allow_html=True)
        options = ['Kuniamuthur (Route 1)', 'Vadaveli (Route 2)', 'Gandhipuram (Route 3)','PN Palayam (Route 4)','Tiruppur (Route 5)','Palladam (Route 6)']
        selected=st.selectbox("",options)

        if selected=='Kuniamuthur (Route 1)':
                route1_pdf()

        elif selected=='Vadaveli (Route 2)':
                route2_pdf()

        elif selected=='Gandhipuram (Route 3)':
                route3_pdf()

        elif selected=='PN Palayam (Route 4)':
                route4_pdf()

        elif selected=='Tiruppur (Route 5)':
                route5_pdf()

        elif selected=='Palladam (Route 6)':
                route6_pdf()

        st.markdown('<span style="color: red;">DOWNLOAD TRANSPORT REQUISITION LETTER FOR FACULTY OR STAFF!</span>', unsafe_allow_html=True)





        def get_word_download_link(file_path):
                with open(file_path, 'rb') as f:
                        doc_data = f.read()
                        b64 = base64.b64encode(doc_data).decode('utf-8')
                        href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="Transport Requesition Letter SAMPLE 2022.doc">Download Word Document</a>'
                return href





        # Display a download button for the Word document
        doc_download_link = get_word_download_link('Transport Requesition Letter SAMPLE 2022.doc')
        st.markdown(doc_download_link, unsafe_allow_html=True)


        st.markdown('<span style="color: #FFA500;">FOR MORE DETAILS VISIT THE COLLEGE OFFICIAL PAGE</span>', unsafe_allow_html=True)


        website_url = 'http://www.psgitech.ac.in/Transport.php'

        # Display the website URL as a link

        st.markdown(f'<a href="{website_url}" target="_blank">Visit {website_url}</a>', unsafe_allow_html=True)





def stu_login():

        st.subheader("Student Login")

        users_stu=db_stu.fetch_all_users()

        usernames_stu=[user['key']for user in users_stu ]
        names_stu=[user['name']for user in users_stu ]
        passwords_stu=[user['password']for user in users_stu ]
        
        hashed_passwords_stu=stauth.Hasher(passwords_stu).generate()

        authenticator_stu=stauth.Authenticate(names_stu,usernames_stu,hashed_passwords_stu,"sales_dashboard_adm","5678")

        name_stu,authentication_status_stu,username_stu=authenticator_stu.login("login","main")

        if authentication_status_stu==False:
                st.error("username/password is incorrect")
        if authentication_status_stu==None:
                st.warning("Please enter your username and password")
        if authentication_status_stu==True:

                user_details = get_user_details(username_stu)
                name = user_details[2]

                # Retrieve student bus details from database
                bus_details = get_student_bus_detail(name_stu)

                options = ['Your Details', 'Send mail', 'Feedback']
                selected_option = st.selectbox('Select an option', options)

                if selected_option == 'Your Details':

                        st.subheader("Your bus details:")
                        st.write(f"Name: {bus_details[0]}")
                        st.write(f"Roll No.: {bus_details[1]}")
                        st.write(f"Department.: {bus_details[2]}")
                        st.write(f"Bus No.: {bus_details[3]}")
                        st.write(f"Gender: {bus_details[4]}")
                        st.write(f"Year: {bus_details[5]}")
                        st.write(f"Bus Route: {bus_details[6]}")
                        st.write(f"Address: {bus_details[7]}")
                        st.write(f"Stop: {bus_details[8]}")


                elif selected_option == 'Send mail':
                        email_request()

                elif selected_option == 'Feedback':
                        Feedback()

                
                authenticator_stu.logout("logout","sidebar")

                






def front():
  html_code="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>College Bus Management App</title>
        </head>
        <body>

            <header>
                <img src="Itechlogo.png" alt="PSG Institute of Technology and Applied Research logo" style="float:left;width:100px;height:100px;">
                <h1 style="display:inline-block;margin-left:10px;">PSG Institute of Technology and Applied Research</h1>
                <br>
                <p style="font-size:14px;margin-top:0;margin-bottom:0;">Neelambur, Coimbatore-641062</p>
            </header>

            <footer>
                <img src="bus.png" alt="Bus Image" style="float:right;width:100px;height:100px;">
            </footer>

        </body>
        </html>
    """
  st.write(html_code,unsafe_allow_html=True)

    








#initialize state admin
def callback1():
    # set load_state1 to True and load_state2 to False
    st.session_state.load_state1 = True
    st.session_state.load_state2 = False
    st.session_state.load_state3 = False




def callback2():
    # set load_state2 to True and load_state1 to False
    st.session_state.load_state2 = True
    st.session_state.load_state1 = False
    st.session_state.load_state3 = False





def callback3():
    # set load_state1 to True and load_state2 to False
    st.session_state.load_state3 = True
    st.session_state.load_state2 = False
    st.session_state.load_state1 = False





#front page with name and image
front()




#initialize state admin
if 'load_state1' not in st.session_state:

    st.session_state.load_state1 = False


if 'load_state2' not in st.session_state:

    st.session_state.load_state2 = False



if 'load_state3' not in st.session_state:

    st.session_state.load_state3 = False






adm = st.sidebar.button('Admin', key='adm', on_click=callback1)
usr = st.sidebar.button('User', key='user', on_click=callback2)
other=st.sidebar.button('Others',key='other',on_click=callback3)






if st.session_state.load_state2:

    stu_login()                           

                                        
elif st.session_state.load_state1:

    admin_login()


elif st.session_state.load_state3:


    st.markdown('<h3 style="text-align:center;">Select your Service</h3>', unsafe_allow_html=True)
    page_names_to_funcs = {"Send Email": Bus_request,"Feedback": Feedback,"More Details": more_details}
    selected_page = st.radio("Select a page", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()

        

#end of program

        




        
    

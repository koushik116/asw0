from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
import sqlite3

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('PlacementManagement.db')
cursor = connector.cursor()

connector.execute(
"CREATE TABLE IF NOT EXISTS PLACEMENT_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, ROLL_NO TEXT, GENDER TEXT, AGG TEXT, PLACE TEXT, PACK TEXT)"
)

# Creating the functions
def reset_fields():
   global name_strvar, email_strvar, roll_strvar, gender_strvar, agg, place_strvar, pack

   for i in ['name_strvar', 'email_strvar', 'roll_strvar', 'gender_strvar', 'agg', 'place_strvar', 'pack']:
       exec(f"{i}.set('')")



def reset_form():
   global tree
   tree.delete(*tree.get_children())

   reset_fields()



def display_records():
   tree.delete(*tree.get_children())

   curr = connector.execute('SELECT * FROM PLACEMENT_MANAGEMENT')
   data = curr.fetchall()

   for records in data:
       tree.insert('', END, values=records)


def add_record():
   global name_strvar, email_strvar, roll_strvar, gender_strvar, agg, place_strvar,pack

   name = name_strvar.get()
   email = email_strvar.get()
   roll = roll_strvar.get()
   gender = gender_strvar.get()
   AGG = agg.get()
   place = place_strvar.get()
   PACK = pack.get()

   if not name or not email or not roll or not gender or not AGG or not place or not PACK:
       mb.showerror('Error!', "Please fill all the missing fields!!")
   else:
       try:
           connector.execute(
           'INSERT INTO PLACEMENT_MANAGEMENT (NAME, EMAIL, ROLL_NO, GENDER, AGG, PLACE, PACK) VALUES (?,?,?,?,?,?,?)', (name, email, roll, gender, AGG, place, PACK, )
           )
           connector.commit()
           mb.showinfo('Record added', f"Record of {name} was successfully added")
           reset_fields()
           display_records()
       except:
           mb.showerror('Wrong type',
                        'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')



def remove_record():
   if not tree.selection():
       mb.showerror('Error!', 'Please select an item from the database')
   else:
       current_item = tree.focus()
       values = tree.item(current_item)
       selection = values["values"]

       tree.delete(current_item)

       connector.execute('DELETE FROM PLACEMENT_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
       connector.commit()

       mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

       display_records()


def view_record():
   global name_strvar, email_strvar, roll_strvar, gender_strvar, agg, place_strvar,pack

   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]


   name_strvar.set(selection[1]); email_strvar.set(selection[2])
   roll_strvar.set(selection[3]); gender_strvar.set(selection[4])
   agg.set(selection[5]); place_strvar.set(selection[6]);pack.set(selection[7]);


# Initializing the GUI window
main = Tk()
main.title('STUDENT MINDS')
main.geometry('1000x600')
main.resizable(0, 0)

# Creating the background and foreground color variables
lf_bg = 'DIMGREY' # bg color for the left_frame
cf_bg = 'CadetBlue' # bg color for the center_frame

# Creating the StringVar or IntVar variables
name_strvar = StringVar()
email_strvar = StringVar()
roll_strvar = StringVar()
gender_strvar = StringVar()
agg = StringVar()
place_strvar = StringVar()
pack = StringVar()

# Placing the components in the main window
Label(main, text="PLACEMENT MANAGEMENT SYSTEM", font=headlabelfont, bg='CadetBlue').pack(side=TOP, fill=X)

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

# Placing components in the left frame
Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.06)
Label(left_frame, text="Roll Number", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.16)
Label(left_frame, text="Email Address", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.26)
Label(left_frame, text="Gender", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.36)
Label(left_frame, text="Aggregate", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.46)
Label(left_frame, text="Placement", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.56)
Label(left_frame, text="Package", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.66)

Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=30, rely=0.1)
Entry(left_frame, width=19, textvariable=roll_strvar, font=entryfont).place(x=30, rely=0.2)
Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=30, rely=0.3)
Entry(left_frame, width=19, textvariable=agg, font=entryfont).place(x=30, rely=0.5)
Entry(left_frame, width=19, textvariable=pack, font=entryfont).place(x=30, rely=0.7)

OptionMenu(left_frame, place_strvar, '1.GOOGLE', '2.WIPRO','3.INFOSYS','4.MICROSOFT','5.JP MORGON').place(x=30, rely=0.6, relwidth=0.52)
OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=30, rely=0.4, relwidth=0.52)


Button(left_frame, text='Submit and Add Record', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)

# Placing components in the center frame
Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Delete database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.55)
Button(center_frame, text='View Placements', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.65)

# Placing components in the right frame
Label(right_frame, text='Students Records', font=headlabelfont, bg='CadetBlue', fg='LightCyan').pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                   columns=('Student ID', "Name", "Email Address", "Roll Number", "Gender", "Aggregate", "Placement","Package"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Roll Number', text='Roll No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Aggregate', text='Aggregate', anchor=CENTER)
tree.heading('Placement', text='Placement', anchor=CENTER)
tree.heading('Package', text='Package', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)
tree.column('#8', width=150, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

# Finalizing the GUI window
main.update()
main.mainloop()
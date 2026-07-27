import tkinter as tk
import sqlite3
conn = sqlite3.connect("contacts.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,phone TEXT)")
conn.commit()
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    if name != "" and phone != "":
        cur.execute("INSERT INTO contacts(name,phone) VALUES(?,?)",(name,phone))
        conn.commit()
        name_entry.delete(0,tk.END)
        phone_entry.delete(0,tk.END)
        show_contacts()
def search_contact():
    text = search_entry.get()
    cur.execute("SELECT name,phone FROM contacts WHERE name LIKE ?",('%'+text+'%',))
    rows = cur.fetchall()
    listbox.delete(0,tk.END)
    for row in rows:
        listbox.insert(tk.END,row[0]+" - "+row[1])
def show_contacts():
    cur.execute("SELECT name,phone FROM contacts")
    rows = cur.fetchall()
    listbox.delete(0,tk.END)
    for row in rows:
        listbox.insert(tk.END,row[0]+" - "+row[1])
def delete_contact():
    if listbox.curselection():
        item = listbox.get(listbox.curselection()[0])
        name = item.split(" - ")[0]
        cur.execute("DELETE FROM contacts WHERE name=?",(name,))
        conn.commit()
        show_contacts()
def update_contact():
    if listbox.curselection():
        item = listbox.get(listbox.curselection()[0])
        old_name = item.split(" - ")[0]
        new_name = name_entry.get()
        new_phone = phone_entry.get()
        cur.execute("UPDATE contacts SET name=?,phone=? WHERE name=?",(new_name,new_phone,old_name))
        conn.commit()
        name_entry.delete(0,tk.END)
        phone_entry.delete(0,tk.END)
        show_contacts()
def select_contact(event):
    if listbox.curselection():
        item = listbox.get(listbox.curselection()[0])
        data = item.split(" - ")
        name_entry.delete(0,tk.END)
        phone_entry.delete(0,tk.END)
        name_entry.insert(0,data[0])
        phone_entry.insert(0,data[1])
root = tk.Tk()
root.title("Mini Contact Book")
root.geometry("420x380")
tk.Label(root,text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()
tk.Label(root,text="Phone").pack()
phone_entry = tk.Entry(root)
phone_entry.pack()
tk.Button(root,text="Add",command=add_contact).pack(pady=2)
tk.Button(root,text="Update",command=update_contact).pack(pady=2)
tk.Button(root,text="Delete",command=delete_contact,).pack(pady=2)
tk.Label(root,text="Search").pack()
search_entry = tk.Entry(root)
search_entry.pack()
tk.Button(root,text="Search",command=search_contact).pack(pady=2)
listbox = tk.Listbox(root,width=40)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>",select_contact)
show_contacts()
root.mainloop()
conn.close()
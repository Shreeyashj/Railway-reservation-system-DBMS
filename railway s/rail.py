from tkinter import *
from tkinter import ttk, messagebox, filedialog
import mysql.connector as mysql
import webview

def open_webview():
    webview.create_window("Railway Management System", html=r"C:\Users\DevRahul\Desktop\railway s_rail.html", width=800, height=600)
    webview.start()

def book():
    train_no = e_a.get()
    journey_date = e_b.get()
    source_station = e_c.get()
    dest_station = e_d.get()
    name = e_name.get()
    age = e_age.get()
    gender = var_gender.get()
    seat_pref = var_seat_pref.get()
    food_choice = var_food_choice.get()

    if not all([train_no, journey_date, source_station, dest_station, name, age, gender, seat_pref, food_choice]):
        messagebox.showinfo("Book Status", "All fields are required")
    else:
        try:
            con = mysql.connect(host="localhost", user="root", password="Shreeyash@123", database="railway1")
            cursor = con.cursor()
            cursor.execute("INSERT INTO rail (train_no, journey_date, source_station, dest_station, name, age, gender, seat_pref, food_choice) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (train_no, journey_date, source_station, dest_station, name, age, gender, seat_pref, food_choice))
            con.commit()
            messagebox.showinfo("Book Status", "Booked successfully")

            # Preview the booked ticket
            ticket_data = f"Train No: {train_no}\nJourney Date: {journey_date}\nSource Station: {source_station}\nDestination Station: {dest_station}\nName: {name}\nAge: {age}\nGender: {gender}\nSeat Preference: {seat_pref}\nFood Preference: {food_choice}"
            preview_ticket(ticket_data)

        except mysql.Error as e:
            messagebox.showerror("Error", f"Error occurred: {e}")
        finally:
            if con.is_connected():
                cursor.close()
                con.close()

def cancel():
    train_no = e_a.get()
    if not train_no:
        messagebox.showinfo("Cancel Status", "Train No is compulsory for deleting")
    else:
        try:
            con = mysql.connect(host="localhost", user="root", password="Shreeyash@123", database="railway1")
            cursor = con.cursor()
            cursor.execute("DELETE FROM rail WHERE train_no = %s", (train_no,))
            con.commit()
            messagebox.showinfo("Cancel Status", "Cancelled successfully")
        except mysql.Error as e:
            messagebox.showerror("Error", f"Error occurred: {e}")
        finally:
            if con.is_connected():
                cursor.close()
                con.close()

def seat():
    try:
        con = mysql.connect(host="localhost", user="root", password="Shreeyash@123", database="railway1")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM rail")
        rows = cursor.fetchall()
        for row in rows:
            insertdata = f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]} {row[7]} {row[8]}"
            listbox.insert(END, insertdata)
    except mysql.Error as e:
        messagebox.showerror("Error", f"Error occurred: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def download_ticket():
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showinfo("Download Status", "Please select a ticket to download.")
        return

    # Get the ticket data
    ticket_data = listbox.get(selected_index[0])

    # Prompt the user to choose a file location to save the ticket
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not file_path:
        return  # User canceled the save operation

    # Write the ticket data to the selected file
    with open(file_path, "w") as file:
        file.write("Railway Ticket\n\n")
        file.write("Ticket Details:\n")
        file.write(ticket_data)
        file.write("\n\nPassenger Information:\n")
        file.write(f"Train No: {e_a.get()}\n")
        file.write(f"Journey Date: {e_b.get()}\n")
        file.write(f"Source Station: {e_c.get()}\n")
        file.write(f"Destination Station: {e_d.get()}\n")
        file.write(f"Name: {e_name.get()}\n")
        file.write(f"Age: {e_age.get()}\n")
        file.write(f"Gender: {var_gender.get()}\n")
        file.write(f"Seat Preference: {var_seat_pref.get()}\n")
        file.write(f"Food Preference: {var_food_choice.get()}\n")

    messagebox.showinfo("Download Status", "Ticket downloaded successfully.")

def preview_ticket(ticket_data):
    preview_window = Toplevel(root)
    preview_window.title("Preview Ticket")
    preview_window.geometry("400x300")

    # Create labels to display ticket details
    Label(preview_window, text="Railway Ticket", font=("Arial", 16, "bold")).pack()
    Label(preview_window, text="Ticket Details:", font=("Arial", 12, "bold")).pack()
    Label(preview_window, text=ticket_data, justify="left").pack(pady=10)

    # Add a close button to close the preview window
    close_button = Button(preview_window, text="Close", command=preview_window.destroy)
    close_button.pack(pady=10)


root = Tk()
root.geometry("800x400")
root.title("Python + Database")

# Labels and Entry fields
Label(root, text="Railway Reservation Management System", background='blue', foreground="white", font=("Times New Roman", 15)).place(x=250, y=10)
Label(root, text='Enter Train No', font=('bold', 10)).place(x=20, y=60)
Label(root, text='Journey Date', font=('bold', 10)).place(x=20, y=90)
Label(root, text='Source Station', font=('bold', 10)).place(x=20, y=120)
Label(root, text='Destination Station', font=('bold', 10)).place(x=20, y=150)
Label(root, text='Name', font=('bold', 10)).place(x=20, y=180)
Label(root, text='Age', font=('bold', 10)).place(x=20, y=210)
Label(root, text='Gender', font=('bold', 10)).place(x=20, y=240)
Label(root, text='Seat Preference', font=('bold', 10)).place(x=20, y=270)
Label(root, text='Food Preference', font=('bold', 10)).place(x=20, y=300)

e_a = Entry()
e_a.place(x=150, y=60)
e_b = Entry()
e_b.place(x=150, y=90)
e_c = Entry()
e_c.place(x=150, y=120)
e_d = Entry()
e_d.place(x=150, y=150)
e_name = Entry()
e_name.place(x=150, y=180)
e_age = Entry()
e_age.place(x=150, y=210)

var_gender = StringVar()
var_seat_pref = StringVar()
var_food_choice = StringVar()

Checkbutton(root, text="Male", variable=var_gender, onvalue="Male", offvalue="").place(x=150, y=240)
Checkbutton(root, text="Female", variable=var_gender, onvalue="Female", offvalue="").place(x=210, y=240)

# Dropdown for Seat Preference
seat_choices = ['Window Seat', 'Lower Berth', 'Upper Berth', 'Middle Berth', 'Side Lower', 'Side Upper']
OptionMenu(root, var_seat_pref, *seat_choices).place(x=150, y=270)

# Checkboxes for Food Preference
Checkbutton(root, text="Veg", variable=var_food_choice, onvalue="Veg", offvalue="").place(x=150, y=300)
Checkbutton(root, text="Non-Veg", variable=var_food_choice, onvalue="Non-Veg", offvalue="").place(x=210, y=300)

# Buttons
Button(root, text="Book Ticket", font=("bold", 10), bg="white", command=book).place(x=20, y=340)
Button(root, text="Cancel Ticket", font=("bold", 10), bg="white", command=cancel).place(x=120, y=340)
Button(root, text="View Ticket", font=("bold", 10), bg="white", command=seat).place(x=220, y=340)
Button(root, text="Download Ticket", font=("bold", 10), bg="white", command=download_ticket).place(x=320, y=340)

# Listbox for displaying data
listbox = Listbox(root)
listbox.place(x=400, y=60, width=350, height=280)

root.mainloop()

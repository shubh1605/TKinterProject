from tkinter import *
import sqlite3
from tkcalendar import DateEntry
import datetime
from tkinter import ttk
from matplotlib import pyplot as plt
from datetime import date, timedelta
import calendar
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import ImageTk, Image

root = Tk()
root.geometry('600x330')
root.configure(background='#FFE4C4')

root.title('Hisaab Khitab')
my_img = ImageTk.PhotoImage(Image.open("HisaabKhaata.jpg"))
root.iconphoto(False, my_img)


def setWindowBackground(window):
    window.configure(background='#FFE4C4')
    window.iconphoto(False, my_img)


def writeData(query, params):
    conn = sqlite3.connect('hisaab.db')
    c = conn.cursor()

    if(params == None):
        c.execute(query)
    else:
        c.execute(query, params)

    conn.commit()
    conn.close()


def getData(query, params=None):

    conn = sqlite3.connect('hisaab.db')
    c = conn.cursor()

    if(params == None):
        c.execute(query)
        records = c.fetchall()
    else:
        c.execute(query, params)
        records = c.fetchall()

    conn.commit()
    conn.close()

    return records

# Delete records

# writeData('DELETE FROM records')

# Create Table

# writeData("""CREATE TABLE records(
#  			type text,
#  			opposite_party text,
#  			date_of_transaction text,
#  			amount real,
#  			current_balance real,
#  			date_of_entry text,
#  			Reason text null,
#  			Category text
#  			) """)


def submitRecord():
    balance = getData(
        " SELECT current_balance FROM records ORDER BY oid DESC LIMIT 1")
    if balance == []:
        cur_balance = amount.get()
    else:
        t = type_.get()

        if t == "Debit":
            cur_balance = float(balance[0][0]) + float(amount.get())

        else:
            cur_balance = float(balance[0][0]) - float(amount.get())

    date = datetime.date.today()
    writeData(" INSERT INTO records VALUES (:type, :opposite_party, :date_of_transaction, :amount, :current_balance,:date_of_entry, :reason, :category) ",
              {
                  "type": type_.get(),
                  "opposite_party": opposite_party.get(),
                  "date_of_transaction": date_of_transaction.get(),
                  "date_of_entry": date.strftime("%m/%d/%y"),
                  "amount": amount.get(),
                  "current_balance": cur_balance,
                  "reason": reason.get("1.0", END),
                  "category": category_.get()
              })

    type_debit.deselect()
    type_credit.deselect()
    opposite_party.delete(0, END)
    amount.delete(0, END)
    reason.delete('1.0', END)


def labelsForRecords(record):
    Label(record, text="Type", font="Helvetica 12 bold",
          bg='#FFE4C4', relief="solid", width=13, padx=4).grid(row=1, column=0)
    Label(record, text="party", font="Helvetica 12 bold",
          bg='#FFE4C4', relief="solid", width=13, padx=4).grid(row=1, column=1)
    Label(record, text="Transaction Date", font="Helvetica 12 bold",
          bg='#FFE4C4', relief="solid", width=13, padx=4).grid(row=1, column=2)
    Label(record, text="Amount", font="Helvetica 12 bold",
          bg='#FFE4C4', relief="solid", width=13, padx=4).grid(row=1, column=3)
    Label(record, text="Date of Entry", font="Helvetica 12 bold ",
          bg='#FFE4C4', relief="solid", width=13, padx=4).grid(row=1, column=5)
    Label(record, text="Reason", font="Helvetica 12 bold ",
          bg='#FFE4C4', relief="solid", width=13, padx=4).grid(row=1, column=6, columnspan=1)
    Label(record, text="Category", font="Helvetica 12 bold ",
          bg='#FFE4C4', relief="solid", width=13, padx=4).grid(row=1, column=7, columnspan=1)


def searchedRecords(search_key):

    records.destroy()

    global searched_records
    searched_records = Toplevel()
    setWindowBackground(searched_records)

    query = str(search_key.get())

    balance = getData(
        " SELECT current_balance FROM records ORDER BY oid DESC LIMIT 1")

    if(balance != []):
        Label(searched_records, text="Current Balance: ", font="Helvetica 12 bold",
              pady=8, padx=2, borderwidth=2, relief="solid").grid(row=0, column=2)
        Label(searched_records, text=u"\u20B9" + str(
            balance[0][0]), font="Helvetica 12 bold", pady=8, padx=45, borderwidth=2, relief="solid").grid(row=0, column=3)

    records_data = getData("SELECT *,oid FROM records WHERE opposite_party like ? or type like ? or category like ? or date_of_transaction like ?",
                           (query, query, query, query,))

    if len(records_data) == 0:
        Label(searched_records, text="No such records found", font="Helvetica 12 bold",
              bg='#FFE4C4', height=2, relief="solid", padx=300).grid(row=1, column=0, columnspan=7)
        Label(searched_records, text="", bg='#FFE4C4',
              height=2).grid(row=2, column=0)

    else:
        labelsForRecords(searched_records)

        x = 0
        for i in range(0, len(records_data)):
            x += 1
            for j in range(8):
                if(j == 4):
                    continue
                if(j == 3):
                    Label(searched_records, text=u"\u20B9" + str(
                        records_data[i][j]), font="Helvetica 11", bg='#FFE4C4', width=15, height=2, relief="solid").grid(row=i+2, column=j)
                    continue
                Label(searched_records, text=str(records_data[i][j]), font="Helvetica 11",
                      bg='#FFE4C4', width=15, height=2, relief="solid").grid(row=i+2, column=j, pady=2)
            edit_id = records_data[i][8]
            Button(searched_records, text="Delete", command=lambda i=edit_id: [searched_records.destroy(
            ), deleteRecord(i)], relief="solid", padx=10, pady=8, height=1).grid(row=i+2, column=8)

        Label(searched_records, text="", bg='#FFE4C4',
              height=2).grid(row=x+2, column=0)
    Button(searched_records, text="Back", font="Helvetica 12 bold", borderwidth=2, relief="solid",
           pady=6, padx=10,  command=lambda: [searched_records.destroy(), displayRecords()]).grid(row=0,  column=0, pady=20)
    Button(searched_records, text="home", font="Helvetica 12 bold", borderwidth=2, relief="solid",
           pady=6, padx=10,  command=lambda: [searched_records.destroy()]).grid(row=0,  column=6, pady=20)


def deleteRecord(id):

    record = getData(
        (" SELECT current_balance,oid FROM records ORDER BY oid DESC LIMIT 1"))

    delete_balance = getData(
        "SELECT type,amount FROM records WHERE oid = ?", (id,))

    if delete_balance[0][0] == "Debit":

        final_balance = float(record[0][0]) - float(delete_balance[0][1])
    else:
        final_balance = float(record[0][0]) + float(delete_balance[0][1])

    writeData("UPDATE records SET current_balance = ? WHERE oid = ?",
              (final_balance, record[0][1],))

    writeData("DELETE FROM records WHERE oid = ?", (id,))


def displayRecords():

    records_data = getData("SELECT *,oid FROM records")

    balance = getData(
        " SELECT current_balance FROM records ORDER BY oid DESC LIMIT 1")

    global records
    records = Toplevel()
    setWindowBackground(records)
    global search

    search_key = StringVar()

    search = Entry(records, width=40, borderwidth=2,
                   textvariable=search_key, relief="solid")

    search.insert(0, "Search here")
    search.grid(row=0, column=6, columnspan=2, pady=20,  ipady=8)
    search_button = Button(records, text="Search", font="Helvetica 12 bold", command=lambda: searchedRecords(
        search_key), pady=6, borderwidth=2, relief="solid")
    search_button.grid(row=0, column=8, columnspan=1, pady=20, padx=0)

    if(balance != []):
        Label(records, text="Current Balance: ", font="Helvetica 12 bold",
              pady=8, padx=2, borderwidth=2, relief="solid").grid(row=0, column=2)
        Label(records, text=u"\u20B9" + str(balance[0][0]), font="Helvetica 12 bold",
              pady=8, padx=45, borderwidth=2, relief="solid").grid(row=0, column=3)

    labelsForRecords(records)

    x = 0
    for i in range(0, len(records_data)):
        x += 1
        for j in range(8):
            if(j == 4):
                continue
            if(j == 3):
                Label(records, text=u"\u20B9" + str(records_data[i][j]), font="Helvetica 11",
                      bg='#FFE4C4', width=15, height=2, relief="solid").grid(row=i+2, column=j)
                continue
            if (j == 6):
                Label(records, text=str(records_data[i][j]), font="Helvetica 11",
                      bg='#FFE4C4', width=15, height=2, relief="solid").grid(row=i+2, column=j)
                continue
            Label(records, text=str(records_data[i][j]), font="Helvetica 11",
                  bg='#FFE4C4', width=15, height=2, relief="solid").grid(row=i+2, column=j)

        edit_id = records_data[i][8]
        Button(records, text="Delete", command=lambda i=edit_id: [records.destroy(), deleteRecord(
            i)], relief="solid", padx=10, pady=8, height=1).grid(row=i+2, column=8, pady=2)
    Label(records, text="", bg='#FFE4C4', height=2).grid(row=x+2, column=0)

    Button(records, text="Back", font="Helvetica 12 bold", borderwidth=2, relief="solid",
                         pady=6, padx=10,  command=lambda: [records.destroy()]).grid(row=0,  column=0)


def getRecordsForMonth(month):
    if month == "current":
        start_day = date.today().replace(day=1)
        dates = calendar.monthrange(
            int(start_day.year), int(start_day.month))
        last_day = date.today().replace(day=dates[1])
    else:
        last_day = date.today().replace(day=1) - timedelta(days=1)
        start_day = date.today().replace(day=1) - timedelta(days=last_day.day)

    first_date = str(start_day.strftime("%m/%d/%y")).lstrip("0")
    last_date = str(last_day.strftime("%m/%d/%y")).lstrip("0")

    records = getData("SELECT amount, category FROM records WHERE type = ? AND date_of_transaction BETWEEN ? AND ?",
                      ("Credit", first_date, last_date,))

    records_dict = {}

    for record in records:
        if record[1] not in records_dict:
            records_dict[record[1]] = float(record[0])
        else:
            records_dict[record[1]] = float(
                records_dict[record[1]]) + float(record[0])

    return records_dict


def displayChart():

    chart = Toplevel()
    chart.geometry('800x381')
    setWindowBackground(chart)

    prev_dict = getRecordsForMonth("previous")

    curr_dict = getRecordsForMonth('current')

    prev_label = prev_dict.keys()
    prev_expense = prev_dict.values()

    curr_label = curr_dict.keys()
    curr_expense = curr_dict.values()

    fig = plt.figure(figsize=(15, 10))

    ax1 = fig.add_axes([0, .2, .5, .5], aspect=1)
    ax1.pie(prev_expense, labels=prev_label, radius=1.2, autopct='%1.2f%%')
    ax2 = fig.add_axes([.5, .2, .5, .5], aspect=1)
    ax2.pie(curr_expense, labels=curr_label, radius=1.2, autopct='%1.2f%%')
    ax1.set_title('Previous Month', pad=40)
    ax2.set_title('Current Month', pad=40)

    fig.patch.set_facecolor('#FFE4C4')

    canvas = FigureCanvasTkAgg(fig, master=chart)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, chart)
    toolbar.update()
    canvas.get_tk_widget().pack()


type_ = StringVar()
category_ = StringVar()

type_label = Label(root, text="TYPE:", font="Helvetica 12 bold italic",
                   pady=10, padx=20, bg='#FFE4C4').grid(row=0, column=0)
opposite_party_label = Label(root, text="OPPOSITE PARTY:", font="Helvetica 12 bold italic",
                             pady=10, padx=20, bg='#FFE4C4').grid(row=1, column=0)
date_of_transaction_label = Label(root, text="DATE OF TRANSACTION:",
                                  font="Helvetica 12 bold italic", pady=10, padx=20, bg='#FFE4C4').grid(row=2, column=0)
amount_label = Label(root, text="AMOUNT:", font="Helvetica 12 bold italic",
                     pady=10, padx=20, bg='#FFE4C4').grid(row=3, column=0)
reason_label = Label(root, text="REASON:", font="Helvetica 12 bold italic",
                     pady=20, padx=20, bg='#FFE4C4').grid(row=4, column=0)
category_label = Label(root, text="CATEGORY:", font="Helvetica 12 bold italic",
                       pady=10, padx=20, bg='#FFE4C4').grid(row=5, column=0)

type_debit = Radiobutton(root, text="DEBIT", font="Helvetica 11 bold",
                         value="Debit", variable=type_, bg='#FFE4C4')
type_credit = Radiobutton(root, text="CREDIT", font="Helvetica 11 bold",
                          value="Credit", variable=type_, bg='#FFE4C4')


opposite_party = Entry(root, width=32, borderwidth=5)
date_of_transaction = DateEntry(root, width=30, borderwidth=5)
amount = Entry(root, width=32, borderwidth=5)
reason = Text(root, width=25, borderwidth=5, height=3)
category = ttk.Combobox(root, width=31, textvariable=category_)
category["values"] = ("Food", "Home expense", "Loan",
                      "Work expense", "Miscellaneous", "-")

type_credit.grid(row=0, column=1)
type_debit.grid(row=0, column=2)
opposite_party.grid(row=1, column=1)
date_of_transaction.grid(row=2, column=1)
amount.grid(row=3, column=1)
reason.grid(row=4, column=1)
category.grid(row=5, column=1)


submitRecord = Button(root, text="Submit Record", font="Helvetica 11 bold", borderwidth=2,
                      relief="solid", command=submitRecord).grid(row=6, column=0,  pady=5, padx=10)
displayRecordss = Button(root, text="Show Records", font="Helvetica 11 bold", borderwidth=2,
                         relief="solid", command=displayRecords).grid(row=6, column=1,  pady=5, padx=10)
displayChart = Button(root, text="Expense Chart", font="Helvetica 11 bold", borderwidth=2,
                      relief="solid", command=displayChart).grid(row=6, column=2,  pady=5, padx=10)


root.mainloop()

from tkinter import * 
import sqlite3
from tkcalendar import DateEntry
import datetime
from tkinter import ttk
from matplotlib import pyplot as plt
import numpy as np
from datetime import date, timedelta
import calendar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

root =Tk()
root.geometry('600x330')
root.configure(background='#FFE4C4')
root.title('Hisaab')

# conn = sqlite3.connect('hisaab.db')
# c= conn.cursor()
# c.execute("DELETE FROM records")
# conn.commit()
# conn.close()

# conn = sqlite3.connect('hisaab.db')
# c= conn.cursor()

# c.execute("""CREATE TABLE records(
# 			type text,
# 			opposite_party text,
# 			date_of_transaction text,			
# 			amount real,
# 			current_balance real,
# 			date_of_entry text,
# 			Reason text null,
# 			Category text 
# 			) """)

# conn.commit()
# conn.close()


def submit():
	conn = sqlite3.connect('hisaab.db')
	c= conn.cursor()

	c.execute(" SELECT current_balance FROM records ORDER BY oid DESC LIMIT 1")
	balance = c.fetchall()
	if balance == []:
		cur_balance = amount.get()  
	else:
		t = type_.get()
		print(t)
		if t == "debit":
			cur_balance = float(balance[0][0])+ float(amount.get()) 
			print("db: ", cur_balance)

		else:
			cur_balance = float(balance[0][0]) - float(amount.get()) 	
			print("cb: ", cur_balance)

	date = datetime.date.today()


	c.execute(" INSERT INTO records VALUES (:type, :opposite_party, :date_of_transaction, :amount, :current_balance,:date_of_entry, :reason, :category) ",
				{
					"type": type_.get(),
					"opposite_party": opposite_party.get(),
					"date_of_transaction": date_of_transaction.get(),
					"date_of_entry":date.strftime("%m/%d/%y"),   
					"amount": amount.get(),
					"current_balance": cur_balance,
					"reason": reason.get("1.0",END),
					"category": category_.get()
				})

	conn.commit()
	conn.close()
# OR type = search_key OR reason = search_key OR category = search_key
def search_func(search_key):
	print("Hiiiii")
	conn = sqlite3.connect('hisaab.db')
	c= conn.cursor()
	
	records.destroy()

	query = str(search_key.get())
	print("abc:",query)


	c.execute("SELECT * FROM records WHERE opposite_party like ? or type like ? or category like ? or date_of_transaction like ?", (query,query,query,query,))
	records_data = c.fetchall()
	print(records_data)

	global searched_records
	searched_records = Toplevel()

	type_head = Label(searched_records, text="Type").grid(row = 1, column =0)
	party_head = Label(searched_records, text="party").grid(row = 1, column =1)
	dateTransaction_head = Label(searched_records, text="Date of Transaction").grid(row = 1, column =2)	
	amount_head = Label(searched_records, text="Amount").grid(row = 1, column =3)
	currentBalance_head = Label(searched_records, text="Current balance").grid(row = 1, column =4)
	dateEntry_head = Label(searched_records, text="Date of Entry").grid(row = 1, column =5)
	reason_head = Label(searched_records, text="Reason").grid(row = 1, column =6, columnspan= 1)
	category_head = Label(searched_records, text="Category").grid(row = 1, column =7, columnspan= 1)

	for i in range(0, len(records_data)):
		for j in range(8):
			Label(searched_records, text=records_data[i][j]).grid(row= i+2,column = j)


	back_button = Button(searched_records, text = "Back", command = lambda: [show_record(), searched_records.destroy()]).grid(row = 10,  column = 0)
	home_button = Button(searched_records, text = "Home", command = lambda: [searched_records.destroy()]).grid(row = 10,  column = 1)

	conn.commit()
	conn.close()


def delete_func(id):
	conn = sqlite3.connect('hisaab.db')
	c= conn.cursor()

	c.execute(" SELECT current_balance,oid FROM records ORDER BY oid DESC LIMIT 1")
	record = c.fetchall()
	print(record[0])

	c.execute("SELECT type,amount FROM records WHERE oid = ?",(id,))
	delete_balance = c.fetchall()
	print(delete_balance[0])

	if delete_balance[0][0] == "debit":
		final_balance = float(record[0][0]) - float(delete_balance[0][1])
	else:
		final_balance = float(record[0][0]) + float(delete_balance[0][1])

	c.execute("UPDATE records SET current_balance = ? WHERE oid = ?",(final_balance,record[0][1],))

	c.execute("DELETE FROM records WHERE oid = ?",(id,))

	# c.execute("DELETE FROM records")
	conn.commit()
	conn.close()
	print(id)

def show_record():
	conn = sqlite3.connect('hisaab.db')
	c= conn.cursor()
 	
	c.execute("SELECT *,oid FROM records")
	records_data = c.fetchall()
	print(records_data)


	c.execute(" SELECT current_balance FROM records ORDER BY oid DESC LIMIT 1")
	balance = c.fetchall()



	global records
	records = Toplevel()

	records.configure(background='#FFE4C4')

	global search

	search_key = StringVar()
	search = Entry(records, width = 20, borderwidth = 5, textvariable = search_key)
	print(search_key.get())
	search.insert(0, "Search here")
	search.grid(row=0, column=0)
	search_button = Button(records, text = "Search", command = lambda: search_func(search_key))
	search_button.grid(row =0, column = 1)

	if(balance != []):
		Label(records, text= "Current Balance: ").grid(row=0,column=2)
		curr_bal = Label(records, text = balance[0][0]).grid(row=0, column=3)

	type_head = Label(records, text="Type",font = "Helvetica 12 bold", bg = '#FFE4C4',relief = "solid", width = 13, padx = 4).grid(row = 1, column =0)
	party_head = Label(records, text="party",font = "Helvetica 12 bold", bg = '#FFE4C4',relief = "solid", width = 13, padx = 4).grid(row = 1, column =1)
	dateTransaction_head = Label(records, text="Transaction Date",font = "Helvetica 12 bold", bg = '#FFE4C4',relief = "solid", width = 13, padx = 4).grid(row = 1, column =2)	
	amount_head = Label(records, text="Amount",font = "Helvetica 12 bold", bg = '#FFE4C4',relief = "solid", width = 13, padx = 4).grid(row = 1, column =3)
	currentBalance_head = Label(records, text="Current balance",font = "Helvetica 12 bold ", bg = '#FFE4C4',relief = "solid", width = 13, padx = 4).grid(row = 1, column =4)
	dateEntry_head = Label(records, text="Date of Entry",font = "Helvetica 12 bold ", bg = '#FFE4C4',relief = "solid", width = 13, padx = 4).grid(row = 1, column =5)
	reason_head = Label(records, text="Reason",font = "Helvetica 12 bold ", bg = '#FFE4C4',relief = "solid", width = 13, padx = 4).grid(row = 1, column =6, columnspan= 1)
	category_head = Label(records, text="Category",font = "Helvetica 12 bold ", bg = '#FFE4C4',relief = "solid", width = 13, padx = 4).grid(row = 1, column =7, columnspan= 1)

	
	for i in range(0, len(records_data)):
		for j in range(8):
			Label(records, text=records_data[i][j],font = "Helvetica 11", bg = '#FFE4C4', width = 15, height = 2 ,relief = "solid").grid(row= i+2, column = j )
		print(records_data[i][8])
		edit_id = records_data[i][8]
		Button(records, text="Delete", command = lambda i=edit_id:[records.destroy() ,delete_func(i)], relief = "solid" ,padx =10, pady =8, height= 1).grid(row = i+2, column = 8)
			




	back_button = Button(records, text = "Back", command = lambda: [records.destroy()]).grid(row = 0,  column = 8)

	conn.commit()
	conn.close()


def show_chart():

	chart = Toplevel()
	chart.geometry('800x381')

	last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
	start_day_of_prev_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)

	prev_first_date = str(start_day_of_prev_month.strftime("%m/%d/%y"))
	prev_last_date = str(last_day_of_prev_month.strftime("%m/%d/%y"))
	prev_first_date = prev_first_date.lstrip("0")
	prev_last_date = prev_last_date.lstrip("0")


	start_day_of_curr_month = date.today().replace(day=1) 
	dates = calendar.monthrange(int(start_day_of_curr_month.year),int(start_day_of_curr_month.month))
	last_day_of_curr_month = date.today().replace(day=dates[1])

	curr_first_date = str(start_day_of_curr_month.strftime("%m/%d/%y"))
	curr_last_date = str(last_day_of_curr_month.strftime("%m/%d/%y"))
	curr_first_date = curr_first_date.lstrip("0")
	curr_last_date = curr_last_date.lstrip("0")

	conn = sqlite3.connect('hisaab.db')
	c= conn.cursor()
	
	c.execute("SELECT amount, category FROM records WHERE type = ? AND date_of_transaction BETWEEN ? AND ?",("credit",prev_first_date ,prev_last_date,))
	prev_records = c.fetchall()
	print(prev_records)

	c.execute("SELECT amount, category FROM records WHERE type = ? AND date_of_transaction BETWEEN ? AND ?",("credit",curr_first_date ,curr_last_date,))
	curr_records = c.fetchall()
	print(curr_records)

	conn.commit()
	conn.close()

	prev_dict = {}

	for record in prev_records:
		if record[1] not in prev_dict:
			prev_dict[record[1]] = float(record[0])
		else:
			prev_dict[record[1]]  = float(prev_dict[record[1]]) + float(record[0]) 

	print(prev_dict)

	curr_dict = {}

	for record in curr_records:
		if record[1] not in curr_dict:
			curr_dict[record[1]] = float(record[0])
		else:
			curr_dict[record[1]]  = float(curr_dict[record[1]]) + float(record[0]) 

	print(curr_dict)

	prev_label = prev_dict.keys()
	prev_expense = prev_dict.values()

	curr_label = curr_dict.keys()
	curr_expense = curr_dict.values()

	fig = plt.figure(figsize = (15,10))

	ax1 = fig.add_axes([0, .2, .5, .5], aspect=1)
	ax1.pie(prev_expense, labels=prev_label, radius = 1.2,autopct='%1.2f%%')
	ax2 = fig.add_axes([.5, .2, .5, .5], aspect=1)
	ax2.pie(curr_expense, labels=curr_label, radius = 1.2,autopct='%1.2f%%')
	ax1.set_title('Previous Month',pad = 40)
	ax2.set_title('Current Month', pad = 40)

	canvas = FigureCanvasTkAgg(fig,master = chart)
	canvas.draw()
	canvas.get_tk_widget().pack()
	toolbar = NavigationToolbar2Tk(canvas,chart)
	toolbar.update()
	canvas.get_tk_widget().pack()





type_ = StringVar()
category_ = StringVar()

type_label = Label(root, text= "TYPE:",font = "Helvetica 12 bold italic" ,pady = 10 , padx = 20, bg = '#FFE4C4').grid(row=0, column =0)
opposite_party_label = Label(root, text= "OPPOSITE PARTY:",font = "Helvetica 12 bold italic" , pady = 10, padx = 20,bg = '#FFE4C4').grid(row=1, column =0) 
date_of_transaction_label = Label(root, text= "DATE OF TRANSACTION:",font = "Helvetica 12 bold italic" ,pady=10,padx = 20, bg = '#FFE4C4').grid(row=2, column =0) 
amount_label = Label(root, text= "AMOUNT:",font = "Helvetica 12 bold italic" , pady = 10,padx = 20, bg = '#FFE4C4').grid(row=3, column =0) 
reason_label = Label(root, text= "REASON:",font = "Helvetica 12 bold italic" , pady = 20,padx = 20, bg = '#FFE4C4').grid(row=4, column =0)
category_label = Label(root, text= "CATEGORY:",font = "Helvetica 12 bold italic" , pady = 10,padx = 20, bg = '#FFE4C4').grid(row=5, column =0)

type_debit = Radiobutton(root, text="DEBIT",font = "Helvetica 11 bold" , value="debit", variable=type_ , bg = '#FFE4C4')
type_credit = Radiobutton(root, text="CREDIT",font = "Helvetica 11 bold" , value="credit", variable=type_ , bg = '#FFE4C4')

opposite_party = Entry(root, width = 32, borderwidth = 5)
date_of_transaction = DateEntry(root, width = 30, borderwidth = 5)
amount = Entry(root, width = 32, borderwidth = 5)
reason = Text(root, width = 25, borderwidth = 5, height = 3)
category = ttk.Combobox(root, width= 31, textvariable= category_)
category["values"] = ("Food","Home expense","Loan","Work expense","Miscellaneous","-")

type_credit.grid(row=0, column=1)
type_debit.grid(row=0, column=2)
opposite_party.grid(row=1,column=1)
date_of_transaction.grid(row=2,column=1)
amount.grid(row=3,column=1)
reason.grid(row=4,column=1)
category.grid(row=5, column =1)




submit = Button(root, text = "Submit an entry",font = "Helvetica 10 bold", command = submit).grid(row=6, column=0,  pady = 5, padx = 10)
show_records = Button(root, text = "Show records",font = "Helvetica 10 bold", command = show_record).grid(row = 6, column =1,  pady = 5, padx = 10)
show_chart = Button(root, text = "Show chart",font = "Helvetica 10 bold", command = show_chart).grid(row = 6, column =2,  pady = 5, padx=10)






root.mainloop()
from tkinter import * 
import sqlite3
from tkcalendar import DateEntry
import datetime
from tkinter import ttk
root =Tk()

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

type_ = StringVar()
category_ = StringVar()

type_label = Label(root, text= "Type:").grid(row=0, column =0)
opposite_party_label = Label(root, text= "opposite Party: ").grid(row=1, column =0) 
date_of_transaction_label = Label(root, text= "date of transaction: ").grid(row=2, column =0) 
amount_label = Label(root, text= "Amount : ").grid(row=3, column =0) 
reason_label = Label(root, text= "Reason : ").grid(row=4, column =0)
category_label = Label(root, text= "Category: ").grid(row=5, column =0)

#type_ = Entry(root,  width = 35, borderwidth = 5)
type_debit = Radiobutton(root, text="Debit", value="debit", variable=type_)
type_credit = Radiobutton(root, text="Credit", value="credit", variable=type_)

opposite_party = Entry(root, width = 35, borderwidth = 5)
date_of_transaction = DateEntry(root, width = 35, borderwidth = 5)
amount = Entry(root, width = 35, borderwidth = 5)
reason = Text(root, width = 35, borderwidth = 5, height = 3)
category = ttk.Combobox(root, width= 35, textvariable= category_)
category["values"] = ("Food","Home expense","Loan","Work expense","Miscellaneous","-")

type_credit.grid(row=0, column=1)
type_debit.grid(row=0, column=2)
opposite_party.grid(row=1,column=1)
date_of_transaction.grid(row=2,column=1)
amount.grid(row=3,column=1)
reason.grid(row=4,column=1)
category.grid(row=5, column =1)

opposite_party.insert(0,"Enter the opposite party name")
amount.insert(0,"Enter the amount of transaction")

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



def show_record():
	conn = sqlite3.connect('hisaab.db')
	c= conn.cursor()
 	
	c.execute("SELECT * FROM records")
	records_data = c.fetchall()

	# if(searched_records != null):
	# 	searched_records.destroy()

	global records
	records = Toplevel()

	global search
	search_key = StringVar()
	search = Entry(records, width = 35, borderwidth = 5, textvariable = search_key)
	print(search_key.get())
	search.insert(0, "Search here")
	search.grid(row=0, column=0)
	

	search_button = Button(records, text = "Search", command = lambda: search_func(search_key))
	search_button.grid(row =0, column = 1)

	type_head = Label(records, text="Type").grid(row = 1, column =0)
	party_head = Label(records, text="party").grid(row = 1, column =1)
	dateTransaction_head = Label(records, text="Date of Transaction").grid(row = 1, column =2)	
	amount_head = Label(records, text="Amount").grid(row = 1, column =3)
	currentBalance_head = Label(records, text="Current balance").grid(row = 1, column =4)
	dateEntry_head = Label(records, text="Date of Entry").grid(row = 1, column =5)
	reason_head = Label(records, text="Reason").grid(row = 1, column =6, columnspan= 1)
	category_head = Label(records, text="Category").grid(row = 1, column =7, columnspan= 1)

	
	for i in range(0, len(records_data)):
		for j in range(8):
			Label(records, text=records_data[i][j]).grid(row= i+2,column = j)

			






	conn.commit()
	conn.close()



submit = Button(root, text = "Submit an entry", command = submit).grid(row=6, column=0, columnspan=2)
show_records = Button(root, text = "Show records", command = show_record).grid(row = 7, column =0, columnspan =2)









root.mainloop()
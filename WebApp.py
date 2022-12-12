import json
import tkinter as tk
import pandas as pd
import requests
import mysql.connector

customer_df=pd.read_csv('customers.csv')

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.ResultsFrame = None
        self.SearchFrame = None
        self.master=master

        self.col_names = customer_df.columns
        self.entry_boxes=list(self.col_names)
        self.create_widgets()

    def create_widgets(self):
        self.SearchFrame=tk.Frame(master=self.master)
        self.SearchFrame.grid(row=1, column=1)
        for i in range(len(self.col_names)):
            self.desc_label=tk.Label(master=self.SearchFrame, text=self.col_names[i])
            self.desc_label.grid(row=i, column=1)
            self.entry_boxes[i]=tk.Entry(master=self.SearchFrame)
            self.entry_boxes[i].grid(row=i, column=2)
        self.ButtonFrame=tk.Frame(master=self.master)
        self.search_button=tk.Button(master=self.ButtonFrame, text='Search', command=self.search_for_customer)
        self.search_button.grid(row=1, column=1)
        self.add_customer_button=tk.Button(master=self.ButtonFrame, text='Add Customer', command=self.add_customer)
        self.add_customer_button.grid(row=1, column=2)
        self.ButtonFrame.grid(row=2, column=1)
        self.ResultsFrame=tk.Frame(master=self.master)
        self.ResultsFrame.grid(row=3, column=1)
        self.label2=tk.Label(master=self.ResultsFrame, text='')
        self.label2.grid(row=1, column=1)

    def search_for_customer(self):
        parameters=dict(zip(self.col_names, [None]*len(self.col_names)))
        for i in range(len(self.col_names)):
            parameters[self.col_names[i]]=self.entry_boxes[i].get()
            self.entry_boxes[i].delete(0, 'end')
        #search_df=customer_df
        sql='SELECT * FROM customer_data'
        for val in parameters.keys():
            if parameters[val]:
                if len(sql)==27:
                    sql+=f' WHERE {val}=\'{parameters[val]}\''
                else:
                    sql+=f' AND {val}=\'{parameters[val]}\''
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='customers'
        )
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(sql)
        if self.mycursor.rowcount ==0:
            self.no_results_text = tk.Label(master=self.ResultsFrame, text='No Results Found')
            self.no_results_text.grid(row=1, column=1)
        else:
            self.search_results=self.mycursor.fetchall()
            for j in range(len(self.col_names)):
                self.label=tk.Label(master=self.ResultsFrame, text=self.col_names[j])
                self.label.grid(row=0, column=j)
            for i in range(min(self.mycursor.rowcount, 10)):
                for j in range(len(self.col_names)):
                    self.label=tk.Label(master=self.ResultsFrame, text=self.search_results[i][j])
                    self.label.grid(row=i+1, column=j)
        self.mydb.close()
        #        search_df=search_df[search_df[val]==parameters[val]]
        #self.ResultsFrame.destroy()
        #self.ResultsFrame=tk.Frame(master=self.master)
        #if search_df.shape[0]==0:
        #    self.no_results_text=tk.Label(master=self.ResultsFrame, text='No Results Found')
        #    self.no_results_text.grid(row=1, column=1)
        #else:
        #    for i in range(len(self.col_names)):
        #        self.label=tk.Label(master=self.ResultsFrame, text=self.col_names[i])
        #        self.label.grid(row=1, column=i)
        #self.ResultsFrame.grid(row=3, column=1)

    def add_customer(self):
        send={}
        for i in range(len(self.col_names)):
            send[self.col_names[i]]=self.entry_boxes[i]
        try:
            post_customer=requests.post('http://127.0.0.1:5000/submit', json=send)
        except:
            print('Oh No!')


window=tk.Tk()
window.title('Customer Information')
webapp=Application(window)
window.mainloop()
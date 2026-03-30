from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from db_helper import fetch_query, execute_query

class SupplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ all variables --------------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        
        
        #---------- Search Frame -------------
        lbl_search=Label(self.root,text="Invoice No.",bg="white",font=("goudy old style",15))
        lbl_search.place(x=700,y=80)

        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=850,y=80,width=160)
        btn_search=Button(self.root,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=980,y=79,width=100,height=28)

        #-------------- title ---------------
        title=Label(self.root,text="Supplier Details",font=("goudy old style",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40)

        #-------------- content ---------------
        #---------- row 1 ----------------
        lbl_supplier_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=50,y=80)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=180,y=80,width=180)
        
        #---------- row 2 ----------------
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=180,y=120,width=180)
        
        #---------- row 3 ----------------
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=180,y=160,width=180)
        
        #---------- row 4 ----------------
        lbl_desc=Label(self.root,text="Description",font=("goudy old style",15),bg="white").place(x=50,y=200)
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_desc.place(x=180,y=200,width=470,height=120)
        
        #-------------- buttons -----------------
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=370,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=370,width=110,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=370,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=370,width=110,height=35)

        #------------ supplier details -------------
        sup_frame=Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=700,y=120,width=380,height=350)

        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)\
        
        self.SupplierTable=ttk.Treeview(sup_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
        self.SupplierTable.heading("invoice",text="Invoice")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("desc",text="Description")
        self.SupplierTable["show"]="headings"
        self.SupplierTable.column("invoice",width=90)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.column("desc",width=100)
        
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
#-----------------------------------------------------------------------------------------------------

    def add(self):
        try:
            # 1. Validation with Early Return
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
                return  # Stop the function here if there is an error

            # 2. Check if the Invoice already exists using our helper
            check_query = "SELECT * FROM supplier WHERE invoice=?"
            existing_supplier = fetch_query(check_query, (self.var_sup_invoice.get(),))

            if existing_supplier: # If the helper returns data, the invoice is a duplicate
                messagebox.showerror("Error", "Invoice no. is already assigned", parent=self.root)
                return  # Stop the function here

            # 3. Insert the new supplier using our helper
            insert_query = "INSERT INTO supplier (invoice, name, contact, desc) VALUES (?,?,?,?)"
            insert_values = (
                self.var_sup_invoice.get(),
                self.var_name.get(),
                self.var_contact.get(),
                self.txt_desc.get('1.0', END)
            )

            # Execute the query (this automatically commits and closes the connection)
            execute_query(insert_query, insert_values)

            # 4. Success UI Updates
            messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
            self.clear()
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def show(self):
        try:
            fetch_all_query = "SELECT * FROM supplier"
            rows = fetch_query(fetch_all_query)

            self.SupplierTable.delete(*self.SupplierTable.get_children())

            for row in rows:
                self.SupplierTable.insert('', 'end', values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])

    def update(self):
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
                return

            check_query = "SELECT * FROM supplier WHERE invoice=?"
            existing_supplier = fetch_query(check_query, (self.var_sup_invoice.get(),))

            if not existing_supplier:
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                return

            update_query = "UPDATE supplier SET name=?, contact=?, desc=? WHERE invoice=?"
            update_values = (
                self.var_name.get(),
                self.var_contact.get(),
                self.txt_desc.get('1.0', END),
                self.var_sup_invoice.get()
            )

            execute_query(update_query, update_values)

            messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def delete(self):
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
                return

            check_query = "SELECT * FROM supplier WHERE invoice=?"
            existing_supplier = fetch_query(check_query, (self.var_sup_invoice.get(),))

            if not existing_supplier:
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                return

            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
            if op == True:
                delete_query = "DELETE FROM supplier WHERE invoice=?"
                execute_query(delete_query, (self.var_sup_invoice.get(),))

                messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent=self.root)
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Invoice No. should be required", parent=self.root)
                return

            search_query = "SELECT * FROM supplier WHERE invoice=?"
            rows = fetch_query(search_query, (self.var_searchtxt.get(),))

            if not rows:
                messagebox.showerror("Error", "No record found!!!", parent=self.root)
                return

            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)



if __name__=="__main__":
    root=Tk()
    obj=SupplierClass(root)
    root.mainloop()
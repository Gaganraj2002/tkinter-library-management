from tkinter import *
from tkinter import ttk
from tkinter import simpledialog, filedialog, messagebox as mb
from datetime import datetime, timedelta


class Library:
    def __init__(self, books):
        self.books = books

    def show_avail_books(self):
        lst = []
        for book, details in self.books.items():
            if details["borrower"] is None:
                lst.append(book)
        return lst

    def lend_book(self, requested_book, name):
        if self.books[requested_book]["borrower"] is None:
            self.books[requested_book]["borrower"] = name
            due_date = datetime.now() + timedelta(days=7)
            self.books[requested_book]["due_date"] = due_date.strftime("%m/%d/%Y")
            st = f"{requested_book} has been marked as 'Borrowed' by: {name} due on {self.books[requested_book]['due_date']}"
            lst = [st, True]
            return lst
        else:
            st = f'Sorry, the {requested_book} is currently on loan to: {self.books[requested_book]["borrower"]}'
            lst = [st, False]
            return lst

    def return_book(self, returned_book):
        st = ""
        if self.books[returned_book]["borrower"] is not None:
            borrower = self.books[returned_book]["borrower"]
            due_date = datetime.strptime(
                self.books[returned_book]["due_date"], "%m/%d/%Y"
            ).date()
            self.books[returned_book]["borrower"] = None
            self.books[returned_book]["due_date"] = None
            st = f"Thanks for returning {returned_book}, {borrower}!"
            # Check if the book was returned after the due date
            if datetime.now().date() > due_date:
                days_late = (datetime.now().date() - due_date).days
                penalty = days_late * 1  # Penalty fee of $1 per day late
                st = f"You returned the book {days_late} days late, and have been charged a penalty of ${penalty}."
        else:
            st = f"{returned_book} is already available in the library"
        return st


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x300")
        self.btn_frame = Frame(self)
        self.main_frame = Frame(self)
        self.btn_frame.place(relx=0, rely=0, relheight=1, relwidth=0.4)
        self.main_frame.place(relx=0.4, rely=0, relheight=1, relwidth=0.6)
        self.create_all_widgets()
        books = {
            "The Last Battle": {"borrower": None, "due_date": None},
            "The Hunger Games": {"borrower": None, "due_date": None},
            "Cracking the Coding Interview": {"borrower": None, "due_date": None},
        }
        self.library = Library(books)
        self.student_example = Student("Saksham", self.library)

    def btns_place(self):
        self.disp_btn.pack()
        self.borrow_btn.pack()
        self.ret_btn.pack()
        self.renew_btn.pack()
        self.view_btn.pack()
        self.exit_btn.pack()

    def create_all_widgets(self):
        self.lbl = Label(self.main_frame)
        self.listbox = Listbox(self.main_frame)
        self.combo_box = ttk.Combobox(self.main_frame)
        self.main_btn = Button(self.main_frame, text="Borrow")
        self.create_btns(self.btn_frame)

    def create_btns(self, top):
        self.disp_btn = Button(top, text="Display Available Books")
        self.disp_btn["command"] = self.displaybooks
        self.borrow_btn = Button(top, text="Borrow a Book")
        self.borrow_btn["command"] = self.borrow_book
        self.ret_btn = Button(top, text="Return a Book")
        self.ret_btn["command"] = self.return_books
        self.renew_btn = Button(top, text="Renew a Book")
        self.renew_btn["command"] = self.renew_books
        self.view_btn = Button(top, text="View Your Books")
        self.view_btn["command"] = self.view_brwd
        self.exit_btn = Button(top, text="Exit")
        self.exit_btn["command"] = exit
        self.btns_place()

    def borrow_book(self):
        self.clear()
        self.combo_box["values"] = self.library.show_avail_books()
        if self.library.show_avail_books() != []:
            self.combo_box.current(0)
        self.main_btn["command"] = self.brw_btn_call
        self.combo_box.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        self.main_btn.place(relx=0.45, rely=0.1)

    def brw_btn_call(self):
        st = self.student_example.request_book(self.combo_box.get())
        mb.showinfo("Borrow", st)
        self.view_brwd()

    def clear(self):
        for widgets in self.main_frame.winfo_children():
            widgets.place_forget()

    def return_books(self):
        self.clear()
        self.combo_box["values"] = self.student_example.view_borrowed()
        if self.student_example.view_borrowed() != []:
            self.combo_box.current(0)
        self.main_btn["text"] = "Return Book"
        self.main_btn["command"] = self.return_books_call
        self.combo_box.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        self.main_btn.place(relx=0.45, rely=0.1)

    def return_books_call(self):
        book = self.combo_box.get().split("(")[0].strip()
        st = self.student_example.return_book(book)
        mb.showinfo("Return", st)
        self.view_brwd()

    def renew_books(self):
        self.clear()
        self.combo_box["values"] = self.student_example.view_borrowed()
        if self.student_example.view_borrowed() != []:
            self.combo_box.current(0)
        self.main_btn["text"] = "Renew Book"
        self.main_btn["command"] = self.renew_books_call
        self.combo_box.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        self.main_btn.place(relx=0.45, rely=0.1)

    def renew_books_call(self):
        book = self.combo_box.get().split("(")[0].strip()
        st = self.student_example.renew_book(book)
        mb.showinfo("Renew", st)
        self.view_brwd()

    def displaybooks(self):
        self.clear()
        count = 0
        self.listbox.delete(0, END)
        for i in self.library.show_avail_books():
            self.listbox.insert(count, i)
            count += 1
        self.listbox.place(relx=0, rely=0, relheight=1, relwidth=1)

    def view_brwd(self):
        self.clear()
        count = 0
        self.listbox.delete(0, END)
        for i in self.student_example.view_borrowed():
            self.listbox.insert(count, i)
            count += 1
        self.listbox.place(relx=0, rely=0, relheight=1, relwidth=1)


class Student:
    def __init__(self, name, library):
        self.name = name
        self.books = []
        self.library = library

    def view_borrowed(self):
        if not self.books:
            return ["None"]
        else:
            lst1 = []
            for book in self.books:
                st = f'{book} (due on {self.library.books[book]["due_date"]})'
                lst1.append(st)
            return lst1

    def request_book(self, book):
        try:
            ans = self.library.lend_book(book, self.name)
            if ans[1]:
                self.books.append(book)
                return ans[0]
            else:
                return ans[0]
        except Exception as e:
            pass

    def return_book(self, book):
        if book in self.books:
            msg = self.library.return_book(book)
            self.books.remove(book)
            return msg
        else:
            return "You haven't borrowed that book."

    def renew_book(self, book):
        st = ""
        if book in self.books:
            if self.library.books[book]["borrower"] == self.name:
                due_date = datetime.strptime(
                    self.library.books[book]["due_date"], "%m/%d/%Y"
                ).date()
                if datetime.now().date() <= due_date:
                    new_due_date = due_date + timedelta(days=7)
                    self.library.books[book]["due_date"] = new_due_date.strftime(
                        "%m/%d/%Y"
                    )
                    st = f"{book} has been renewed and is now due on {self.library.books[book]['due_date']}"
                else:
                    st = f"Sorry, you cannot renew {book} as it is already overdue."
            else:
                st = f"Sorry, {book} is currently borrowed by someone else."
        else:
            st = "You haven't borrowed that book, try another..."
        return st


if __name__ == "__main__":
    app = App()
    app.mainloop()

import json
from datetime import datetime

class Book:
    def __init__(self, id, title, author, isbn):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_barrower = False

    def to_dic(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'is_barrower': self.is_barrower
        }    
    
    @classmethod
    def from_dic(cls, data):
        book = cls(data['id'], data['title'], data['author'], data['isbn'])
        book.is_barrower = data.get('is_barrower', False)
        return book


class Member:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.barrower_books = []


    def to_dic(self):
        return {
            'id': self.id,
            'name': self.name,
            'barrower_books': self.barrower_books
        }    
    
    @classmethod
    def from_dic(cls, data):
        member = cls(data['id'], data['name'])
        member.barrower_books = data.get("barrower_books", [])
        return member



class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.load_book_from_json()
        self.load_member_from_json()

    def add_book(self, id, title, author, isbn):
        self.books.append(Book(id=id, title=title, author=author, isbn=isbn))
        print(f"{title} book has been successfully added to the book list.\n")

    def show_books(self):
        if not self.books:
            print('No books avaliable.\n')
            return
        
        for i, book in enumerate(self.books, start=1):
            print(f"{i}. {book.title} by {book.author} (ID: {book.id})")  

    def remove_book(self):
        if not self.books:
            print("Not books avaliable.\n")        
            return
        
        for i , book in enumerate(self.books, start=1):
            print(f"{i}. {book.title} - {book.author} - ID: {book.id}")

        try:
            del_book = input('Enter ID of the book remove: ').strip()
            removed_book = None

            for book in self.books:
                if str(book.id) == del_book:
                    removed_book = book  
                    break
            if removed_book:
                self.books.remove(removed_book)
                print(f"{removed_book.title} has been removed.")
            else:
                raise ValueError("Invalid ID")
        except ValueError:
            print("please enter a valid Id")

        self.save_book_to_json()  

    def barrow_book(self):

        if not self.books:
            print("No books available.\n")
            return
        if not self.members:
            print("No members registraion.\n")
            return
        self.show_books()
        book_title = input("enter the title of the book to borrow: ").strip()

        selected_book = None
        for book in self.books:
            if book.title.lower() == book_title.lower():
                selected_book = book
                break

        if not selected_book:
            print("book not found.")
            return
        if selected_book.is_barrower:
            print("this book is already barrowed.")
            return

        self.show_members()
        member_id = input('enter the member id who want to barrow the book: ').strip()

        selected_member = None
        for member in self.members:
            if str(member.id) == member_id:
                selected_member = member
                break
        if not selected_book:
            print("member not found.")
            return
        
        selected_book.is_barrower = True
        selected_member.barrower_books.append({
            'book_id': selected_book.id,
            'barrowed_at': datetime.now().isoformat()
        })
        
        print(f"{selected_member.name} successfully barrowed '{selected_book.title}'.")

        self.save_book_to_json()
        self.save_member_to_json()


    def show_barrowed_books(self):
        if not self.members:
            print("no members registered.\n")
            return
        
        any_barrowed = False
        for member in self.members:
            if not member.barrower_books:
                continue

            print(f"{member.name} - {member.id} has barrowed: ")

            for i in member.barrower_books:
                book_id = i.get('book_id')
                barrowed_at = i.get('barrowed_at')

            book = next((b for b in self.books if str(b.id) == str(book_id)), None)

            if book:
                print(f"-{book.title} by {book.author} -- Barrowed at: {barrowed_at}")
                any_barrowed =True
            else:
                print(f"- Book with ID {book_id} not found in current book list.\n")

        if not any_barrowed:
            print("No books have been barrowed yet.\n")            


    def regestration_member(self, id, name):
        self.members.append(Member(id=id, name=name))
        print(f"{name} was added to the member list.\n")
        self.save_member_to_json()

   
    def show_members(self):
        if not self.members:
            print('the member list is empty.\n')
            return
        for i,member in enumerate(self.members, start=1):
            print(f"{i}. {member.name} - ID:{member.id}")

    def remove_member(self):
        # if not self.members:
        #     print("the members list is empty.")
        #     return
        
        # # for i, member in enumerate(self.members, start=1):
        # #     print(f"{i}. {member.name} (ID: {member.id})")
        self.show_members()

        try:
            del_id = input("Enter the ID of the member to remove:  ").strip()
            member_to_remove = None

            for member in self.members:
                if str(member.id) == del_id:
                    member_to_remove = member
                    break
            if member_to_remove:
                self.members.remove(member_to_remove)
                print(f"{member_to_remove.name} has been removed.")
            else:
                raise ValueError("Invalid ID")
        except ValueError:
            print("Please enter a valid ID.")            
                    
        self.save_member_to_json()


# ========================== save data to json =====================================================

    def save_book_to_json(self, filename='library/library_data_book.json'):
        with open(filename, 'w') as file:
            json.dump([book.to_dic() for book in self.books], file) 

    def load_book_from_json(self, filename='library/library_data_book.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            self.books = [Book.from_dic(i) for i in data]    
        except FileNotFoundError:
            self.books = []

    def save_member_to_json(self, filename="library/library_data_member.json"):
        with open(filename, 'w') as file:
            json.dump([member.to_dic() for member in self.members], file)

   
        
    def load_member_from_json(self, filename="library/library_data_member.json"):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            self.members = [Member.from_dic(i) for i in data]
        except FileNotFoundError:
            self.members = []
              
        

        







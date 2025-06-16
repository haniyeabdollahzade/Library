from library import Library

def main():
    library = Library()

    while True:
        print("===== menue =====")
        print("1.add book")
        print("2.new member registration")
        print("3.show all books")
        print("4.show all members")
        print("5.remove member")
        print("6.remove book")
        print("7.borrwe book ")
        print("8.show barrowed books")
        print("9.Search Book")
        print("10. Search Member")
        print("0.exit")
        print("=====================================")


        choice = input("select item: ")

        if choice == '1':
            id = input('enter the bookId: ')
            title = input('enter the book title: ')
            author = input('enter the book author: ')
            isbn = input('enter the book isbn: ')

            library.add_book(id, title, author, isbn)
            library.save_book_to_json()

        elif choice == '2':
            id = input('enter the memberId: ')
            name = input('enter the memner name: ')
            library.regestration_member(id, name)
            library.save_member_to_json()

        elif choice == '3':
            library.show_books()

        elif choice == '4':
            library.show_members()   

        elif choice == '5':
            library.remove_member() 
            library.save_member_to_json()

        elif choice == '6':
            library.remove_book()
            library.save_book_to_json()   

        elif choice == '7':
            library.barrow_book()
            library.save_book_to_json() 

        elif choice == '8':
            library.show_barrowed_books()
            library.save_book_to_json()  

        elif choice == '9':
            library.search_book()

        elif choice == '10':
            library.search_member()    

        elif choice == '0':
            
            print('exit')
            break

        else:
            raise ValueError("Invalid choice")

if __name__ == "__main__"  :
    main()           

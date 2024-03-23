from classes import AddressBook, Record
from interfaceclases import ColorBot, TableBot, StandardBot
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  
    

#DECORATORS
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name, phone and/or birthday please."
        except KeyError:
            return "Enter user name"
        except IndexError:
            return "Enter user name"
    return inner


#MAIN FUNCTIONS
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book:AddressBook,bt:ColorBot):
    name, phone = args
    
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(book, phone)
    display = 'Contact added'
    return bt.format_display(display)

    
@input_error
def change_contact(args, book:AddressBook, bt:ColorBot):
    name, phone_old, phone_new = args
    record = book.find(name)
    record.edit_phone(book, phone_old, phone_new)
    display = 'Contact changed'
    return bot.format_display(display)


@input_error 
def show_all(args, book:AddressBook, bt:ColorBot):
    return bt.return_all_users(book)


@input_error
def get_contact(args, book:AddressBook, bt:ColorBot):
    name = args[0]
    record = book.find(name)
    display = record.phone_list()
    return bt.format_display(display)

@input_error
def del_contact(args, book:AddressBook, bt:ColorBot):
    name, phone = args
    record = book.find(name)
    record.remove_phone(phone)
    display = 'Phone deleted'
    return bt.format_display(display)


@input_error
def get_birthday(args, book:AddressBook, bt:ColorBot):
    name = args[0]
    record = book.find(name)
    display = record.birthday
    return bt.format_display(display)


@input_error
def add_birthday(args, book:AddressBook, bt:ColorBot):
    name, date = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birth(date)
    display = 'Birthday added'
    return bt.format_display(display)

@input_error
def to_congratulate(args, book:AddressBook, bt:ColorBot):
    return bt.birthdays_congratulate(book.get_upcoming_birthdays())

@input_error
def bot_selection(args, book:AddressBook, bt:ColorBot):
    bot_type = args
    global bot
    if bot_type[0] == "1":
        bot = ColorBot()
    elif bot_type[0] == "2":
        bot = TableBot()
    else:
        bot = StandardBot()
    return bot



def main():
    global bot
    bot = StandardBot()
    book = load_data()
    print(f"Welcome to the assistant bot! \n For RED bot - input 'bot 1' \nFor TABLE bot - input 'bot 2'; \nFor STANDARD bot - any other input")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "bot":
            print(bot_selection(args, book, bot)) 
        elif command == "add":
            print(add_contact(args, book, bot))
        elif command == "change":
            print(change_contact(args, book, bot))    
        elif command == "all":
            print(show_all(args, book, bot))  
        elif command == "phone":
            print(get_contact(args, book, bot))  
        elif command == "delete":
            print(del_contact(args, book, bot))   
        elif command == "add-birthday":
            print(add_birthday(args, book, bot))  
        elif command == "show-birthday":
            print(get_birthday(args, book, bot))
        elif command == "birthdays":
            print(to_congratulate(args, book, bot))


        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
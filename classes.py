from collections import UserDict
import datetime
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.value = value


class Birthday(Field):
        def __init__(self, value):
            try:
                date = datetime.strptime(value, "%d.%m.%Y").date()
                super().__init__(date)
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Phone(Field):

    def __init__(self, value):
        if not self.check_phone(value):
            raise ValueError("Not 10 digits") 
        super().__init__(value)

    def check_phone(self, value):
        return len(value) == 10 and value.isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, book, value):
        number=Phone(value) 
        if number.check_phone(value):
            self.phones.append(number)
        else:
            book.dell_record(self.name)


    def add_birth(self, value):
        date=Birthday(value)
        self.birthday = date 
        return self.birthday


    def remove_phone(self, value):
            for p in self.phones:
                if value==str(p):
                    self.phones.pop(self.phones.index(p))

    def edit_phone(self,book, old_num,new_num):
        if self.find_phone(old_num):
            self.remove_phone(old_num)
            self.add_phone(book, new_num)
        else:
            raise ValueError("Whong phone number")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
            
    def phone_list(self):
        phone_items=''
        for i in self.phones:
            phone_items = phone_items + f'{i}, '
        return phone_items.rstrip(', ')

        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
    

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def dell_record(self,record):
        del self.data[record.name.value]

    
    def find(self, name):
        return self.data.get(name)


    def __str__(self):
        contacts = ''

        for el in self.data:
            contacts = contacts + f'{self.find(el)}\n'
        return contacts.rstrip('\n')
    
    def get_upcoming_birthdays(self):
        birth_list=[]
        for i in self.data:
            birth_dict = {}
            birth_dict['name'] = i
            birthday_date = str(self.find(i).birthday)
            birth_dict['birthday'] = str(birthday_date)
            birth_list.append(birth_dict)
        
        upcoming_birthdays=[]
        for user in birth_list:
            birthday = user["birthday"]

            if str(birthday) == 'None':            
                continue

            bir = datetime.strptime(str(birthday), '%Y-%m-%d').date()
            today = datetime.today().date()
            curr_birthday = datetime(today.year, bir.month, bir.day).date()

            diff = curr_birthday - today

            if diff <= timedelta(days=6) and diff>= timedelta(days=0):
                if curr_birthday.weekday() == 5:
                    curr_birthday = curr_birthday + timedelta(days=2)
                if curr_birthday.weekday() == 6:
                    curr_birthday = curr_birthday + timedelta(days=1)

                cong_date_str = curr_birthday.strftime("%Y-%m-%d")

                to_congratulate = {"name": user["name"], "congratulation_date": cong_date_str}
                upcoming_birthdays.append(to_congratulate.copy())
        return upcoming_birthdays

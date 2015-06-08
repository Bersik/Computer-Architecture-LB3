__author__ = 'Bersik'

from string import lower
from client import Client

global client_

def menu():
    global client_
    client_ = Client()
    while True:
        print "Menu:"
        print "1. Add student"
        print "2. Show student by id"
        print "3. Show all students"
        print "4. Edit student by id"
        print "5. Delete student by id"
        print "6. Clear"
        print "   Exit"

        selected = raw_input()
        if (not selected.isdigit()) or (not (1 <= int(selected) <= 6)):
            break

        selected = int(selected)

        if selected == 1:
            add()
        elif selected == 2:
            read()
        elif selected == 3:
            read_all()
        elif selected == 4:
            edit()
        elif selected == 5:
            remove()
        else:
            clear()

        print "\n"


def read_text_field(name_field):
    while True:
        value = raw_input("\t %s: " % name_field)
        if value == "" or value.isspace():
            print "Error! Please repeat."
        else:
            return value


def read_int_field(name_field):
    while True:
        value = raw_input("\t %s: " % name_field)
        if value.isdigit():
            return value
        print "Error! Please repeat."


def read_text_field_update(name_field, b_value):
    while True:
        value = raw_input("\t %s(%s): " % (name_field, b_value))
        if value == "" or value.isspace():
            return b_value
        else:
            return value


def read_int_field_update(name_field, b_value):
    while True:
        value = raw_input("\t %s(%s): " % (name_field, str(b_value)))
        if value == "" or value.isspace():
            return b_value
        elif value.isdigit():
            return value
        print "Error! Please repeat."



def read_student():
    print "Enter the field of student:"
    name = read_text_field("Name")
    surname = read_text_field("Surname")
    age = read_int_field("Age")
    group = read_text_field("Group")
    hostel = read_int_field("Hostel")
    room = read_int_field("Room")
    return client_.create_student(name, surname, age, group, hostel, room)


def read_id():
    print "Enter student id"
    return read_int_field("id")


def print_title():
    print "ID".ljust(5), "NAME".ljust(20), "SURNAME".ljust(20), \
        "AGE".ljust(15), "GROUP".ljust(15), "HOSTEL".ljust(10), \
        "ROOM".ljust(10)


def print_student(student):
    print str(student._idn).ljust(5), student.name.ljust(20), student.surname.ljust(20), \
        str(student.age).ljust(15), student.group.ljust(15), str(student.hostel).ljust(10), \
        str(student.room).ljust(10)


def print_students(students):
    for student in students:
        print_student(student)


def add():
    idn = client_.add(read_student())
    if idn:
        print "Added! id=%d" % idn
    else:
        print "Append error!"


def read():
    student = client_.read(read_id())
    if student:
        print_title()
        print_student(student)
    else:
        print "Read error!"


def read_all():
    students = client_.read_all()
    if students:
        print_title()
        print_students(students)
    else:
        print "Empty!"


def edit():
    idn = read_id()
    student = client_.read(idn)
    if student:
        print "Enter the new field of student:"
        name = read_text_field_update("Name", student.name)
        surname = read_text_field_update("Surname", student.surname)
        age = read_int_field_update("Age", student.age)
        group = read_text_field_update("Group", student.group)
        hostel = read_int_field_update("Hostel", student.hostel)
        room = read_int_field_update("Room", student.room)
        student = client_.create_student(name, surname, age, group, hostel, room)
        client_.update(idn, student)
        print "Changed!"
    else:
        print "Edit error!"


def remove():
    if client_.remove(read_id()):
        print "Deleted!"
    else:
        print "Delete error!"


def clear():
    yn = raw_input("You seriously? (y/N)\n")
    if lower(yn) == "y":
        if client_.clear():
            print "Cleared!"


if __name__ == '__main__':
    menu()

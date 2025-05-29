# main.py

from sqlalchemy import or_
from models.contacts import Contact, Base
from db.connection import engine, session
import time

# Create the table
Base.metadata.create_all(engine)

# Creating helper functions to manage the data
def search_contacts():
    keyword = input("Search by name, phone, or email: ").strip()
    if not keyword:
        print("Search term cannot be empty.")
        return

    results = session.query(Contact).filter(
        or_(
            Contact.name.ilike(f'%{keyword}%'),
            Contact.phone.ilike(f'%{keyword}%'),
            Contact.email.ilike(f'%{keyword}%')
        )
    ).all()

    if results:
        for c in results:
            fav = "★" if c.is_favorite else " "
            print(f"{c.id}. {c.name} - {c.phone} - {c.email or 'No email'} {fav}")
    else:
        print("No matching contacts found.")

def edit_contact():
    try:
        contact_id = int(input("Enter contact ID to edit: "))
    except ValueError:
        print("Invalid ID.")
        return

    contact = session.query(Contact).get(contact_id)
    if not contact:
        print("Contact not found.")
        return

    name = input(f"New name [{contact.name}]: ").strip() or contact.name
    phone = input(f"New phone [{contact.phone}]: ").strip() or contact.phone
    email = input(f"New email [{contact.email or 'None'}]: ").strip() or contact.email

    contact.name = name
    contact.phone = phone
    contact.email = email

    session.commit()
    print("Contact updated successfully.")

def toggle_favorite():
    try:
        contact_id = int(input("Enter contact ID to toggle favorite: "))
    except ValueError:
        print("Invalid ID.")
        return

    contact = session.query(Contact).get(contact_id)
    if not contact:
        print("Contact not found.")
        return

    contact.is_favorite = not contact.is_favorite
    session.commit()

    time.sleep(2)
    status = "added to" if contact.is_favorite else "removed from"
    print(f"{contact.name} has been {status} favorites.")

def run_cli():
    time.sleep(2)
    while True:
        print('\nContact Management CLI')
        print('1. Add new contact')
        print('2. View all contacts')
        print('3. Delete all contacts')
        print('4. Search contacts')
        print('5. Edit a contact')
        print('6. Mark/unmark favorite')
        print('q. Quit')

        option = input('Choose an option: ').strip().lower()

        if option == '1':
            name = input('Name: ').strip()
            phone = input('Phone: ').strip()
            email = input('Email (optional): ').strip() or None

            if not name or not phone:
                print("Name and phone are required.")
                continue

            contact = Contact(name=name, phone=phone, email=email)
            session.add(contact)
            session.commit()
            print(f"Saved contact: {contact}")

        elif option == '2':
            contacts = session.query(Contact).all()
            if contacts:
                for c in contacts:
                    print(f"{c.id}. {c.name} - {c.phone} - {c.email or 'No email'}")
            else:
                print("No contacts found.")

        elif option == '3':
            confirm = input("Are you sure you want to delete all contacts? (y/n): ").strip().lower()
            if confirm == 'y':
                session.query(Contact).delete()
                session.commit()
                print("All contacts deleted.")
        elif option == '4':
            search_contacts()
        elif option == '5':
            edit_contact()
        elif option == '6':
            toggle_favorite()

        elif option == 'q':
            print("Exiting CLI.")
            break

        else:
            print("Invalid option. Try again.")
            

if __name__ == '__main__':
    run_cli()
    
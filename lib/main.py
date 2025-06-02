# main.py

from datetime import datetime
import time
from sqlalchemy import or_
from models.calls import Call
from models.contacts import Contact, Base
from db.connection import engine, session
from models.messages import Message

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

def log_message():
    try:
        contact_id = int(input("Enter contact ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    contact = session.get(Contact, contact_id)
    if not contact:
        print("Contact not found.")
        return

    content = input("Enter message content: ").strip()
    if not content:
        print("Message can't be empty.")
        return

    direction = input("Is this message Sent or Received? (s/r): ").strip().lower()
    if direction not in ['s', 'r']:
        print("Invalid input. Use 's' for sent, 'r' for received.")
        return

    is_sent = direction == 's'
    message = Message(content=content, is_sent=is_sent, contact=contact)
    session.add(message)
    session.commit()

    print("Message logged.")

def view_conversation():
    try:
        contact_id = int(input("Enter contact ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    contact = session.query(Contact).get(contact_id)
    if not contact:
        print("Contact not found.")
        return

    print(f"\nConversation with {contact.name}:")
    for msg in contact.messages:
        direction = "You" if msg.is_sent else contact.name
        print(f"{direction}: {msg.content}") 
        
def search_messages():
    keyword = input("Enter keyword to search messages: ").strip()
    if not keyword:
        print("Keyword can't be empty.")
        return

    messages = session.query(Message).filter(Message.content.ilike(f"%{keyword}%")).all()
    if not messages:
        print("No messages found.")
        return

    for msg in messages:
        direction = "Sent" if msg.is_sent else "Received"
        print(f"[{msg.contact.name}] {direction}: {msg.content}")
    
def log_call():
    try:
        contact_id = int(input("Enter contact ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    contact = session.get(Contact, contact_id)
    if not contact:
        print("Contact not found.")
        return

    print("Call type options: incoming / outgoing / missed")
    call_type = input("Enter call type: ").strip().lower()
    if call_type not in ['incoming', 'outgoing', 'missed']:
        print("Invalid call type.")
        return

    # Optional: custom timestamp
    date_input = input("Enter date and time (YYYY-MM-DD HH:MM) or press Enter for now: ").strip()
    if date_input:
        try:
            timestamp = datetime.strptime(date_input, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date format.")
            return
    else:
        timestamp = datetime.utcnow()

    call = Call(contact=contact, call_type=call_type, timestamp=timestamp)
    session.add(call)
    session.commit()
    print("Call logged.")

def filter_calls():
    print("Filter by:")
    print("1. Type (incoming/outgoing/missed)")
    print("2. Date (YYYY-MM-DD)")

    choice = input("Choose filter: ").strip()
    if choice == '1':
        call_type = input("Enter call type: ").strip().lower()
        if call_type not in ['incoming', 'outgoing', 'missed']:
            print("Invalid type.")
            return
        calls = session.query(Call).filter(Call.call_type == call_type).all()
    elif choice == '2':
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format.")
            return
        calls = session.query(Call).filter(
            Call.timestamp >= datetime.combine(date_obj, datetime.min.time()),
            Call.timestamp <= datetime.combine(date_obj, datetime.max.time())
        ).all()
    else:
        print("Invalid choice.")
        return

    if not calls:
        print("No matching call logs found.")
        return

    for call in calls:
        print(f"[{call.timestamp.strftime('%Y-%m-%d %H:%M')}] {call.call_type.capitalize()} - {call.contact.name}")


def view_call_history():
    choice = input("View calls for a contact? (y/n): ").strip().lower()
    if choice == 'y':
        try:
            contact_id = int(input("Enter contact ID: "))
        except ValueError:
            print("Invalid ID.")
            return

        contact = session.get(Contact, contact_id)
        if not contact:
            print("Contact not found.")
            return

        calls = contact.calls
    else:
        calls = session.query(Call).order_by(Call.timestamp.desc()).all()

    if not calls:
        print("No call logs found.")
        return

    for call in calls:
        print(f"[{call.timestamp.strftime('%Y-%m-%d %H:%M')}] {call.call_type.capitalize()} - {call.contact.name}")

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
        print('7. Log a message')
        print('8. View conversation by contact')
        print('9. Search messages')
        print('10. Log a call')
        print('11. View call history')
        print('12. Filter calls')
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
        elif option == '7':
            log_message()
        elif option == '8':
            view_conversation()
        elif option == '9':
            search_messages()
        elif option == '10':
            log_call()
        elif option == '11':
            view_call_history()
        elif option == '12':
            filter_calls()
        elif option == 'q':
            print("Exiting CLI.")
            break

        else:
            print("Invalid option. Try again.")
            

if __name__ == '__main__':
    run_cli()
    
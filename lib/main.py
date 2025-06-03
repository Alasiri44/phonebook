# main.py

from datetime import datetime
import time
from sqlalchemy import or_
from models.calls import Call
from models.contacts import Contact, Base
from db.connection import engine, session
from models.messages import Message
from rich.console import Console

# Create the table
Base.metadata.create_all(engine)

console = Console()

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
        console.print('[bold green]------------------------------------------ [/bold green]')
        for c in results:
            fav = "★" if c.is_favorite else " "
            print(f"{c.id}. {c.name} - {c.phone} - {c.email or 'No email'} {fav}")
        console.print('[bold green]------------------------------------------ [/bold green]')
    else:
        console.print('[bold red]------------------------------------------ [/bold red]')
        print("No matching contacts found.")
        console.print('[bold red]------------------------------------------ [/bold red]')

def edit_contact():
    try:
        contact_id = int(input("Enter contact ID to edit: "))
    except ValueError:
        console.print('[bold red]------------------------------------------ [/bold red]')
        print("Invalid ID.")
        console.print('[bold red]------------------------------------------ [/bold red]')
        return

    contact = session.query(Contact).get(contact_id)
    if not contact:
        console.print('[bold red]------------------------------------------ [/bold red]')
        print("Contact not found.")
        console.print('[bold red]------------------------------------------ [/bold red]')
        return

    name = input(f"New name [{contact.name}]: ").strip() or contact.name
    phone = input(f"New phone [{contact.phone}]: ").strip() or contact.phone
    email = input(f"New email [{contact.email or 'None'}]: ").strip() or contact.email

    contact.name = name
    contact.phone = phone
    contact.email = email

    session.commit()
    console.print('[bold green]------------------------------------------ [/bold green]')
    print("Contact updated successfully.")
    console.print('[bold green]------------------------------------------ [/bold green]')

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
        console.print('[bold red]------------------------------------------ [/bold red]')
        print("Message can't be empty.")
        console.print('[bold red]------------------------------------------ [/bold red]')
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
        console.print('[bold red]------------------------------------------ [/bold red]')
        print("Invalid ID.")
        console.print('[bold red]------------------------------------------ [/bold red]')
        return

    contact = session.get(Contact, contact_id)
    if not contact:
        print("Contact not found.")
        return

    console.print('[bold green]------------------------------------------ [/bold green]')
    print(f"\nConversation with {contact.name}:")
    for msg in contact.messages:
        direction = "You" if msg.is_sent else contact.name
        print(f"{direction}: {msg.content}") 
    console.print('[bold green]------------------------------------------ [/bold green]')
        
def search_messages():
    keyword = input("Enter keyword to search messages: ").strip()
    if not keyword:
        console.print('[bold red]------------------------------------------ [/bold red]')
        print("Keyword can't be empty.")
        console.print('[bold red]------------------------------------------ [/bold red]')
        return

    messages = session.query(Message).filter(Message.content.ilike(f"%{keyword}%")).all()
    if not messages:
        console.print('[bold red]------------------------------------------ [/bold red]')
        print("No messages found.")
        console.print('[bold red]------------------------------------------ [/bold red]')
        return
    
    console.print('[bold green]------------------------------------------ [/bold green]')
    for msg in messages:
        direction = "Sent" if msg.is_sent else "Received"
        print(f"[{msg.contact.name}] {direction}: {msg.content}")
    console.print('[bold green]------------------------------------------ [/bold green]')
    
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
        console.print('[bold red]------------------------------------------ [/bold red]')
        print("Invalid choice.")
        console.print('[bold red]------------------------------------------ [/bold red]')
        return

    if not calls:
        console.print('[bold red]------------------------------------------ [/bold red]')
        print("No matching call logs found.")
        console.print('[bold red]------------------------------------------ [/bold red]')
        return

    console.print('[bold green]------------------------------------------ [/bold green]')
    for call in calls:
        print(f"[{call.timestamp.strftime('%Y-%m-%d %H:%M')}] {call.call_type.capitalize()} - {call.contact.name}")
    console.print('[bold green]------------------------------------------ [/bold green]')


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
            console.print('[bold red]------------------------------------------ [/bold red]')
            print("Contact not found.")
            console.print('[bold red]------------------------------------------ [/bold red]')
            return

        calls = contact.calls
    else:
        calls = session.query(Call).order_by(Call.timestamp.desc()).all()

    if not calls:
        print("No call logs found.")
        return
    
    console.print('[bold green]------------------------------------------ [/bold green]')
    for call in calls:
        print(f"[{call.timestamp.strftime('%Y-%m-%d %H:%M')}] {call.call_type.capitalize()} - {call.contact.name}")
    console.print('[bold green]------------------------------------------ [/bold green]')


def run_cli():
    time.sleep(2)
    while True:
        console.print('\n[bold green]------- Contact Management CLI--------- [/bold green]')
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
        console.print('[bold green]------------------------------------------ [/bold green]')

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
            console.print('[bold green]------------------------------------------ [/bold green]')
            print(f"Saved contact: {contact}")
            console.print('[bold green]------------------------------------------ [/bold green]')

        elif option == '2':
            contacts = session.query(Contact).all()
            console.print('[bold green]------------------------------------------ [/bold green]')
            if contacts:
                for c in contacts:
                    print(f"{c.id}. {c.name} - {c.phone} - {c.email or 'No email'}")
                console.print('[bold green]------------------------------------------ [/bold green]')
            else:
                print("No contacts found.")

        elif option == '3':
            confirm = input("Are you sure you want to delete all contacts? (y/n): ").strip().lower()
            if confirm == 'y':
                session.query(Contact).delete()
                session.commit()
                console.print('[bold red]------------------------------------------ [/bold red]')
                print("All contacts deleted.")
                console.print('[bold red]------------------------------------------ [/bold red]')
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
    
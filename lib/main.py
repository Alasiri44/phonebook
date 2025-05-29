# main.py

from models.contacts import Contact, Base
from db.connection import engine, session

# Create the table
Base.metadata.create_all(engine)

def run_cli():
    while True:
        print('\nContact Management CLI')
        print('1. Add new contact')
        print('2. View all contacts')
        print('3. Delete all contacts')
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

        elif option == 'q':
            print("Exiting CLI.")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    run_cli()

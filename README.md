# 📱 Terminal Phonebook App

A terminal-based phonebook application built with Python and SQLAlchemy. This app lets you manage contacts, track call and message logs, organize contacts by tags, and interact with your data via a simple CLI interface.

---

## ✅ Features

### 📇 Contact Management
- [x] **Add Contact** – Add a new contact with name, phone, and optional email.
- [x] **View All Contacts** – Display a list of all saved contacts.
- [x] **Search Contacts** – Search by name, phone number, or email.
- [ ] **Edit Contact** – Update existing contact details.
- [ ] **Favorite Contacts** – Mark/unmark contacts as favorites.
- [ ] **Group/Tag Contacts** – Organize contacts by tags (e.g., Family, Work, Friends).

---

### 📞 Call Logs
- [ ] **Log Calls** – Save records of incoming, outgoing, or missed calls.
- [ ] **View Call History** – View call logs per contact or full history.
- [ ] **Filter Calls** – Filter logs by type or date.

---

### 💬 Message Logs
- [ ] **Log Messages** – Record sent and received messages.
- [ ] **View Messages** – View conversations by contact.
- [ ] **Search Messages** – Keyword-based message lookup.

---

### 💻 CLI Features
- [x] **Menu-based Interface** or use of commands like:
  ```bash
  python main.py add "Alice" "0712345678" --email "alice@mail.com"
  python main.py list
  python main.py search "Alice"

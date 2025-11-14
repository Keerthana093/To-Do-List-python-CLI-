📌 To Do List (Python CLI)

A simple and efficient **Command-Line Interface (CLI) To-Do List** application built using Python.
This project helps you manage tasks directly from the terminal with options to add, view, update, and delete tasks.
All data is stored locally in JSON files.

✨ Features

* ➕ **Add Tasks**
* 📋 **View Tasks**
* 🔄 **Update Tasks**
* ❌ **Delete Tasks**
* 📝 **Mark Tasks as Completed / Pending**
* 💾 **Persistent Storage using JSON**
* 🖥️ **Fully CLI-Based (Terminal Project)**

📁 Project Structure

```
ToDo-CLI/
│
├── todo.py            # Main CLI program
├── tasks.json         # Stores active/pending tasks
├── completed.json     # Stores completed tasks history
├── sss/               # Contains screenshots (optional folder)
└── README.md          # Documentation

```



🛠️ Installation

1. Make sure Python is installed on your system.
2. Clone this repository:

```
git clone <your-repo-link>
```

3. Navigate into the project folder:

```
cd project
```

▶️ How to Run

Run the CLI program:

```
python cli.py
```
📘 Usage

When you run the program, you will see a menu like this:

```
====== To-Do List Menu ======
1. Add a new task
2. Update a task
3. Delete a task
4. View all tasks
5. Mark task as complete
6. View completed tasks
7. Exit
=============================
```

Choose any option (1–7) to perform actions.

 🗂️ Data Files

This project stores tasks in JSON files:

* `tasks.json` → stores **pending tasks**
* `completed.json` → stores **completed tasks**

These files auto-update based on your actions.

📸 Screenshots

You can add screenshots like this:

```
![Screenshot](./screenshot.png)
```

🤝 Contributing

Feel free to contribute by opening issues or pull requests.

📜 License

This project is open-source and free to use.



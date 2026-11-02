"""todo.py - a tiny local task manager (CLI) with a menu and typed commands."""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


# ---------- storage ----------

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError) as e:
        print(f"! Could not read {DATA_FILE}: {e}")
        return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


# ---------- helpers ----------

def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def ask_int(prompt):
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        print("! Please type a number.")
        return None


def clean_arg(arg):
    """Strip whitespace and a matching pair of surrounding quotes."""
    arg = arg.strip()
    if len(arg) >= 2 and arg[0] == arg[-1] and arg[0] in ('"', "'"):
        arg = arg[1:-1].strip()
    return arg


def parse_id_arg(arg):
    """Return (ok, id_or_None). ok=False means arg was given but not an integer."""
    arg = arg.strip()
    if not arg:
        return True, None
    try:
        return True, int(arg)
    except ValueError:
        return False, None


# ---------- actions ----------

def add_task(tasks, title):
    title = clean_arg(title)
    if not title:
        print("! Empty description, nothing added.\n")
        return
    task = {
        "id": next_id(tasks),
        "title": title,
        "completed": False,
        "created": datetime.now().isoformat(timespec="seconds"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"+ Added #{task['id']}: {title}\n")


def action_add(tasks):
    add_task(tasks, input("Task description: "))


def action_list(tasks):
    if not tasks:
        print("(the list is empty)\n")
        return
    print()
    for t in tasks:
        mark = "x" if t["completed"] else " "
        print(f"  [{mark}] {t['id']:>3}  {t['title']}")
    done = sum(1 for t in tasks if t["completed"])
    print(f"\n  {done}/{len(tasks)} completed\n")


def action_done(tasks, task_id=None):
    if task_id is None:
        action_list(tasks)
        if not tasks:
            return
        task_id = ask_int("Task id to mark as completed: ")
        if task_id is None:
            return
    task = find_task(tasks, task_id)
    if not task:
        print(f"! No task with id {task_id}.\n")
        return
    if task["completed"]:
        print(f"= #{task['id']} is already completed.\n")
        return
    task["completed"] = True
    save_tasks(tasks)
    print(f"* Completed #{task['id']}: {task['title']}\n")


def action_undo(tasks, task_id=None):
    if task_id is None:
        action_list(tasks)
        if not tasks:
            return
        task_id = ask_int("Task id to reopen: ")
        if task_id is None:
            return
    task = find_task(tasks, task_id)
    if not task:
        print(f"! No task with id {task_id}.\n")
        return
    task["completed"] = False
    save_tasks(tasks)
    print(f"~ Reopened #{task['id']}: {task['title']}\n")


def action_delete(tasks, task_id=None):
    if task_id is None:
        action_list(tasks)
        if not tasks:
            return
        task_id = ask_int("Task id to delete: ")
        if task_id is None:
            return
    task = find_task(tasks, task_id)
    if not task:
        print(f"! No task with id {task_id}.\n")
        return
    confirm = input(f"Delete #{task['id']} '{task['title']}'? [y/N] ").strip().lower()
    if confirm != "y":
        print("Cancelled.\n")
        return
    tasks.remove(task)
    save_tasks(tasks)
    print(f"- Deleted #{task['id']}: {task['title']}\n")


# ---------- menu / command loop ----------

def print_menu():
    print("""
====================================
         LOCAL TASK MANAGER
====================================
  add / 1           Add a new item          
  list / 2          Show the list           
  done / 3          Mark item as completed 
  undo / 4          Mark item as not done  
  delete / 5        Delete an item          
  menu / ?          Show this menu         
  exit / 0          Quit                    

====================================""")


def parse_line(line):
    """Split 'cmd rest of line' -> (cmd_lower, rest)."""
    parts = line.strip().split(maxsplit=1)
    if not parts:
        return "", ""
    return parts[0].lower(), (parts[1] if len(parts) > 1 else "")


def main():
    tasks = load_tasks()
    print_menu()

    shortcuts = {"1": "add", "2": "list", "3": "done",
                 "4": "undo", "5": "delete", "0": "exit"}

    while True:
        try:
            line = input("todo> ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not line.strip():
            continue

        cmd, arg = parse_line(line)
        if cmd in shortcuts:                # numeric menu option
            cmd = shortcuts[cmd]

        if cmd == "add":
            if arg:
                add_task(tasks, arg)        # add Buy milk
            else:
                action_add(tasks)           # prompt for description

        elif cmd == "list":
            action_list(tasks)

        elif cmd in ("done", "complete", "d"):
            ok, task_id = parse_id_arg(arg)
            if not ok:
                print(f"! '{arg}' is not a valid task id.\n")
                continue
            action_done(tasks, task_id)

        elif cmd in ("undo", "reopen", "u"):
            ok, task_id = parse_id_arg(arg)
            if not ok:
                print(f"! '{arg}' is not a valid task id.\n")
                continue
            action_undo(tasks, task_id)

        elif cmd in ("delete", "del", "rm", "remove"):
            ok, task_id = parse_id_arg(arg)
            if not ok:
                print(f"! '{arg}' is not a valid task id.\n")
                continue
            action_delete(tasks, task_id)

        elif cmd in ("menu", "m", "?"):
            print_menu()

        elif cmd in ("exit", "quit", "q"):
            print("Bye!")
            break

        else:
            print(f"! Unknown command '{cmd}'. Type 'help' to see commands.\n")


if __name__ == "__main__":
    main()
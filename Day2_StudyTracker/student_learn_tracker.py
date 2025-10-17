import json
import os
import getpass
import hashlib
from datetime import datetime, timedelta

STUDENTS_FILE = "students.txt"
SESSIONS_FILE = "sessions.txt"
DATE_FORMAT = "%Y-%m-%d %H:%M"  # user input format for start/end


# ---------- utils ----------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_json_list(path):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("[]")
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_json_list(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def input_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Value required.")


def parse_datetime(s):
    try:
        return datetime.strptime(s, DATE_FORMAT)
    except ValueError:
        return None


# ---------- data managers ----------
class StudentManager:
    def __init__(self, path=STUDENTS_FILE):
        self.path = path
        self.students = load_json_list(path)

    def save(self):
        save_json_list(self.path, self.students)

    def find_by_username(self, username):
        for s in self.students:
            if s.get("username") == username:
                return s
        return None

    def register(self, username, name, age, student_class, password):
        if self.find_by_username(username):
            return False, "Username already exists."
        user = {
            "username": username,
            "name": name,
            "age": age,
            "class": student_class,
            "password_hash": hash_password(password),
            "subjects": []  # list of subject names
        }
        self.students.append(user)
        self.save()
        return True, "Registered successfully."

    def verify_login(self, username, password):
        user = self.find_by_username(username)
        if not user:
            return False, "User not found."
        if user.get("password_hash") != hash_password(password):
            return False, "Incorrect password."
        return True, user

    def update_profile(self, username, **fields):
        user = self.find_by_username(username)
        if not user:
            return False
        for k, v in fields.items():
            if k in ("name", "age", "class"):
                user[k] = v
        self.save()
        return True

    def add_subject(self, username, subject):
        user = self.find_by_username(username)
        if not user:
            return False
        if subject not in user["subjects"]:
            user["subjects"].append(subject)
            self.save()
        return True

    def remove_subject(self, username, subject):
        user = self.find_by_username(username)
        if not user:
            return False
        if subject in user["subjects"]:
            user["subjects"].remove(subject)
            self.save()
        return True


class SessionManager:
    def __init__(self, path=SESSIONS_FILE):
        self.path = path
        self.sessions = load_json_list(path)

    def save(self):
        save_json_list(self.path, self.sessions)

    def add_session(self, username, subject, start_dt, end_dt, break_minutes, focus_rating, notes):
        duration_min = int((end_dt - start_dt).total_seconds() / 60)
        effective_min = max(0, duration_min - int(break_minutes))
        session = {
            "id": f"s{len(self.sessions)+1}",
            "username": username,
            "subject": subject,
            "start": start_dt.strftime(DATE_FORMAT),
            "end": end_dt.strftime(DATE_FORMAT),
            "duration_min": duration_min,
            "break_min": int(break_minutes),
            "effective_min": effective_min,
            "focus_rating": int(focus_rating),
            "notes": notes
        }
        self.sessions.append(session)
        self.save()
        return session

    def get_user_sessions(self, username, date_from=None, date_to=None, subject=None):
        out = []
        for s in self.sessions:
            if s["username"] != username:
                continue
            dt = datetime.strptime(s["start"], DATE_FORMAT)
            ok = True
            if date_from and dt < date_from:
                ok = False
            if date_to and dt > date_to:
                ok = False
            if subject and s["subject"].lower() != subject.lower():
                ok = False
            if ok:
                out.append(s)
        return out


# ---------- CLI interaction ----------
def register_flow(student_mgr):
    print("\n--- Register ---")
    username = input_nonempty("Choose username (unique): ")
    name = input_nonempty("Full name: ")
    age = input_nonempty("Age: ")
    student_class = input_nonempty("Class (e.g., 10, BSc Year1): ")
    while True:
        password = getpass.getpass("Choose password: ")
        password2 = getpass.getpass("Confirm password: ")
        if password != password2:
            print("Passwords do not match. Try again.")
        elif len(password) < 4:
            print("Password too short. Use at least 4 characters.")
        else:
            break
    ok, msg = student_mgr.register(username, name, age, student_class, password)
    print(msg)


def login_flow(student_mgr):
    print("\n--- Login ---")
    username = input_nonempty("Username: ")
    password = getpass.getpass("Password: ")
    ok, res = student_mgr.verify_login(username, password)
    if not ok:
        print(res)
        return None
    print(f"Welcome back, {res['name']}!")
    return res["username"]


def profile_menu(student_mgr, username):
    while True:
        print("\nProfile Menu:")
        print(" 1. View profile")
        print(" 2. Edit name/age/class")
        print(" 3. Add subject")
        print(" 4. Remove subject")
        print(" 5. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            user = student_mgr.find_by_username(username)
            print(json.dumps(user, indent=2, ensure_ascii=False))
        elif choice == "2":
            name = input("New name (leave blank to skip): ").strip()
            age = input("New age (leave blank to skip): ").strip()
            student_class = input("New class (leave blank to skip): ").strip()
            updates = {}
            if name:
                updates["name"] = name
            if age:
                updates["age"] = age
            if student_class:
                updates["class"] = student_class
            if updates:
                student_mgr.update_profile(username, **updates)
                print("Profile updated.")
            else:
                print("No changes provided.")
        elif choice == "3":
            subj = input_nonempty("Subject name to add: ")
            student_mgr.add_subject(username, subj)
            print("Subject added.")
        elif choice == "4":
            subj = input_nonempty("Subject name to remove: ")
            student_mgr.remove_subject(username, subj)
            print("If existed, subject removed.")
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def add_session_flow(student_mgr, session_mgr, username):
    user = student_mgr.find_by_username(username)
    print("\n--- Add Study Session ---")
    # show existing subjects
    if user and user.get("subjects"):
        print("Your subjects:", ", ".join(user["subjects"]))
    subject = input_nonempty("Subject (type new or existing): ")
    # if new subject, add to user
    if subject not in user.get("subjects", []):
        student_mgr.add_subject(username, subject)
    while True:
        start_s = input_nonempty(f"Start time ({DATE_FORMAT}): ")
        start_dt = parse_datetime(start_s)
        if not start_dt:
            print("Invalid format. Try again.")
            continue
        end_s = input_nonempty(f"End time ({DATE_FORMAT}): ")
        end_dt = parse_datetime(end_s)
        if not end_dt:
            print("Invalid format. Try again.")
            continue
        if end_dt <= start_dt:
            print("End must be after start.")
            continue
        break
    break_min = input_nonempty("Break minutes during session (integer): ")
    focus = input_nonempty("Focus rating 1-5: ")
    notes = input("Notes (optional): ").strip()
    session = session_mgr.add_session(username, subject, start_dt, end_dt, break_min, focus, notes)
    print("Session saved:", session["id"])


def show_sessions_flow(session_mgr, username):
    print("\n--- Show Sessions ---")
    print("Options: 1) all 2) by date range 3) by subject")
    choice = input("Choose: ").strip()
    if choice == "1":
        sessions = session_mgr.get_user_sessions(username)
    elif choice == "2":
        from_s = input_nonempty("From date (YYYY-MM-DD) : ")
        to_s = input_nonempty("To date (YYYY-MM-DD) : ")
        try:
            dfrom = datetime.strptime(from_s + " 00:00", "%Y-%m-%d %H:%M")
            dto = datetime.strptime(to_s + " 23:59", "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid dates")
            return
        sessions = session_mgr.get_user_sessions(username, date_from=dfrom, date_to=dto)
    elif choice == "3":
        subj = input_nonempty("Subject name: ")
        sessions = session_mgr.get_user_sessions(username, subject=subj)
    else:
        print("Invalid choice.")
        return
    if not sessions:
        print("No sessions found.")
        return
    # pretty print
    for s in sessions:
        print("-" * 40)
        print(f"ID: {s['id']} | Subject: {s['subject']} | Start: {s['start']} | End: {s['end']}")
        print(f"Duration: {s['duration_min']} min | Break: {s['break_min']} min | Effective: {s['effective_min']} min")
        print(f"Focus: {s['focus_rating']} | Notes: {s['notes']}")


def user_dashboard(student_mgr, session_mgr, username):
    while True:
        print("\n=== User Dashboard ===")
        print(" 1. Add study session")
        print(" 2. Show sessions")
        print(" 3. Profile / subjects")
        print(" 4. Logout")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_session_flow(student_mgr, session_mgr, username)
        elif choice == "2":
            show_sessions_flow(session_mgr, username)
        elif choice == "3":
            profile_menu(student_mgr, username)
        elif choice == "4":
            print("Logging out.")
            break
        else:
            print("Invalid choice.")


def main_menu():
    student_mgr = StudentManager()
    session_mgr = SessionManager()
    print("=== Study Tracker CLI ===")
    while True:
        print("\nMain Menu:")
        print(" 1. Register")
        print(" 2. Login")
        print(" 3. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            register_flow(student_mgr)
        elif choice == "2":
            username = login_flow(student_mgr)
            if username:
                user_dashboard(student_mgr, session_mgr, username)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid. Choose 1/2/3.")


if __name__ == "__main__":
    main_menu()

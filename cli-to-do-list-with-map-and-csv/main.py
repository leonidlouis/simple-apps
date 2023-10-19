import argparse
import csv
import sys

class ToDo:
    def __init__(self, file_name=""):
        self.to_do = {}
        self.task_id = 0
        self.file_name = file_name

        if self.file_name:
            self.load_from_csv()

    def get_task_by_id(self, id):
        id = int(id)
        return self.to_do.get(id, None)

    def add(self, task_name):
        self.task_id +=1
        self.to_do[self.task_id] = {
            "id": self.task_id,
            "name": task_name,
            "is_done": False

        }
        return "Successfully Added"
    
    def load_from_csv(self):
        try:
            with open(self.file_name, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    task_id = int(row[0])
                    self.to_do[task_id] = {
                        "id": task_id,
                        "name": row[1],
                        "is_done": True if row[2].lower() == 'true' else False
                    }
                    self.task_id = max(self.task_id, task_id) # since we don't know the ordering of the csv
        except FileNotFoundError:
            print(f"File {self.file_name} is not found, skipping loading from csv")
            pass
    
    def mark_as_done(self, id):
        task = self.get_task_by_id(id)
        if task:
            task['is_done'] = True
            return f"Task of ID {id} is marked as done"
        
        return f"Task of ID {id} is not found"
    
    def delete(self, id):
        task = self.get_task_by_id(id)
        if task:
            del self.to_do[task['id']]
            return f"Task of ID {id} is deleted"
        
        return f"Task of ID {id} is not found"
    
    def update(self, id, task_name):
        task = self.get_task_by_id(id)

        if task:
            task['name'] = task_name
            return f"Task of ID {id} is updated"
        
        return f"Task of ID {id} is not found"

    def list(self):
        return list(self.to_do.values())

    def execute(self, command, should_write_to_file=False):
        parts = command.split()
        operation = parts[0]

        operation_map = {
            "add": self.add,
            "done": self.mark_as_done,
            "delete": self.delete,
            "update": self.update,
            "list": self.list,
        }

        if operation not in operation_map:
            return "Invalid Command"
        
        res = None
        if operation == "update":
            id = parts[1]
            task_name = ' '.join(parts[2:])
            res = operation_map[operation](id, task_name)
        
        if operation in ["list"]:
            res = operation_map[operation]()
        
        if operation in ["add", "done", "delete"]:
            value = ' '.join(parts[1:])
            res = operation_map[operation](value)

        if should_write_to_file and operation in ["add", "done", "delete", "update"]:
            self.save_to_csv()

        return res
    
    def save_to_csv(self):
        with open(self.file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "is_done"])  # header
            for task in self.to_do.values():
                writer.writerow([task["id"], task["name"], task["is_done"]])

def main():
    parser = argparse.ArgumentParser("To Do List")
    parser.add_argument("--read-from-file", type=str, help="if set, it will initially read from that file")
    parser.add_argument("--write-to-file", action="store_true", help="if used, it will write back to file every changes")

    args = parser.parse_args()

    if len(sys.argv) == 1: #means no argument is provided
        print("You've provided no arguments and have entered interactive mode, please put in the required information")
        read_from_file = input("Input the filepath of your CSV (default: None): ").strip()
        args.read_from_file = read_from_file if read_from_file else args.read_from_file

        if args.read_from_file:
            write_to_file = input("If set, application will write to file (true/false): ").lower() == "true"
            args.write_to_file = write_to_file

    to_do_app = ToDo(file_name=args.read_from_file)

    while True:
        command = input("> ")

        if command == "exit":
            break

        print(to_do_app.execute(command, args.write_to_file))

if __name__ == "__main__":
    main()
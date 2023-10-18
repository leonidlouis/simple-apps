import csv

class ToDo:
    def __init__(self):
        self.to_do = {}
        self.task_id = 0
        self.file_name = "tasks.csv"

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
        # return self.to_do
        return list(self.to_do.values())

    def execute(self, command):
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

        if operation in ["add", "done", "delete", "update"]:
            self.save_to_csv()

        return res
    
    def save_to_csv(self):
        with open(self.file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "is_done"])  # header
            for task in self.to_do.values():
                writer.writerow([task["id"], task["name"], task["is_done"]])

def main():
    to_do_app = ToDo()
    to_do_app.load_from_csv()

    while True:
        command = input("> ")

        if command == "exit":
            break

        print(to_do_app.execute(command))

if __name__ == "__main__":
    main()
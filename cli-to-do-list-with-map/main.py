class ToDo:
    def __init__(self):
        self.to_do = {}
        self.task_id = 0

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
        
        if operation == "update":
            id = parts[1]
            task_name = ' '.join(parts[2:])
            return operation_map[operation](id, task_name)
        
        if operation in ["list"]:
            return operation_map[operation]()
        
        if operation in ["add", "done", "delete"]:
            value = ' '.join(parts[1:])
            return operation_map[operation](value)


def main():
    to_do_app = ToDo()

    while True:
        command = input("> ")

        if command == "exit":
            break

        print(to_do_app.execute(command))

if __name__ == "__main__":
    main()
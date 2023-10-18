import psycopg2

class ToDo:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="todo",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432"
        )
        
        # create table if it doesn't exist
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('''
            create table if not exists todo (
                id serial primary key,
                name text not null,
                is_done boolean not null default false
            );
            ''')
            self.conn.commit()


    def get(self, id):
        id = int(id)
        cur = self.conn.cursor()
        cur.execute('select * from todo where id=%s', [id])
        
        row = cur.fetchone()

        if not row:
            return f"Task of ID {id} is not found"

        return {
            "id":row[0],
            "name":row[1],
            "is_done":row[2],
        }

    def add(self, task_name):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('insert into todo (name, is_done) values(%s, %s)', [task_name, False])
            self.conn.commit()
        return "Successfully Added"
    
    def mark_as_done(self, id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('update todo set is_done=true where id=%s', [id])
            if cur.rowcount == 0:
                return f"Task of ID {id} is not found"
            self.conn.commit()

        return f"Task of ID {id} is marked as done"
    
    def delete(self, id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('delete from todo where id=%s', [id])
            if cur.rowcount == 0:
                return f"Task of ID {id} is not found"
            self.conn.commit()
        return f"Task of ID {id} is successfully deleted"
    
    def update(self, id, task_name):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("update todo set name=%s where id=%s", [task_name, id])
            if cur.rowcount == 0:
                return f"Task of ID {id} is not found"
            self.conn.commit()

        return f"Task of ID {id} is updated"

    def list(self):
        cur = self.conn.cursor()
        cur.execute("select * from todo order by id asc")
        rows = cur.fetchall()

        tasks = []
        for row in rows:
            tasks.append({
                "id":row[0],
                "name":row[1],
                "is_done":row[2],
            })

        return tasks

    def execute(self, command):
        parts = command.split()
        operation = parts[0]

        operation_map = {
            "add": self.add,
            "done": self.mark_as_done,
            "delete": self.delete,
            "update": self.update,
            "list": self.list,
            "get": self.get
        }

        if operation not in operation_map:
            return "Invalid Command"
        
        if operation == "update":
            id = parts[1]
            task_name = ' '.join(parts[2:])
            return operation_map[operation](id, task_name)
        
        if operation in ["list"]:
            return operation_map[operation]()
        
        if operation in ["add", "done", "delete", "get"]:
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
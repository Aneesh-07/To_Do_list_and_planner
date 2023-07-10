import sqlite3

class Database():
    def __init__(self):
        self.con = sqlite3.connect("task-database.db")
        self.cursor = self.con.cursor()
        self.create_task_table()

# Createing the task table
    def create_task_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL,due_date varchar(50),due_time varchar(50), completed BOOLEAN NOT NULL CHECK(completed IN (0,1)))")
        self.con.commit()

# Creating the task
    def create_task(self, task,due_date = None,due_time = None):
        self.cursor.execute("INSERT INTO tasks(task, due_date,due_time, completed) VALUES(?,?,?,?)",(task, due_date,due_time, 0))
        self.con.commit()

        #getting the last entered item so we can add it to the task list

        created_task = self.cursor.execute("SELECT id, task, due_date,due_time FROM tasks WHERE task = ? and completed = 0 ORDER BY due_date,due_time", (task,)).fetchall()
        return created_task[-1]
    
    #getting the tasks

    def get_task(self):
        '''getting all tasks : completed and incompleted'''
        incompleted_tasks = self.cursor.execute("SELECT id, task, due_date, due_time FROM tasks WHERE completed = 0 ORDER BY due_date,due_time").fetchall()
        
        completed_tasks = self.cursor.execute("SELECT id, task, due_date, due_time FROM tasks WHERE completed = 1 ORDER BY due_date,due_time").fetchall()

        return completed_tasks , incompleted_tasks

    # Updating the tasks
    def mark_task_as_completed(self, taskid):
        '''Mark tasks as completed'''
        self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ? ",(taskid,))
        self.con.commit()
    def mark_task_as_incompleted(self, taskid):
        '''Mark tasks as incompleted'''
        self.cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ? ",(taskid,))
        self.con.commit()

        #return the task text
        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id = ?", (taskid,)).fetchall()

        return task_text[0][0]
    

    def delete_task(self,taskid):
        '''Delete a task'''
        self.cursor.execute("DELETE FROM tasks WHERE id = ? ", (taskid,) )
        self.con.commit()

    def close_db_connection(self):
        self.con.close()
    
        

    
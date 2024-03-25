from database.db import get_connection
from .entities.Task import Task
import uuid

class TaskModel():
    @classmethod
    def get_tasks_by_user(self, id):
        try:
            connection = get_connection()
            tasks = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (id,))
                result_set = cursor.fetchall()

                for row in result_set:
                    task = Task(row[0], row[1], row[2], row[3], row[4], row[5])
                    tasks.append(task.to_JSON())

            connection.close()
            return tasks
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_task(self, task):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO tasks (id, name, description, user_id) 
                                VALUES (%s, %s, %s, %s)""", (task.id, task.name, task.description, task.user_id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_task(self, task):
        print(f"status update: {task.status}")
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE tasks SET name = %s, description = %s, status = %s 
                                WHERE id = %s""", (task.name, task.description, task.status , task.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def delete_task(self, id):
        print(id)
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

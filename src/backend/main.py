from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MariaDB Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_server_connection("127.0.0.1", "root", "", "please")

class TaskBase(BaseModel):
    user_id: str
    task: str
    timestamp: datetime
    # on normal mysql like workbench chnage isCompleted in database and here to boolean instead
    isCompleted: int

# CREATE
@app.post("/tasks/")
def create_task(task: TaskBase):
    cursor = connection.cursor()
    current_timestamp = datetime.now()  # Get the current timestamp
    cursor.execute("INSERT INTO taskbase (task, user_id, timestamp, isCompleted) VALUES (%s, %s, %s, %s)",
                   (task.task, task.user_id, current_timestamp, task.isCompleted))
    connection.commit()
    new_id = cursor.lastrowid  # Get the new task ID
    cursor.close()
    return {
        "task_id": new_id,
        "task": task.task,
        "user_id": task.user_id,
        "timestamp": current_timestamp,
        "isCompleted": task.isCompleted
    }

# READ by ID
@app.get("/tasks/{user_id}")
def read_task(user_id: str):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, user_id, task, isCompleted, timestamp FROM taskbase WHERE user_id = %s", (user_id,))
        results = cursor.fetchall()
        cursor.close()

        if results:
            tasks = []
            for result in results:
                task_id, user_id, task, isCompleted, timestamp = result
                tasks.append({"task_id": task_id, "user_id": user_id, "task": task, "isCompleted": isCompleted, "timestamp": timestamp})
            return tasks
        else:
            return []

    except Exception as e:
        print("Error fetching tasks:", str(e))
        return {"message": "Error fetching tasks"}


# UPDATE

# this should work but mysqlworkbench broken so i used mariadb, but it does not have datatype boolean so i set isCompleted in mine as tinyint

# @app.put("/tasks/{task_id}")
# def update_task(task_id: int, task: TaskBase):
#     cursor = connection.cursor()

#     cursor.execute("SELECT task, isCompleted, timestamp FROM taskbase WHERE id = %s", (task_id,))
#     current_task = cursor.fetchone()

#     if current_task:
#         current_title, current_isCompleted, current_timestamp = current_task
#         if current_title == task.task:
#             # Toggle the value of isCompleted between 0 and 1
#             newisCompleted = not current_isCompleted
#         else:
#             newisCompleted = task.isCompleted

#         # Use the current_timestamp from the database
#         cursor.execute("UPDATE taskbase SET task = %s, isCompleted = %s, timestamp = %s WHERE id = %s",
#                        (task.task, newisCompleted, current_timestamp, task_id))
#         connection.commit()
#         cursor.close()
#         return {"message": "Task updated successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskBase):
    cursor = connection.cursor()

    cursor.execute("SELECT task, isCompleted, timestamp FROM taskbase WHERE id = %s", (task_id,))
    current_task = cursor.fetchone()

    if current_task:
        current_title, current_isCompleted, current_timestamp = current_task
        if current_title == task.task:
            # Toggle the value of isCompleted between 0 and 1
            newisCompleted = 1 if current_isCompleted == 0 else 0
        else:
            newisCompleted = task.isCompleted

        # Use the current_timestamp from the database
        cursor.execute("UPDATE taskbase SET task = %s, isCompleted = %s, timestamp = %s WHERE id = %s",
                       (task.task, newisCompleted, current_timestamp, task_id))
        connection.commit()
        cursor.close()
        return {"message": "Task updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")




# DELETE
@app.delete("/tasks/{task_id}/{user_id}")
def delete_task(task_id: int, user_id: str):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM taskbase WHERE id = %s AND user_id = %s", (task_id, user_id))
    connection.commit()
    cursor.close()
    return {"message": "Task deleted successfully"}

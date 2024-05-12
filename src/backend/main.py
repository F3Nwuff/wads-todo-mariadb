from fastapi import FastAPI, HTTPException                                                                                                                      # type: ignore
from fastapi.middleware.cors import CORSMiddleware                                                                                              # type: ignore
from pydantic import BaseModel                                                                                                                      # type: ignore
import mysql.connector                                                                                                                                  # type: ignore
from mysql.connector import Error                                                                                                                # type: ignore
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
    is_completed: bool

# CREATE
@app.post("/tasks/")
def create_task(task: TaskBase):
    cursor = connection.cursor()
    current_timestamp = datetime.now()  # Get the current timestamp
    cursor.execute("INSERT INTO taskbase (task, user_id, timestamp, isCompleted) VALUES (%s, %s, %s, %s)",
                   (task.task, task.user_id, current_timestamp, task.is_completed))
    new_id = cursor.lastrowid  # Get the new task ID
    connection.commit()
    cursor.close()
    return {"id": new_id, "task": task.task, "user_id": task.user_id, "timestamp": current_timestamp, "is_completed": task.is_completed}


# READ by ID
@app.get("/tasks/{user_id}")
def read_task(user_id: str):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, task, isCompleted, timestamp FROM taskbase WHERE user_id = %s", (user_id,))
        results = cursor.fetchall()
        cursor.close()

        if results:
            tasks = []
            for result in results:
                task_id, task, is_completed, timestamp = result
                tasks.append({"id": task_id, "task": task, "is_completed": is_completed, "timestamp": timestamp})
            return tasks
        else:
            return {"message": "No tasks found for this user"}

    except Exception as e:
        print("Error fetching tasks:", str(e))
        return {"message": "Error fetching tasks"}

# UPDATE
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskBase):
    cursor = connection.cursor()

    cursor.execute("SELECT task, isCompleted, timestamp FROM taskbase WHERE id = %s AND user_id = %s", (task_id, task.user_id))
    current_task = cursor.fetchone()

    if current_task:
        current_title, current_is_completed, current_timestamp = current_task
        if current_title == task.task:
            # Toggle the value of isCompleted between 0 and 1
            new_is_completed = not current_is_completed
        else:
            new_is_completed = task.is_completed

        # Use the current_timestamp from the database
        cursor.execute("UPDATE taskbase SET task = %s, isCompleted = %s, timestamp = %s WHERE id = %s AND user_id = %s",
                       (task.task, new_is_completed, current_timestamp, task_id, task.user_id))
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)                                                                                                                                   # type: ignore
import { useEffect, useState } from "react";
import { Header } from "./components/header";
import { Tasks } from "./components/tasks";
import axios from "axios";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    // Check user authentication status
    // Assuming you have implemented authentication with Firebase
    // If not, you might need to replace this logic with your authentication method
    const user = auth.currentUser;
    if (user) {
      setIsAuthenticated(true);
      setUserEmail(user.email);
      loadTasks();
    } else {
      setIsAuthenticated(false);
      setUserEmail('');
      setTasks([]);
    }
  }, []);

  async function loadTasks() {
    try {
      const response = await axios.get("http://localhost:8000/tasks/" + auth.currentUser.uid);
      setTasks(response.data);
    } catch (error) {
      console.error("Error loading tasks:", error);
    }
  }

  async function addTask(taskTitle) {
    try {
      await axios.post("http://localhost:8000/tasks/", {
        user_id: auth.currentUser.uid,
        task: taskTitle,
        timestamp: new Date().toISOString(),
        is_completed: false
      });
      loadTasks();
    } catch (error) {
      console.error("Error adding task:", error);
    }
  }

  async function deleteTaskById(taskId) {
    try {
      await axios.delete(`http://localhost:8000/tasks/${taskId}/${auth.currentUser.uid}`);
      loadTasks();
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  }

  async function onDeleteAllCompleted() {
    try {
      const response = await axios.delete(`http://localhost:8000/tasks/${auth.currentUser.uid}`);
      loadTasks();
    } catch (error) {
      console.error("Error deleting all completed tasks:", error);
    }
  }

  async function toggleTaskCompletedById(taskId) {
    try {
      await axios.put(`http://localhost:8000/tasks/${taskId}`, {
        user_id: auth.currentUser.uid,
        task: tasks.find(task => task.id === taskId).task,
        is_completed: !tasks.find(task => task.id === taskId).is_completed
      });
      loadTasks();
    } catch (error) {
      console.error("Error updating task:", error);
    }
  }

  return (
    !isAuthenticated ? (
      <>
        <Login />
      </>
    ) : (
      <>
        <Header 
          handleAddTask={addTask} 
          userEmail={userEmail} 
          handleLogout={() => signOut(auth)} 
        />
        <Tasks
          tasks={tasks}
          onDelete={deleteTaskById}
          onComplete={toggleTaskCompletedById}
          onDeleteAllCompleted={onDeleteAllCompleted}
        />
      </>
    )
  );
}

export default App;

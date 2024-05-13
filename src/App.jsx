import { useEffect, useState } from "react";
import { Header } from "./components/header";
import { Tasks } from "./components/tasks";
import { auth } from "./firebase/firebase"; 
import { onAuthStateChanged, signOut } from "firebase/auth";
import Login from "./components/auth/login";
import { AuthProvider } from "./contexts/authContext";
import axios from "axios";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, user => {
      if (user) {
        setIsAuthenticated(true);
        setUserEmail(user.email);
        loadTasks(); // Load tasks when user is authenticated
      } else {
        setIsAuthenticated(false);
        setUserEmail('');
        setTasks([]); // Clear tasks when user is not authenticated
      }
    });

    return () => unsubscribe();
  }, []);

  async function loadTasks() {
    try {
      const response = await axios.get("http://localhost:8000/tasks/" + auth.currentUser.uid);
      console.log(response.data)
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
        isCompleted: false
      });
      loadTasks();
    } catch (error) {
      console.error("Error adding task:", error);
    }
  }

  async function deleteTaskById(taskId) {
    console.log(auth.currentUser.uid)
    try {
      await axios.delete(`http://localhost:8000/tasks/${taskId}/${auth.currentUser.uid}`);
      loadTasks();
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  }

  async function onDeleteAllCompleted() {
    try {
      const tasksResponse = await axios.get(`http://localhost:8000/tasks/${auth.currentUser.uid}`);
      const tasks = tasksResponse.data;
      console.log(tasks)
      console.log(tasks.isCompleted)
  
      // Filter completed tasks
      const completedTasks = tasks.filter(task => task.isCompleted === true || task.isCompleted === 1);
      console.log(completedTasks)
      console.log(completedTasks.map)

      // Delete completed tasks
      await Promise.all(completedTasks.map(async task => {
        await axios.delete(`http://localhost:8000/tasks/${task.task_id}/${auth.currentUser.uid}`);
      }));
  
      loadTasks();
    } catch (error) {
      console.error("Error deleting all completed tasks:", error);
    }
  }
  
  
  async function toggleTaskCompletedById(taskId) {
    try {
        const task = tasks.find(task => task.task_id === taskId);
        if (task) {
            const newIsCompleted = task.isCompleted === 1 ? 0 : 1;
            const current_timestamp = new Date().toISOString();

            await axios.put(`http://localhost:8000/tasks/${taskId}`, {
                user_id: auth.currentUser.uid,
                task: task.task,
                isCompleted: newIsCompleted,
                timestamp: current_timestamp
            });
            loadTasks();
        } else {
            console.error("Task not found");
        }
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

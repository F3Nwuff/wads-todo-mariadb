import styles from './task.module.css';
import { BsFillCheckCircleFill } from 'react-icons/bs';
import { TbTrash } from 'react-icons/tb';

// export function DateTimeDisplay() {
//   const formattedDateTime = new Date().toLocaleDateString("en-US", {
//     year: 'numeric', month: 'long', day: 'numeric'
//   });

//   return (
//     <p>{formattedDateTime}</p>
//   );
// }

export function Task({ task, onDelete, onComplete }) {
  // Function to format datetime string
  const formatDateTime = (datetime) => {
    console.log('Datetime:', datetime);
    const formattedDate = new Date(datetime).toLocaleString();
    return formattedDate;
  };
  
  return (
    <div className={styles.task} key={task.task_id}>
      <button className={styles.checkContainer} onClick={() => onComplete(task.task_id)}>
        {task.isCompleted ? <BsFillCheckCircleFill /> : <div />}
      </button>

      <p className={task.isCompleted ? styles.textCompleted : ""}>
        {task.task}
      </p>
      <br />
      <p className={task.isCompleted ? styles.textCompleted : ""}>
        {formatDateTime(task.timestamp)}
      </p>

      <button className={styles.deleteButton} onClick={() => onDelete(task.task_id)}>
        <TbTrash size={20} />
      </button>
    </div>
  );
}
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Dashboard = () => {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [user, setUser] = useState(null);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [toast, setToast] = useState({ show: false, msg: '', type: '' });

  useEffect(() => {
    fetchUser();
    fetchTasks();
  }, []);

  const showToast = (msg, type='success') => {
    setToast({ show: true, msg, type });
    setTimeout(() => setToast({ show: false, msg: '', type: '' }), 3000);
  };

  const fetchUser = async () => {
    try {
      const res = await api.get('/auth/me');
      setUser(res.data);
    } catch (err) {
      if (err.response?.status === 401) handleLogout();
    }
  };

  const fetchTasks = async () => {
    try {
      const res = await api.get('/tasks/');
      setTasks(res.data);
    } catch (err) {
      showToast('Failed to load tasks', 'error');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
    window.location.reload();
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    if (!newTask.title.trim()) return;
    try {
      const res = await api.post('/tasks/', newTask);
      setTasks([...tasks, res.data]);
      setNewTask({ title: '', description: '' });
      showToast('Task created!');
    } catch (err) {
      showToast('Failed to create task', 'error');
    }
  };

  const handleToggleComplete = async (task) => {
    try {
      const res = await api.put(`/tasks/${task.id}`, { completed: !task.completed });
      setTasks(tasks.map((t) => (t.id === task.id ? res.data : t)));
    } catch (err) {
      showToast('Failed to update task', 'error');
    }
  };

  const handleDeleteTask = async (id) => {
    try {
      await api.delete(`/tasks/${id}`);
      setTasks(tasks.filter((t) => t.id !== id));
      showToast('Task deleted!');
    } catch (err) {
      showToast('Failed to delete task', 'error');
    }
  };

  return (
    <div className="dashboard-container">
      {toast.show && <div className={`toast ${toast.type}`}>{toast.msg}</div>}
      
      <header className="header">
        <h1 className="header-title">Welcome, {user?.username || 'User'} <span style={{fontSize: '0.5em', color: 'var(--text-muted)'}}>[{user?.role}]</span></h1>
        <button className="btn btn-small" onClick={handleLogout}>Sign Out</button>
      </header>

      <form className="create-form" onSubmit={handleCreateTask}>
        <h3>Create New Task</h3>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <input 
            className="form-control" 
            placeholder="Task Title..." 
            value={newTask.title}
            onChange={(e) => setNewTask({...newTask, title: e.target.value})}
            required
          />
          <input 
            className="form-control" 
            placeholder="Description (Optional)" 
            value={newTask.description}
            onChange={(e) => setNewTask({...newTask, description: e.target.value})}
          />
          <button type="submit" className="btn btn-small">Add Task</button>
        </div>
      </form>

      <div className="task-grid">
        {tasks.map(task => (
          <div className="task-card" key={task.id} style={{ opacity: task.completed ? 0.6 : 1 }}>
            <h3 className="task-title" style={{ textDecoration: task.completed ? 'line-through' : 'none' }}>
              {task.title}
            </h3>
            <p className="task-desc">{task.description || 'No description provided.'}</p>
            <div className="task-actions">
              <button 
                className="btn btn-small" 
                style={{ background: task.completed ? 'var(--text-muted)' : 'var(--success)' }}
                onClick={() => handleToggleComplete(task)}
              >
                {task.completed ? 'Undo' : 'Complete'}
              </button>
              <button 
                className="btn btn-small btn-danger" 
                onClick={() => handleDeleteTask(task.id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
        {tasks.length === 0 && <p style={{ color: 'var(--text-muted)' }}>No tasks found. Create one above!</p>}
      </div>
    </div>
  );
};

export default Dashboard;

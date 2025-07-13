import { useState } from 'react';
import HomePage from './HomePage.jsx';
import Dashboard from './Dashboard.jsx';

export default function App() {
  const [page, setPage] = useState('home');

  return (
    <div>
      <nav className="flex justify-center gap-6 py-4 bg-black text-white">
        <button onClick={() => setPage('home')}>Home</button>
        <button onClick={() => setPage('dashboard')}>Dashboard</button>
      </nav>

      {page === 'home' && <HomePage />}
      {page === 'dashboard' && <Dashboard />}
    </div>
  );
}

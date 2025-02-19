import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ManagerialSignup from './pages/ManagerialSignup';
import Login from './pages/Login';
import Banner from './components/Banner';
function AppRoutes() {
  return (
    <Routes>
      <Route path="/managerial-signup" element={<ManagerialSignup />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AppRoutes />
    </Router>
  );
}

export default App;
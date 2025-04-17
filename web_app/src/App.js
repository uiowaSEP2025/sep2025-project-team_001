import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Home from './pages/Home';
import Registration from './pages/Registration';
import Login from './pages/Login';
import './auth';
import Dashboard from './pages/Dashboard';
import OrdersPage from './pages/OrdersPage';
import MenuPage from './pages/MenuPage';
import PrivateRoute from './PrivateRoute';
import ManagerRegistrationPage from './pages/ManagerRegistrationPage';
import ManagerDashboard from './pages/ManagerDashboard';
import BartenderRegistrationPage from './pages/BartenderRegistrationPage';
import ProductStatisticsPage from './pages/ProductStatisticsPage';

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/register" element={<Registration />} />
      <Route path="/login" element={<Login />} />
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        }
      />
      <Route
        path="/bartender_registration"
        element={
          <PrivateRoute>
            <BartenderRegistrationPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/manager_registration"
        element={
          <PrivateRoute>
            <ManagerRegistrationPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/manager_dashboard"
        element={
          <PrivateRoute>
            <ManagerDashboard />
          </PrivateRoute>
        }
      />
      <Route
        path="/orders"
        element={
          <PrivateRoute>
            <OrdersPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/product_statistics"
        element={
          <PrivateRoute>
            <ProductStatisticsPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/menu"
        element={
          <PrivateRoute>
            <MenuPage />
          </PrivateRoute>
        }
      />
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

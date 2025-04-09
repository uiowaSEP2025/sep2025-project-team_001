// src/pages/Dashboard.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import OwnerAuthModal from '../components/OwnerAuthModal';

function Dashboard() {
  const navigate = useNavigate();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const barName = sessionStorage.getItem('barName');
    
  const handleAuthenticated = (data) => {
    sessionStorage.setItem('accessToken', data.tokens.access);
    sessionStorage.setItem('refreshToken', data.tokens.refresh);
    sessionStorage.setItem('barName', data.bar_name);
    sessionStorage.setItem('restaurantId', data.restaurant_id);
    navigate('/manager_registration');
  };
  const handleOrderClick = () => {
    navigate('/orders');
  };

  const handleMenuClick = () => {
    navigate('/menu');
  };
  const handleManagerLoginClick = () => {
    navigate('/manager_login');
  }
  const handleBartenderClick = () => {
    navigate('/bartender_login')
  }
  const handleLogOutClick = () => {
    // Clear all relevant auth data from sessionStorage
    sessionStorage.removeItem('accessToken');
    sessionStorage.removeItem('refreshToken');
    sessionStorage.removeItem('barName');
    navigate('/');
  };

  return (
    <Container className="text-center mt-5">
      {barName && <h2 className="mb-4">Restaurant: {barName}</h2>}
      <Button variant="success" size="lg" onClick={handleOrderClick}>
        Orders
      </Button>
      <Button variant="primary" size="lg" onClick={handleMenuClick}>
        Menu
      </Button>
      <Button variant="primary" size="lg" onClick={handleBartenderClick}>
        Bartender Login
      </Button>
      <Button variant="primary" size="lg" onClick={handleManagerLoginClick}>
        Manager Login
      </Button>
      <Button
        variant="warning"
        size="lg"
        className="mt-3"
        onClick={() => setShowAuthModal(true)}
      >
        Create Manager
      </Button>
      <Button variant="danger" size="lg" onClick={handleLogOutClick}>
        Log Out
      </Button>
      <OwnerAuthModal
        show={showAuthModal}
        onHide={() => setShowAuthModal(false)}
        onOwnerAuthenticated={handleAuthenticated}
      />
 
    </Container>
  );
}

export default Dashboard;

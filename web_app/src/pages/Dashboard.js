// src/pages/Dashboard.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import OwnerAuthModal from '../components/OwnerAuthModal';

function Dashboard() {
  const navigate = useNavigate();
  const [ownerInfo, setOwnerInfo] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const barName = sessionStorage.getItem('barName');

  const handleAuthenticated = (data) => {
    setOwnerInfo(data);
    navigate('manager_registration');
  }

  const handleOrderClick = () => {
    navigate('/orders');
  };

  const handleMenuClick = () => {
    navigate('/menu');
  };

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
      <Button variant="danger" size="lg" onClick={handleLogOutClick}>
        Log Out
      </Button>
      <Button
        variant="warning"
        size="lg"
        className="mt-3"
        onClick={() => setShowAuthModal(true)}
      >
        Create Manager
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

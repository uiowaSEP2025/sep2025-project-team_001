import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import OwnerAuthModal from '../components/OwnerAuthModal';

function ManagerDashboard() {
  const navigate = useNavigate();
  const barName = sessionStorage.getItem('barName');
  const [showAuthModal, setShowAuthModal] = useState(false);

  const handleAuthenticated = (data) => {
    sessionStorage.setItem('accessToken', data.tokens.access);
    sessionStorage.setItem('refreshToken', data.tokens.refresh);
    sessionStorage.setItem('barName', data.bar_name);
    sessionStorage.setItem('restaurantId', data.restaurant_id);
    navigate('/manager_registration');
  };

  const handleMenuClick = () => {
    navigate('/menu');
  };

  const handleOrdersClick = () => {
    navigate('/orders');
  };

  const handleBartenderClick = () => {
    navigate('/bartender_registration');
  };

  const handleLogOutClick = () => {
    navigate('/dashboard');
  };

  return (
    <Container className="text-center mt-5">
      <h1 className="mb-4">Manager Dashboard</h1>
      {barName && <h2 className="mb-4">Restaurant: {barName}</h2>}

      <Button variant="primary" size="lg" onClick={handleMenuClick} className="mb-3">
        Menu
      </Button>
      <Button variant="primary" size="lg" onClick={handleOrdersClick} className="mb-3">
        Orders
      </Button>
      <Button variant="primary" size="lg" onClick={handleBartenderClick} className="mb-3">
        Create Bartender
      </Button>
      <Button
        variant="warning"
        size="lg"
        className="mb-3"
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

export default ManagerDashboard;
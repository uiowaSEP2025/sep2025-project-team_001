import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import OwnerAuthModal from '../components/OwnerAuthModal';
import axios from 'axios';

function ManagerDashboard() {
  const navigate = useNavigate();
  const barName = sessionStorage.getItem('barName');
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [workers, setWorkers] = useState([]);

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

  useEffect(() => {
    const fetchWorkers = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/get-workers/`);

        setWorkers(response.data);
      } catch (error) {
        console.error('Error fetching workers:', error);
      }
    };
  
    fetchWorkers();
  }, []);

  return (
    <Container className="text-center mt-5">
      <h1 className="mb-4">Manager Dashboard</h1>
      {barName && <h2 className="mb-4">Restaurant: {barName}</h2>}

      <Button
        variant="primary"
        size="lg"
        onClick={handleMenuClick}
        className="mb-3"
      >
        Menu
      </Button>
      <Button
        variant="primary"
        size="lg"
        onClick={handleOrdersClick}
        className="mb-3"
      >
        Orders
      </Button>
      <Button
        variant="primary"
        size="lg"
        onClick={handleBartenderClick}
        className="mb-3"
      >
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
      <div className="mt-4">
        <h3>Workers</h3>
        {workers.length > 0 ? (
          <ul className="list-unstyled">
            {workers.map((worker) => (
              <li key={worker.id}>
                {worker.name} - {worker.role} (PIN: {worker.pin})
              </li>
            ))}
          </ul>
        ) : (
          <p>No workers found.</p>
        )}
      </div>

    </Container>
  );
}

export default ManagerDashboard;

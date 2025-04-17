import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import OwnerAuthModal from '../components/OwnerAuthModal';
import axios from 'axios';
import {
  Box,
  Typography,
  TextField,
  Button as MuiButton,
  Paper,
  Stack,
} from '@mui/material';

function ManagerDashboard() {
  const navigate = useNavigate();
  const barName = sessionStorage.getItem('barName');
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [workers, setWorkers] = useState({ managers: [], bartenders: [] });
  const [newName, setNewName] = useState('');
  const [newPin, setNewPin] = useState('');
  const [inlineError, setInlineError] = useState('');
  const [inlineSuccess, setInlineSuccess] = useState('');


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
        const allWorkers = response.data;
  
        const managers = allWorkers.filter((worker) => worker.role === 'manager');
        const bartenders = allWorkers.filter((worker) => worker.role === 'bartender');
  
        setWorkers({ managers, bartenders });
      } catch (error) {
        console.error('Error fetching workers:', error);
      }
    };
  
    fetchWorkers();
  }, []);  

  const handleInlineBartenderCreate = async () => {
    const restaurantId = sessionStorage.getItem('restaurantId');
    setInlineError('');
    setInlineSuccess('');
  
    if (!restaurantId) {
      setInlineError('Restaurant ID not found.');
      return;
    }
  
    if (newPin.length !== 4 || !/^\d{4}$/.test(newPin)) {
      setInlineError('PIN must be exactly 4 digits.');
      return;
    }
  
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/create-worker/`, {
        pin: newPin,
        name: newName,
        restaurant_id: restaurantId,
        role: 'bartender',
      });
  
      setInlineSuccess('Bartender created!');
      setNewName('');
      setNewPin('');

      // Re-fetch the list after new bartender is added
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/get-workers/`);
      const allWorkers = res.data;
      const managers = allWorkers.filter((w) => w.role === 'manager');
      const bartenders = allWorkers.filter((w) => w.role === 'bartender');
      setWorkers({ managers, bartenders });
    } catch (error) {
      console.error(error);
      if (error.response?.data?.error) {
        setInlineError(error.response.data.error);
      } else {
        setInlineError('Failed to create bartender.');
      }
    }
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
      {/* Managers */}
      <div className="mt-4">
        <h3>Managers</h3>
        {workers.managers.length > 0 ? (
          <ul className="list-unstyled">
            {workers.managers.map((worker) => (
              <li key={worker.id}>
                {worker.name} - {worker.role} (PIN: {worker.pin})
              </li>
            ))}
          </ul>
        ) : (
          <p>No managers found.</p>
        )}
      </div>
  
      {/*Bartenders*/}
      <Box className="mt-4" sx={{ maxWidth: 600, mx: 'auto' }}>
        <Typography variant="h5" gutterBottom>Bartenders</Typography>
  
        <Paper elevation={2} sx={{ p: 2 }}>
          <Stack spacing={1}>
            <Box sx={{ display: 'flex', fontWeight: 'bold' }}>
              <Box sx={{ width: '40%' }}>Name</Box>
              <Box sx={{ width: '30%' }}>Role</Box>
              <Box sx={{ width: '30%' }}>PIN</Box>
            </Box>
  
            {/* Bartender List */}
            {workers.bartenders.map((worker) => (
              <Box key={worker.id} sx={{ display: 'flex', alignItems: 'center' }}>
                <Box sx={{ width: '40%' }}>{worker.name}</Box>
                <Box sx={{ width: '30%' }}>{worker.role}</Box>
                <Box sx={{ width: '30%' }}>{worker.pin}</Box>
              </Box>
            ))}
  
            {/* Inline Input Row */}
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <TextField
                label="Name"
                size="small"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                sx={{ width: '40%', mr: 1 }}
              />
              <TextField
                label="4-digit PIN"
                size="small"
                type="password"
                value={newPin}
                onChange={(e) => setNewPin(e.target.value)}
                sx={{ width: '30%', mr: 1 }}
              />
              <MuiButton variant="contained" onClick={handleInlineBartenderCreate}>
                + Add
              </MuiButton>
            </Box>
            
            {inlineError && <Typography color="error">{inlineError}</Typography>}
            {inlineSuccess && (
              <Typography color="success.main">{inlineSuccess}</Typography>
            )}
          </Stack>
        </Paper>
      </Box>
    </Container>
  );  
}

export default ManagerDashboard;

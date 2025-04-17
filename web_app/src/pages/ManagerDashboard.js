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
  const [workers, setWorkers] = useState({ managers: [], bartenders: [] });
  const [bartenderName, setBartenderName] = useState('');
  const [bartenderPin, setBartenderPin] = useState('');
  const [bartenderError, setBartenderError] = useState('');
  const [bartenderSuccess, setBartenderSuccess] = useState('');
  const [managerName, setManagerName] = useState('');
  const [managerPin, setManagerPin] = useState('');
  const [showManagerAuthModal, setShowManagerAuthModal] = useState(false);
  const [managerError, setManagerError] = useState('');
  const [managerSuccess, setManagerSuccess] = useState('');

  const handleMenuClick = () => {
    navigate('/menu');
  };

  const handleOrdersClick = () => {
    navigate('/orders');
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

  const handleCreateBartender = async () => {
    const restaurantId = sessionStorage.getItem('restaurantId');
    setBartenderError('');
    setBartenderSuccess('');
  
    if (!restaurantId) {
      setBartenderError('Restaurant ID not found.');
      return;
    }
  
    if (bartenderPin.length !== 4 || !/^\d{4}$/.test(bartenderPin)) {
      setBartenderError('PIN must be exactly 4 digits.');
      return;
    }
  
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/create-worker/`, {
        pin: bartenderPin,
        name: bartenderName,
        restaurant_id: restaurantId,
        role: 'bartender',
      });
  
      console.log(response.data);

      setBartenderSuccess('Bartender created!');
      setBartenderName('');
      setBartenderPin('');

      // Re-fetch the list after new bartender is added
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/get-workers/`);
      const allWorkers = res.data;
      const managers = allWorkers.filter((w) => w.role === 'manager');
      const bartenders = allWorkers.filter((w) => w.role === 'bartender');
      setWorkers({ managers, bartenders });
    } catch (error) {
      console.error(error);
      if (error.response?.data?.error) {
        setBartenderError(error.response.data.error);
      } else {
        setBartenderError('Failed to create bartender.');
      }
    }
  };


  const handleCreateManager = async () => {
    const restaurantId = sessionStorage.getItem('restaurantId');
  
    if (!restaurantId) {
      setManagerError('Restaurant ID not found.');
      return;
    }
  
    if (managerPin.length !== 4 || !/^\d{4}$/.test(managerPin)) {
      setManagerError('PIN must be exactly 4 digits.');
      return;
    }
  
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/create-worker/`, {
        pin: managerPin,
        name: managerName,
        restaurant_id: restaurantId,
        role: 'manager',
      });
  
      console.log(response.data)
      
      setManagerSuccess('Manager created!');
      setManagerName('');
      setManagerPin('');
      setShowManagerAuthModal(false);
  
      // Refresh worker list
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/get-workers/`);
      const allWorkers = res.data;
      const managers = allWorkers.filter((w) => w.role === 'manager');
      const bartenders = allWorkers.filter((w) => w.role === 'bartender');
      setWorkers({ managers, bartenders });
    } catch (error) {
      console.error(error);
      setManagerError(error.response?.data?.error || 'Failed to create manager.');
    }
  };
  
  const handleManagerAddClick = () => {
    setManagerError('');
    setManagerSuccess('');
    setShowManagerAuthModal(true);
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
      <Button variant="danger" size="lg" onClick={handleLogOutClick}>
        Log Out
      </Button>
      {/* Managers */}
      <Box className="mt-4" sx={{ maxWidth: 600, mx: 'auto' }}>
        <Typography variant="h5" gutterBottom>Managers</Typography>

        <Paper elevation={2} sx={{ p: 2 }}>
          <Stack spacing={1}>
            {/* Table Header */}
            <Box sx={{ display: 'flex', fontWeight: 'bold' }}>
              <Box sx={{ width: '40%' }}>Name</Box>
              <Box sx={{ width: '30%' }}>Role</Box>
              <Box sx={{ width: '30%' }}>PIN</Box>
            </Box>

            {/* Manager List */}
            {workers.managers.map((worker) => (
              <Box key={worker.id} sx={{ display: 'flex', alignItems: 'center' }}>
                <Box sx={{ width: '40%' }}>{worker.name}</Box>
                <Box sx={{ width: '30%' }}>{worker.role}</Box>
                <Box sx={{ width: '30%' }}>{worker.pin}</Box>
              </Box>
            ))}

            {/* Input Row */}
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <TextField
                label="Name"
                size="small"
                value={managerName}
                onChange={(e) => setManagerName(e.target.value)}
                sx={{ width: '40%', mr: 1 }}
              />
              <TextField
                label="4-digit PIN"
                size="small"
                type="password"
                value={managerPin}
                onChange={(e) => setManagerPin(e.target.value)}
                sx={{ width: '30%', mr: 1 }}
              />
              <MuiButton variant="contained" onClick={handleManagerAddClick}>
                + Add
              </MuiButton>
            </Box>

            {/* Messages */}
            {managerError && <Typography color="error">{managerError}</Typography>}
            {managerSuccess && (
              <Typography color="success.main">{managerSuccess}</Typography>
            )}
          </Stack>
        </Paper>
      </Box>
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
                value={bartenderName}
                onChange={(e) => setBartenderName(e.target.value)}
                sx={{ width: '40%', mr: 1 }}
              />
              <TextField
                label="4-digit PIN"
                size="small"
                type="password"
                value={bartenderPin}
                onChange={(e) => setBartenderPin(e.target.value)}
                sx={{ width: '30%', mr: 1 }}
              />
              <MuiButton variant="contained" onClick={handleCreateBartender}>
                + Add
              </MuiButton>
            </Box>

            {bartenderError && <Typography color="error">{bartenderError}</Typography>}
            {bartenderSuccess && (
              <Typography color="success.main">{bartenderSuccess}</Typography>
            )}
          </Stack>
        </Paper>
      </Box>
      <OwnerAuthModal
        show={showManagerAuthModal}
        onHide={() => setShowManagerAuthModal(false)}
        onOwnerAuthenticated={handleCreateManager}
      />
    </Container>
  );  
}

export default ManagerDashboard;

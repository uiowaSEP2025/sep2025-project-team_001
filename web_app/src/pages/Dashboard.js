import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, Paper, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import NumberPad from '../components/NumberPad';

const Dashboard = () => {
  const [pin, setPin] = useState('');
  const [error, setError] = useState('');
  const [barName, setBarName] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const name = sessionStorage.getItem('barName');
    if (name) {
      setBarName(name);
    }
  }, []);

  const logout = () => {
    sessionStorage.clear();
    navigate('/');
  };

  const handleDigitPress = (digit) => {
    if (pin.length < 4) {
      setPin((prev) => prev + digit);
    }
  };

  const handleDelete = () => {
    setPin((prev) => prev.slice(0, -1));
  };

  const handleClear = () => {
    setPin('');
  };

  const loginWithPin = async () => {
    try {
      const restaurantId = sessionStorage.getItem('restaurantId');

      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/login_user/`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pin, restaurant_id: restaurantId }),
        },
      );

      const data = await response.json();
      if (response.ok) {
        sessionStorage.setItem('accessToken', data.tokens.access);
        sessionStorage.setItem('refreshToken', data.tokens.refresh);
        sessionStorage.setItem('barName', data.bar_name);
        sessionStorage.setItem('restaurantId', data.restaurant_id);
        sessionStorage.setItem('workerId', data.worker_id);

        if (data.role === 'manager') {
          navigate('/manager_dashboard');
        } else if (data.role === 'bartender') {
          navigate('/orders');
        } else {
          setError('Unknown role.');
        }
      } else {
        setError(data.error || 'Invalid PIN');
      }
    } catch (err) {
      console.error('Error:', err);
      setError('An error occurred while logging in.');
    }
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      const { key } = event;
      if (/^\d$/.test(key)) handleDigitPress(key);
      else if (key === 'Backspace') handleDelete();
      else if (key === 'Enter') loginWithPin();
      else if (key.toLowerCase() === 'c') handleClear();
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [pin]);

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: '#1e3c72',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 3,
      }}
    >
      <Button
        color="error"
        size="large"
        onClick={logout}
        sx={{ position: 'absolute', top: 20, right: 20 }}
      >
        Logout
      </Button>

      <Paper
        elevation={6}
        sx={{ p: 4, maxWidth: 400, width: '100%', textAlign: 'center' }}
      >
        <Typography variant="h5" gutterBottom>
          {barName || 'Welcome'}
        </Typography>
        <Typography variant="h6" gutterBottom>
          Enter PIN
        </Typography>

        <Box sx={{ minHeight: '2.5rem', mb: 2 }}>
          <Typography variant="h4">
            {pin.length > 0 ? '*'.repeat(pin.length) : '\u00A0'}
          </Typography>
        </Box>

        {error && <Alert severity="error">{error}</Alert>}

        <Box mt={2}>
          <NumberPad
            onDigitPress={handleDigitPress}
            onDelete={handleDelete}
            onClear={handleClear}
            onEnter={loginWithPin}
          />
        </Box>
      </Paper>
    </Box>
  );
};

export default Dashboard;

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Card, Alert, Button } from 'react-bootstrap';
import NumberPad from '../components/NumberPad';
import './styles/Dashboard.css';

function Dashboard() {
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
    sessionStorage.clear(); // Remove all session data
    navigate('/'); // Redirect to home page
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
          body: JSON.stringify({ pin: pin, restaurant_id: restaurantId }),
        },
      );

      const data = await response.json();
      if (response.ok) {
        sessionStorage.setItem('accessToken', data.tokens.access);
        sessionStorage.setItem('refreshToken', data.tokens.refresh);
        sessionStorage.setItem('barName', data.bar_name);
        sessionStorage.setItem('restaurantId', data.restaurant_id);

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

  // useEffect(() => {
  //   if (pin.length === 4) {
  //     loginWithPin();
  //   }
  // }, [pin]);

  useEffect(() => {
    const handleKeyDown = (event) => {
      const { key } = event;
  
      if (/^\d$/.test(key)) {
        // If it's a digit (0-9)
        handleDigitPress(key);
      } else if (key === 'Backspace') {
        handleDelete();
      } else if (key === 'Enter') {
        loginWithPin();
      } else if (key.toLowerCase() === 'c') {
        handleClear();
      }
    };
  
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [pin]);

  return (
    <div style={{ position: 'relative' }}>
      <Button
        variant="outline-danger"
        size="sm"
        className="logout-btn"
        onClick={logout}
      >
        Logout
      </Button>

      <Container className="mt-5">
        <Row className="justify-content-center">
          <Col md={6}>
            <Card className="text-center p-4">
              <h3>{barName || 'Welcome'}</h3>
              <h4>Enter PIN</h4>

              <div className="pin-display">
                <h4 style={{ margin: 0 }}>
                  {pin.length > 0 ? '*'.repeat(pin.length) : '\u00A0'}
                </h4>
              </div>

              {error && <Alert variant="danger">{error}</Alert>}

              <NumberPad
                onDigitPress={handleDigitPress}
                onDelete={handleDelete}
                onClear={handleClear}
                onEnter={loginWithPin}
              />
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Dashboard;

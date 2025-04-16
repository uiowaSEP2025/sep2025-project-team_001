import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Form, Button, Alert, Card } from 'react-bootstrap';
import axios from 'axios';

function BartenderRegistrationPage() {
  const navigate = useNavigate();
  const [pin, setPin] = useState('');
  const [name, setName] = useState('');
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const restaurantId = sessionStorage.getItem('restaurantId');
    if (!restaurantId) {
      setError('Restaurant ID not found.');
      return;
    }

    if (pin.length !== 4 || !/^\d{4}$/.test(pin)) {
      setError('PIN must be 4 digits.');
      return;
    }

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/create-worker/`,
        {
          pin,
          name,
          restaurant_id: restaurantId,
          role: 'bartender',
        }
      );

      console.log(response.data);
  
      setSuccess('Bartender created successfully.');
      setTimeout(() => {
        navigate('/dashboard');
      }, 1000);
    } catch (err) {
      console.error('Error:', err);
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError('An error occurred while creating bartender.');
      }
    }
  };

  return (
    <Container className="mt-5">
      <h2>Create Bartender</h2>
      <Card className="p-4">
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formBasicName">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </Form.Group>

          <Form.Group controlId="formPIN" className="mt-3">
            <Form.Label>4-Digit PIN</Form.Label>
            <Form.Control
              type="password"
              placeholder="Enter 4-digit PIN"
              value={pin}
              maxlength={4}
              onChange={(e) => setPin(e.target.value)}
              required
            />
          </Form.Group>
          {success && <Alert variant="success">{success}</Alert>}
          {error && <Alert variant="danger">{error}</Alert>}

          <div className="d-flex justify-content-between">
            <Button variant="secondary" onClick={() => navigate(-1)}>
              Back
            </Button>
            <Button variant="primary" type="submit">
              Create Bartender
            </Button>
          </div>
        </Form>
      </Card>
    </Container>
  );
}

export default BartenderRegistrationPage;

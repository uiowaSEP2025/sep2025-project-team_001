import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../index.css';
import axios from 'axios';

function Login() {
  const navigate = useNavigate();

  // State to store form values
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (event) => {
    event.preventDefault();
    console.log('Login form submitted');

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}login/`, {
        username,
        password,
      });

      console.log('Login successful:', response.data);
      // Redirect to the dashboard
      navigate('/');
    } catch (error) {
      console.error('Login error:', error.response?.data || error.message);
      alert('Invalid username or password. Please try again.');
    }
  };

  return (
    <Container className="page-container">
      <h1>Login</h1>
      <Form onSubmit={handleLogin} className="form-container">
        <Form.Group controlId="username" className="form-group-spacing">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter username"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </Form.Group>
        <Form.Group controlId="password" className="form-group-spacing">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Login
        </Button>
      </Form>
    </Container>
  );
}

export default Login;
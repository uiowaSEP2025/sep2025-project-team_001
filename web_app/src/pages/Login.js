import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../index.css';

function Login() {
  const navigate = useNavigate();
  const handleLogin = (event) => {
    event.preventDefault();
    console.log('Login form submitted');
    navigate('/dashboard'); // Redirect to the dashboard after login
  };

  return (
    <Container className="page-container">
      <h1>Login</h1>
      <Form onSubmit={handleLogin} className="form-container">
        <Form.Group controlId="username" className="form-group-spacing">
          <Form.Label>Username</Form.Label>
          <Form.Control type="text" placeholder="Enter username" required />
        </Form.Group>
        <Form.Group controlId="password" className="form-group-spacing">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Enter password" required />
        </Form.Group>
        <Button variant="primary" type="submit">
          Login
        </Button>
      </Form>
    </Container>
  );
}

export default Login;
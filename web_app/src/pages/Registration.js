import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../index.css';

function Registration() {
  const navigate = useNavigate();
  const handleRegister = (event) => {
    event.preventDefault();
    console.log('Form submitted');
    navigate('/login'); // Redirect to the home page after submission
  };

  return (
    <Container className="page-container">
      <h1>Online Manager Registration</h1>
      <Form onSubmit={handleRegister} className="form-container">
        <Form.Group controlId="name" className="form-group-spacing">
          <Form.Label>First & Last Name</Form.Label>
          <Form.Control type="text" placeholder="Enter first and last name" required />
        </Form.Group>
        <Form.Group controlId="desiredUsername" className="form-group-spacing">
          <Form.Label>Desired Username</Form.Label>
          <Form.Control type="text" placeholder="Enter desired username" required />
        </Form.Group>
        <Form.Group controlId="desiredPassword" className="form-group-spacing">
          <Form.Label>Desired Password</Form.Label>
          <Form.Control type="password" placeholder="Enter desired password" required />
        </Form.Group>
        <Form.Group controlId="confirmPassword" className="form-group-spacing">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control type="password" placeholder="Confirm password" required />
        </Form.Group>
        <Form.Group controlId="email" className="form-group-spacing">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" placeholder="Enter email" required />
        </Form.Group>
        <Form.Group controlId="phoneNumber" className="form-group-spacing">
          <Form.Label>Phone Number</Form.Label>
          <Form.Control type="tel" placeholder="Enter phone number" required />
        </Form.Group>
        <Form.Group controlId="businessName" className="form-group-spacing">
          <Form.Label>Business Name</Form.Label>
          <Form.Control type="text" placeholder="Enter business name" required />
        </Form.Group>
        <Form.Group controlId="businessAddress" className="form-group-spacing">
          <Form.Label>Business Address</Form.Label>
          <Form.Control type="text" placeholder="Enter business address" required />
        </Form.Group>
        <Button variant="primary" type="submit">
          Register
        </Button>
      </Form>
    </Container>
  );
}

export default Registration;
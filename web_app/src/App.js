import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

function Signup() {
  const navigate = useNavigate();
  const handleRegister = (event) => {
    console.log('Form submitted');
    navigate('/login'); // Redirect to the home page after submission
  };
  return (
    <Container className = "page-container">
      <h1>Online Registration</h1>
      <Form onSubmit = {handleRegister} className = "form-container">
        <Form.Group controlId = "desiredUsername" className = "form-group-spacing">
          <Form.Label>Desired Username</Form.Label>
          <Form.Control type = "text" placeholder = "Enter desired username" required />
        </Form.Group>
        <Button variant="primary" type="submit">
          Register
        </Button>
      </Form>
    </Container>
  )
}
function AppRoutes() {
  return (
    <Routes>
      <Route path ="/signup" element={<Signup />} />
      {/* <Route path ="/login" element={<Login />} /> */}
    </Routes>
  )
}

function App() {
  return (
    <Router>
      <AppRoutes />
    </Router>
  );
}

export default App;

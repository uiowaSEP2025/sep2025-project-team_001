import React from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <Container className="d-flex flex-column justify-content-center align-items-center vh-100">
      <Button variant="primary">Login</Button>
    </Container>
  );
}

export default App;

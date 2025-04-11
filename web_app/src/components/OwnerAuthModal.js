// src/components/OwnerAuthModal.js
import React, { useState } from 'react';
import { Modal, Button, Form, Alert, Spinner } from 'react-bootstrap';

const OwnerAuthModal = ({ show, onHide, onOwnerAuthenticated }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [authError, setAuthError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleOwnerLogin = async () => {
    setLoading(true);
    setAuthError('');
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/login_restaurant/`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password }),
        },
      );

      const data = await response.json();

      if (response.ok && data.tokens) {
        onOwnerAuthenticated(data); // Pass tokens and restaurant info back
        setUsername('');
        setPassword('');
        onHide(); // Close modal
      } else {
        setAuthError(data.error || 'Invalid credentials');
      }
    } catch (error) {
      console.error(error);
      setAuthError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>Owner Verification</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {authError && <Alert variant="danger">{authError}</Alert>}
        <Form>
          <Form.Group controlId="ownerUsername">
            <Form.Label>Username</Form.Label>
            <Form.Control
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </Form.Group>
          <Form.Group controlId="ownerPassword" className="mt-2">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Cancel
        </Button>
        <Button variant="primary" onClick={handleOwnerLogin} disabled={loading}>
          {loading ? <Spinner size="sm" animation="border" /> : 'Authenticate'}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default OwnerAuthModal;

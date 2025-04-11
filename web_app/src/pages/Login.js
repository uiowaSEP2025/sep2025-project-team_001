import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/Login.css';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/login_restaurant/`,
        {
          username,
          password,
        },
      );

      const { access, refresh } = response.data.tokens;

      sessionStorage.setItem(
        'barName',
        response.data.bar_name || 'Error retrieving bar name',
      );
      sessionStorage.setItem('accessToken', access);
      sessionStorage.setItem('refreshToken', refresh);
      sessionStorage.setItem('restaurantId', response.data.restaurant_id);

      navigate('/dashboard');
    } catch (error) {
      toast.error('Invalid username or password. Please try again.');
    }
  };

  return (
    <div className="login-page-container">
      <Modal
        show
        centered
        backdrop="static"
        keyboard={false}
        dialogClassName="login-modal-dialog"
      >
        <Modal.Header className="login-modal-header">
          <button className="modal-back-button" onClick={() => navigate('/')}>
            Back
          </button>
          <Modal.Title className="login-modal-title w-100 text-center">
            Restaurant Login
          </Modal.Title>
        </Modal.Header>
        <Modal.Body className="login-modal-body">
          <Form onSubmit={handleLogin}>
            <Form.Group controlId="username" className="login-form-group">
              <Form.Control
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="login-form-control"
              />
            </Form.Group>
            <Form.Group controlId="password" className="login-form-group">
              <Form.Control
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="login-form-control"
              />
            </Form.Group>
            <Button variant="primary" type="submit" className="login-button">
              Login
            </Button>
            <div className="register-link-container">
              <span>Don't have an account? </span>
              <span
                className="register-link"
                onClick={() => navigate('/register')}
              >
                Register
              </span>
            </div>
          </Form>
        </Modal.Body>
      </Modal>

      <ToastContainer
        position="top-center"
        autoClose={4000}
        hideProgressBar
        closeButton={false}
        toastStyle={{
          textAlign: 'center',
          fontSize: '16px',
          borderRadius: '10px',
          background: '#333',
          color: '#fff',
        }}
      />
    </div>
  );
}

export default Login;

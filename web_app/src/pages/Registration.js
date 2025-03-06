import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import "./styles/Registration.css";

function Registration() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // Step 1 or Step 2

  const [formData, setFormData] = useState({
    name: "",
    username: "",
    password: "",
    confirmPassword: "",
    email: "",
    phone: "",
    business_name: "",
    business_address: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleContinue = () => {
    if (!formData.name || !formData.username || !formData.password || !formData.confirmPassword) {
      alert("Please fill out all fields.");
      return;
    }
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    setStep(2); // Move to the next step
  };

  const handleBack = () => {
    setStep(1); // Go back to the first step
  };

  const handleRegister = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}register/`, {
        name: formData.name,
        username: formData.username,
        password: formData.password,
        email: formData.email,
        phone: formData.phone,
        business_name: formData.business_name,
        business_address: formData.business_address,
      });

      console.log("Registration successful:", response.data);
      const { access, refresh } = response.data.tokens;

      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);

      navigate("/"); // Redirect after successful registration
    } catch (error) {
      console.error("Registration failed:", error.response?.data || error.message);
      alert("Registration failed: " + (error.response?.data || error.message));
    }
  };

  return (
    <div className="page-container">
      {/* Title Always Visible at the Very Top */}
      <h1 className="page-title">Online Manager Registration</h1>

      {/* Step 1 - First Modal */}
      <Modal show={step === 1} backdrop="static" keyboard={false}>
        <Modal.Header>
          <Modal.Title>Step 1: Basic Information</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="name">
              <Form.Label>First & Last Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter full name"
                required
                value={formData.name}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="username">
              <Form.Label>Desired Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username"
                required
                value={formData.username}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="password">
              <Form.Label>Desired Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Enter password"
                required
                value={formData.password}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="confirmPassword">
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Confirm password"
                required
                value={formData.confirmPassword}
                onChange={handleChange}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={handleContinue}>
            Continue
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Step 2 - Second Modal */}
      <Modal show={step === 2} backdrop="static" keyboard={false}>
        <Modal.Header>
          <Modal.Title>Step 2: Contact & Business Info</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleRegister}>
            <Form.Group controlId="email">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                required
                value={formData.email}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="phone">
              <Form.Label>Phone Number</Form.Label>
              <Form.Control
                type="tel"
                placeholder="Enter phone number"
                required
                value={formData.phone}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="business_name">
              <Form.Label>Business Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter business name"
                required
                value={formData.business_name}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="business_address">
              <Form.Label>Business Address</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter business address"
                required
                value={formData.business_address}
                onChange={handleChange}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleBack}>
            Back
          </Button>
          <Button variant="success" type="submit" onClick={handleRegister}>
            Register
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default Registration;

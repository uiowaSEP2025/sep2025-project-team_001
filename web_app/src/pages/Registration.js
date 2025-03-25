import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import "./styles/Registration.css";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";


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
      toast.error("Please fill out all fields.");
      return;
    }
    if (formData.password !== formData.confirmPassword) {
      toast.error("Passwords do not match!");
      return;
    }
    if (formData.password.length < 6) {
      toast.error("Password must be at least 6 characters long.");
      return;
    }
    setStep(2); // Move to the next step
  };

  const handleBack = () => {
    setStep(1); // Go back to the first step
  };

  const handleRegister = async (event) => {
    event.preventDefault();

    // Validate step 2 fields before sending
    if (!formData.email || !formData.phone || !formData.business_name || !formData.business_address) {
      toast.error("Please fill out all fields in Step 2.");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      toast.error("Please enter a valid email address.");
      return;
    }

    const phoneRegex = /^\d{10}$/;
    if (!phoneRegex.test(formData.phone)) {
      toast.error("Phone number must be exactly 10 digits.");
      return;
    }

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/register/`, {
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
  
      // Store tokens in localStorage
      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);
  
      // Redirect to dashboard
      navigate("/dashboard");
    } catch (error) {
      console.error("Registration failed:", error.response?.data || error.message);
      toast.error("Registration failed: " + (error.response?.data || error.message));
    }
  };  

  return (
    <div className="page-container">
      <h1 className="page-title">Online Manager Registration</h1>

      <Modal show={step === 1} backdrop="static" keyboard={false}>
        <Modal.Header>
          <Modal.Title>Step 1: Basic Information</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="name">
              <Form.Control
                type="text"
                placeholder="First & Last Name"
                required
                value={formData.name}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="username">
              <Form.Control
                type="text"
                placeholder="Desired Username"
                required
                value={formData.username}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="password">
              <Form.Control
                type="password"
                placeholder="Desired Password"
                required
                value={formData.password}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="confirmPassword">
              <Form.Control
                type="password"
                placeholder="Confirm Password"
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

      <Modal show={step === 2} backdrop="static" keyboard={false}>
        <Modal.Header>
          <Modal.Title>Step 2: Contact & Business Info</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleRegister}>
            <Form.Group controlId="email">
              <Form.Control
                type="email"
                placeholder="Email"
                required
                value={formData.email}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="phone">
              <Form.Control
                type="tel"
                placeholder="Phone Number"
                required
                value={formData.phone}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="business_name">
              <Form.Control
                type="text"
                placeholder="Business Name"
                required
                value={formData.business_name}
                onChange={handleChange}
              />
            </Form.Group>
            <Form.Group controlId="business_address">
              <Form.Control
                type="text"
                placeholder="Business Address"
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

      <ToastContainer
        position="top-center"
        autoClose={4000}
        hideProgressBar
        closeButton={false}
        toastStyle={{
          textAlign: "center",
          fontSize: "16px",
          borderRadius: "10px",
          background: "#333",
          color: "#fff",
        }}
      />
    </div>
  );
}

export default Registration;

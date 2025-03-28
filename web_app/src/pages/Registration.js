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
  const [step, setStep] = useState(1);

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
    const { name, username, password, confirmPassword } = formData;
    if (!name || !username || !password || !confirmPassword) {
      toast.error("Please fill out all fields.");
      return;
    }
    if (password !== confirmPassword) {
      toast.error("Passwords do not match!");
      return;
    }
    if (password.length < 6) {
      toast.error("Password must be at least 6 characters long.");
      return;
    }
    setStep(2);
  };

  const handleBack = () => setStep(1);

  const handleRegister = async (event) => {
    event.preventDefault();
    const { email, phone, business_name, business_address } = formData;

    if (!email || !phone || !business_name || !business_address) {
      toast.error("Please fill out all fields in Step 2.");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^\d{10}$/;

    if (!emailRegex.test(email)) {
      toast.error("Please enter a valid email address.");
      return;
    }

    if (!phoneRegex.test(phone)) {
      toast.error("Phone number must be exactly 10 digits.");
      return;
    }

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/register/`, formData);
      const { access, refresh } = response.data.tokens;

      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);

      navigate("/dashboard");
    } catch (error) {
      toast.error("Registration failed: " + (error.response?.data?.message || error.message));
    }
  };

  return (
    <div className="registration-page-container">
      <Modal
        show={step === 1}
        centered
        backdrop="static"
        keyboard={false}
        dialogClassName="registration-modal-dialog"
      >
        <Modal.Header>
          <Modal.Title className="modal-title">Manager Registration</Modal.Title>
        </Modal.Header>
        <Modal.Body className="registration-modal-body">
          <Form>
            <Form.Group controlId="name" className="registration-form-group">
              <Form.Control
                type="text"
                placeholder="First & Last Name"
                required
                value={formData.name}
                onChange={handleChange}
                className="registration-form-control"
              />
            </Form.Group>
            <Form.Group controlId="username" className="registration-form-group">
              <Form.Control
                type="text"
                placeholder="Desired Username"
                required
                value={formData.username}
                onChange={handleChange}
                className="registration-form-control"
              />
            </Form.Group>
            <Form.Group controlId="password" className="registration-form-group">
              <Form.Control
                type="password"
                placeholder="Desired Password"
                required
                value={formData.password}
                onChange={handleChange}
                className="registration-form-control"
              />
            </Form.Group>
            <Form.Group controlId="confirmPassword" className="registration-form-group">
              <Form.Control
                type="password"
                placeholder="Confirm Password"
                required
                value={formData.confirmPassword}
                onChange={handleChange}
                className="registration-form-control"
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer className="registration-modal-footer">
          <Button className="registration-button" variant="primary" onClick={handleContinue}>
            Continue
          </Button>
        </Modal.Footer>
      </Modal>

      <Modal
        show={step === 2}
        centered
        backdrop="static"
        keyboard={false}
        dialogClassName="registration-modal-dialog"
      >
        <Modal.Header>
          <Modal.Title className="modal-title">Manager Registration</Modal.Title>
        </Modal.Header>
        <Modal.Body className="registration-modal-body">
          <Form onSubmit={handleRegister}>
            <Form.Group controlId="email" className="registration-form-group">
              <Form.Control
                type="email"
                placeholder="Email"
                required
                value={formData.email}
                onChange={handleChange}
                className="registration-form-control"
              />
            </Form.Group>
            <Form.Group controlId="phone" className="registration-form-group">
              <Form.Control
                type="tel"
                placeholder="Phone Number"
                required
                value={formData.phone}
                onChange={handleChange}
                className="registration-form-control"
              />
            </Form.Group>
            <Form.Group controlId="business_name" className="registration-form-group">
              <Form.Control
                type="text"
                placeholder="Business Name"
                required
                value={formData.business_name}
                onChange={handleChange}
                className="registration-form-control"
              />
            </Form.Group>
            <Form.Group controlId="business_address" className="registration-form-group">
              <Form.Control
                type="text"
                placeholder="Business Address"
                required
                value={formData.business_address}
                onChange={handleChange}
                className="registration-form-control"
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer className="registration-modal-footer">
          <Button className="registration-button" variant="secondary" onClick={handleBack}>
            Back
          </Button>
          <Button className="registration-button" variant="success" type="submit" onClick={handleRegister}>
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

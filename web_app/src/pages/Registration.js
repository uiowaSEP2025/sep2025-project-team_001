import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";
import "../index.css";
import axios from "axios";

function Registration() {
  const navigate = useNavigate();
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

  const handleRegister = async (event) => {
    event.preventDefault();
  
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match!");
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
      alert("Registration failed: " + (error.response?.data || error.message));
    }
  };  

  return (
    <Container className="page-container">
      <h1>Online Manager Registration</h1>
      <Form onSubmit={handleRegister} className="form-container">
        <Form.Group controlId="name" className="form-group-spacing">
          <Form.Label>First & Last Name</Form.Label>
          <Form.Control type="text" placeholder="Enter first and last name" required value={formData.name} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="username" className="form-group-spacing">
          <Form.Label>Desired Username</Form.Label>
          <Form.Control type="text" placeholder="Enter desired username" required value={formData.username} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="password" className="form-group-spacing">
          <Form.Label>Desired Password</Form.Label>
          <Form.Control type="password" placeholder="Enter desired password" required value={formData.password} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="confirmPassword" className="form-group-spacing">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control type="password" placeholder="Confirm password" required value={formData.confirmPassword} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="email" className="form-group-spacing">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" placeholder="Enter email" required value={formData.email} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="phone" className="form-group-spacing">
          <Form.Label>Phone Number</Form.Label>
          <Form.Control type="tel" placeholder="Enter phone number" required value={formData.phone} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="business_name" className="form-group-spacing">
          <Form.Label>Business Name</Form.Label>
          <Form.Control type="text" placeholder="Enter business name" required value={formData.business_name} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="business_address" className="form-group-spacing">
          <Form.Label>Business Address</Form.Label>
          <Form.Control type="text" placeholder="Enter business address" required value={formData.business_address} onChange={handleChange} />
        </Form.Group>
        <Button variant="primary" type="submit">
          Register
        </Button>
      </Form>
    </Container>
  );
}

export default Registration;

// src/pages/Dashboard.js
import React from "react";
import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";

function Dashboard() {
  const navigate = useNavigate();

  const barName = localStorage.getItem("barName");

  const handleOrderClick = () => {
    navigate("/orders");
  };

  const handleMenuClick = () => {
    navigate("/menu");
  };

  const handleLogOutClick = () => {
    // Clear all relevant auth data from localStorage
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("barName");
    navigate("/");
  };

  return (
    <Container className="text-center mt-5">
      {barName && <h2 className="mb-4">Restaurant: {barName}</h2>}
      <Button variant="success" size="lg" onClick={handleOrderClick}>
        Orders
      </Button>
      <Button variant="primary" size="lg" onClick={handleMenuClick}>
        Menu
      </Button>
      <Button variant="danger" size="lg" onClick={handleLogOutClick}>
        Log Out
      </Button>
    </Container>
  );
}

export default Dashboard;

// src/pages/Dashboard.js
import React from "react";
import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";

function Dashboard() {
  const navigate = useNavigate();

  const handleOrderClick = () => {
    navigate("/orders");
  };

  return (
    <Container className="text-center mt-5">
      <Button variant="success" size="lg" onClick={handleOrderClick}>
        Orders
      </Button>
    </Container>
  );
}

export default Dashboard;

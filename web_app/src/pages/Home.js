import React from "react";
import { Button, Container } from "react-bootstrap";
import { Link } from "react-router-dom";

function Home() {
  return (
    <Container className="text-center mt-5">
      <Link to="/register">
        <Button variant="primary" className="m-2">Register</Button>
      </Link>
      <Link to="/login">
        <Button variant="secondary" className="m-2">Log In</Button>
    </Link>
    </Container>
  );
}

export default Home;

import React from "react";
import { Button, Container } from "react-bootstrap";

function Home() {
  return (
    <Container className="text-center mt-5">
      <Button variant="primary" className="m-2">Register</Button>
      <Button variant="secondary" className="m-2">Log In</Button>
    </Container>
  );
}

export default Home;

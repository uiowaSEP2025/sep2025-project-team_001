import React from 'react';
import { Button, Container, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import './styles/Home.css';

function Home() {
  return (
    <Container fluid className="home-container">
      <Row className="justify-content-center align-items-center home-content">
        <Col xs={12} className="text-center">
          {/* Logo */}
          <img
            src="/images/StreamlineLogo.png"
            alt="Streamline Logo"
            className="home-logo"
          />

          {/* Buttons */}
          <div className="home-button-group">
            <Link to="/register">
              <Button variant="primary" className="home-btn">
                Register
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="secondary" className="home-btn">
                Log In
              </Button>
            </Link>
          </div>

          {/* Copyright Note */}
          <p className="home-footer">
            &copy; {new Date().getFullYear()} Streamline App. All rights
            reserved.
          </p>
        </Col>
      </Row>
    </Container>
  );
}

export default Home;

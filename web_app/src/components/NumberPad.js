import React from 'react';
import { Button, Row, Col } from 'react-bootstrap';

const NumberPad = ({ onDigitPress, onDelete, onClear, onEnter }) => {
  const digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'];

  return (
    <div className="text-center">
      <Row className="mb-2">
        {digits.slice(0, 3).map((digit) => (
          <Col key={digit}>
            <Button variant="secondary" onClick={() => onDigitPress(digit)}>
              {digit}
            </Button>
          </Col>
        ))}
      </Row>
      <Row className="mb-2">
        {digits.slice(3, 6).map((digit) => (
          <Col key={digit}>
            <Button variant="secondary" onClick={() => onDigitPress(digit)}>
              {digit}
            </Button>
          </Col>
        ))}
      </Row>
      <Row className="mb-2">
        {digits.slice(6, 9).map((digit) => (
          <Col key={digit}>
            <Button variant="secondary" onClick={() => onDigitPress(digit)}>
              {digit}
            </Button>
          </Col>
        ))}
      </Row>
      <Row className="mb-2">
        <Col>
          <Button variant="danger" onClick={onClear}>
            Clear
          </Button>
        </Col>
        <Col>
          <Button variant="secondary" onClick={() => onDigitPress('0')}>
            0
          </Button>
        </Col>
        <Col>
          <Button variant="warning" onClick={onDelete}>
            ←
          </Button>
        </Col>
      </Row>
      <Row className="mb-2">
        <Col>
          <Button variant="success" className="w-100" onClick={onEnter}>
            Enter
          </Button>
        </Col>
      </Row>
    </div>
  );
};
export default NumberPad;

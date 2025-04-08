import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import NumberPad from "../components/NumberPad";
import { Container, Row, Col, Card, Alert} from 'react-bootstrap'

const BartenderLoginPage = () => {
    const [pin, setPin] = useState("");
    const [error, setError] = useState("");
    const [barName, setBarName] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const name = sessionStorage.getItem('barName');
        if (name) {
            setBarName(name);
        }
    }, []);

    const handleDigitPress = (digit) => {
        if (pin.length < 4) {
            setPin(prev => pin + digit);
        }
    };

    const handleDelete = () => {
        setPin(prev => prev.slice(0, -1));
    }
    const handleClear = () => {
        setPin("");
    }

    const loginWithPin = async () => {
        try{
            const response = await fetch(`${process.env.REACT_APP_API_URL}/login/`, {
                method : 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({pin})
            });

            const data = await response.json();
            if(response.ok){
                navigate('/orders');
            } else {
                setError(data.message || 'Invalid PIN');
            }
        }
        catch (error) {
            console.error('Error:', error);
            setError('An error occurred while logging in.');
        }
    };

    useEffect(() => {
        if (pin.length === 4) {
            loginWithPin();
        }
    }
    , [pin]);

    return (
        <Container className="mt-5">
          <Row className="justify-content-center">
            <Col md={6}>
              <Card className="text-center p-4">
                <h3>{barName || 'Your Bar'}</h3>
                <h4>Bartender Login</h4>
    
                <div className="mb-3">
                  <h4>{'*'.repeat(pin.length)}</h4>
                </div>
    
                {error && <Alert variant="danger">{error}</Alert>}
    
                <NumberPad
                  onDigitPress={handleDigitPress}
                  onBackspace={handleDelete}
                  onClear={handleClear}
                />
              </Card>
            </Col>
          </Row>
        </Container>
      );
    };
    
    export default BartenderLoginPage;
    
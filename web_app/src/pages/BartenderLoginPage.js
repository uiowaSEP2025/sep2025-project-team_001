import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import { Container, Row, Col, Card, Image, Alert} from 'react-bootstrap'

const BartenderLoginPage = () => {
    const [pin, setPin] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleDigitPres = (digit) => {
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
            const response = await fetch('/login/', {
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

    React.useEffect(() => {

        if (pin.length === 4) {
            loginWithPin();
        }
    }
    , [pin]);

};
export default BartenderLoginPage;
    
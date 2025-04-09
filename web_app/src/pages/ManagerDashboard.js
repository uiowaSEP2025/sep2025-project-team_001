import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';

function ManagerDashboard() {
  const navigate = useNavigate();
  const barName = sessionStorage.getItem('barName');
    

  const handleMenuClick = () => {
    navigate('/menu');
  };

  const handleLogOutClick = () => {
    // Clear all relevant auth data from sessionStorage
    sessionStorage.removeItem('accessToken');
    sessionStorage.removeItem('refreshToken');
    sessionStorage.removeItem('barName');
    navigate('/');
  };

  const handleBartenderClick = () => {
    navigate('/bartender_registration')
  };

  return (
    <Container className="text-center mt-5">
        <h1 className="mb-4">Manager Dashboard</h1>
      {barName && <h2 className="mb-4">Restaurant: {barName}</h2>}
      <Button variant="primary" size="lg" onClick={handleMenuClick}>
        Menu
      </Button>
      <Button variant="primary" size="lg" onClick={handleBartenderClick}>
        Create Bartender
      </Button>
      <Button variant="danger" size="lg" onClick={handleLogOutClick}>
        Log Out
      </Button>
    </Container>
  );
}

export default ManagerDashboard;

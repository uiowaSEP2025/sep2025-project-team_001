// Full ManagerDashboard with inline editing fixes + modal auth role update + flash messages

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Box,
  Typography,
  TextField,
  Paper,
  Stack,
  MenuItem,
  Button as MuiButton,
  Snackbar,
  Alert,
  Slide,
} from '@mui/material';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import OwnerAuthModal from '../components/OwnerAuthModal';

function ManagerDashboard() {
  const navigate = useNavigate();
  const barName = sessionStorage.getItem('barName');
  const [workers, setWorkers] = useState({ managers: [], bartenders: [] });
  const [editing, setEditing] = useState({ id: null, field: null });
  const [editValue, setEditValue] = useState('');
  const [pendingRoleChange, setPendingRoleChange] = useState(null);

  const [bartenderName, setBartenderName] = useState('');
  const [bartenderPin, setBartenderPin] = useState('');
  const [bartenderError, setBartenderError] = useState('');
  const [bartenderSuccess, setBartenderSuccess] = useState('');
  const [managerName, setManagerName] = useState('');
  const [managerPin, setManagerPin] = useState('');
  const [showManagerAuthModal, setShowManagerAuthModal] = useState(false);
  const [managerError, setManagerError] = useState('');
  const [managerSuccess, setManagerSuccess] = useState('');
  const [creatingManager, setCreatingManager] = useState(false);

  const [flashMessage, setFlashMessage] = useState('');
  const [flashSeverity, setFlashSeverity] = useState('success');
  const [flashOpen, setFlashOpen] = useState(false);

  const showFlash = (message, severity = 'success') => {
    setFlashMessage(message);
    setFlashSeverity(severity);
    setFlashOpen(true);
  };

  const fetchWorkers = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/get-workers/`);
      const allWorkers = response.data.sort((a, b) => a.id - b.id);
      setWorkers({
        managers: allWorkers.filter(w => w.role === 'manager'),
        bartenders: allWorkers.filter(w => w.role === 'bartender'),
      });
    } catch (error) {
      console.error('Error fetching workers:', error);
    }
  };

  useEffect(() => {
    fetchWorkers();
  }, []);

  const handleEditStart = (workerId, field, currentValue) => {
    setEditing({ id: workerId, field });
    setEditValue(currentValue);
  };

  const handleEditSave = async () => {
    const worker = [...workers.managers, ...workers.bartenders].find(w => w.id === editing.id);
    if (!worker) return;

    const updatedWorker = { ...worker, [editing.field]: editValue };

    try {
      const response = await axios.put(`${process.env.REACT_APP_API_URL}/update-worker/${worker.id}/`, updatedWorker);
      console.log(response.data);
      setEditing({ id: null, field: null });
      setEditValue('');
      await fetchWorkers();
      showFlash('Worker updated successfully!');
    } catch (err) {
      console.error('Update failed:', err);
    }
  };

  const handleRoleChangeWithAuth = async () => {
    if (creatingManager) {
      await handleCreateManager();
      setCreatingManager(false);
      return;
    }

    if (pendingRoleChange) {
      try {
        const updatedWorker = {
          ...pendingRoleChange,
          role: 'manager'
        };

        const response = await axios.put(`${process.env.REACT_APP_API_URL}/update-worker/${pendingRoleChange.id}/`, updatedWorker);
        console.log(response.data);
        setPendingRoleChange(null);
        setShowManagerAuthModal(false);
        setEditing({ id: null, field: null });
        setEditValue('');
        await fetchWorkers();
        showFlash('Worker role updated to manager!');
      } catch (err) {
        console.error('Failed to update role after auth:', err);
      }
    }
  };

  const renderWorkerField = (worker, field) => {
    const value = worker[field];
    const isEditing = editing.id === worker.id && editing.field === field;

    if (isEditing && field === 'role') {
      return (
        <TextField
          select
          value={editValue}
          onChange={async (e) => {
            const newRole = e.target.value;
            if (worker.role !== 'manager' && newRole === 'manager') {
              setPendingRoleChange(worker);
              setShowManagerAuthModal(true);
              return;
            }

            try {
              const updatedWorker = { ...worker, role: newRole };
              const response = await axios.put(`${process.env.REACT_APP_API_URL}/update-worker/${worker.id}/`, updatedWorker);
              console.log(response.data);
              setEditing({ id: null, field: null });
              setEditValue('');
              fetchWorkers();
              showFlash('Worker role updated to bartender!');
            } catch (err) {
              console.error('Failed to update role directly:', err);
            }
          }}
          size="small"
        >
          <MenuItem value="manager">manager</MenuItem>
          <MenuItem value="bartender">bartender</MenuItem>
        </TextField>
      );
    }

    return isEditing ? (
      <TextField
        value={editValue}
        onChange={(e) => setEditValue(e.target.value)}
        onBlur={handleEditSave}
        onKeyDown={(e) => {
          if (e.key === 'Enter') handleEditSave();
          if (e.key === 'Escape') setEditing({ id: null, field: null });
        }}
        size="small"
        autoFocus
      />
    ) : (
      <span onClick={() => handleEditStart(worker.id, field, value)}>{value}</span>
    );
  };

  const renderWorkerRow = (worker) => (
    <Box key={worker.id} sx={{ display: 'flex', alignItems: 'center' }}>
      <Box sx={{ width: '40%' }}>{renderWorkerField(worker, 'name')}</Box>
      <Box sx={{ width: '30%' }}>{renderWorkerField(worker, 'role')}</Box>
      <Box sx={{ width: '30%' }}>{renderWorkerField(worker, 'pin')}</Box>
    </Box>
  );

  const handleCreateManager = async () => {
    const restaurantId = sessionStorage.getItem('restaurantId');
    if (!restaurantId) return showFlash('Restaurant ID not found.', 'error');
    if (managerPin.length !== 4 || !/^[0-9]{4}$/.test(managerPin)) return showFlash('PIN must be 4 digits', 'error');

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/create-worker/`, {
        name: managerName,
        pin: managerPin,
        role: 'manager',
        restaurant_id: restaurantId
      });
      console.log(response.data);
      setManagerName('');
      setManagerPin('');
      setShowManagerAuthModal(false);
      fetchWorkers();
      showFlash('Manager created!');
    } catch (err) {
      showFlash(err.response?.data?.error || 'Failed to create manager', 'error');
    }
  };

  const handleCreateManagerWithAuth = () => {
    setCreatingManager(true);
    setShowManagerAuthModal(true);
  };

  const handleCreateBartender = async () => {
    const restaurantId = sessionStorage.getItem('restaurantId');
    if (!restaurantId) return showFlash('Restaurant ID not found.', 'error');
    if (bartenderPin.length !== 4 || !/^[0-9]{4}$/.test(bartenderPin)) return showFlash('PIN must be 4 digits', 'error');

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/create-worker/`, {
        name: bartenderName,
        pin: bartenderPin,
        role: 'bartender',
        restaurant_id: restaurantId
      });
      console.log(response.data);
      setBartenderName('');
      setBartenderPin('');
      fetchWorkers();
      showFlash('Bartender created!');
    } catch (err) {
      showFlash(err.response?.data?.error || 'Failed to create bartender', 'error');
    }
  };

  return (
    <Box sx={{ overflowY: 'auto', maxHeight: '100vh', pb: 10 }}>
      <Container className="text-center mt-5">
        <h1 className="mb-4">Manager Dashboard</h1>
        {barName && <h2 className="mb-4">Restaurant: {barName}</h2>}

        <Button variant="primary" size="lg" onClick={() => navigate('/menu')} className="mb-3">Menu</Button>
        <Button variant="primary" size="lg" onClick={() => navigate('/orders')} className="mb-3">Orders</Button>
        <Button variant="danger" size="lg" onClick={() => navigate('/dashboard')}>Log Out</Button>

        {/* Manager Section */}
        <Box className="mt-4" sx={{ maxWidth: 600, mx: 'auto' }}>
          <Typography variant="h5">Managers</Typography>
          <Paper elevation={2} sx={{ p: 2 }}>
            <Stack spacing={1}>
              <Box sx={{ display: 'flex', fontWeight: 'bold' }}>
                <Box sx={{ width: '40%' }}>Name</Box>
                <Box sx={{ width: '30%' }}>Role</Box>
                <Box sx={{ width: '30%' }}>PIN</Box>
              </Box>
              {workers.managers.map(renderWorkerRow)}
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <TextField label="Name" size="small" value={managerName} onChange={(e) => setManagerName(e.target.value)} sx={{ width: '40%', mr: 1 }} />
                <TextField label="4-digit PIN" size="small" type="password" value={managerPin} onChange={(e) => setManagerPin(e.target.value)} sx={{ width: '30%', mr: 1 }} />
                <MuiButton variant="contained" onClick={handleCreateManagerWithAuth}>+ Add</MuiButton>
              </Box>
            </Stack>
          </Paper>
        </Box>

        {/* Bartender Section */}
        <Box className="mt-4 mb-5" sx={{ maxWidth: 600, mx: 'auto' }}>
          <Typography variant="h5">Bartenders</Typography>
          <Paper elevation={2} sx={{ p: 2 }}>
            <Stack spacing={1}>
              <Box sx={{ display: 'flex', fontWeight: 'bold' }}>
                <Box sx={{ width: '40%' }}>Name</Box>
                <Box sx={{ width: '30%' }}>Role</Box>
                <Box sx={{ width: '30%' }}>PIN</Box>
              </Box>
              {workers.bartenders.map(renderWorkerRow)}
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <TextField label="Name" size="small" value={bartenderName} onChange={(e) => setBartenderName(e.target.value)} sx={{ width: '40%', mr: 1 }} />
                <TextField label="4-digit PIN" size="small" type="password" value={bartenderPin} onChange={(e) => setBartenderPin(e.target.value)} sx={{ width: '30%', mr: 1 }} />
                <MuiButton variant="contained" onClick={handleCreateBartender}>+ Add</MuiButton>
              </Box>
            </Stack>
          </Paper>
        </Box>

        <OwnerAuthModal
          show={showManagerAuthModal}
          onHide={() => setShowManagerAuthModal(false)}
          onOwnerAuthenticated={handleRoleChangeWithAuth}
        />

        <Snackbar
          open={flashOpen}
          autoHideDuration={3000}
          onClose={() => setFlashOpen(false)}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
          TransitionComponent={(props) => <Slide {...props} direction="down" />}
        >
          <Alert onClose={() => setFlashOpen(false)} severity={flashSeverity} sx={{ width: '100%', fontWeight: 'bold', fontSize: '1rem' }}>
            {flashMessage}
          </Alert>
        </Snackbar>
      </Container>
    </Box>
  );
}

export default ManagerDashboard;
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
  IconButton,
  Dialog,
  DialogActions,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import OwnerAuthModal from '../components/OwnerAuthModal';
import './styles/ManagerDashboard.css';

function ManagerDashboard() {
  const navigate = useNavigate();
  const barName = sessionStorage.getItem('barName');
  const [workers, setWorkers] = useState({ managers: [], bartenders: [] });
  const [editing, setEditing] = useState({ id: null, field: null });
  const [editValue, setEditValue] = useState('');
  const [pendingRoleChange, setPendingRoleChange] = useState(null);

  const [workerName, setWorkerName] = useState('');
  const [workerPin, setWorkerPin] = useState('');
  const [workerRole, setWorkerRole] = useState('bartender');
  const [showManagerAuthModal, setShowManagerAuthModal] = useState(false);
  const [creatingManager, setCreatingManager] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [deletingWorker, setDeletingWorker] = useState(null);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [dailyStats, setDailyStats] = useState(null);

  const [flashMessage, setFlashMessage] = useState('');
  const [flashSeverity, setFlashSeverity] = useState('success');
  const [flashOpen, setFlashOpen] = useState(false);

  const showFlash = (message, severity = 'success') => {
    setFlashOpen(false);
    setTimeout(() => {
      setFlashMessage(message);
      setFlashSeverity(severity);
      setFlashOpen(true);
    }, 50); // Small delay to ensure re-open works
  };

  const fetchDailyStats = async () => {
    const today = new Date().toISOString().split('T')[0]; // format YYYY-MM-DD
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_URL}/daily_stats?date=${today}`,
      );
      setDailyStats(response.data);
    } catch (err) {
      console.error('Failed to fetch daily stats:', err);
    }
  };

  const fetchWorkers = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_URL}/get-workers/`,
      );
      const allWorkers = response.data.sort((a, b) => a.id - b.id);
      setWorkers({
        managers: allWorkers.filter((w) => w.role === 'manager'),
        bartenders: allWorkers.filter((w) => w.role === 'bartender'),
      });
    } catch (error) {
      console.error('Error fetching workers:', error);
    }
  };

  useEffect(() => {
    fetchWorkers();
    fetchDailyStats();
  }, []);

  const handleEditStart = (workerId, field, currentValue) => {
    setEditing({ id: workerId, field });
    setEditValue(currentValue);
  };

  const handleEditSave = async () => {
    const worker = [...workers.managers, ...workers.bartenders].find(
      (w) => w.id === editing.id,
    );
    if (!worker) return;

    // Prevent saving if no changes were made
    if (editValue === worker[editing.field]) {
      setEditing({ id: null, field: null });
      return;
    }

    // PIN validation
    if (editing.field === 'pin') {
      if (editValue.length !== 4 || !/^[0-9]{4}$/.test(editValue)) {
        showFlash('PIN must be exactly 4 digits', 'error');
        return;
      }

      const allWorkers = [...workers.managers, ...workers.bartenders];
      const duplicate = allWorkers.find(
        (w) => w.pin === editValue && w.id !== worker.id,
      );
      if (duplicate) {
        showFlash('PIN already in use for this restaurant', 'error');
        return;
      }
    }

    const updatedWorker = { ...worker, [editing.field]: editValue };

    try {
      const response = await axios.put(
        `${process.env.REACT_APP_API_URL}/update-worker/${worker.id}/`,
        updatedWorker,
      );
      console.log(response.data);
      setEditing({ id: null, field: null });
      setEditValue('');
      await fetchWorkers();
      showFlash('Worker updated successfully!');
    } catch (err) {
      console.error('Update failed:', err);
      showFlash(
        err.response?.data?.error || 'Failed to update worker',
        'error',
      );
    }
  };

  const handleRoleChangeWithAuth = async () => {
    if (creatingManager) {
      setCreatingManager(false);
      try {
        const restaurantId = sessionStorage.getItem('restaurantId');
        const response = await axios.post(
          `${process.env.REACT_APP_API_URL}/create-worker/`,
          {
            name: workerName,
            pin: workerPin,
            role: 'manager',
            restaurant_id: restaurantId,
          },
        );
        console.log(response.data);
        setWorkerName('');
        setWorkerPin('');
        setWorkerRole('bartender');
        setShowManagerAuthModal(false);
        fetchWorkers();
        showFlash('Manager created!');
      } catch (err) {
        showFlash(
          err.response?.data?.error || 'Failed to create manager',
          'error',
        );
      }
      return;
    }

    if (pendingRoleChange) {
      try {
        const updatedWorker = {
          ...pendingRoleChange,
          role: 'manager',
        };

        const response = await axios.put(
          `${process.env.REACT_APP_API_URL}/update-worker/${pendingRoleChange.id}/`,
          updatedWorker,
        );
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
            if (worker.role === 'manager' && newRole === 'bartender') {
              const numManagers = workers.managers.length;
              if (numManagers <= 1) {
                showFlash('At least one manager is required', 'error');
                return;
              }
            }

            if (worker.role !== 'manager' && newRole === 'manager') {
              setPendingRoleChange(worker);
              setShowManagerAuthModal(true);
              return;
            }

            try {
              const updatedWorker = { ...worker, role: newRole };
              const response = await axios.put(
                `${process.env.REACT_APP_API_URL}/update-worker/${worker.id}/`,
                updatedWorker,
              );
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
      <span onClick={() => handleEditStart(worker.id, field, value)}>
        {value}
      </span>
    );
  };

  const renderWorkerRow = (worker) => (
    <Box key={worker.id} sx={{ display: 'flex', alignItems: 'center' }}>
      <Box sx={{ width: '40%' }}>{renderWorkerField(worker, 'name')}</Box>
      <Box sx={{ width: '30%' }}>{renderWorkerField(worker, 'role')}</Box>
      <Box
        sx={{
          width: '30%',
          position: 'relative',
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <Box>{renderWorkerField(worker, 'pin')}</Box>
        <IconButton
          color="error"
          size="small"
          onClick={() => {
            setDeletingWorker(worker);
            setConfirmOpen(true);
          }}
          sx={{
            position: 'absolute',
            right: 0,
            top: '50%',
            transform: 'translateY(-50%)',
          }}
        >
          <DeleteIcon />
        </IconButton>
      </Box>
    </Box>
  );

  const handleCreateWorker = async () => {
    const restaurantId = sessionStorage.getItem('restaurantId');
    if (!restaurantId) return showFlash('Restaurant ID not found.', 'error');
    if (workerPin.length !== 4 || !/^[0-9]{4}$/.test(workerPin))
      return showFlash('PIN must be 4 digits', 'error');

    if (workerRole === 'manager') {
      setCreatingManager(true);
      setShowManagerAuthModal(true);
      return;
    }

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/create-worker/`,
        {
          name: workerName,
          pin: workerPin,
          role: workerRole,
          restaurant_id: restaurantId,
        },
      );
      console.log(response.data);
      setWorkerName('');
      setWorkerPin('');
      setWorkerRole('bartender');
      fetchWorkers();
      showFlash('Employee created!');
    } catch (err) {
      showFlash(
        err.response?.data?.error || 'Failed to create employee',
        'error',
      );
    }
  };

  return (
    <Box sx={{ overflowY: 'auto', maxHeight: '100vh', pb: 10 }}>
      <Container className="manager-dashboard">
        {barName && <h2>Restaurant: {barName}</h2>}

        {/* Top Controls */}
        <div className="top-controls">
          <div className="left-buttons">
            <Button variant="primary" size="lg" onClick={() => navigate('/menu')}>Menu</Button>
            <Button variant="primary" size="lg" onClick={() => navigate('/orders')}>Orders</Button>
            <Button variant="primary" size="lg" onClick={() => navigate('/product_statistics')}>Product Statistics</Button>
            <Button variant="primary" size = "lg" onClick={() => navigate('/reviews')}>Customer Reviews</Button>
            <Button variant="primary" size="lg" onClick={() => navigate('/promotions')}>Promotions</Button>
          </div>
          <Button
            variant="danger"
            size="lg"
            onClick={() => navigate('/dashboard')}
            className="logout"
          >
            Log Out
          </Button>
        </div>

        <div className="panel-wrapper">
          {/* Left Panel - Daily Stats */}
          {dailyStats && (
            <Paper className="panel" elevation={4}>
              <Typography variant="h5" gutterBottom>
                📊 Today's Stats
              </Typography>
              <Typography>
                <strong>Total Orders:</strong> {dailyStats.total_orders}
              </Typography>
              <Typography>
                <strong>Total Sales:</strong> $
                {dailyStats.total_sales.toFixed(2)}
              </Typography>
              <Typography>
                <strong>Average Order Value:</strong> $
                {dailyStats.avg_order_value.toFixed(2)}
              </Typography>
              <Typography>
                <strong>Active Workers:</strong> {dailyStats.active_workers}
              </Typography>
            </Paper>
          )}

          {/* Right Panel - Employees */}
          <Paper className="panel" elevation={4}>
            <Typography variant="h5" gutterBottom>
              👨‍🍳 Employees
            </Typography>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Stack spacing={1}>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    mb: 2,
                  }}
                >
                  <TextField
                    label="Search by name"
                    size="small"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    sx={{ width: '60%' }}
                  />
                  <TextField
                    select
                    label="Filter by role"
                    value={roleFilter}
                    onChange={(e) => setRoleFilter(e.target.value)}
                    size="small"
                    sx={{ width: '35%' }}
                  >
                    <MenuItem value="all">All</MenuItem>
                    <MenuItem value="manager">Manager</MenuItem>
                    <MenuItem value="bartender">Bartender</MenuItem>
                  </TextField>
                </Box>

                <Box
                  sx={{
                    display: 'flex',
                    fontWeight: 'bold',
                    justifyContent: 'space-between',
                  }}
                >
                  <Box sx={{ width: '40%' }}>Name</Box>
                  <Box sx={{ width: '30%' }}>Role</Box>
                  <Box sx={{ width: '30%', textAlign: 'center' }}>PIN</Box>
                </Box>

                {[...workers.managers, ...workers.bartenders]
                  .sort((a, b) => a.id - b.id)
                  .filter((worker) => {
                    const nameMatch = worker.name
                      .toLowerCase()
                      .includes(searchTerm.toLowerCase());
                    const roleMatch =
                      roleFilter === 'all' || worker.role === roleFilter;
                    return nameMatch && roleMatch;
                  })
                  .map(renderWorkerRow)}

                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <TextField
                    label="Name"
                    size="small"
                    value={workerName}
                    onChange={(e) => setWorkerName(e.target.value)}
                    sx={{ width: '30%', mr: 1 }}
                  />
                  <TextField
                    label="4-digit PIN"
                    size="small"
                    type="password"
                    value={workerPin}
                    onChange={(e) => setWorkerPin(e.target.value)}
                    sx={{ width: '30%', mr: 1 }}
                  />
                  <TextField
                    select
                    label="Role"
                    value={workerRole}
                    onChange={(e) => setWorkerRole(e.target.value)}
                    size="small"
                    sx={{ width: '20%', mr: 1 }}
                  >
                    <MenuItem value="manager">manager</MenuItem>
                    <MenuItem value="bartender">bartender</MenuItem>
                  </TextField>
                  <MuiButton variant="contained" onClick={handleCreateWorker}>
                    + Add
                  </MuiButton>
                </Box>
              </Stack>
            </Paper>
          </Paper>
        </div>

        <OwnerAuthModal
          show={showManagerAuthModal}
          onHide={() => setShowManagerAuthModal(false)}
          onOwnerAuthenticated={handleRoleChangeWithAuth}
        />

        {/* Delete Confirmation Dialog */}
        <Dialog open={confirmOpen} onClose={() => setConfirmOpen(false)}>
          <Box sx={{ p: 2 }}>
            <Typography>
              Are you sure you want to remove{' '}
              <strong>{deletingWorker?.name}</strong>?
            </Typography>
          </Box>
          <DialogActions>
            <MuiButton onClick={() => setConfirmOpen(false)}>Cancel</MuiButton>
            <MuiButton
              color="error"
              onClick={async () => {
                try {
                  if (
                    deletingWorker.role === 'manager' &&
                    workers.managers.length <= 1
                  ) {
                    showFlash('At least one manager is required.', 'error');
                    return;
                  }
                  const response = await axios.delete(
                    `${process.env.REACT_APP_API_URL}/delete-worker/${deletingWorker.id}/`,
                  );
                  console.log(response.data);
                  setConfirmOpen(false);
                  setDeletingWorker(null);
                  fetchWorkers();
                  showFlash('Employee removed successfully!');
                } catch (err) {
                  console.error('Delete failed:', err);
                  showFlash('Failed to remove employee.', 'error');
                }
              }}
            >
              Remove
            </MuiButton>
          </DialogActions>
        </Dialog>

        <Snackbar
          open={flashOpen}
          autoHideDuration={3000}
          onClose={() => setFlashOpen(false)}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
          TransitionComponent={(props) => <Slide {...props} direction="down" />}
        >
          <Alert
            onClose={() => setFlashOpen(false)}
            severity={flashSeverity}
            sx={{ width: '100%', fontWeight: 'bold', fontSize: '1rem' }}
          >
            {flashMessage}
          </Alert>
        </Snackbar>
      </Container>
    </Box>
  );
}

export default ManagerDashboard;

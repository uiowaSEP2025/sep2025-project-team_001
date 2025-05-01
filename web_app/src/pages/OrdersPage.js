import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Checkbox,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  FormControlLabel,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
  CircularProgress
} from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const OrdersPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const navigate = useNavigate();
  const [statusFilter, setStatusFilter] = useState([
    'pending',
    'in_progress',
    'completed',
    'picked_up',
    'cancelled',
  ]);
  const [searchTerm, setSearchTerm] = useState('');
  const [workerSearchTerm, setWorkerSearchTerm] = useState('');

  const statusColorMap = {
    pending: 'secondary',
    in_progress: 'warning',
    completed: 'info',
    picked_up: 'success',
    cancelled: 'error'
  };;

  const handleUpdateOrderStatus = async (orderId, nextStatus) => {
    try {
      const restaurantId = sessionStorage.getItem('restaurantId');
      const workerID = sessionStorage.getItem('workerId');
      const workerName = sessionStorage.getItem('workerName');
  
      const currentOrder = orders.find((o) => o.id === orderId);
      const isAssigningWorker = currentOrder.status === 'pending' && nextStatus === 'in_progress';
  
      const response = await axios.patch(
        `${process.env.REACT_APP_API_URL}/orders/${restaurantId}/${orderId}/${nextStatus}/`,
        isAssigningWorker ? { worker_id: workerID } : {},
      );
  
      const updatedData = {
        ...response.data,
        ...(isAssigningWorker ? { worker_name: workerName } : {})
      };
  
      const updatedOrders = orders.map((order) =>
        order.id === orderId ? { ...order, ...updatedData } : order
      );
      setOrders(updatedOrders);
  
      setSelectedOrder((prev) => (prev ? { ...prev, ...updatedData } : null));
    } catch (error) {
      console.error('Error updating order status: ', error);
    }
  };  

  const handleUpdateCategoryStatus = async (orderId, category, newStatus) => {
    try {
      const restaurantId = sessionStorage.getItem('restaurantId');
      const response = await axios.patch(
        `${process.env.REACT_APP_API_URL}/orders/${restaurantId}/${orderId}/${category}/${newStatus}/`
      );

      const updated = response.data;
      setSelectedOrder((prev) => prev ? { ...prev, ...updated } : null);
      setOrders((prev) =>
        prev.map((o) => o.id === updated.order_id ? { ...o, ...updated } : o)
      );
    } catch (err) {
      console.error('Error updating category status:', err);
    }
  };

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/retrieve/orders/`);
        setOrders((prev) => JSON.stringify(prev) !== JSON.stringify(response.data) ? response.data : prev);
        if (loading) setLoading(false);
      } catch (error) {
        console.error('Error fetching orders:', error);
        if (loading) setLoading(false);
      }
    };

    fetchOrders();
    const intervalId = setInterval(fetchOrders, 3000);
    return () => clearInterval(intervalId);
  }, []);

  const formatStatus = (status) => status.replace('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <Box p={3}>
      <Button
        variant="contained"
        color="error"
        onClick={() => navigate('/dashboard')}
        sx={{ mb: 2 }}
      >
        Log Out
      </Button>

      <Typography variant="h4" align="center" gutterBottom>Active Orders</Typography>

      <Stack direction="row" spacing={2} alignItems="center" flexWrap="wrap" mb={2}>
        {['pending', 'in_progress', 'completed', 'picked_up', 'cancelled'].map((status) => (
          <FormControlLabel
            key={status}
            control={
              <Checkbox
                checked={statusFilter.includes(status)}
                onChange={() =>
                  setStatusFilter((prev) =>
                    prev.includes(status) ? prev.filter((s) => s !== status) : [...prev, status]
                  )
                }
              />
            }
            label={formatStatus(status)}
          />
        ))}
      </Stack>

      <Stack direction="row" spacing={2} mb={3}>
        <TextField
          label="Search Customer"
          variant="outlined"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <TextField
          label="Search Worker"
          variant="outlined"
          value={workerSearchTerm}
          onChange={(e) => setWorkerSearchTerm(e.target.value)}
        />
      </Stack>

      {loading ? (
        <Box textAlign="center"><CircularProgress /></Box>
      ) : (
        <TableContainer component={Paper} elevation={3} sx={{ borderRadius: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Order #</TableCell>
                <TableCell>Customer</TableCell>
                <TableCell>ETA</TableCell>
                <TableCell>Total Price</TableCell>
                <TableCell>Worker</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {orders
                .filter((order) =>
                  statusFilter.includes(order.status) &&
                  order.customer_name.toLowerCase().includes(searchTerm.toLowerCase()) &&
                  (!order.worker_name || order.worker_name.toLowerCase().includes(workerSearchTerm.toLowerCase()))
                )
                .map((order) => (
                  <TableRow
                    key={order.id}
                    hover
                    onClick={() => setSelectedOrder(order)}
                    sx={{
                      cursor: 'pointer',
                      backgroundColor: '#fafafa',
                      '&:hover': { backgroundColor: '#f0f0f0' },
                      ...(order.status === 'cancelled' && {
                        outline: '2px solid #f44336',
                        backgroundColor: '#ffebee'
                      })
                    }}
                  >
                    <TableCell>{order.id}</TableCell>
                    <TableCell>{order.customer_name}</TableCell>
                    <TableCell>
                      {order.food_eta_minutes && <div><strong>Food:</strong> {order.food_eta_minutes} min</div>}
                      {order.beverage_eta_minutes && <div><strong>Bev:</strong> {order.beverage_eta_minutes} min</div>}
                    </TableCell>
                    <TableCell>${Number(order.total_price).toFixed(2)}</TableCell>
                    <TableCell>{order.worker_name || '-'}</TableCell>
                    <TableCell>
                      <Chip
                        label={formatStatus(order.status)}
                        color={statusColorMap[order.status] || 'default'}
                        variant="outlined"
                      />
                    </TableCell>
                  </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <Dialog open={!!selectedOrder} onClose={() => setSelectedOrder(null)} maxWidth="md" fullWidth>
        <DialogTitle>Order Details</DialogTitle>
        <DialogContent>
          {selectedOrder && (
            <Stack spacing={3}>
              {['beverage', 'food'].map((category, idx) => {
                const items = selectedOrder.order_items.filter((item) =>
                  (category === 'beverage'
                    ? item.category?.toLowerCase() === 'beverage'
                    : item.category?.toLowerCase() !== 'beverage')
                );
                if (!items.length) return null;
                const status = category === 'beverage' ? selectedOrder.beverage_status : selectedOrder.food_status;

                return (
                  <Box key={category}>
                    {idx === 1 && <Divider sx={{ my: 2 }} />}
                    <Typography variant="h6" gutterBottom>
                      {category === 'beverage' ? 'Beverages' : 'Food'} (Status: {formatStatus(status)})
                    </Typography>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Item</TableCell>
                          <TableCell>Quantity</TableCell>
                          <TableCell>Unwanted Ingredients</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {items.map((item, index) => (
                          <TableRow key={index}>
                            <TableCell>{item.item_name}</TableCell>
                            <TableCell>{item.quantity}</TableCell>
                            <TableCell>
                              {item.unwanted_ingredient_names?.length > 0
                                ? `${item.unwanted_ingredient_names.length} Ingredient(s): ${item.unwanted_ingredient_names.join(', ')}`
                                : 'N/A'}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>

                    {status === 'in_progress' && (
                      <Button
                        variant="contained"
                        color="info"
                        sx={{ mt: 1 }}
                        onClick={() => handleUpdateCategoryStatus(selectedOrder.id, category, 'completed')}
                      >
                        Mark {category} Completed
                      </Button>
                    )}
                    {status === 'completed' && (
                      <Button
                        variant="contained"
                        color="success"
                        sx={{ mt: 1 }}
                        onClick={() => handleUpdateCategoryStatus(selectedOrder.id, category, 'picked_up')}
                      >
                        Mark {category} Picked Up
                      </Button>
                    )}
                  </Box>
                );
              })}
            </Stack>
          )}
        </DialogContent>
        <DialogActions>
          {selectedOrder?.status === 'pending' && (
            <Button
              variant="contained"
              color="warning"
              onClick={() => handleUpdateOrderStatus(selectedOrder.id, 'in_progress')}
            >
              Mark In Progress
            </Button>
          )}
          <Button onClick={() => setSelectedOrder(null)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default OrdersPage;
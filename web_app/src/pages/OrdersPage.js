import React, { useEffect, useRef, useState } from 'react';
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
  const [offset, setOffset] = useState(0);
  const [nextOffset, setNextOffset] = useState(null);
  const [fetching, setFetching] = useState(false);
  const [totalCount, setTotalCount] = useState(0);
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
  const fullOrderMap = useRef({});
  const loadedLimit = useRef(3);
  const role = sessionStorage.getItem('workerRole');

  const statusColorMap = {
    pending: 'secondary',
    in_progress: 'warning',
    completed: 'info',
    picked_up: 'success',
    cancelled: 'error'
  };

  const fetchOrders = async ({ statuses, limit, replace = false }) => {
    if (fetching) return;
    setFetching(true);
    try {
      const query = new URLSearchParams({
        statuses: statuses.join(','),
        limit: limit.toString(),
      });

      const response = await axios.get(`${process.env.REACT_APP_API_URL}/retrieve/orders/?${query}`);
      const data = response.data;

      const newMap = { ...fullOrderMap.current };
      for (const order of data.results) {
        newMap[order.id] = order;
      }
      fullOrderMap.current = newMap;

      const sortedOrders = Object.values(newMap)
        .sort((a, b) => new Date(b.start_time) - new Date(a.start_time))
        .slice(0, limit);

      setOrders(sortedOrders);
      setNextOffset(data.next_offset);
      setTotalCount(data.total);
    } catch (err) {
      console.error('Error fetching orders:', err);
    } finally {
      setLoading(false);
      setFetching(false);
    }
  };

  useEffect(() => {
    fullOrderMap.current = {};
    loadedLimit.current = 20;
    fetchOrders({ statuses: statusFilter, limit: loadedLimit.current });

    const intervalId = setInterval(() => {
      fetchOrders({ statuses: statusFilter, limit: loadedLimit.current });
    }, 3000);

    return () => clearInterval(intervalId);
  }, [statusFilter]);

  const handleStatusFilterChange = (status) => {
    const newStatuses = statusFilter.includes(status)
      ? statusFilter.filter(s => s !== status)
      : [...statusFilter, status];
    setStatusFilter(newStatuses);
    setLoading(true);
  };

  const handleLoadMore = () => {
    loadedLimit.current += 10;
    fetchOrders({ statuses: statusFilter, limit: loadedLimit.current });
  };

  const handleUpdateOrderStatus = async (orderId, nextStatus) => {
    try {
      const restaurantId = sessionStorage.getItem('restaurantId');
      const workerId = sessionStorage.getItem('workerId');
      const workerName = sessionStorage.getItem('workerName');

      const currentOrder = orders.find(o => o.id === orderId);
      const isAssigningWorker = currentOrder.status === 'pending' && nextStatus === 'in_progress';

      const response = await axios.patch(
        `${process.env.REACT_APP_API_URL}/orders/${restaurantId}/${orderId}/${nextStatus}/`,
        isAssigningWorker ? { worker_id: workerId } : {}
      );

      console.log(response.data)

      const updatedData = {
        ...response.data,
        ...(isAssigningWorker ? { worker_name: workerName } : {})
      };

      fullOrderMap.current[orderId] = {
        ...fullOrderMap.current[orderId],
        ...updatedData
      };
      const sortedOrders = Object.values(fullOrderMap.current)
        .sort((a, b) => new Date(b.start_time) - new Date(a.start_time))
        .slice(0, loadedLimit.current);
      setOrders(sortedOrders);
      setSelectedOrder(prev => (prev ? { ...prev, ...updatedData } : null));
    } catch (err) {
      console.error('Error updating order status:', err);
    }
  };

  const handleUpdateCategoryStatus = async (orderId, category, newStatus) => {
    try {
      const restaurantId = sessionStorage.getItem('restaurantId');
      const response = await axios.patch(
        `${process.env.REACT_APP_API_URL}/orders/${restaurantId}/${orderId}/${category}/${newStatus}/`
      );

      console.log(response.data)

      const updated = response.data;
      fullOrderMap.current[orderId] = {
        ...fullOrderMap.current[orderId],
        ...updated
      };
      const sortedOrders = Object.values(fullOrderMap.current)
        .sort((a, b) => new Date(b.start_time) - new Date(a.start_time))
        .slice(0, loadedLimit.current);
      setOrders(sortedOrders);
      setSelectedOrder(prev => (prev ? { ...prev, ...updated } : null));
    } catch (err) {
      console.error('Error updating category status:', err);
    }
  };

  const formatStatus = status =>
    status.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase());

  return (
    <Box p={3} pb={8}>
      <Box mb={2}>
        {role?.toLowerCase() === 'manager' ? (
          <Button variant="contained" color="primary" onClick={() => navigate('/manager_dashboard')}>
            Dashboard
          </Button>
        ) : (
          <Button variant="contained" color="error" onClick={() => navigate('/dashboard')}>
            Log Out
          </Button>
        )}
      </Box>
      <Typography variant="h4" align="center" gutterBottom>Active Orders</Typography>

      <Stack direction="row" spacing={2} alignItems="center" flexWrap="wrap" mb={2}>
        {['pending', 'in_progress', 'completed', 'picked_up', 'cancelled'].map(status => (
          <FormControlLabel
            key={status}
            control={<Checkbox checked={statusFilter.includes(status)} onChange={() => handleStatusFilterChange(status)} />}
            label={formatStatus(status)}
          />
        ))}
      </Stack>

      <Stack direction="row" spacing={2} mb={3}>
        <TextField label="Search Customer" variant="outlined" value={searchTerm} onChange={e => setSearchTerm(e.target.value)} />
        <TextField label="Search Worker" variant="outlined" value={workerSearchTerm} onChange={e => setWorkerSearchTerm(e.target.value)} />
      </Stack>

      {loading ? (
        <Box textAlign="center"><CircularProgress /></Box>
      ) : (
        <>
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
                  .filter(order =>
                    statusFilter.includes(order.status) &&
                    order.customer_name.toLowerCase().includes(searchTerm.toLowerCase()) &&
                    (workerSearchTerm === '' || order.worker_name?.toLowerCase().includes(workerSearchTerm.toLowerCase()))
                  )
                  .map(order => (
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

          {orders.length < totalCount && (
            <Box textAlign="center" mt={2}>
              <Button variant="contained" onClick={handleLoadMore}>Load More Orders</Button>
            </Box>
          )}
        </>
      )}

      <Dialog open={!!selectedOrder} onClose={() => setSelectedOrder(null)} maxWidth="md" fullWidth>
        <DialogTitle>Order Details</DialogTitle>
        <DialogContent>
          {selectedOrder && (
            <Stack spacing={3}>
              {['beverage', 'food'].map((category, idx) => {
                const items = selectedOrder.order_items.filter(item =>
                  category === 'beverage'
                    ? item.category?.toLowerCase() === 'beverage'
                    : item.category?.toLowerCase() !== 'beverage'
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
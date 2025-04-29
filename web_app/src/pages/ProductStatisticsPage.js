import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Grid,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const StatisticsPage = () => {
  const [productStats, setProductStats] = useState([]);
  const [workerStats, setWorkerStats] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [productRes, workerRes] = await Promise.all([
          axios.get(`${process.env.REACT_APP_API_URL}/api/statistics/`),
          axios.get(`${process.env.REACT_APP_API_URL}/bartender-statistics/`),
        ]);

        console.log(workerRes.data)
        setProductStats(productRes.data.items || []);
        setWorkerStats(workerRes.data.bartender_statistics || []);
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    };

    fetchStats();
  }, []);

  return (
    <Box sx={{ mt: 4, px: 6 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Button onClick={() => navigate('/manager_dashboard')}>Back to Dashboard</Button>
        <Typography variant="h4">Statistics</Typography>
        <Box width={100} />
      </Box>

      <Grid container spacing={4}>
        {/* Left Side - Worker Statistics */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" sx={{ mb: 2 }}>Worker Statistics</Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell><strong>Name</strong></TableCell>
                    <TableCell><strong>Role</strong></TableCell>
                    <TableCell><strong>Orders</strong></TableCell>
                    <TableCell><strong>Avg Time</strong></TableCell>
                    <TableCell><strong>Sales</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {workerStats.map((worker, index) => (
                    <TableRow key={index}>
                      <TableCell>{worker.worker_name}</TableCell>
                      <TableCell>
                        {worker.role ? worker.role.charAt(0).toUpperCase() + worker.role.slice(1) : ''}
                      </TableCell>
                      <TableCell>{worker.total_orders}</TableCell>
                      <TableCell>
                        {worker.average_time_seconds !== null
                          ? `${worker.average_time_seconds.toFixed(1)} sec`
                          : 'N/A'}
                      </TableCell>
                      <TableCell>${worker.total_sales.toFixed(2)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        {/* Right Side - Product Statistics */}
        <Grid item xs={12} md={8}>
          <Paper elevation={3}>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell><strong>Item Name</strong></TableCell>
                    <TableCell><strong>Price</strong></TableCell>
                    <TableCell><strong># Ordered</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {productStats.map((item, index) => (
                    <TableRow key={index}>
                      <TableCell>{item.name}</TableCell>
                      <TableCell>${parseFloat(item.price).toFixed(2)}</TableCell>
                      <TableCell>{item.times_ordered}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StatisticsPage;
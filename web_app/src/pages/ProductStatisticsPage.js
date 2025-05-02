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

        console.log(workerRes.data);

        setProductStats(productRes.data.items || []);
        setWorkerStats(workerRes.data.bartender_statistics || []);
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    };

    fetchStats();
  }, []);

  const uniformRowSx = {
    height: 56,
    '& td, & th': {
      paddingTop: 1,
      paddingBottom: 1,
      height: 56,
      verticalAlign: 'middle',
      textAlign: 'center',
    },
  };

  return (
    <Box sx={{ mt: 4, px: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'center', mb: 4 }}>
        <Typography variant="h4" align="center">Statistics</Typography>
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
        <Button variant="outlined" onClick={() => navigate('/manager_dashboard')}>
          Back to Dashboard
        </Button>
      </Box>

      <Grid container spacing={4} justifyContent="center">
        {/* Worker Statistics */}
        <Grid item xs={12} md={5}>
          <Paper elevation={4} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" align="center" sx={{ mb: 2 }}>
              Worker Statistics
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow sx={uniformRowSx}>
                    <TableCell><strong>Name</strong></TableCell>
                    <TableCell><strong>Role</strong></TableCell>
                    <TableCell><strong>Orders</strong></TableCell>
                    <TableCell><strong>Avg Time</strong></TableCell>
                    <TableCell><strong>Sales</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {workerStats.map((worker, index) => (
                    <TableRow key={index} sx={uniformRowSx}>
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

        {/* Product Statistics */}
        <Grid item xs={12} md={7}>
          <Paper elevation={4} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" align="center" sx={{ mb: 2 }}>
              Product Statistics
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow sx={uniformRowSx}>
                    <TableCell><strong>Item Name</strong></TableCell>
                    <TableCell><strong>Price</strong></TableCell>
                    <TableCell><strong># Ordered</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {productStats.map((item, index) => (
                    <TableRow key={index} sx={uniformRowSx}>
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
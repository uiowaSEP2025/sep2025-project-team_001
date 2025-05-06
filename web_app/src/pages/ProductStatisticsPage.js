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
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  TextField,
  ToggleButton,
  ToggleButtonGroup,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const StatisticsPage = () => {
  const [itemStats, setItemStats] = useState([]);
  const [workerStats, setWorkerStats] = useState([]);
  const [salesData, setSalesData] = useState([]);
  const [timeRange, setTimeRange] = useState('week');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortOption, setSortOption] = useState('total_sales');
  const [sortOrder, setSortOrder] = useState('desc');
  const [selectedCategory, setSelectedCategory] = useState('worker');
  const [itemSortOption, setItemSortOption] = useState('sales');
  const [itemSortOrder, setItemSortOrder] = useState('desc');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [itemRes, workerRes] = await Promise.all([
          axios.get(`${process.env.REACT_APP_API_URL}/api/statistics/`),
          axios.get(`${process.env.REACT_APP_API_URL}/bartender-statistics/`),
        ]);
        setItemStats(itemRes.data.items || []);
        setWorkerStats(workerRes.data.bartender_statistics || []);
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    };

    fetchStats();
  }, []);

  useEffect(() => {
    const fetchSalesData = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_URL}/restaurant-statistics/?range=${timeRange}`,
        );

        const dataMap = new Map(
          res.data.map((d) => [
            new Date(d.period).toISOString(),
            d.total_sales,
          ]),
        );

        let formatted = [];
        const now = new Date();

        if (timeRange === 'day') {
          for (let h = 0; h < 24; h++) {
            const hour = new Date(now);
            hour.setHours(h, 0, 0, 0);
            const label =
              h % 4 === 0
                ? hour.toLocaleTimeString([], { hour: 'numeric', hour12: true })
                : '';
            formatted.push({
              date: label,
              fullLabel: hour.toLocaleTimeString([], {
                hour: 'numeric',
                minute: '2-digit',
              }),
              sales: dataMap.get(hour.toISOString()) || 0,
            });
          }
        } else if (timeRange === 'week') {
          for (let i = 6; i >= 0; i--) {
            const day = new Date(now);
            day.setDate(now.getDate() - i);
            const key = day.toISOString().split('T')[0];
            const match = Array.from(dataMap.entries()).find(([k]) =>
              k.startsWith(key),
            );
            formatted.push({
              date: day.toLocaleDateString(undefined, { weekday: 'short' }),
              fullLabel: day.toLocaleDateString(undefined, { weekday: 'long' }),
              sales: match ? match[1] : 0,
            });
          }
        } else if (timeRange === 'month') {
          const year = now.getFullYear();
          const month = now.getMonth();
          const daysInMonth = new Date(year, month + 1, 0).getDate();

          for (let d = 1; d <= daysInMonth; d++) {
            const day = new Date(year, month, d);
            const key = day.toISOString().split('T')[0];
            const match = Array.from(dataMap.entries()).find(([k]) =>
              k.startsWith(key),
            );
            const label =
              d % 5 === 0 || d === 1 || d === daysInMonth
                ? day.toLocaleDateString(undefined, {
                    month: 'short',
                    day: 'numeric',
                  })
                : '';
            formatted.push({
              date: label,
              fullLabel: day.toLocaleDateString(undefined, {
                month: 'short',
                day: 'numeric',
              }),
              sales: match ? match[1] : 0,
            });
          }
        } else if (timeRange === 'year') {
          const today = new Date();
          for (let i = 11; i >= 0; i--) {
            const month = new Date(
              today.getFullYear(),
              today.getMonth() - i,
              1,
            );
            const key = month.toISOString().slice(0, 7);
            const match = Array.from(dataMap.entries()).find(([k]) =>
              k.startsWith(key),
            );
            formatted.push({
              date: month.toLocaleDateString(undefined, { month: 'short' }), // e.g., "Jan"
              fullLabel: month.toLocaleDateString(undefined, { month: 'long' }), // e.g., "January"
              sales: match ? match[1] : 0,
            });
          }
        }

        setSalesData(formatted);
      } catch (error) {
        console.error('Error fetching sales data:', error);
      }
    };

    fetchSalesData();
  }, [timeRange]);

  const handleSort = (data) => {
    if (!sortOption) return data;
    const sorted = [...data].sort((a, b) => {
      const aVal = a[sortOption] ?? '';
      const bVal = b[sortOption] ?? '';
      return sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
    });
    return sorted;
  };

  const handleItemSort = (data) => {
    if (!itemSortOption) return data;
    const sorted = [...data].sort((a, b) => {
      const aVal = a[itemSortOption] ?? '';
      const bVal = b[itemSortOption] ?? '';
      return itemSortOrder === 'asc' ? aVal - bVal : bVal - aVal;
    });
    return sorted;
  };

  const filteredWorkers = handleSort(
    workerStats.filter((w) =>
      w.worker_name.toLowerCase().includes(searchTerm.toLowerCase()),
    ),
  );

  const filteredItems = handleItemSort(
    itemStats.filter((item) =>
      item.name.toLowerCase().includes(searchTerm.toLowerCase()),
    ),
  );

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

  const handleRangeChange = (event, newRange) => {
    if (newRange) {
      setTimeRange(newRange);
    }
  };

  return (
    <Box sx={{ mt: 4, px: 4, pb: 8 }}>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 3,
        }}
      >
        <Typography variant="h4">Statistics</Typography>
        <Button
          variant="outlined"
          onClick={() => navigate('/manager_dashboard')}
        >
          Back to Dashboard
        </Button>
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 4 }}>
        <FormControl>
          <InputLabel>Select Category</InputLabel>
          <Select
            value={selectedCategory}
            label="Select Category"
            onChange={(e) => setSelectedCategory(e.target.value)}
            sx={{ minWidth: 220 }}
          >
            <MenuItem value="worker">Worker Statistics</MenuItem>
            <MenuItem value="item">Item Statistics</MenuItem>
            <MenuItem value="sales">Restaurant Sales</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {selectedCategory === 'worker' && (
        <>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 3 }}>
            <TextField
              label="Search Worker"
              variant="outlined"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              sx={{ minWidth: 300 }}
            />
            <FormControl sx={{ minWidth: 200 }}>
              <InputLabel>Sort By</InputLabel>
              <Select
                value={sortOption}
                label="Sort By"
                onChange={(e) => setSortOption(e.target.value)}
              >
                <MenuItem value="total_orders">Total Orders</MenuItem>
                <MenuItem value="average_time_seconds">Average Time</MenuItem>
                <MenuItem value="total_sales">Total Sales</MenuItem>
              </Select>
            </FormControl>
            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Order</InputLabel>
              <Select
                value={sortOrder}
                label="Order"
                onChange={(e) => setSortOrder(e.target.value)}
              >
                <MenuItem value="asc">Ascending</MenuItem>
                <MenuItem value="desc">Descending</MenuItem>
              </Select>
            </FormControl>
          </Box>

          <Paper elevation={4} sx={{ p: 3, mb: 5 }}>
            <Typography variant="h6" align="center" sx={{ mb: 2 }}>
              Worker Statistics
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow sx={uniformRowSx}>
                    <TableCell>
                      <strong>Name</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Role</strong>
                    </TableCell>
                    <TableCell>
                      <strong># Orders</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Avg Time</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Sales</strong>
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredWorkers.map((worker, index) => (
                    <TableRow key={index} sx={uniformRowSx}>
                      <TableCell>{worker.worker_name}</TableCell>
                      <TableCell>
                        {worker.role?.charAt(0).toUpperCase() +
                          worker.role.slice(1)}
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

          <Box sx={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
            <Box sx={{ flex: 1, minWidth: 400 }}>
              <Paper elevation={4} sx={{ p: 3 }}>
                <Typography variant="h6" align="center" sx={{ mb: 2 }}>
                  Worker Total Sales
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={filteredWorkers}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="worker_name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="total_sales" fill="#82ca9d" />
                  </BarChart>
                </ResponsiveContainer>
              </Paper>
            </Box>

            <Box sx={{ flex: 1, minWidth: 400 }}>
              <Paper elevation={4} sx={{ p: 3 }}>
                <Typography variant="h6" align="center" sx={{ mb: 2 }}>
                  Worker Avg Time (sec)
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={filteredWorkers}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="worker_name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="average_time_seconds" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </Paper>
            </Box>
          </Box>
        </>
      )}

      {selectedCategory === 'item' && (
        <>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 3 }}>
            <TextField
              label="Search Item"
              variant="outlined"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              sx={{ minWidth: 300 }}
            />
            <FormControl sx={{ minWidth: 200 }}>
              <InputLabel>Sort By</InputLabel>
              <Select
                value={itemSortOption}
                label="Sort By"
                onChange={(e) => setItemSortOption(e.target.value)}
              >
                <MenuItem value="sales">Total Sales</MenuItem>
                <MenuItem value="times_ordered"># Ordered</MenuItem>
                <MenuItem value="avg_rating">Average Rating</MenuItem>
              </Select>
            </FormControl>
            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Order</InputLabel>
              <Select
                value={itemSortOrder}
                label="Order"
                onChange={(e) => setItemSortOrder(e.target.value)}
              >
                <MenuItem value="asc">Ascending</MenuItem>
                <MenuItem value="desc">Descending</MenuItem>
              </Select>
            </FormControl>
          </Box>

          <Paper elevation={4} sx={{ p: 3, mb: 5 }}>
            <Typography variant="h6" align="center" sx={{ mb: 2 }}>
              Item Statistics
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow sx={uniformRowSx}>
                    <TableCell>
                      <strong>Item Name</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Sales</strong>
                    </TableCell>
                    <TableCell>
                      <strong># Ordered</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Avg Rating</strong>
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredItems.map((item, index) => (
                    <TableRow key={index} sx={uniformRowSx}>
                      <TableCell>{item.name}</TableCell>
                      <TableCell>
                        ${parseFloat(item.sales).toFixed(2)}
                      </TableCell>
                      <TableCell>{item.times_ordered}</TableCell>
                      <TableCell>
                        {item.avg_rating !== null
                          ? item.avg_rating.toFixed(1)
                          : 'N/A'}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>

          <Box sx={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
            <Box sx={{ flex: 1, minWidth: 400 }}>
              <Paper elevation={4} sx={{ p: 3 }}>
                <Typography variant="h6" align="center" sx={{ mb: 2 }}>
                  Item Total Sales
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={filteredItems}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="sales" fill="#82ca9d" />
                  </BarChart>
                </ResponsiveContainer>
              </Paper>
            </Box>

            <Box sx={{ flex: 1, minWidth: 400 }}>
              <Paper elevation={4} sx={{ p: 3 }}>
                <Typography variant="h6" align="center" sx={{ mb: 2 }}>
                  Item Avg Rating
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={filteredItems}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="avg_rating" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </Paper>
            </Box>
          </Box>
        </>
      )}

      {selectedCategory === 'sales' && (
        <Paper elevation={4} sx={{ p: 3 }}>
          <Typography variant="h6" align="center" sx={{ mb: 2 }}>
            Restaurant Sales Over Time
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
            <ToggleButtonGroup
              value={timeRange}
              exclusive
              onChange={handleRangeChange}
            >
              <ToggleButton value="day">1 Day</ToggleButton>
              <ToggleButton value="week">1 Week</ToggleButton>
              <ToggleButton value="month">1 Month</ToggleButton>
              <ToggleButton value="year">1 Year</ToggleButton>
            </ToggleButtonGroup>
          </Box>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              data={salesData}
              margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="sales"
                stroke="#8884d8"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </Paper>
      )}
    </Box>
  );
};

export default StatisticsPage;

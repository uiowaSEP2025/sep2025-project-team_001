import React from 'react';
import {
  render,
  screen,
  fireEvent,
  waitFor,
} from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import { BrowserRouter } from 'react-router-dom';
import ManagerDashboard from '../pages/ManagerDashboard';

jest.mock('axios');

const mockDailyStats = {
  total_orders: 5,
  total_sales: 123.45,
  avg_order_value: 24.69,
  active_workers: 3,
};

beforeEach(() => {
  jest.clearAllMocks();
  sessionStorage.setItem('barName', 'Test Bar');
  sessionStorage.setItem('restaurantId', '42');
});

test('renders ManagerDashboard and fetches workers and stats', async () => {
  axios.get
    .mockResolvedValueOnce({ data: [] }) // get-workers
    .mockResolvedValueOnce({ data: mockDailyStats }); // daily-stats

  render(<ManagerDashboard />, { wrapper: BrowserRouter });

  expect(await screen.findByText(/restaurant: test bar/i)).toBeInTheDocument();
  expect(await screen.findByText(/📊 Today's Stats/i)).toBeInTheDocument();
  expect(await screen.findByText('$123.45')).toBeInTheDocument();
});

test('shows error if PIN is not 4 digits when adding worker', async () => {
  axios.get
    .mockResolvedValueOnce({ data: [] })
    .mockResolvedValueOnce({ data: mockDailyStats });

  render(<ManagerDashboard />, { wrapper: BrowserRouter });

  const nameInputs = await screen.findAllByLabelText(/name/i);
  const pinInput = screen.getByLabelText(/pin/i);
  const addButton = screen.getByRole('button', { name: /\+ add/i });

  fireEvent.change(nameInputs[nameInputs.length - 1], {
    target: { value: 'John Doe' },
  });
  fireEvent.change(pinInput, {
    target: { value: '123' },
  });
  fireEvent.click(addButton);

  expect(await screen.findByText(/pin must be 4 digits/i)).toBeInTheDocument();
});

test('adds worker successfully when inputs are valid', async () => {
  axios.get
    .mockResolvedValueOnce({ data: [] })
    .mockResolvedValueOnce({ data: mockDailyStats });

  axios.post.mockResolvedValueOnce({
    data: { id: 1, name: 'Jane Doe', pin: '1234', role: 'bartender' },
  });

  axios.get.mockResolvedValueOnce({
    data: [{ id: 1, name: 'Jane Doe', pin: '1234', role: 'bartender' }],
  });

  render(<ManagerDashboard />, { wrapper: BrowserRouter });

  const nameInputs = await screen.findAllByLabelText(/name/i);
  const pinInput = screen.getByLabelText(/pin/i);
  const addButton = screen.getByRole('button', { name: /\+ add/i });

  fireEvent.change(nameInputs[nameInputs.length - 1], {
    target: { value: 'Jane Doe' },
  });
  fireEvent.change(pinInput, {
    target: { value: '1234' },
  });
  fireEvent.click(addButton);

  expect(await screen.findByText(/jane doe/i)).toBeInTheDocument();
});

test('search filters worker list by name', async () => {
  const workers = [
    { id: 1, name: 'Alice', pin: '1111', role: 'bartender' },
    { id: 2, name: 'Bob', pin: '2222', role: 'manager' },
  ];

  axios.get
    .mockResolvedValueOnce({ data: workers })
    .mockResolvedValueOnce({ data: mockDailyStats });

  render(<ManagerDashboard />, { wrapper: BrowserRouter });

  expect(await screen.findByText(/alice/i)).toBeInTheDocument();
  expect(screen.getByText(/bob/i)).toBeInTheDocument();

  const searchBox = screen.getByLabelText(/search by name/i);
  fireEvent.change(searchBox, { target: { value: 'alice' } });

  await waitFor(() => {
    expect(screen.getByText(/alice/i)).toBeInTheDocument();
    expect(screen.queryByText(/bob/i)).not.toBeInTheDocument();
  });
});

test('can edit a worker name inline', async () => {
  const workers = [
    { id: 1, name: 'Charlie', pin: '9999', role: 'bartender' },
  ];

  axios.get
    .mockResolvedValueOnce({ data: workers })
    .mockResolvedValueOnce({ data: mockDailyStats });

  axios.put.mockResolvedValueOnce({ data: { ...workers[0], name: 'Chuck' } });
  axios.get.mockResolvedValueOnce({ data: [{ ...workers[0], name: 'Chuck' }] });

  render(<ManagerDashboard />, { wrapper: BrowserRouter });

  const nameElement = await screen.findByText('Charlie');
  fireEvent.click(nameElement);

  const input = screen.getByDisplayValue('Charlie');
  fireEvent.change(input, { target: { value: 'Chuck' } });
  fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });

  expect(await screen.findByText('Chuck')).toBeInTheDocument();
});

test('shows delete confirmation dialog and deletes worker', async () => {
  const workers = [
    { id: 1, name: 'Dana', pin: '4444', role: 'bartender' },
  ];

  axios.get
    .mockResolvedValueOnce({ data: workers })
    .mockResolvedValueOnce({ data: mockDailyStats });

  render(<ManagerDashboard />, { wrapper: BrowserRouter });

  const deleteButtons = await screen.findAllByRole('button', { name: '' });
  fireEvent.click(deleteButtons[deleteButtons.length - 1]);

  const confirmButton = await screen.findByText('Remove');
  axios.delete.mockResolvedValueOnce({});
  axios.get.mockResolvedValueOnce({ data: [] });

  fireEvent.click(confirmButton);
  await waitFor(() => expect(screen.queryByText('Dana')).not.toBeInTheDocument());
});
import React from 'react';
import {render, screen, waitFor} from '@testing-library/react';
import OrdersPage from '../pages/OrdersPage';
import axios from 'axios';

jest.mock('axios');

describe('OrdersPage Component', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  it('displays a loading spinner initially', () => {
    // Make axios.get return a promise that never resolves immediately.
    const promise = new Promise(() => {});
    axios.get.mockReturnValue(promise);
    render(<OrdersPage />);
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders orders in the table after successful fetch', async () => {
    const orders = [
      {
        id: 1,
        item_name: 'Burger',
        quantity: 2,
        status: 'Pending',
        created_at: '2022-01-01T00:00:00Z'
      },
      {
        id: 2,
        item_name: 'Fries',
        quantity: 1,
        status: 'Served',
        created_at: '2022-01-01T01:00:00Z'
      }
    ];
    axios.get.mockResolvedValue({ data: orders });
    render(<OrdersPage />);

    // Wait for the header to appear (indicating that loading is done)
    await waitFor(() => expect(screen.getByText('Active Orders')).toBeInTheDocument());

    // Check that the orders are rendered in the table.
    expect(screen.getByText('Burger')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
    expect(screen.getByText('Pending')).toBeInTheDocument();
    const createdAtFormatted = new Date('2022-01-01T00:00:00Z').toLocaleString();
    expect(screen.getByText(createdAtFormatted)).toBeInTheDocument();

    expect(screen.getByText('Fries')).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('Served')).toBeInTheDocument();
    const createdAtFormatted2 = new Date('2022-01-01T01:00:00Z').toLocaleString();
    expect(screen.getByText(createdAtFormatted2)).toBeInTheDocument();
  });

  it('renders table with no orders when axios fetch fails', async () => {
    axios.get.mockRejectedValue(new Error('Network Error'));
    render(<OrdersPage />);

    // Wait for the component to finish loading
    await waitFor(() => expect(screen.getByText('Active Orders')).toBeInTheDocument());

    // Ensure that the loading spinner is gone.
    expect(screen.queryByRole('status')).not.toBeInTheDocument();

    // The table should render the header but no order rows.
    const rows = screen.getAllByRole('row');
    // The header row is present so we expect only one row.
    expect(rows.length).toBe(1);
  });
});

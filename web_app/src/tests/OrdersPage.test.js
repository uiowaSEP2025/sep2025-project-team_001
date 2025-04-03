import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import OrdersPage from '../pages/OrdersPage';
import axios from 'axios';
import { MemoryRouter } from 'react-router-dom';

jest.mock('axios');

describe('OrdersPage Component', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  it('displays a loading spinner initially', () => {
    // Make axios.get return a promise that never resolves immediately.
    const promise = new Promise(() => {});
    axios.get.mockReturnValue(promise);
    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );    
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders orders in the table after successful fetch', async () => {
    const orders = [
      {
        id: 1,
        customer_name: 'Burger Customer',
        start_time: '2022-01-01T00:00:00Z',
        status: 'Pending'
      },
      {
        id: 2,
        customer_name: 'Fries Customer',
        start_time: '2022-01-01T01:00:00Z',
        status: 'Served'
      }
    ];
    axios.get.mockResolvedValue({ data: orders });
    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );    

    // Wait for the header to appear (loading done)
    await waitFor(() => expect(screen.getByText('Active Orders')).toBeInTheDocument());

    // Check that orders are rendered.
    expect(screen.getByText('Burger Customer')).toBeInTheDocument();
    expect(screen.getByText('Pending')).toBeInTheDocument();
    const startTimeFormatted = new Date('2022-01-01T00:00:00Z').toLocaleString();
    expect(screen.getByText(startTimeFormatted)).toBeInTheDocument();

    expect(screen.getByText('Fries Customer')).toBeInTheDocument();
    expect(screen.getByText('Served')).toBeInTheDocument();
    const startTimeFormatted2 = new Date('2022-01-01T01:00:00Z').toLocaleString();
    expect(screen.getByText(startTimeFormatted2)).toBeInTheDocument();
  });

  it('renders table with no orders when axios fetch fails', async () => {
    axios.get.mockRejectedValue(new Error('Network Error'));
    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );    

    // Wait for loading to finish.
    await waitFor(() => expect(screen.getByText('Active Orders')).toBeInTheDocument());

    // Loading spinner should be gone.
    expect(screen.queryByRole('status')).not.toBeInTheDocument();

    // Only header row should be rendered.
    const rows = screen.getAllByRole('row');
    expect(rows.length).toBe(1);
  });

  // --- New tests for modal and complete order functionality ---

  it('opens order details modal when clicking on an order row', async () => {
    const order = {
      id: 1,
      customer_name: 'Test Customer',
      start_time: '2022-01-01T00:00:00Z',
      status: 'Pending',
      order_items: [
        { item_name: 'Test Item', quantity: 2 }
      ]
    };
    axios.get.mockResolvedValue({ data: [order] });
    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );    
    await waitFor(() => expect(screen.getByText('Active Orders')).toBeInTheDocument());

    // Simulate clicking the order row by clicking on the customer's name.
    fireEvent.click(screen.getByText('Test Customer'));
    // Modal should now appear.
    await waitFor(() => expect(screen.getByText('Order Details')).toBeInTheDocument());
    // Verify that the order items are displayed.
    expect(screen.getByText('Test Item')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
  });

  it('completes order successfully', async () => {
    const order = {
      id: 1,
      customer_name: 'Test Customer',
      start_time: '2022-01-01T00:00:00Z',
      status: 'Pending',
      order_items: [
        { item_name: 'Test Item', quantity: 2 }
      ]
    };
    axios.get.mockResolvedValue({ data: [order] });
    axios.patch.mockResolvedValue({ data: { order_id: 1 } });
    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );    
    await waitFor(() => expect(screen.getByText('Active Orders')).toBeInTheDocument());

    // Open the order details modal.
    fireEvent.click(screen.getByText('Test Customer'));
    await waitFor(() => expect(screen.getByText('Order Details')).toBeInTheDocument());

    // "Complete Order" button should be visible.
    const completeButton = screen.getByText('Complete Order');
    fireEvent.click(completeButton);

    // After completion, the modal should update and hide the complete button.
    await waitFor(() => {
      expect(screen.queryByText('Complete Order')).not.toBeInTheDocument();
    });
  });

  it('handles error in completing order', async () => {
    const order = {
      id: 1,
      customer_name: 'Test Customer',
      start_time: '2022-01-01T00:00:00Z',
      status: 'Pending',
      order_items: [
        { item_name: 'Test Item', quantity: 2 }
      ]
    };
    axios.get.mockResolvedValue({ data: [order] });
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    axios.patch.mockRejectedValue(new Error('Patch error'));
    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );    
    await waitFor(() => expect(screen.getByText('Active Orders')).toBeInTheDocument());

    fireEvent.click(screen.getByText('Test Customer'));
    await waitFor(() => expect(screen.getByText('Order Details')).toBeInTheDocument());

    const completeButton = screen.getByText('Complete Order');
    fireEvent.click(completeButton);

    await waitFor(() =>
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        'Error marking order as completed:',
        expect.any(Error)
      )
    );
    consoleErrorSpy.mockRestore();
  });
});

import React from 'react';
import {
  render,
  screen,
  fireEvent,
  waitFor,
  within,
  act,
} from '@testing-library/react';
import '@testing-library/jest-dom';
import OrdersPage from '../pages/OrdersPage';
import { MemoryRouter } from 'react-router-dom';
import axios from 'axios';

jest.mock('axios');

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

beforeAll(() => jest.useFakeTimers());
afterAll(() => jest.useRealTimers());

const setSessionMocks = () => {
  Storage.prototype.getItem = jest.fn((key) => {
    switch (key) {
      case 'workerRole':
        return 'manager';
      case 'restaurantId':
        return '1';
      case 'workerId':
        return '42';
      case 'workerName':
        return 'Alice';
      default:
        return null;
    }
  });
};

const baseOrders = [
  {
    id: 1,
    customer_name: 'Bob',
    total_price: 25,
    status: 'pending',
    worker_name: '',
    food_eta_minutes: 10,
    beverage_eta_minutes: 5,
    food_status: 'pending',
    beverage_status: 'pending',
    order_items: [
      {
        item_name: 'Burger',
        quantity: 1,
        category: 'food',
        unwanted_ingredient_names: ['Lettuce'],
      },
    ],
  },
  {
    id: 2,
    customer_name: 'Charlie',
    total_price: 15,
    status: 'completed',
    worker_name: 'Sam',
    food_eta_minutes: null,
    beverage_eta_minutes: null,
    food_status: 'completed',
    beverage_status: 'completed',
    order_items: [],
  },
];

const mockGetOnce = (results, next_offset = null, total = results.length) => {
  axios.get.mockResolvedValueOnce({
    data: {
      results,
      next_offset,
      total,
    },
  });
};

beforeEach(() => {
  jest.clearAllMocks();
  setSessionMocks();
});

describe('OrdersPage', () => {
  test('renders headings and Dashboard button (manager role)', async () => {
    mockGetOnce(baseOrders);

    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );

    expect(await screen.findByText(/Active Orders/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Dashboard/i })).toBeInTheDocument();
  });

  test('search filters customer list', async () => {
    mockGetOnce(baseOrders);

    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );

    expect(await screen.findByText('Bob')).toBeInTheDocument();
    expect(screen.getByText('Charlie')).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText(/Search Customer/i), {
      target: { value: 'Bob' },
    });

    await waitFor(() => {
      expect(screen.getByText('Bob')).toBeInTheDocument();
      expect(screen.queryByText('Charlie')).not.toBeInTheDocument();
    });
  });

  test('opens order dialog and closes it', async () => {
    mockGetOnce(baseOrders);

    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );

    fireEvent.click(await screen.findByText('Bob'));
    expect(await screen.findByText(/Order Details/i)).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /Close/i }));
    await waitFor(() =>
      expect(screen.queryByText(/Order Details/i)).not.toBeInTheDocument()
    );
  });

  test('marks order In Progress and updates UI', async () => {
    mockGetOnce(baseOrders);

    axios.patch.mockResolvedValueOnce({
      data: { status: 'in_progress' },
    });

    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );

    fireEvent.click(await screen.findByText('Bob'));
    const markBtn = await screen.findByRole('button', { name: /Mark In Progress/i });

    await act(async () => {
      fireEvent.click(markBtn);
    });

    await waitFor(() =>
      expect(screen.getAllByText(/In Progress/i).length).toBeGreaterThan(0)
    );
    expect(axios.patch).toHaveBeenCalledTimes(1);
  });

  test('updates food status from in_progress → completed', async () => {
    const updated = {
      ...baseOrders[0],
      status: 'in_progress',
      worker_name: 'Alice',
      food_status: 'in_progress',
      beverage_status: 'completed',
    };
    mockGetOnce([updated]);

    axios.patch.mockResolvedValueOnce({
      data: { food_status: 'completed' },
    });

    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );

    fireEvent.click(await screen.findByText('Bob'));

    const foodBtn = await screen.findByRole('button', { name: /Mark food Completed/i });

    await act(async () => {
      fireEvent.click(foodBtn);
    });

    await waitFor(() =>
      expect(screen.getByText(/Food.*Completed/i)).toBeInTheDocument()
    );
  });

  test('load more button fetches additional records', async () => {
    mockGetOnce(baseOrders, 20, 50);

    render(
      <MemoryRouter>
        <OrdersPage />
      </MemoryRouter>
    );

    const loadBtn = await screen.findByRole('button', { name: /Load More Orders/i });
    mockGetOnce(baseOrders);

    await act(async () => {
      fireEvent.click(loadBtn);
    });

    expect(axios.get).toHaveBeenCalledTimes(2);
  });
});

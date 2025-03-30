import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import MenuPage from '../pages/MenuPage';
import ItemCard from '../components/ItemCard';
import '@testing-library/jest-dom';
import fetchMock from 'jest-fetch-mock';

fetchMock.enableMocks();

// Mock localStorage
beforeAll(() => {
  Storage.prototype.getItem = jest.fn((key) => {
    if (key === 'accessToken') return 'test-token';
    if (key === 'barName') return 'Test Bar';
    return null;
  });
});

jest.mock('../components/ItemCard', () => (props) => (
  <div data-testid="item-card">
    <button onClick={() => props.onToggle(props.item)}>Toggle</button>
    <button onClick={() => props.onDelete(props.item.id)}>Delete</button>
  </div>
));

beforeEach(() => {
  fetch.resetMocks();
});

describe('MenuPage Component', () => {
  test('renders MenuPage with section headers and fetches items', async () => {
    fetch.mockResponseOnce(JSON.stringify({ items: [] }));

    render(<MenuPage />);
    expect(await screen.findByText(/Menu Manager/)).toBeInTheDocument();
    expect(screen.getByText(/Available Items/)).toBeInTheDocument();
    expect(screen.getByText(/Unavailable Items/)).toBeInTheDocument();
  });

  test('displays item cards for available food and beverages', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          { id: 1, name: 'Beer', available: true, category: 'beverage' },
          { id: 2, name: 'Burger', available: true, category: 'food' },
          { id: 3, name: 'Water', available: false, category: 'beverage' },
          { id: 4, name: 'Pizza', available: false, category: 'food' },
        ],
      })
    );

    render(<MenuPage />);
    const cards = await screen.findAllByTestId('item-card');
    expect(cards.length).toBe(4);
  });

  test('opens and closes create modal', async () => {
    fetch.mockResponseOnce(JSON.stringify({ items: [] }));

    render(<MenuPage />);
    fireEvent.click(screen.getByText(/Create New Item/));
    expect(screen.getByText(/Create New Menu Item/)).toBeInTheDocument();

    fireEvent.click(screen.getByText(/Cancel/));
    await waitFor(() =>
      expect(screen.queryByText(/Create New Menu Item/)).not.toBeInTheDocument()
    );
  });


  test('toggles item availability', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [{ id: 1, name: 'Water', available: false, category: 'beverage' }],
      })
    );

    render(<MenuPage />);
    const toggleButton = await screen.findByText('Toggle');
    fireEvent.click(toggleButton);
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(2)); // toggle + refresh
  });

  test('opens and confirms delete modal', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [{ id: 1, name: 'DeleteMe', available: true, category: 'food' }],
      })
    );

    render(<MenuPage />);
    const deleteBtn = await screen.findByText('Delete');
    fireEvent.click(deleteBtn);

    expect(screen.getByText(/Confirm Delete/)).toBeInTheDocument();
    fireEvent.click(screen.getByText(/Yes/));

    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(2)); // delete + refresh
  });

  test('cancel delete modal closes it', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [{ id: 2, name: 'NoDelete', available: true, category: 'food' }],
      })
    );

    render(<MenuPage />);
    fireEvent.click(await screen.findByText('Delete'));

    expect(screen.getByText(/Confirm Delete/)).toBeInTheDocument();
    fireEvent.click(screen.getByText(/Cancel/));

    await waitFor(() =>
      expect(screen.queryByText(/Confirm Delete/)).not.toBeInTheDocument()
    );
  });
});
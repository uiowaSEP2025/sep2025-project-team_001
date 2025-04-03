import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import MenuPage from '../pages/MenuPage';
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

// Mock ItemCard component to simplify test behavior
jest.mock('../components/ItemCard', () => (props) => (
  <div data-testid="item-card">
    <button onClick={() => props.onToggle(props.item)}>Toggle</button>
    <button onClick={() => props.onDelete(props.item.id)}>Delete</button>
  </div>
));

beforeEach(() => {
  fetch.resetMocks();
  jest.restoreAllMocks();
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
      }),
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
    await waitFor(() => {
      expect(
        screen.queryByText(/Create New Menu Item/),
      ).not.toBeInTheDocument();
    });
  });

  test('toggles item availability', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          { id: 1, name: 'Water', available: false, category: 'beverage' },
        ],
      }),
    );
    render(<MenuPage />);
    const toggleButton = await screen.findByText('Toggle');
    fireEvent.click(toggleButton);
    // Expect three fetch calls: 1 from mount, 1 for update POST, 1 for refetch.
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3));
  });

  test('handles error in creating menu item (line 101)', async () => {
    const consoleErrorSpy = jest
      .spyOn(console, 'error')
      .mockImplementation(() => {});
    fetch.mockResponseOnce(JSON.stringify({ items: [] }));
    // Store the render result to access container.
    const { container } = render(<MenuPage />);
    fireEvent.click(screen.getByText(/Create New Item/));
    expect(screen.getByText(/Create New Menu Item/)).toBeInTheDocument();

    // Simulate a failure for the create request.
    fetch.mockRejectOnce(new Error('Creation failed'));

    // Use container.querySelector since labels are not properly associated.
    const nameInput = container.querySelector('input[name="name"]');
    fireEvent.change(nameInput, { target: { value: 'Error Item' } });
    const priceInput = container.querySelector('input[name="price"]');
    fireEvent.change(priceInput, { target: { value: '10' } });
    const categorySelect = container.querySelector('select[name="category"]');
    fireEvent.change(categorySelect, { target: { value: 'food' } });
    const stockInput = container.querySelector('input[name="stock"]');
    fireEvent.change(stockInput, { target: { value: '1' } });
    const fileInput = container.querySelector('input[type="file"]');
    const file = new File(['dummy'], 'error.png', { type: 'image/png' });
    fireEvent.change(fileInput, { target: { files: [file] } });

    fireEvent.click(screen.getByText(/^Create$/));

    await waitFor(() => {
      expect(consoleErrorSpy).toHaveBeenCalled();
      expect(consoleErrorSpy.mock.calls[0][0]).toContain(
        'Error creating item:',
      );
    });
    consoleErrorSpy.mockRestore();
  });

  test('handles error in updating item availability (line 131)', async () => {
    const consoleErrorSpy = jest
      .spyOn(console, 'error')
      .mockImplementation(() => {});
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          {
            id: 1,
            name: 'Test Item',
            available: false,
            category: 'beverage',
            description: 'desc',
            price: 10,
            stock: 5,
            base64_image: '',
          },
        ],
      }),
    );
    render(<MenuPage />);
    const toggleButton = await screen.findByText('Toggle');
    fetch.mockRejectOnce(new Error('Update failed'));
    fireEvent.click(toggleButton);
    await waitFor(() =>
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        'Error updating item availability:',
        expect.any(Error),
      ),
    );
    consoleErrorSpy.mockRestore();
  });

  test('opens and confirms delete modal', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [{ id: 1, name: 'DeleteMe', available: true, category: 'food' }],
      }),
    );
    render(<MenuPage />);
    fireEvent.click(await screen.findByText('Delete'));
    expect(screen.getByText(/Confirm Delete/)).toBeInTheDocument();

    fireEvent.click(screen.getByText(/Yes/));
    // Expect three fetch calls: 1 from mount, 1 for delete POST, 1 for refetch.
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3));
  });

  test('cancel delete modal closes it', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [{ id: 2, name: 'NoDelete', available: true, category: 'food' }],
      }),
    );
    render(<MenuPage />);
    fireEvent.click(await screen.findByText('Delete'));
    expect(screen.getByText(/Confirm Delete/)).toBeInTheDocument();

    fireEvent.click(screen.getByText(/Cancel/));
    await waitFor(() => {
      expect(screen.queryByText(/Confirm Delete/)).not.toBeInTheDocument();
    });
  });

  test('handles error in deleting item', async () => {
    const consoleErrorSpy = jest
      .spyOn(console, 'error')
      .mockImplementation(() => {});
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          { id: 1, name: 'DeleteError', available: true, category: 'food' },
        ],
      }),
    );
    render(<MenuPage />);
    fireEvent.click(await screen.findByText('Delete'));
    expect(screen.getByText(/Confirm Delete/)).toBeInTheDocument();
    fetch.mockRejectOnce(new Error('Delete failed'));
    fireEvent.click(screen.getByText(/Yes/));
    await waitFor(() =>
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        'Error deleting item:',
        expect.any(Error),
      ),
    );
    consoleErrorSpy.mockRestore();
  });

  test('creates a new menu item successfully', async () => {
    fetch.mockResponses(
      [JSON.stringify({ created: true, id: 10 }), { status: 200 }],
      [JSON.stringify({ items: [] }), { status: 200 }],
    );
    const { container } = render(<MenuPage />);
    fireEvent.click(screen.getByText(/Create New Item/));
    expect(screen.getByText(/Create New Menu Item/)).toBeInTheDocument();

    const nameInput = container.querySelector('input[name="name"]');
    const descriptionInput = container.querySelector(
      'input[name="description"]',
    );
    const priceInput = container.querySelector('input[name="price"]');
    const categorySelect = container.querySelector('select[name="category"]');
    const stockInput = container.querySelector('input[name="stock"]');
    const fileInput = container.querySelector('input[type="file"]');

    fireEvent.change(nameInput, { target: { value: 'Test Item' } });
    fireEvent.change(descriptionInput, {
      target: { value: 'Test description' },
    });
    fireEvent.change(priceInput, { target: { value: '12.34' } });
    fireEvent.change(categorySelect, { target: { value: 'food' } });
    fireEvent.change(stockInput, { target: { value: '5' } });

    const file = new File(['dummy content'], 'test.png', { type: 'image/png' });
    fireEvent.change(fileInput, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByAltText('Preview')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText(/^Create$/));

    await waitFor(() => {
      expect(
        screen.queryByText(/Create New Menu Item/),
      ).not.toBeInTheDocument();
    });

    expect(fetch).toHaveBeenCalledTimes(3);
  });

  test('updates available checkbox in create modal (line 278)', async () => {
    fetch.mockResponseOnce(JSON.stringify({ items: [] }));
    render(<MenuPage />);
    fireEvent.click(screen.getByText(/Create New Item/));
    expect(screen.getByText(/Create New Menu Item/)).toBeInTheDocument();

    // Since the checkbox doesn't have an associated accessible label,
    // use getByRole to fetch the checkbox.
    const availableCheckbox = screen.getByRole('checkbox');
    expect(availableCheckbox.checked).toBe(true);

    fireEvent.click(availableCheckbox);
    expect(availableCheckbox.checked).toBe(false);
  });
});

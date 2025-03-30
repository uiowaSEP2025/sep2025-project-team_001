import React from 'react';
import {fireEvent, render, screen, waitFor} from '@testing-library/react';
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
});

describe('MenuPage Component', () => {
  test('renders MenuPage with section headers and fetches items', async () => {
    fetch.mockResponseOnce(JSON.stringify({items: []}));
    render(<MenuPage/>);
    expect(await screen.findByText(/Menu Manager/)).toBeInTheDocument();
    expect(screen.getByText(/Available Items/)).toBeInTheDocument();
    expect(screen.getByText(/Unavailable Items/)).toBeInTheDocument();
  });

  test('displays item cards for available food and beverages', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          {id: 1, name: 'Beer', available: true, category: 'beverage'},
          {id: 2, name: 'Burger', available: true, category: 'food'},
          {id: 3, name: 'Water', available: false, category: 'beverage'},
          {id: 4, name: 'Pizza', available: false, category: 'food'},
        ],
      })
    );
    render(<MenuPage/>);
    const cards = await screen.findAllByTestId('item-card');
    expect(cards.length).toBe(4);
  });

  test('opens and closes create modal', async () => {
    fetch.mockResponseOnce(JSON.stringify({items: []}));
    render(<MenuPage/>);
    fireEvent.click(screen.getByText(/Create New Item/));
    expect(screen.getByText(/Create New Menu Item/)).toBeInTheDocument();

    fireEvent.click(screen.getByText(/Cancel/));
    await waitFor(() => {
      expect(screen.queryByText(/Create New Menu Item/)).not.toBeInTheDocument();
    });
  });

  test('toggles item availability', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [{id: 1, name: 'Water', available: false, category: 'beverage'}],
      })
    );
    render(<MenuPage/>);
    const toggleButton = await screen.findByText('Toggle');
    fireEvent.click(toggleButton);
    // Expect two fetch calls: one for toggle update and one for refetching items
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(2));
  });

  test('handles error in creating menu item (line 101)', async () => {
    // Spy on console.error to verify the error logging.
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {
    });
    // Initial fetch from useEffect
    fetch.mockResponseOnce(JSON.stringify({items: []}));
    render(<MenuPage/>);
    fireEvent.click(screen.getByText(/Create New Item/));
    expect(screen.getByText(/Create New Menu Item/)).toBeInTheDocument();

    // For the create request, simulate a failure.
    fetch.mockRejectOnce(new Error('Creation failed'));

    // Fill out the form minimally.
    const nameInput = screen.getByLabelText(/Item Name:/);
    fireEvent.change(nameInput, {target: {value: 'Error Item'}});
    // Provide required fields with dummy values.
    fireEvent.change(screen.getByLabelText(/Price:/), {target: {value: '10'}});
    fireEvent.change(screen.getByLabelText(/Category:/), {target: {value: 'food'}});
    fireEvent.change(screen.getByLabelText(/Stock:/), {target: {value: '1'}});
    const fileInput = screen.getByLabelText(/Upload Image:/);
    const file = new File(['dummy'], 'error.png', {type: 'image/png'});
    fireEvent.change(fileInput, {target: {files: [file]}});

    fireEvent.click(screen.getByText(/^Create$/));

    await waitFor(() =>
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        'Error creating item:',
        expect.any(Error)
      )
    );
    consoleErrorSpy.mockRestore();
  });

  test('handles error in updating item availability (line 131)', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {
    });
    // Initial fetch from useEffect with one item.
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [{
          id: 1,
          name: 'Test Item',
          available: false,
          category: 'beverage',
          description: 'desc',
          price: 10,
          stock: 5,
          base64_image: ''
        }],
      })
    );
    render(<MenuPage/>);
    const toggleButton = await screen.findByText('Toggle');
    // For the toggle update, simulate a failure.
    fetch.mockRejectOnce(new Error('Update failed'));
    fireEvent.click(toggleButton);
    await waitFor(() =>
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        'Error updating item availability:',
        expect.any(Error)
      )
    );
    consoleErrorSpy.mockRestore();
  });

  test('opens and confirms delete modal', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [{id: 1, name: 'DeleteMe', available: true, category: 'food'}],
      })
    );
    render(<MenuPage/>);
    fireEvent.click(await screen.findByText('Delete'));
    expect(screen.getByText(/Confirm Delete/)).toBeInTheDocument();

    fireEvent.click(screen.getByText(/Yes/));
    // Expect two fetch calls: one for deletion and one for refetching items
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(2));
  });

  test('cancel delete modal closes it', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [{id: 2, name: 'NoDelete', available: true, category: 'food'}],
      })
    );
    render(<MenuPage/>);
    fireEvent.click(await screen.findByText('Delete'));
    expect(screen.getByText(/Confirm Delete/)).toBeInTheDocument();

    fireEvent.click(screen.getByText(/Cancel/));
    await waitFor(() => {
      expect(screen.queryByText(/Confirm Delete/)).not.toBeInTheDocument();
    });
  });

  test('handles error in deleting item', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {
    });
    // Initial fetch from useEffect with one item.
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [{id: 1, name: 'DeleteError', available: true, category: 'food'}],
      })
    );
    render(<MenuPage/>);
    fireEvent.click(await screen.findByText('Delete'));
    expect(screen.getByText(/Confirm Delete/)).toBeInTheDocument();
    // For the delete request, simulate a failure.
    fetch.mockRejectOnce(new Error('Delete failed'));
    fireEvent.click(screen.getByText(/Yes/));
    await waitFor(() =>
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        'Error deleting item:',
        expect.any(Error)
      )
    );
    consoleErrorSpy.mockRestore();
  });

  test('creates a new menu item successfully', async () => {
    // Set up responses: first for the create request, then for refetching items.
    fetch.mockResponses(
      [JSON.stringify({created: true, id: 10}), {status: 200}],
      [JSON.stringify({items: []}), {status: 200}]
    );

    const {container} = render(<MenuPage/>);
    // Open the create modal.
    fireEvent.click(screen.getByText(/Create New Item/));
    expect(screen.getByText(/Create New Menu Item/)).toBeInTheDocument();

    // Fill out the form fields.
    const nameInput = container.querySelector('input[name="name"]');
    const descriptionInput = container.querySelector('input[name="description"]');
    const priceInput = container.querySelector('input[name="price"]');
    const categorySelect = container.querySelector('select[name="category"]');
    const stockInput = container.querySelector('input[name="stock"]');
    const fileInput = container.querySelector('input[type="file"]');

    fireEvent.change(nameInput, {target: {value: 'Test Item'}});
    fireEvent.change(descriptionInput, {target: {value: 'Test description'}});
    fireEvent.change(priceInput, {target: {value: '12.34'}});
    fireEvent.change(categorySelect, {target: {value: 'food'}});
    fireEvent.change(stockInput, {target: {value: '5'}});

    // Simulate file upload.
    const file = new File(['dummy content'], 'test.png', {type: 'image/png'});
    fireEvent.change(fileInput, {target: {files: [file]}});

    // Wait for the image preview to appear (indicating the file was processed).
    await waitFor(() => {
      expect(screen.getByAltText('Preview')).toBeInTheDocument();
    });

    // Submit the form.
    fireEvent.click(screen.getByText(/^Create$/));

    // Wait for the modal to close.
    await waitFor(() => {
      expect(screen.queryByText(/Create New Menu Item/)).not.toBeInTheDocument();
    });

    // Ensure that fetch was called twice: once for creation and once for refetching items.
    expect(fetch).toHaveBeenCalledTimes(3);
  });

  test('updates available checkbox in create modal (line 278)', async () => {
    // Initial fetch from useEffect
    fetch.mockResponseOnce(JSON.stringify({items: []}));
    render(<MenuPage/>);
    fireEvent.click(screen.getByText(/Create New Item/));
    expect(screen.getByText(/Create New Menu Item/)).toBeInTheDocument();

    // Find the available checkbox. It should be initially checked (true).
    const availableCheckbox = screen.getByRole('checkbox', {name: /Available:/i});
    expect(availableCheckbox.checked).toBe(true);

    // Simulate changing the checkbox (uncheck it).
    fireEvent.click(availableCheckbox);
    expect(availableCheckbox.checked).toBe(false);
  });
});

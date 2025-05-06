import React from 'react';
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import PromotionNotificationPage from '../pages/PromotionNotificationPage';
import axios from 'axios';

jest.mock('axios');
const API = 'http://test.local/api';
process.env.REACT_APP_API_URL = API;

const makePromo = (id, overrides = {}) => ({
  id,
  title: `Title ${id}`,
  body: `Body ${id}`,
  sent: false,
  ...overrides,
});


const typeText = (textbox, value) => {
  fireEvent.change(textbox, { target: { value } });
};


describe('PromotionNotificationPage', () => {
  const promos = [makePromo(1), makePromo(2)];

  beforeEach(() => {
    jest.clearAllMocks();
    axios.get.mockResolvedValue({ data: promos });
  });

  const renderPage = () => render(<PromotionNotificationPage />);

  test('loads and displays promotions', async () => {
    renderPage();

    // header & create form visible immediately
    expect(screen.getByRole('heading', { name: /promotions/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /create/i })).toBeInTheDocument();

    // wait for fetchPromotions
    expect(axios.get).toHaveBeenCalledWith(`${API}/promotions/`);
    await waitFor(() => {
      expect(screen.getByText('Title 1')).toBeInTheDocument();
      expect(screen.getByText('Body 2')).toBeInTheDocument();
    });
  });

  test('creates a new promotion', async () => {
    axios.post.mockResolvedValue({}); // success

    renderPage();

    // fill in create form
    typeText(screen.getByLabelText(/title/i), 'New Promo');
    typeText(screen.getByLabelText(/body/i), 'Hello world');

    fireEvent.click(screen.getByRole('button', { name: /^create$/i }));

    await waitFor(() =>
      expect(axios.post).toHaveBeenCalledWith(
        `${API}/promotions/create/`,
        { title: 'New Promo', body: 'Hello world' },
      ),
    );

    // flash appears
    expect(await screen.findByText(/promotion created!/i)).toBeVisible();
  });

  test('edits and saves a promotion', async () => {
    axios.patch.mockResolvedValue({}); // success

    renderPage();
    await screen.findByText('Title 1');

    // click first edit icon
    const editButton = screen.getAllByTestId('EditIcon')[0].closest('button');
    fireEvent.click(editButton);

    // change title textfield now visible
    const titleBox = screen.getByDisplayValue('Title 1');
    typeText(titleBox, 'Updated Title');
    fireEvent.click(screen.getByRole('button', { name: /save/i }));

    await waitFor(() =>
      expect(axios.patch).toHaveBeenCalledWith(
        `${API}/promotions/1/update/`,
        expect.objectContaining({ title: 'Updated Title' }),
      ),
    );
    expect(await screen.findByText(/promotion updated!/i)).toBeVisible();
  });

  test('deletes a promotion', async () => {
    axios.delete.mockResolvedValue({}); // success

    renderPage();
    await screen.findByText('Title 2');

    const deleteButton = screen.getAllByTestId('DeleteIcon')[1].closest('button');
    fireEvent.click(deleteButton);

    await waitFor(() =>
      expect(axios.delete).toHaveBeenCalledWith(`${API}/promotions/2/delete/`),
    );
    expect(await screen.findByText(/promotion deleted!/i)).toBeVisible();
  });

  test('opens confirmation dialog and sends promotion', async () => {
    axios.post.mockResolvedValue({}); // success for /send/

    renderPage();
    await screen.findByText('Title 1');

    const sendButton = screen.getAllByTestId('SendIcon')[0].closest('button');
    fireEvent.click(sendButton);

    // dialog opens
    expect(
      screen.getByRole('dialog', { name: /confirm send/i }),
    ).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /yes, send/i }));

    await waitFor(() =>
      expect(axios.post).toHaveBeenCalledWith(`${API}/promotions/1/send/`),
    );
    expect(await screen.findByText(/promotion sent to all customers!/i)).toBeVisible();
  });
});

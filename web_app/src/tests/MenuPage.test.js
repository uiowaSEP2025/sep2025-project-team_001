import React from 'react';
import {
  render,
  screen,
  fireEvent,
  waitFor,
  within,
} from '@testing-library/react';
import '@testing-library/jest-dom';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import fetchMock from 'jest-fetch-mock';
import MenuPage from '../pages/MenuPage';

fetchMock.enableMocks();

beforeAll(() => {
  Storage.prototype.getItem = jest.fn((k) =>
    k === 'accessToken' ? 'token' : k === 'barName' ? 'Test Bar' : null,
  );
});

jest.mock('../components/ItemCard', () => ({ item, onToggle, onDelete }) => (
  <div data-testid="item-card">
    <span>{item.name}</span>
    <button onClick={() => onToggle(item)}>Toggle</button>
    <button onClick={() => onDelete(item.id)}>Delete</button>
  </div>
));

global.FileReader = class {
  readAsDataURL() {
    this.onloadend();
  }
  onloadend() {}
  result = 'data:image/png;base64,test';
};

beforeEach(() => {
  fetch.resetMocks();
  jest.clearAllMocks();
});

describe('MenuPage', () => {
  test('basic render', async () => {
    fetch.mockResponseOnce(JSON.stringify({ items: [] }));

    render(
      <MemoryRouter>
        <MenuPage />
      </MemoryRouter>,
    );

    expect(await screen.findByText('Menu Manager')).toBeInTheDocument();
    expect(screen.getByText('Available Items')).toBeInTheDocument();
    expect(screen.getByText('Unavailable Items')).toBeInTheDocument();
  });

  test('lists item cards', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          {
            id: 1,
            name: 'Beer',
            available: true,
            category: 'beverage',
            ingredients: [],
          },
          {
            id: 2,
            name: 'Burger',
            available: true,
            category: 'food',
            ingredients: [],
          },
          {
            id: 3,
            name: 'Water',
            available: false,
            category: 'beverage',
            ingredients: [],
          },
          {
            id: 4,
            name: 'Pizza',
            available: false,
            category: 'food',
            ingredients: [],
          },
        ],
      }),
    );

    render(
      <MemoryRouter>
        <MenuPage />
      </MemoryRouter>,
    );
    expect((await screen.findAllByTestId('item-card')).length).toBe(4);
  });

  test('search filter works', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          {
            id: 1,
            name: 'Fries',
            available: true,
            category: 'food',
            ingredients: [],
          },
          {
            id: 2,
            name: 'Soda',
            available: true,
            category: 'beverage',
            ingredients: [],
          },
        ],
      }),
    );

    render(
      <MemoryRouter>
        <MenuPage />
      </MemoryRouter>,
    );
    fireEvent.change(screen.getByLabelText(/Search menu items/i), {
      target: { value: 'Soda' },
    });

    await waitFor(() =>
      expect(screen.getAllByTestId('item-card').length).toBe(1),
    );
    expect(screen.getByText('Soda')).toBeInTheDocument();
  });

  test('open & close create modal', async () => {
    fetch.mockResponseOnce(JSON.stringify({ items: [] }));

    render(
      <MemoryRouter>
        <MenuPage />
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByText('Add Item'));
    expect(
      await screen.findByText('Create New Menu Item'),
    ).toBeInTheDocument();

    fireEvent.click(screen.getByText('Cancel'));
    await waitFor(() =>
      expect(
        screen.queryByText('Create New Menu Item'),
      ).not.toBeInTheDocument(),
    );
  });

  test('toggle availability success', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          {
            id: 1,
            name: 'Water',
            available: false,
            category: 'beverage',
            ingredients: [],
          },
        ],
      }),
    );

    render(
      <MemoryRouter>
        <MenuPage />
      </MemoryRouter>,
    );
    const btn = await screen.findByText('Toggle');

    fetch.mockResponses(
      [JSON.stringify({ ok: true }), { status: 200 }],
      [JSON.stringify({ items: [] }), { status: 200 }],
    );

    fireEvent.click(btn);
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3));
  });

  test('toggle availability – server 500 handled', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          {
            id: 2,
            name: 'FailToggle',
            available: true,
            category: 'food',
            ingredients: [],
          },
        ],
      }),
    );

    render(
      <MemoryRouter>
        <MenuPage />
      </MemoryRouter>,
    );
    const btn = await screen.findByText('Toggle');

    fetch.mockResponses(
      [JSON.stringify({ error: 'fail' }), { status: 500 }],
      [JSON.stringify({ items: [] }), { status: 200 }],
    );

    fireEvent.click(btn);
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3));
  });

  test('delete item success', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          {
            id: 3,
            name: 'DeleteMe',
            available: true,
            category: 'food',
            ingredients: [],
          },
        ],
      }),
    );

    render(
      <MemoryRouter>
        <MenuPage />
      </MemoryRouter>,
    );
    const del = await screen.findByText('Delete');

    fetch.mockResponses(
      [JSON.stringify({ ok: true }), { status: 200 }],
      [JSON.stringify({ items: [] }), { status: 200 }],
    );

    fireEvent.click(del);
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3));
  });

  test('delete item – server 500 handled', async () => {
    fetch.mockResponseOnce(
      JSON.stringify({
        items: [
          {
            id: 4,
            name: 'FailDelete',
            available: false,
            category: 'beverage',
            ingredients: [],
          },
        ],
      }),
    );

    render(
      <MemoryRouter>
        <MenuPage />
      </MemoryRouter>,
    );
    const del = await screen.findByText('Delete');

    fetch.mockResponses(
      [JSON.stringify({ error: 'fail' }), { status: 500 }],
      [JSON.stringify({ items: [] }), { status: 200 }],
    );

    fireEvent.click(del);
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3));
  });
});

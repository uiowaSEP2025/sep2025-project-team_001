// src/tests/StatisticsPage.test.tsx
import React from 'react';
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import StatisticsPage from '../pages/ProductStatisticsPage';
import axios from 'axios';

/* ────────── mocks & shims ──────────────────────────────────────────── */

// 1. Recharts → lightweight stubs (strip unknown DOM props such as dataKey)
jest.mock('recharts', () => {
  /* eslint‑disable react/prop‑types */
  const Dummy = ({ children, ...rest }) => {
    // eslint‑disable-next-line @typescript-eslint/no-unused-vars
    const { dataKey, stroke, fill, ...safe } = rest;
    return <div data-testid="chart" {...safe}>{children}</div>;
  };
  return {
    ResponsiveContainer: Dummy,
    BarChart: Dummy,
    LineChart: Dummy,
    CartesianGrid: Dummy,
    XAxis: Dummy,
    YAxis: Dummy,
    Tooltip: Dummy,
    Legend: Dummy,
    Bar: Dummy,
    Line: Dummy,
  };
});

// 2. Global ResizeObserver shim so JSDOM doesn’t explode
global.ResizeObserver = class {
  observe() {/* noop */}
  unobserve() {/* noop */}
  disconnect() {/* noop */}
};

// 3. Axios mock helpers
jest.mock('axios');
const queueAxios = (...responses) => {
  axios.get.mockReset();
  responses.forEach(r => axios.get.mockResolvedValueOnce(r));
};

/* ────────── canned API payloads ────────────────────────────────────── */

const fakeItemStats = {
  data: {
    items: [
      { name: 'Burger', sales: 120, times_ordered: 12, avg_rating: 4.5 },
      { name: 'Fries',  sales:  80, times_ordered: 20, avg_rating: 4.2 },
    ],
  },
};

const fakeWorkerStats = {
  data: {
    bartender_statistics: [
      {
        worker_name: 'Alice',
        role: 'bartender',
        total_orders: 25,
        average_time_seconds: 65,
        total_sales: 300,
      },
      {
        worker_name: 'Bob',
        role: 'barback',
        total_orders: 15,
        average_time_seconds: 90,
        total_sales: 150,
      },
    ],
  },
};

const makeSalesPayload = () => ({
  data: [{ period: new Date().toISOString(), total_sales: 500 }],
});

/* ────────── utilities ─────────────────────────────────────────────── */

// render page with three queued GETs (items, workers, sales‑week default)
const renderPage = async () => {
  queueAxios(fakeItemStats, fakeWorkerStats, makeSalesPayload());
  render(
    <MemoryRouter>
      <StatisticsPage />
    </MemoryRouter>,
  );
  // first worker name shows once both first requests resolved & rendered
  await screen.findByText('Alice');
};

// opens a MUI <Select> and returns its <ul role="listbox">
const openSelect = async (button: HTMLElement) => {
  await userEvent.click(button);
  return await screen.findByRole('listbox');
};

/* ────────── test suite ────────────────────────────────────────────── */

describe('StatisticsPage behaviour', () => {
  it('renders Worker stats by default', async () => {
    await renderPage();

    expect(
      screen.getByRole('heading', { name: /worker statistics/i }),
    ).toBeInTheDocument();
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
  });

  it('allows switching to Item statistics', async () => {
    await renderPage();

    const categorySelect = screen.getAllByRole('combobox')[0];
    const listbox      = await openSelect(categorySelect);
    await userEvent.click(within(listbox).getByText(/item statistics/i));

    expect(
      await screen.findByRole('heading', { name: /item statistics/i }),
    ).toBeInTheDocument();
    expect(screen.getByText('Burger')).toBeInTheDocument();
  });

  it('shows Restaurant sales & fetches when range toggled', async () => {
    await renderPage();

    // change category → “Restaurant Sales”
    let categorySelect = screen.getAllByRole('combobox')[0];
    let listbox        = await openSelect(categorySelect);
    await userEvent.click(within(listbox).getByText(/restaurant sales/i));

    expect(
      await screen.findByRole('heading', { name: /restaurant sales over time/i }),
    ).toBeInTheDocument();

    // queue a new response before clicking “1 Day”
    axios.get.mockResolvedValueOnce(makeSalesPayload());

    await userEvent.click(screen.getByRole('button', { name: /1 day/i }));

    await waitFor(() =>
      expect(axios.get).toHaveBeenLastCalledWith(
        expect.stringContaining('range=day'),
      ),
    );
  });

  it('changes Sort‑By and reflects the new choice', async () => {
    await renderPage();

    const sortSelect = screen.getAllByRole('combobox')[1]; // second <Select>
    const listbox    = await openSelect(sortSelect);
    await userEvent.click(within(listbox).getByText(/average time/i));

    await waitFor(() =>
      expect(sortSelect).toHaveTextContent(/average time/i),
    );
  });

  it('filters workers with the search box', async () => {
    await renderPage();

    const search = screen.getByRole('textbox', { name: /search worker/i });
    await userEvent.type(search, 'Bob');

    await waitFor(() => {
      expect(screen.queryByText('Alice')).not.toBeInTheDocument();
      expect(screen.getByText('Bob')).toBeInTheDocument();
    });
  });
});

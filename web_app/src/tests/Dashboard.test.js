import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Dashboard from '../pages/Dashboard';

// Create a mock for useNavigate so we can check that it is called correctly.
const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
  // Preserve other exports if needed.
  useNavigate: () => mockedUsedNavigate,
}));

describe('Dashboard Component', () => {
  beforeEach(() => {
    // Clear sessionStorage and reset the navigate mock before each test.
    sessionStorage.clear();
    mockedUsedNavigate.mockReset();
  });

  it('renders the restaurant name when barName is in sessionStorage', () => {
    sessionStorage.setItem('barName', 'Test Restaurant');
    render(<Dashboard />);
    expect(screen.getByText(/Restaurant: Test Restaurant/)).toBeInTheDocument();
  });

  it('does not render the restaurant name when barName is not in sessionStorage', () => {
    render(<Dashboard />);
    expect(screen.queryByText(/Restaurant:/)).not.toBeInTheDocument();
  });

  it('navigates to "/orders" when the Orders button is clicked', () => {
    render(<Dashboard />);
    const ordersButton = screen.getByRole('button', { name: /Orders/i });
    fireEvent.click(ordersButton);
    expect(mockedUsedNavigate).toHaveBeenCalledWith('/orders');
  });

  it('navigates to "/menu" when the Menu button is clicked', () => {
    render(<Dashboard />);
    const menuButton = screen.getByRole('button', { name: /Menu/i });
    fireEvent.click(menuButton);
    expect(mockedUsedNavigate).toHaveBeenCalledWith('/menu');
  });
});

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Dashboard from '../pages/Dashboard';

// Mock useNavigate from react-router-dom
const mockedUsedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  useNavigate: () => mockedUsedNavigate,
}));

describe('Dashboard Component', () => {
  const getPinDisplay = () => screen.getByRole('heading', { level: 4 });

  beforeEach(() => {
    sessionStorage.clear();
    mockedUsedNavigate.mockReset();
  });

  it('renders the barName from sessionStorage', () => {
    sessionStorage.setItem('barName', 'Test Bar');
    render(<Dashboard />);
    expect(screen.getByText('Test Bar')).toBeInTheDocument();
  });

  it('falls back to "Welcome" when no barName is in sessionStorage', () => {
    render(<Dashboard />);
    expect(screen.getByText('Welcome')).toBeInTheDocument();
  });

  it('calls logout and navigates to root when Logout is clicked', () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByRole('button', { name: 'Logout' }));
    expect(mockedUsedNavigate).toHaveBeenCalledWith('/');
  });

  it('updates the PIN when digits are pressed on NumberPad', () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByRole('button', { name: '1' }));
    expect(getPinDisplay()).toHaveTextContent('*');
  });

  it('clears the PIN when Clear is pressed', () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByRole('button', { name: '1' }));
    fireEvent.click(screen.getByRole('button', { name: 'Clear' }));
    expect(getPinDisplay().textContent.trim()).toBe('');
  });

  it('deletes the last digit when ← is pressed', () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByRole('button', { name: '1' }));
    fireEvent.click(screen.getByRole('button', { name: '←' }));
    expect(getPinDisplay().textContent.trim()).toBe('');
  });
});

import React from 'react';
import { act, fireEvent, render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from '../pages/Login';
import axios from 'axios';
import { toast } from 'react-toastify';

// Mock toast
jest.mock('react-toastify', () => ({
  toast: { error: jest.fn() },
  ToastContainer: () => <div />,
}));

// Mock axios
jest.mock('axios');

// Mock useNavigate
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('Login Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders login modal with input fields and button', () => {
    render(<Login />, { wrapper: BrowserRouter });

    expect(screen.getByPlaceholderText(/username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();

    expect(screen.getAllByText(/login/i).length).toBeGreaterThanOrEqual(1);
  });

  test('updates input fields when user types', () => {
    render(<Login />, { wrapper: BrowserRouter });

    const usernameInput = screen.getByPlaceholderText(/username/i);
    const passwordInput = screen.getByPlaceholderText(/password/i);

    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'secret' } });

    expect(usernameInput.value).toBe('testuser');
    expect(passwordInput.value).toBe('secret');
  });

  test('successful login stores barName when provided in response', async () => {
    axios.post.mockResolvedValue({
      data: {
        tokens: {
          access: 'access-token',
          refresh: 'refresh-token',
        },
        bar_name: 'Test Bar',
      },
    });

    render(<Login />, { wrapper: BrowserRouter });

    fireEvent.change(screen.getByPlaceholderText(/username/i), {
      target: { value: 'user' },
    });
    fireEvent.change(screen.getByPlaceholderText(/password/i), {
      target: { value: 'pass' },
    });

    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /login/i }));
    });

    expect(sessionStorage.getItem('barName')).toBe('Test Bar');
  });

  test('successful login stores tokens and navigates', async () => {
    axios.post.mockResolvedValue({
      data: {
        tokens: {
          access: 'access-token',
          refresh: 'refresh-token',
        },
      },
    });

    render(<Login />, { wrapper: BrowserRouter });

    fireEvent.change(screen.getByPlaceholderText(/username/i), {
      target: { value: 'user' },
    });
    fireEvent.change(screen.getByPlaceholderText(/password/i), {
      target: { value: 'pass' },
    });

    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /login/i }));
    });

    expect(sessionStorage.getItem('accessToken')).toBe('access-token');
    expect(sessionStorage.getItem('refreshToken')).toBe('refresh-token');
    expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
  });

  test('failed login shows toast error', async () => {
    axios.post.mockRejectedValue(new Error('Invalid credentials'));

    render(<Login />, { wrapper: BrowserRouter });

    fireEvent.change(screen.getByPlaceholderText(/username/i), {
      target: { value: 'wrong' },
    });
    fireEvent.change(screen.getByPlaceholderText(/password/i), {
      target: { value: 'incorrect' },
    });

    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /login/i }));
    });

    expect(toast.error).toHaveBeenCalledWith(
      'Invalid username or password. Please try again.',
    );
  });
});

import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Registration from '../pages/Registration';
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

const fillStep1 = () => {
  fireEvent.change(screen.getByPlaceholderText(/First & Last Name/i), {
    target: { value: 'Test User' },
  });
  fireEvent.change(screen.getByPlaceholderText(/Desired Username/i), {
    target: { value: 'testuser' },
  });
  fireEvent.change(screen.getByPlaceholderText(/Desired Password/i), {
    target: { value: 'password123' },
  });
  fireEvent.change(screen.getByPlaceholderText(/Confirm Password/i), {
    target: { value: 'password123' },
  });
};

const fillStep2 = () => {
  fireEvent.change(screen.getByPlaceholderText(/Email/i), {
    target: { value: 'test@example.com' },
  });
  fireEvent.change(screen.getByPlaceholderText(/Phone Number/i), {
    target: { value: '1234567890' },
  });
  fireEvent.change(screen.getByPlaceholderText(/Business Name/i), {
    target: { value: 'Test Business' },
  });
  fireEvent.change(screen.getByPlaceholderText(/Business Address/i), {
    target: { value: '123 Test St' },
  });
};

describe('Registration Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders Step 1 fields and Continue button', () => {
    render(<Registration />, { wrapper: BrowserRouter });

    expect(screen.getByPlaceholderText(/First & Last Name/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Desired Username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Desired Password/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Confirm Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Continue/i })).toBeInTheDocument();
  });

  test('shows error if Step 1 fields are missing', () => {
    render(<Registration />, { wrapper: BrowserRouter });

    fireEvent.click(screen.getByRole('button', { name: /Continue/i }));
    expect(toast.error).toHaveBeenCalledWith('Please fill out all fields.');
  });

  test('shows error if passwords do not match', () => {
    render(<Registration />, { wrapper: BrowserRouter });

    fireEvent.change(screen.getByPlaceholderText(/First & Last Name/i), {
      target: { value: 'Test User' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Desired Username/i), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Desired Password/i), {
      target: { value: 'password123' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Confirm Password/i), {
      target: { value: 'wrongpass' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Continue/i }));
    expect(toast.error).toHaveBeenCalledWith('Passwords do not match!');
  });

  test('goes to Step 2 with valid Step 1 inputs', () => {
    render(<Registration />, { wrapper: BrowserRouter });
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

    expect(screen.getByPlaceholderText(/Email/i)).toBeInTheDocument();
  });

  test('shows error if Step 2 fields are missing', () => {
    render(<Registration />, { wrapper: BrowserRouter });
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

    fireEvent.click(screen.getByRole('button', { name: /Register/i }));
    expect(toast.error).toHaveBeenCalledWith('Please fill out all fields in Step 2.');
  });

  test('shows error for invalid email or phone', () => {
    render(<Registration />, { wrapper: BrowserRouter });
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

    fireEvent.change(screen.getByPlaceholderText(/Email/i), {
      target: { value: 'invalid-email' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Phone Number/i), {
      target: { value: '123' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Business Name/i), {
      target: { value: 'Biz' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Business Address/i), {
      target: { value: '123 Street' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Register/i }));
    expect(toast.error).toHaveBeenCalledWith('Please enter a valid email address.');
  });

  test('successful registration stores tokens and navigates', async () => {
    axios.post.mockResolvedValue({
      data: {
        tokens: { access: 'access-token', refresh: 'refresh-token' },
      },
    });

    render(<Registration />, { wrapper: BrowserRouter });
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /Continue/i }));
    fillStep2();

    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /Register/i }));
    });

    expect(localStorage.getItem('accessToken')).toBe('access-token');
    expect(localStorage.getItem('refreshToken')).toBe('refresh-token');
    expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
  });

  test('shows error on registration failure', async () => {
    axios.post.mockRejectedValue({ response: { data: 'Error from API' } });

    render(<Registration />, { wrapper: BrowserRouter });
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /Continue/i }));
    fillStep2();

    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /Register/i }));
    });

    expect(toast.error).toHaveBeenCalledWith('Registration failed: Error from API');
  });
});

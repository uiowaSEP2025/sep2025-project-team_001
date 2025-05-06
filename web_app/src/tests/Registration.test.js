/* __tests__/Registration.test.js */
import React from 'react';
import { render, fireEvent, screen, act, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Registration from '../pages/Registration';          // ← adjust if your path differs
import axios from 'axios';
import { toast } from 'react-toastify';

/* ------------------------------------------------------------------ */
/*  Mocks                                                              */
/* ------------------------------------------------------------------ */
process.env.REACT_APP_API_URL = 'http://api.test';

jest.mock('axios');
jest.mock('react-toastify', () => ({
  toast: { error: jest.fn() },
  ToastContainer: () => <div data-testid="toast-container" />,
}));
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

/* mock FileReader once for all tests */
const fileReaderMock = () => {
  const onloadend = jest.fn();
  return {
    readAsDataURL: function () {
      this.result = 'data:image/png;base64,MOCK';
      onloadend();
      if (typeof this.onloadend === 'function') this.onloadend();
    },
    onloadend: null,
    result: null,
  };
};

beforeEach(() => {
  jest.spyOn(global, 'FileReader').mockImplementation(fileReaderMock);
  sessionStorage.clear();
  jest.clearAllMocks();
});
afterAll(() => {
  global.FileReader.mockRestore();
});

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */
const renderPage = () => render(<Registration />, { wrapper: BrowserRouter });

const fillStep1 = ({
  name = 'User Name',
  username = 'user',
  password = 'password123',
  confirmPassword = 'password123',
  pin = '1234',
} = {}) => {
  fireEvent.change(screen.getByPlaceholderText(/First & Last Name/i), {
    target: { value: name },
  });
  fireEvent.change(screen.getByPlaceholderText(/Desired Username/i), {
    target: { value: username },
  });
  fireEvent.change(screen.getByPlaceholderText(/Desired Password/i), {
    target: { value: password },
  });
  fireEvent.change(screen.getByPlaceholderText(/Confirm Password/i), {
    target: { value: confirmPassword },
  });
  fireEvent.change(screen.getByPlaceholderText(/4-digit pin/i), {
    target: { value: pin },
  });
};

const fillStep2 = ({
  email = 'user@test.com',
  phone = '1234567890',
  business_name = 'Test Bar',
  business_address = '123 Test St',
  withImage = true,
} = {}) => {
  fireEvent.change(screen.getByPlaceholderText(/Email/i), {
    target: { value: email },
  });
  fireEvent.change(screen.getByPlaceholderText(/Phone Number/i), {
    target: { value: phone },
  });
  fireEvent.change(screen.getByPlaceholderText(/Business Name/i), {
    target: { value: business_name },
  });
  fireEvent.change(screen.getByPlaceholderText(/Business Address/i), {
    target: { value: business_address },
  });

  if (withImage) {
    const input = document.getElementById('upload');
    fireEvent.change(input, {
      target: { files: [new File(['x'], 'x.png', { type: 'image/png' })] },
    });
  }
};

/* ------------------------------------------------------------------ */
/*  Tests                                                              */
/* ------------------------------------------------------------------ */
describe('Registration page', () => {
  /* ---------- Step‑1 basic rendering ---------- */
  test('renders Step 1 inputs and Continue button', () => {
    renderPage();
    expect(screen.getByRole('button', { name: /continue/i })).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Desired Username/i)).toBeInTheDocument();
  });

  /* ---------- Step‑1 validation branches ---------- */
  test('shows error when Step 1 fields missing', () => {
    renderPage();
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    expect(toast.error).toHaveBeenCalledWith('Please fill out all fields.');
  });

  test('mismatched passwords error', () => {
    renderPage();
    fillStep1({ confirmPassword: 'nope' });
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    expect(toast.error).toHaveBeenCalledWith('Passwords do not match!');
  });

  test('short password error', () => {
    renderPage();
    fillStep1({ password: '123', confirmPassword: '123' });
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    expect(toast.error).toHaveBeenCalledWith(
      'Password must be at least 6 characters long.',
    );
  });

  test('pin must be 4 digits', () => {
    renderPage();
    fillStep1({ pin: '12' });
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    expect(toast.error).toHaveBeenCalledWith('PIN must be exactly 4 digits.');
  });

  /* ---------- Move to Step‑2 ---------- */
  test('advances to Step 2 with valid inputs', () => {
    renderPage();
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    expect(screen.getByPlaceholderText(/Email/i)).toBeInTheDocument();
  });

  /* ---------- Step‑2 validation ---------- */
  test('missing Step 2 fields error', () => {
    renderPage();
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    fireEvent.click(screen.getByRole('button', { name: /register/i }));
    expect(toast.error).toHaveBeenCalledWith(
      'Please fill out all fields in Step 2.',
    );
  });

  test('invalid email address error', () => {
    renderPage();
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    fillStep2({ email: 'bad@email', withImage: true });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));
    expect(toast.error).toHaveBeenCalledWith('Please enter a valid email address.');
  });

  test('invalid phone digits error', () => {
    renderPage();
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    fillStep2({ phone: '999', withImage: true });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));
    expect(toast.error).toHaveBeenCalledWith(
      'Phone number must be exactly 10 digits.',
    );
  });

  /* ---------- Restaurant validation fails ---------- */
  test('shows error when restaurant address invalid', async () => {
    axios.post.mockResolvedValueOnce({ data: { valid: false } }); // validate_restaurant
    renderPage();
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    fillStep2();

    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /register/i }));
    });

    expect(toast.error).toHaveBeenCalledWith(
      'Invalid business address. Contact streamlinebars@gmail.com for manual verification',
    );
    expect(axios.post).toHaveBeenCalledTimes(1); // never hit /register/
  });

  /* ---------- Successful registration ---------- */
  test('stores tokens & navigates on success', async () => {
    axios.post
      .mockResolvedValueOnce({ data: { valid: true } }) // validate_restaurant
      .mockResolvedValueOnce({
        data: {
          tokens: { access: 'ac', refresh: 'rf' },
          restaurant_id: 99,
        },
      }); // register

    renderPage();
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    fillStep2();

    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /register/i }));
    });

    expect(sessionStorage.getItem('accessToken')).toBe('ac');
    expect(sessionStorage.getItem('refreshToken')).toBe('rf');
    expect(sessionStorage.getItem('restaurantId')).toBe('99');
    expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
  });

  /* ---------- API ‑ explicit error message ---------- */
  test('displays API error message', async () => {
    axios.post
      .mockResolvedValueOnce({ data: { valid: true } })
      .mockRejectedValueOnce({ response: { data: { message: 'API bad' } } });

    renderPage();
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    fillStep2();

    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /register/i }));
    });

    expect(toast.error).toHaveBeenCalledWith('Registration failed: API bad');
  });

  /* ---------- API ‑ network failure ---------- */
  test('handles network error gracefully', async () => {
    axios.post
      .mockResolvedValueOnce({ data: { valid: true } })
      .mockRejectedValueOnce(new Error('Network'));

    renderPage();
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    fillStep2();

    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /register/i }));
    });

    expect(toast.error).toHaveBeenCalledWith('Registration failed: Network');
  });

  /* ---------- Image upload UI ---------- */
  test('shows file chosen indicator', async () => {
    renderPage();
    fillStep1();
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));

    await act(async () => {
      const input = document.getElementById('upload');
      fireEvent.change(input, {
        target: { files: [new File(['x'], 'x.png', { type: 'image/png' })] },
      });
    });

    expect(screen.getByText(/Image selected/i)).toBeInTheDocument();
  });
});

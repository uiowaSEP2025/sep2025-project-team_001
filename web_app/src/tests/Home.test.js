import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Home from '../pages/Home';

test('renders Home page with Register and Log In buttons', () => {
  render(
    <BrowserRouter>
      <Home />
    </BrowserRouter>,
  );

  const registerButton = screen.getByRole('button', { name: /register/i });
  expect(registerButton).toBeInTheDocument();

  const loginButton = screen.getByRole('button', { name: /log in/i });
  expect(loginButton).toBeInTheDocument();

  expect(screen.getByRole('link', { name: /register/i })).toHaveAttribute(
    'href',
    '/register',
  );
  expect(screen.getByRole('link', { name: /log in/i })).toHaveAttribute(
    'href',
    '/login',
  );
});

test('renders footer with a year present', () => {
  render(
    <BrowserRouter>
      <Home />
    </BrowserRouter>,
  );

  const footer = screen.getByText(
    /© \d{4} Streamline App\. All rights reserved\./i,
  );
  expect(footer).toBeInTheDocument();
});

test('renders logo with correct src and alt text', () => {
  render(
    <BrowserRouter>
      <Home />
    </BrowserRouter>,
  );

  const logo = screen.getByAltText(/streamline logo/i);
  expect(logo).toBeInTheDocument();
  expect(logo).toHaveAttribute('src', '/images/StreamlineLogo.png');
});

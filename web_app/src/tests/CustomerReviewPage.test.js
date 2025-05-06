import React from 'react';
import { render, screen, within } from '@testing-library/react';
import CustomerReviewPage from '../pages/CustomerReviewPage';
import axios from 'axios';

jest.mock('axios');

describe('CustomerReviewPage', () => {
  const mockReviews = [
    {
      id: 1,
      customer_name: 'John Doe',
      worker_name: 'Jane Smith',
      rating: 4,
      comment: 'Great service!',
      created_at: '2024-05-01T12:00:00Z',
    },
    {
      id: 2,
      customer_name: 'Alice',
      worker_name: null,
      rating: 5,
      comment: '',
      created_at: '2024-05-02T15:30:00Z',
    },
  ];

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders customer reviews when data is fetched', async () => {
    axios.get.mockResolvedValueOnce({ data: mockReviews });

    render(<CustomerReviewPage />);

    expect(await screen.findByText(/Customer Reviews/i)).toBeInTheDocument();

    const cardElements = (
      await screen.findAllByText(/Customer:/i)
    ).map(el => el.closest('.MuiPaper-root'));

    expect(cardElements).toHaveLength(2);

    const first = within(cardElements[0]);

    expect(first.getByText(/Customer:/i)).toBeInTheDocument();
    expect(first.getByText(/John Doe/i)).toBeInTheDocument();
    expect(first.getByText(/Worker:/i)).toBeInTheDocument();
    expect(first.getByText(/Jane Smith/i)).toBeInTheDocument();
    expect(first.getByText(/Comment:/i)).toBeInTheDocument();
    expect(first.getByText(/Great service!/i)).toBeInTheDocument();

    const second = within(cardElements[1]);

    expect(second.getByText(/Customer:/i)).toBeInTheDocument();
    expect(second.getByText(/Alice/i)).toBeInTheDocument();
    expect(second.getByText(/Worker:/i)).toBeInTheDocument();
    expect(second.getByText(/N\/A/i)).toBeInTheDocument();
    expect(second.getByText(/Comment:/i)).toBeInTheDocument();
    expect(second.getByText(/No comment provided\./i)).toBeInTheDocument();
  });

  it('renders fallback text when there are no reviews', async () => {
    axios.get.mockResolvedValueOnce({ data: [] });

    render(<CustomerReviewPage />);

    expect(await screen.findByText(/No reviews yet\./i)).toBeInTheDocument();
  });

  it('logs an error when the API call fails', async () => {
    const consoleSpy = jest
      .spyOn(console, 'error')
      .mockImplementation(() => {});

    axios.get.mockRejectedValueOnce(new Error('Network error'));

    render(<CustomerReviewPage />);

    // component shows fallback UI when fetch fails
    await screen.findByText(/No reviews yet\./i);

    expect(consoleSpy).toHaveBeenCalledWith(
      'Error fetching reviews:',
      expect.any(Error)
    );

    consoleSpy.mockRestore();
  });
});

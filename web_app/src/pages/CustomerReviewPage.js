import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Paper, Stack, Divider } from '@mui/material';

const CustomerReviewPage = () => {
    const [reviews, setReviews] = useState([]);

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_API_URL}/reviews/`);
                setReviews(response.data);
            } catch (error) {
                console.error('Error fetching reviews:', error);
            }
        };

        fetchReviews();
    }, []);
    return (
        <Box sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>Customer Reviews</Typography>
          <Stack spacing={2}>
            {reviews.map((review) => (
              <Paper key={review.id} sx={{ p: 2 }}>
                <Typography variant="subtitle1"><strong>Customer:</strong> {review.order.customer.user.username}</Typography>
                <Typography variant="subtitle2"><strong>Worker:</strong> {review.order.worker?.name || 'N/A'}</Typography>
                <Typography><strong>Rating:</strong> {review.rating} / 5</Typography>
                <Typography><strong>Comment:</strong> {review.comment || 'No comment provided.'}</Typography>
                <Typography variant="caption" color="text.secondary">
                  Submitted on: {new Date(review.created_at).toLocaleString()}
                </Typography>
              </Paper>
            ))}
            {reviews.length === 0 && <Typography>No reviews yet.</Typography>}
          </Stack>
        </Box>
      );
    };
    
    export default ReviewPage;
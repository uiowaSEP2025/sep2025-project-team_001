import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Paper, Stack, Divider } from '@mui/material';
import Rating from '@mui/material/Rating';
import StarIcon from '@mui/icons-material/Star';

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
                <Typography variant="subtitle1"><strong>Customer:</strong> {review.customer_name}</Typography>
                <Typography variant="subtitle2"><strong>Worker:</strong> {review.worker_name || 'N/A'}</Typography>
    
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Typography><strong>Rating:</strong></Typography>
                  <Rating
                    name="read-only-rating"
                    value={review.rating}
                    readOnly
                    precision={1}
                    icon={<StarIcon fontSize="inherit" />}
                    emptyIcon={<StarIcon fontSize="inherit" style={{ opacity: 0.3 }} />}
                  />
                </Box>
    
                <Typography sx={{ mt: 1 }}><strong>Comment:</strong> {review.comment || 'No comment provided.'}</Typography>
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
    
    export default CustomerReviewPage;
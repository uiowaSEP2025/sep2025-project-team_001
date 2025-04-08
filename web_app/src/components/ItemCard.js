import React from 'react';
import {
  Box,
  Card,
  CardContent,
  CardMedia,
  Chip,
  IconButton,
  Switch,
  Typography,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

const ItemCard = ({ item, onToggle, onDelete }) => {
  const handleToggle = () => onToggle(item);
  const handleDelete = () => onDelete(item.id);

  return (
    <Card
      sx={{
        width: 320,
        height: 250,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        position: 'relative',
        overflow: 'hidden',
        transition: 'all 0.2s ease-in-out',
        '&:hover': {
          boxShadow: 6,
          transform: 'scale(1.01)',
        },
      }}
    >
      <CardContent sx={{ paddingBottom: '48px' }}>
        {/* Content row: Text + Image */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 1 }}>
          {/* Left side (name, desc, chips) */}
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              {item.name}
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
              }}
            >
              {item.description}
            </Typography>

            <Box
              sx={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: 0.5,
                mt: 1,
                maxHeight: 56,
                overflowY: 'auto',
                '&::-webkit-scrollbar': { display: 'none' },
                '&:hover::-webkit-scrollbar': { display: 'block' },
                '&::-webkit-scrollbar-thumb': {
                  backgroundColor: '#ccc',
                  borderRadius: '4px',
                },
              }}
            >
              {item.ingredients.map((ing, idx) => (
                <Chip key={idx} label={ing.name || ing} size="small" />
              ))}
            </Box>
          </Box>

          {/* Image */}
          <CardMedia
            component="img"
            image={item.base64_image}
            alt={item.name}
            sx={{
              width: 140,
              height: 140,
              objectFit: 'cover',
              borderRadius: 1,
              border: '1px solid #ccc',
              flexShrink: 0,
            }}
          />
        </Box>

        {/* Price and toggle */}
        <Typography variant="body2" sx={{ mt: 1 }}>
          Price: ${item.price.toFixed(2)}
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
          <Typography variant="body2" sx={{ mr: 1 }}>
            Available:
          </Typography>
          <Switch
            checked={item.available}
            onChange={handleToggle}
            color="primary"
            size="small"
          />
        </Box>
      </CardContent>

      {/* Trash icon */}
      <IconButton
        onClick={handleDelete}
        sx={{
          position: 'absolute',
          bottom: 8,
          right: 8,
          color: 'error.main',
        }}
      >
        <DeleteIcon />
      </IconButton>
    </Card>
  );
};

export default ItemCard;

// 🟢 HEAD IMPORTS
import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Checkbox,
  Chip,
  Collapse,
  FormControlLabel,
  Grid,
  IconButton,
  MenuItem,
  Modal,
  Paper,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import { useNavigate } from 'react-router-dom';
import ItemCard from '../components/ItemCard';

const MenuPage = () => {
  const navigate = useNavigate();
  const barName = sessionStorage.getItem('barName');

  const [items, setItems] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [imageBase64, setImageBase64] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    category: '',
    stock: '',
    available: true,
    ingredients: [],
  });

  // Collapse states
  const [showAvailable, setShowAvailable] = useState(true);
  const [showUnavailable, setShowUnavailable] = useState(true);
  const [showAvailableFood, setShowAvailableFood] = useState(true);
  const [showAvailableBeverages, setShowAvailableBeverages] = useState(true);
  const [showUnavailableFood, setShowUnavailableFood] = useState(true);
  const [showUnavailableBeverages, setShowUnavailableBeverages] =
    useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = () => {
    fetch(`${process.env.REACT_APP_API_URL}/api/menu-items/`, {
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem('accessToken')}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        const normalized = (data.items || []).map((item) => ({
          ...item,
          ingredients: item.ingredients.map((ing) =>
            typeof ing === 'string' ? ing : ing.name,
          ),
        }));
        setItems(normalized);
      });
  };

  const toggleAvailability = (item) => {
    const updatedItem = {
      item_id: item.id,
      name: item.name,
      description: item.description,
      price: item.price,
      category: item.category,
      stock: item.stock,
      available: !item.available,
      image: item.base64_image,
      ingredients: item.ingredients.map((ing) =>
        typeof ing === 'string' ? ing : ing.name,
      ),
      action: 'update',
    };

    fetch(`${process.env.REACT_APP_API_URL}/api/manage-item/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${sessionStorage.getItem('accessToken')}`,
      },
      body: JSON.stringify(updatedItem),
    }).then(() => fetchItems());
  };

  const handleDelete = (itemId) => {
    fetch(`${process.env.REACT_APP_API_URL}/api/manage-item/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${sessionStorage.getItem('accessToken')}`,
      },
      body: JSON.stringify({ action: 'delete', item_id: itemId }),
    }).then(() => fetchItems());
  };

  // Modal Handlers
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onloadend = () => setImageBase64(reader.result);
    if (file) reader.readAsDataURL(file);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      e.preventDefault();
      setFormData((prev) => ({
        ...prev,
        ingredients: prev.ingredients.includes(inputValue.trim())
          ? prev.ingredients
          : [...prev.ingredients, inputValue.trim()],
      }));
      setInputValue('');
    }
  };

  const handleChipDelete = (ingredientToDelete) => () => {
    setFormData((prev) => ({
      ...prev,
      ingredients: prev.ingredients.filter((i) => i !== ingredientToDelete),
    }));
  };

  const handleCreate = (e) => {
    e.preventDefault();
    fetch(`${process.env.REACT_APP_API_URL}/api/manage-item/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${sessionStorage.getItem('accessToken')}`,
      },
      body: JSON.stringify({
        action: 'create',
        ...formData,
        price: parseFloat(formData.price),
        stock: parseInt(formData.stock),
        image: imageBase64,
      }),
    })
      .then((res) => res.json())
      .then(() => {
        setShowCreateModal(false);
        fetchItems();
      });
  };

  // Filters
  const availableItems = items.filter((i) => i.available);
  const unavailableItems = items.filter((i) => !i.available);
  const byCategory = (list, category) =>
    list.filter((i) => i.category.toLowerCase() === category);
  const filteredItems = items.filter((item) =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  return (
    <Box sx={{ mt: 4, px: 6, maxWidth: '1460px', mx: 'auto', pb: 10 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Button onClick={() => navigate('/manager_dashboard')}>Dashboard</Button>
        <Typography variant="h4">Menu Manager</Typography>
        <Box width={100} />
      </Box>

      {/* Search Bar and Add Item Button */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 3,
        }}
      >
        <Button
          startIcon={<AddCircleOutlineIcon />}
          variant="contained"
          onClick={() => setShowCreateModal(true)}
          sx={{ mr: 1, height: 56, width: 180 }}
        >
          Add Item
        </Button>
        <TextField
          label="Search menu items"
          variant="outlined"
          fullWidth
          sx={{ height: 56 }}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </Box>

      {/* If searching, display flat list of filtered items */}
      {searchTerm ? (
        <>
          <Typography variant="h5" mb={2}>
            Search Results
          </Typography>
          <Grid container spacing={2}>
            {filteredItems.map((item) => (
              <Grid item xs={12} sm={6} md={3} key={item.id}>
                <ItemCard
                  item={item}
                  onDelete={handleDelete}
                  onToggle={toggleAvailability}
                />
              </Grid>
            ))}
          </Grid>
        </>
      ) : (
        <>
          {/* Available */}
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              mb: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <IconButton onClick={() => setShowAvailable((prev) => !prev)}>
                {showAvailable ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              </IconButton>
              <Typography variant="h5">Available Items</Typography>
            </Box>
          </Box>

          <Collapse in={showAvailable}>
            <Box sx={{ backgroundColor: '#e3f2fd', p: 2, borderRadius: 2 }}>
              {/* Available Beverages */}
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <IconButton
                  onClick={() => setShowAvailableBeverages((prev) => !prev)}
                >
                  {showAvailableBeverages ? (
                    <ExpandLessIcon />
                  ) : (
                    <ExpandMoreIcon />
                  )}
                </IconButton>
                <Typography variant="h6">Beverages</Typography>
              </Box>
              <Collapse in={showAvailableBeverages}>
                <Grid container spacing={2}>
                  {byCategory(availableItems, 'beverage').map((item) => (
                    <Grid item xs={12} sm={6} md={3} key={item.id}>
                      <ItemCard
                        item={item}
                        onDelete={handleDelete}
                        onToggle={toggleAvailability}
                      />
                    </Grid>
                  ))}
                </Grid>
              </Collapse>

              {/* Available Food */}
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 4, mb: 1 }}>
                <IconButton
                  onClick={() => setShowAvailableFood((prev) => !prev)}
                >
                  {showAvailableFood ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                </IconButton>
                <Typography variant="h6">Food</Typography>
              </Box>
              <Collapse in={showAvailableFood}>
                <Grid container spacing={2}>
                  {byCategory(availableItems, 'food').map((item) => (
                    <Grid item xs={12} sm={6} md={3} key={item.id}>
                      <ItemCard
                        item={item}
                        onDelete={handleDelete}
                        onToggle={toggleAvailability}
                      />
                    </Grid>
                  ))}
                </Grid>
              </Collapse>
            </Box>
          </Collapse>

          {/* Unavailable */}
          <Box sx={{ display: 'flex', alignItems: 'center', mt: 6, mb: 2 }}>
            <IconButton onClick={() => setShowUnavailable((prev) => !prev)}>
              {showUnavailable ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            </IconButton>
            <Typography variant="h5">Unavailable Items</Typography>
          </Box>

          <Collapse in={showUnavailable}>
            <Box sx={{ backgroundColor: '#ffcdd2', p: 2, borderRadius: 2 }}>
              {/* Unavailable Beverages */}
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <IconButton
                  onClick={() => setShowUnavailableBeverages((prev) => !prev)}
                >
                  {showUnavailableBeverages ? (
                    <ExpandLessIcon />
                  ) : (
                    <ExpandMoreIcon />
                  )}
                </IconButton>
                <Typography variant="h6">Beverages</Typography>
              </Box>
              <Collapse in={showUnavailableBeverages}>
                <Grid container spacing={2}>
                  {byCategory(unavailableItems, 'beverage').map((item) => (
                    <Grid item xs={12} sm={6} md={3} key={item.id}>
                      <ItemCard
                        item={item}
                        onDelete={handleDelete}
                        onToggle={toggleAvailability}
                      />
                    </Grid>
                  ))}
                </Grid>
              </Collapse>

              {/* Unavailable Food */}
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 4, mb: 1 }}>
                <IconButton
                  onClick={() => setShowUnavailableFood((prev) => !prev)}
                >
                  {showUnavailableFood ? (
                    <ExpandLessIcon />
                  ) : (
                    <ExpandMoreIcon />
                  )}
                </IconButton>
                <Typography variant="h6">Food</Typography>
              </Box>
              <Collapse in={showUnavailableFood}>
                <Grid container spacing={2}>
                  {byCategory(unavailableItems, 'food').map((item) => (
                    <Grid item xs={12} sm={6} md={3} key={item.id}>
                      <ItemCard
                        item={item}
                        onDelete={handleDelete}
                        onToggle={toggleAvailability}
                      />
                    </Grid>
                  ))}
                </Grid>
              </Collapse>
            </Box>
          </Collapse>
        </>
      )}

      {/* CREATE ITEM MODAL */}
      <Modal open={showCreateModal} onClose={() => setShowCreateModal(false)}>
        <Box
          component={Paper}
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: 500,
            p: 4,
            maxHeight: '90vh',
            overflowY: 'auto',
          }}
        >
          <Typography variant="h6" mb={2}>
            Create New Menu Item
          </Typography>
          <form onSubmit={handleCreate}>
            <TextField
              fullWidth
              label="Item Name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              multiline
              rows={2}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Price"
              name="price"
              type="number"
              value={formData.price}
              onChange={handleChange}
              required
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Category"
              name="category"
              select
              value={formData.category}
              onChange={handleChange}
              required
              sx={{ mb: 2 }}
            >
              <MenuItem value="beverage">Beverage</MenuItem>
              <MenuItem value="food">Food</MenuItem>
            </TextField>
            <TextField
              fullWidth
              label="Stock"
              name="stock"
              type="number"
              value={formData.stock}
              onChange={handleChange}
              required
              sx={{ mb: 2 }}
            />
            <FormControlLabel
              control={
                <Checkbox
                  name="available"
                  checked={formData.available}
                  onChange={handleChange}
                />
              }
              label="Available"
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Add Ingredient"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              sx={{ mb: 1 }}
            />
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
              {formData.ingredients.map((ing, idx) => (
                <Chip key={idx} label={ing} onDelete={handleChipDelete(ing)} />
              ))}
            </Box>
            <Button
              fullWidth
              component="label"
              variant="outlined"
              sx={{ mb: 2 }}
            >
              Upload Image
              <input
                type="file"
                accept="image/*"
                hidden
                onChange={handleImageUpload}
              />
            </Button>
            {imageBase64 && (
              <Box sx={{ mb: 2, textAlign: 'center' }}>
                <img
                  src={imageBase64}
                  alt="Preview"
                  style={{ maxHeight: 150, maxWidth: '100%', borderRadius: 4 }}
                />
              </Box>
            )}
            <Stack direction="row" spacing={2} justifyContent="flex-end">
              <Button variant="contained" type="submit">
                Create
              </Button>
              <Button onClick={() => setShowCreateModal(false)}>Cancel</Button>
            </Stack>
          </form>
        </Box>
      </Modal>
    </Box>
  );
};

export default MenuPage;

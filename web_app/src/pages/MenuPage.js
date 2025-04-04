import React, { useEffect, useState } from 'react';
import '../pages/styles/MenuPage.css';
import ItemCard from '../components/ItemCard.js';
import { useNavigate } from 'react-router-dom';

const MenuPage = () => {
  const [items, setItems] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteItemId, setDeleteItemId] = useState(null);
  const [imageBase64, setImageBase64] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    category: '',
    stock: '',
    available: true,
  });
  const barName = sessionStorage.getItem('barName');
  const navigate = useNavigate();

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = () => {
    fetch(`${process.env.REACT_APP_API_URL}/api/menu-items/`, {
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem('accessToken')}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setItems(data.items || []);
      })
      .catch((error) => {
        console.error('Error fetching menu items:', error);
      });
  };

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

    reader.onloadend = () => {
      setImageBase64(reader.result);
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const openCreateModal = () => {
    setFormData({
      name: '',
      description: '',
      price: '',
      category: '',
      stock: '',
      available: true,
    });
    setImageBase64('');
    setShowCreateModal(true);
  };

  const closeCreateModal = () => {
    setShowCreateModal(false);
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
      .then((response) => response.json())
      .then((data) => {
        console.log('Created item:', data); // ← log here
        setShowCreateModal(false);
        fetchItems();
      })
      .catch((error) => {
        console.error('Error creating item:', error);
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
      action: 'update',
    };

    fetch(`${process.env.REACT_APP_API_URL}/api/manage-item/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${sessionStorage.getItem('accessToken')}`,
      },
      body: JSON.stringify(updatedItem),
    })
      .then(() => {
        fetchItems();
      })
      .catch((error) => {
        console.error('Error updating item availability:', error);
      });
  };

  const confirmDelete = (itemId) => {
    setDeleteItemId(itemId);
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = () => {
    fetch(`${process.env.REACT_APP_API_URL}/api/manage-item/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${sessionStorage.getItem('accessToken')}`,
      },
      body: JSON.stringify({
        action: 'delete',
        item_id: deleteItemId,
      }),
    })
      .then(() => {
        setDeleteItemId(null);
        setShowDeleteModal(false);
        fetchItems();
      })
      .catch((error) => {
        console.error('Error deleting item:', error);
      });
  };

  const availableBeverages = items.filter(
    (item) => item.available && item.category.toLowerCase() === 'beverage',
  );
  const availableFood = items.filter(
    (item) => item.available && item.category.toLowerCase() === 'food',
  );
  const unavailableBeverages = items.filter(
    (item) => !item.available && item.category.toLowerCase() === 'beverage',
  );
  const unavailableFood = items.filter(
    (item) => !item.available && item.category.toLowerCase() === 'food',
  );

  return (
    <div>
      <div className="menu-page">
        <div className="menu-page-container">
          <button
            className="menu-back-button"
            onClick={() => navigate('/dashboard')}
          >
            Dashboard
          </button>

          {barName && <h2> Restaurant: {barName} </h2>}
          <h2>Menu Manager</h2>
          <button className="menu-create-button" onClick={openCreateModal}>
            Create New Item
          </button>
        </div>

        <div className="menu-section-header">Available Items</div>
        <div className="menu-sub-section-header">Beverages</div>
        {availableBeverages.length === 0 && <p>No available beverages.</p>}
        {availableBeverages.map((item) => (
          <ItemCard
            key={item.id}
            item={item}
            onToggle={toggleAvailability}
            onDelete={confirmDelete}
          />
        ))}

        <div className="menu-sub-section-header">Food</div>
        {availableFood.length === 0 && <p>No available food items.</p>}
        {availableFood.map((item) => (
          <ItemCard
            key={item.id}
            item={item}
            onToggle={toggleAvailability}
            onDelete={confirmDelete}
          />
        ))}

        <div className="menu-section-header">Unavailable Items</div>
        <div className="menu-sub-section-header">Beverages</div>
        {unavailableBeverages.length === 0 && <p>No unavailable beverages.</p>}
        {unavailableBeverages.map((item) => (
          <ItemCard
            key={item.id}
            item={item}
            onToggle={toggleAvailability}
            onDelete={confirmDelete}
          />
        ))}

        <div className="menu-sub-section-header">Food</div>
        {unavailableFood.length === 0 && <p>No unavailable food items.</p>}
        {unavailableFood.map((item) => (
          <ItemCard
            key={item.id}
            item={item}
            onToggle={toggleAvailability}
            onDelete={confirmDelete}
          />
        ))}

        {/* Create Modal */}
        {showCreateModal && (
          <div className="menu-modal-overlay">
            <div className="menu-modal-content">
              <h3>Create New Menu Item</h3>
              <form onSubmit={handleCreate}>
                <div>
                  <label>Item Name:</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <label>Description:</label>
                  <input
                    type="text"
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label>Price:</label>
                  <input
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <label>Category:</label>
                  <select
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    required
                  >
                    <option value="">Select Category</option>
                    <option value="beverage">Beverage</option>
                    <option value="food">Food</option>
                  </select>
                </div>
                <div>
                  <label>Stock:</label>
                  <input
                    type="number"
                    name="stock"
                    value={formData.stock}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <label>Available:</label>
                  <input
                    type="checkbox"
                    name="available"
                    checked={formData.available}
                    onChange={(e) =>
                      setFormData({ ...formData, available: e.target.checked })
                    }
                  />
                </div>
                <div>
                  <label>Upload Image:</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    required
                  />
                </div>
                {imageBase64 && (
                  <div className="menu-image-preview-container">
                    <p>Image Preview:</p>
                    <img
                      src={imageBase64}
                      alt="Preview"
                      className="menu-image-preview"
                    />
                  </div>
                )}
                <button type="submit">Create</button>
                <button
                  type="button"
                  className="cancel-button"
                  onClick={closeCreateModal}
                >
                  Cancel
                </button>
              </form>
            </div>
          </div>
        )}

        {/* Delete Modal */}
        {showDeleteModal && (
          <div className="menu-modal-overlay">
            <div className="menu-modal-content">
              <h3>Confirm Delete</h3>
              <p>Are you sure you want to delete this item?</p>
              <button onClick={handleDeleteConfirm}>Yes</button>
              <button
                className="cancel-button"
                onClick={() => setShowDeleteModal(false)}
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
export default MenuPage;

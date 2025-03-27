import React, { useState, useEffect } from 'react';
import '../pages/styles/MenuPage.css';
import ItemCard from '../components/ItemCard.js'; 
const MenuPage = () => {
    const [items, setItems] = useState([]);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [deleteItemId, setDeleteItemId] = useState(null);

    const [formData, setFormData] = useState({
        name: '',
        description: '',
        price: '',
        category: '',
        stock: '',
        available: true
    });

    useEffect(() => {
        fetchItems();
    }, []);

    const fetchItems = () => {
        fetch('/api/menu-items/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
            }
        })
            .then(response => response.json())
            .then(data => {
                setItems(data.items || []);
            })
            .catch(error => {
                console.error('Error fetching menu items:', error);
            });
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const openCreateModal = () => {
        setFormData({
            name: '',
            description: '',
            price: '',
            category: '',
            stock: '',
            available: true
        });
        setShowCreateModal(true);
    };

    const closeCreateModal = () => {
        setShowCreateModal(false);
    };

    const handleCreate = (e) => {
        e.preventDefault();
        fetch('/api/manage-item/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization' : `Bearer ${localStorage.getItem('accessToken')}`
            },
            body: JSON.stringify({
                action: 'create',
                ...formData,
                price: parseFloat(formData.price),
                stock: parseInt(formData.stock)
            }),
        })
            .then(() => {
                setShowCreateModal(false);
                fetchItems();
            })
            .catch(error => {
                console.error('Error creating item:', error);
            });
    };

    const toggleAvailability = (item) => {
        const updatedItem = {
            ...item,
            available: !item.available,
            action: 'update',
        };

        fetch('/api/manage-item', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization' : `Bearer ${localStorage.getItem('accessToken')}`

             },
            body: JSON.stringify(updatedItem)
        })
            .then(() => {
                fetchItems();
            })
            .catch(error => {
                console.error('Error updating item availability:', error);
            });
    };

    const confirmDelete = (itemId) => {
        setDeleteItemId(itemId);
        setShowDeleteModal(true);
    };

    const handleDeleteConfirm = () => {
        fetch('/api/manage-item', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization' : `Bearer ${localStorage.getItem('accessToken')}`

             },
            body: JSON.stringify({
                action: 'delete',
                id: deleteItemId
            })
        })
            .then(() => {
                setDeleteItemId(null);
                setShowDeleteModal(false);
                fetchItems();
            })
            .catch(error => {
                console.error('Error deleting item:', error);
            });
    };

    const availableBeverages = items.filter(
        (item) => item.available && item.category.toLowerCase() === 'beverage'
    );
    const availableFood = items.filter(
        (item) => item.available && item.category.toLowerCase() === 'food'
    );
    const unavailableBeverages = items.filter(
        (item) => !item.available && item.category.toLowerCase() === 'beverage'
    );
    const unavailableFood = items.filter(
        (item) => !item.available && item.category.toLowerCase() === 'food'
    );

    return (
        <div>
            <div className="menu-page-container">
                <h2>Menu Manager</h2>
                <button className="create-button" onClick={openCreateModal}>
                    Create New Item
                </button>
            </div>

            <div className="section-header">Available Items</div>
                <div className="sub-section-header">Beverages</div>
                    {availableBeverages.length === 0 && <p>No available beverages.</p>}
                    {availableBeverages.map((item) => (
                        <ItemCard key={item.id} item={item} onToggle={toggleAvailability} onDelete={confirmDelete} />
                    ))}

                <div className="sub-section-header">Food</div>
                {availableFood.length === 0 && <p>No available food items.</p>}
                {availableFood.map((item) => (
                    <ItemCard key={item.id} item={item} onToggle={toggleAvailability} onDelete={confirmDelete} />
                    ))}

            <div className="section-header">Unavailable Items</div>
                <div className="sub-section-header">Beverages</div>
                    {unavailableBeverages.length === 0 && <p>No unavailable beverages.</p>}
                    {unavailableBeverages.map((item) => (
                        <ItemCard key={item.id} item={item} onToggle={toggleAvailability} onDelete={confirmDelete} />
                    ))}

                <div className="sub-section-header">Food</div>
                    {unavailableFood.length === 0 && <p>No unavailable food items.</p>}
                    {unavailableFood.map((item) => (
                        <ItemCard key={item.id} item={item} onToggle={toggleAvailability} onDelete={confirmDelete} />
                    ))}

            {/* Create Modal */}
            {showCreateModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
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
                    <div className="modal-overlay">
                    <div className="modal-content">
                        <h3>Confirm Delete</h3>
                        <p>Are you sure you want to delete this item?</p>
                        <button onClick={handleDeleteConfirm}>Yes</button>
                        <button className="cancel-button" onClick={() => setShowDeleteModal(false)}>
                        Cancel
                        </button>
                    </div>
                    </div>
            )}
        </div>
    );
};
export default MenuPage;
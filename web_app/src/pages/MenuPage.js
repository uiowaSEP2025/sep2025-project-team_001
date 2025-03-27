import React, { useState, useEffect } from 'react';
import '../styles/MenuPage.css';

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
        fetch('/api/menu-items/')
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
        const data = new FormData();
        data.append('action', 'create');
        Object.entries(formData).forEach(([key, val]) => {
            data.append(key, typeof val === 'boolean' ? (val ? 'true' : 'false') : val);
        });

        fetch('/api/manage-item/', {
            method: 'POST',
            body: data
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
        const newAvailability = !item.available;
        const data = new FormData();
        data.append('action', 'update');
        data.append('item_id', item.id);
        data.append('name', item.name);
        data.append('description', item.description);
        data.append('price', item.price);
        data.append('category', item.category);
        data.append('stock', item.stock);
        data.append('available', newAvailability ? 'true' : 'false');

        fetch('/api/manage-item', {
            method: 'POST',
            body: data
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
        if (!deleteItemId) return;
        const data = new FormData();
        data.append('action', 'delete');
        data.append('item_id', deleteItemId);

        fetch('/api/manage-item', {
            method: 'POST',
            body: data
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

    const handleDeleteCancel = () => {
        setShowDeleteModal(false);
        setDeleteItemId(null);
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
            {availableBeverages.length === 0 && <p>No available beverages</p>}
            {availableBeverages.map(item => (
                <div key={item.id} className="item-container">
                    <div className="item-card">
                        <h3>{item.name}</h3>
                        {item.description}<br />
                        Price: ${item.price}<br />
                        Stock: {item.stock}<br />
                        Available: {' '}
                        <input
                            type="checkbox"
                            checked={item.available}
                            onChange={() => toggleAvailability(item)}
                        />
                        <br />
                        <button onClick={() => confirmDelete(item.id)}>Delete</button>
                    </div>
                </div>
            ))}

            <div className="sub-section-header">Food</div>
            {availableFood.length === 0 && <p>No available food items</p>}
            {availableFood.map(item => (
                <div key={item.id} className="item-container">
                    <div className="item-card">
                        <h3>{item.name}</h3>
                        {item.description}<br />
                        Price: ${item.price}<br />
                        Stock: {item.stock}<br />
                        Available: {' '}
                        <input
                            type="checkbox"
                            checked={item.available}
                            onChange={() => toggleAvailability(item)}
                        />
                        <br />
                        <button onClick={() => confirmDelete(item.id)}>Delete</button>
                    </div>
                </div>
            ))}

            <div className="section-header">Unavailable Items</div>

            <div className="sub-section-header">Beverages</div>
            {unavailableBeverages.length === 0 && <p>No unavailable beverages</p>}
            {unavailableBeverages.map(item => (
                <div key={item.id} className="item-container">
                    <div className="item-card">
                        <h3>{item.name}</h3>
                        {item.description}<br />
                        Price: ${item.price}<br />
                        Stock: {item.stock}<br />
                        Available: {' '}
                        <input
                            type="checkbox"
                            checked={item.available}
                            onChange={() => toggleAvailability(item)}
                        />
                        <br />
                        <button onClick={() => confirmDelete(item.id)}>Delete</button>
                    </div>
                </div>
            ))}

            <div className="sub-section-header">Food</div>
            {unavailableFood.length === 0 && <p>No unavailable food items</p>}
            {unavailableFood.map(item => (
                <div key={item.id} className="item-container">
                    <div className="item-card">
                        <h3>{item.name}</h3>
                        {item.description}<br />
                        Price: ${item.price}<br />
                        Stock: {item.stock}<br />
                        Available: {' '}
                        <input
                            type="checkbox"
                            checked={item.available}
                            onChange={() => toggleAvailability(item)}
                        />
                        <br />
                        <button onClick={() => confirmDelete(item.id)}>Delete</button>
                    </div>
                </div>
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
                        <button className="cancel-btn" onClick={handleDeleteCancel}>
                            Cancel
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MenuPage;
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMenuItems } from '../api/menuApi';
import '../styles/MenuPage.css';

const MenuPage = () => {
    // Modals are used for being able to create 'popup' forms for creating and deleting items
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
    
    const fetchItems = () => {
        getMenuItems()
            .then(data => setItems(data))
            .catch(error => console.error('Error fetching menu items:', error));
    
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

    const toggleAvailability = (item) => {
        const newAvailability = !item.available;
        const data = new FormData();
        data.append('action', 'update')
        data.append('item_id', item.id);
        data.append('name', item.name);
        data.append('description', item.description);
        data.append('price', item.price);
        data.append('category', item.category);
        data.append('stock', item.stock);
        data.append('available', newAvailability? 'true' : 'false');

        fetch('/api/menu', {
            method: 'POST',
            body: data
        })
        .then(() => {
            fetchItems();
        })
        .catch(error => {
            console.error('Error updating item availability:', error);
        });
    }
    return (
        <div>
            <div className = "menu-page-container">
                <h2>Menu Manager</h2>

                <button className = "create-button" onClick={openCreateModal}>
                    Create New Item
                </button>
            </div>

            <div className = "section-header">Available Items</div>
                <div className = "sub-section-header">Beverages</div>
                {availableBeverages.length == 0 && <p>No available beverages</p>}
                {availableBeverages.map(item => (
                    <div key={item.id} className="item-container">
                        <div className="item-card">
                            <h3>{item.name}</h3>
                            {item.description}<br />
                            Price: ${item.price}<br />
                            Stock: {item.stock}<br />
                            Available: {' '}
                        </div>
                        <input
                            type="checkbox"
                            checked={item.available}
                            onChange={() => toggleAvailability(item)}
                        />
                    </div>
                ))}
            <div className = "section-header">Unavailable Items</div>
        </div>
    )
    
}
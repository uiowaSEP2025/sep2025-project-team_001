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
    return (
        <div className = 'menu-page-container'>
            <h2>Menu Manager</h2>

            <button className = "create-button" onClick={openCreateModal}>
                Create New Item
            </button>
        </div>
    )
}
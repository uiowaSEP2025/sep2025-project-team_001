import React from 'react';
import '../pages/styles/ItemCard.css';

const ItemCard = ({ item, onToggle, onDelete }) => (
  <div className="item-container">
    <div className="item-card">
      <h3>{item.name}</h3>
      {item.description}<br />
      Price: ${item.price}<br />
      Stock: {item.stock}<br />
      Available: <input type="checkbox" checked={item.available} onChange={() => onToggle(item)} /><br />
      <button onClick={() => onDelete(item.id)}>Delete</button>
    </div>
  </div>
);

export default ItemCard;
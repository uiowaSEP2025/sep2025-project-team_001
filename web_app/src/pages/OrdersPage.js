import React, { useEffect, useState } from 'react';
import { Container, Table, Spinner, Modal, Button } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const OrdersPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const navigate = useNavigate();

  const handleUpdateOrderStatus = async (orderId, nextStatus) => {
    try {
      const restaurantId = sessionStorage.getItem('restaurantId');
      const workerID = sessionStorage.getItem('workerId');

      const currentOrder = orders.find((o) => o.id === orderId);
      const isAssigningWorker =
        currentOrder.status === 'pending' && nextStatus === 'in_progress';

      const response = await axios.patch(
        `${process.env.REACT_APP_API_URL}/orders/${restaurantId}/${orderId}/${nextStatus}/`,
        isAssigningWorker ? { worker_id: workerID } : {},
      );
      console.log(`Order ${response.data.order_id} updated to ${nextStatus}`);
      console.log('Updated order status:', {
        status: response.data.status,
        food_status: response.data.food_status,
        beverage_status: response.data.beverage_status,
      });
      

      const updatedOrders = orders.map((order) =>
        order.id === orderId
          ? {
              ...order,
              status: response.data.status,
              food_status: response.data.food_status,
              beverage_status: response.data.beverage_status,
            }
          : order
      );      
      setOrders(updatedOrders);

      // Automatically close modal if final status
      if (nextStatus === 'picked_up') {
        setSelectedOrder(null);
      } else {
        setSelectedOrder((prev) =>
          prev
            ? {
                ...prev,
                status: response.data.status,
                food_status: response.data.food_status,
                beverage_status: response.data.beverage_status,
              }
            : null
        );        
      }
    } catch (error) {
      console.error('Error updating order status: ', error);
    }
  };

  const handleUpdateCategoryStatus = async (orderId, category, newStatus) => {
    try {
      const restaurantId = sessionStorage.getItem('restaurantId');
      const url = `${process.env.REACT_APP_API_URL}/orders/${restaurantId}/${orderId}/${category}/${newStatus}/`;
      const response = await axios.patch(url);
  
      const updated = response.data;
  
      setSelectedOrder((prev) => {
        if (!prev) return null;
        return {
          ...prev,
          status: updated.status,
          food_status:
            category === 'food' ? updated.food_status : prev.food_status,
          beverage_status:
            category === 'beverage' ? updated.beverage_status : prev.beverage_status,
        };
      });
  
      setOrders((prev) =>
        prev.map((o) =>
          o.id === updated.order_id
            ? {
                ...o,
                status: updated.status,
                food_status:
                  category === 'food' ? updated.food_status : o.food_status,
                beverage_status:
                  category === 'beverage' ? updated.beverage_status : o.beverage_status,
              }
            : o
        )
      );
  
      if (updated.status === 'picked_up') {
        setTimeout(() => setSelectedOrder(null), 300);
      }
  
      console.log(`Updated ${category} to ${newStatus} for order #${orderId}`);
      console.log(`Updated ${category} status:`, {
        status: updated.status,
        food_status: updated.food_status,
        beverage_status: updated.beverage_status,
      });      
    } catch (err) {
      console.error('Error updating category status:', err);
    }
  };    

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_API_URL}/retrieve/orders/`,
        );
        const newOrders = response.data;

        if (JSON.stringify(newOrders) !== JSON.stringify(orders)) {
          //checks if orders have changed, if same do nothing
          setOrders(newOrders);
        }

        if (loading) {
          setLoading(false); // Only clear loading on first fetch
        }
      } catch (error) {
        console.error('Error fetching orders:', error);
        if (loading) {
          setLoading(false);
        }
      }
    };

    fetchOrders(); // On Page entry

    const intervalId = setInterval(fetchOrders, 3000); // Poll every 3s
    return () => clearInterval(intervalId);
  }, []);

  const getNextStatus = (status) => {
    switch (status) {
      case 'pending':
        return 'in_progress';
      case 'in_progress':
        return 'completed';
      case 'completed':
        return 'picked_up';
      default:
        return null;
    }
  };

  const formatStatus = (status) => {
    switch (status) {
      case 'pending':
        return 'Pending';
      case 'in_progress':
        return 'In Progress';
      case 'completed':
        return 'Completed';
      case 'picked_up':
        return 'Picked Up';
      case 'cancelled':
        return 'Cancelled';
      default:
        return status;
    }
  };

  if (loading && orders.length === 0) {
    return (
      <Container className="mt-5 text-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </Container>
    );
  }

  return (
    <Container className="mt-5">
      <Button
        variant="outline-primary"
        className="mb-3"
        onClick={() => navigate('/dashboard')}
        style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          zIndex: 1051,
        }}
      >
        Log Out
      </Button>
      <h1>Active Orders</h1>
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Order #</th>
            <th>Customer</th>
            <th>Ordered Time</th>
            <th>Total Price</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr
              key={order.id}
              onClick={() => setSelectedOrder(order)}
              style={{ cursor: 'pointer' }}
            >
              <td>{order.id}</td>
              <td>{order.customer_name}</td>
              <td>{new Date(order.start_time).toLocaleString()}</td>
              <td>${Number(order.total_price).toFixed(2)}</td>
              <td>{formatStatus(order.status)}</td>
            </tr>
          ))}
        </tbody>
      </Table>
      <Modal show={!!selectedOrder} onHide={() => setSelectedOrder(null)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Order Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedOrder && (
            <>
              {/* Beverage Items */}
              <h5>Beverages (Status: {formatStatus(selectedOrder.beverage_status)})</h5>
              <Table striped bordered hover size="sm" className="mb-3">
                <thead>
                  <tr>
                    <th>Item</th>
                    <th>Quantity</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedOrder.order_items
                    .filter((item) => item.category?.toLowerCase() === "beverage")
                    .map((item, index) => (
                      <tr key={`bev-${index}`}>
                        <td>{item.item_name}</td>
                        <td>{item.quantity}</td>
                      </tr>
                    ))}
                </tbody>
              </Table>
  
              {selectedOrder.beverage_status === 'in_progress' && (
                <Button
                  variant="warning"
                  className="mb-3"
                  onClick={() =>
                    handleUpdateCategoryStatus(selectedOrder.id, 'beverage', 'completed')
                  }
                >
                  Mark Beverage Completed
                </Button>
              )}
              {selectedOrder.beverage_status === 'completed' && (
                <Button
                  variant="success"
                  className="mb-3"
                  onClick={() =>
                    handleUpdateCategoryStatus(selectedOrder.id, 'beverage', 'picked_up')
                  }
                >
                  Mark Beverage Picked Up
                </Button>
              )}
  
              {/* Food Items */}
              <h5>Food (Status: {formatStatus(selectedOrder.food_status)})</h5>
              <Table striped bordered hover size="sm" className="mb-3">
                <thead>
                  <tr>
                    <th>Item</th>
                    <th>Quantity</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedOrder.order_items
                    .filter((item) => item.category?.toLowerCase() !== "beverage")
                    .map((item, index) => (
                      <tr key={`food-${index}`}>
                        <td>{item.item_name}</td>
                        <td>{item.quantity}</td>
                      </tr>
                    ))}
                </tbody>
              </Table>
  
              {selectedOrder.food_status === 'in_progress' && (
                <Button
                  variant="warning"
                  className="mb-3"
                  onClick={() =>
                    handleUpdateCategoryStatus(selectedOrder.id, 'food', 'completed')
                  }
                >
                  Mark Food Completed
                </Button>
              )}
              {selectedOrder.food_status === 'completed' && (
                <Button
                  variant="success"
                  className="mb-3"
                  onClick={() =>
                    handleUpdateCategoryStatus(selectedOrder.id, 'food', 'picked_up')
                  }
                >
                  Mark Food Picked Up
                </Button>
              )}
            </>
          )}
        </Modal.Body>
        <Modal.Footer>
          {selectedOrder && selectedOrder.status === 'pending' && (
            <Button
              variant="success"
              onClick={() =>
                handleUpdateOrderStatus(selectedOrder.id, 'in_progress')
              }
            >
              Mark In Progress
            </Button>
          )}
          <Button variant="secondary" onClick={() => setSelectedOrder(null)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );  
};

export default OrdersPage;

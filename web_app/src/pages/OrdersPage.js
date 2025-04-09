import React, { useEffect, useState } from 'react';
import { Container, Table, Spinner, Modal, Button } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const OrdersPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const navigate = useNavigate();

  const handleCompleteOrder = async (orderId) => {
    try {
      const response = await axios.patch(
        `${process.env.REACT_APP_API_URL}/orders/${orderId}/complete/`,
      );
      console.log(`Order ${response.data.order_id} marked as completed.`);

      // Update local state
      const updatedOrders = orders.map((order) =>
        order.id === orderId ? { ...order, status: 'completed' } : order,
      );
      setOrders(updatedOrders);

      // Update selected order in modal too
      setSelectedOrder((prev) =>
        prev ? { ...prev, status: 'completed' } : null,
      );
    } catch (error) {
      console.error('Error marking order as completed:', error);
    }
  };

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_API_URL}/retrieve/orders/`
        );
        const newOrders = response.data;

        if (JSON.stringify(newOrders) !== JSON.stringify(orders)) { //checks if orders have changed, if same do nothing
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
        Dashboard
      </Button>

      <h1>Active Orders</h1>
      <Table striped bordered hover responsive>
        <thead>
          <tr>
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
              <td>{order.customer_name}</td>
              <td>{new Date(order.start_time).toLocaleString()}</td>
              <td>${Number(order.total_price).toFixed(2)}</td>
              <td>{order.status}</td>
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Modal for Order Details */}
      <Modal
        show={!!selectedOrder}
        onHide={() => setSelectedOrder(null)}
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>Order Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedOrder && (
            <>
              <Table striped bordered hover size="sm">
                <thead>
                  <tr>
                    <th>Item</th>
                    <th>Quantity</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedOrder.order_items.map((item, index) => (
                    <tr key={index}>
                      <td>{item.item_name}</td>
                      <td>{item.quantity}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </>
          )}
        </Modal.Body>
        <Modal.Footer>
          {selectedOrder?.status !== 'completed' && (
            <Button
              variant="success"
              onClick={() => handleCompleteOrder(selectedOrder.id)}
            >
              Complete Order
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

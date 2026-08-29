import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import api from '../api/axios';

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const location = useLocation();
  const justPlacedOrderId = location.state?.justPlacedOrderId;

  useEffect(() => {
    api.get('/orders/').then(({ data }) => setOrders(data)).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="container"><p>Loading orders...</p></div>;

  return (
    <div className="container">
      <h2>My Orders</h2>
      {justPlacedOrderId && (
        <p className="success-msg">Order #{justPlacedOrderId} placed successfully!</p>
      )}
      {orders.length === 0 && <p>You haven't placed any orders yet.</p>}
      {orders.map((order) => (
        <div className="order-card" key={order.id}>
          <div className="order-card-header">
            <span>Order #{order.id}</span>
            <span className={`status status-${order.status}`}>{order.status}</span>
            <span className={`status status-payment-${order.payment_status}`}>
              {order.payment_method === 'razorpay' ? 'Paid Online' : 'Cash on Delivery'} · {order.payment_status}
            </span>
            <span>{new Date(order.created_at).toLocaleDateString()}</span>
          </div>
          <ul>
            {order.items.map((item) => (
              <li key={item.id}>
                {item.quantity} x {item.product_name} — ₹{item.subtotal}
              </li>
            ))}
          </ul>
          <p>Shipping to: {order.shipping_address}</p>
          <p><strong>Total: ₹{order.total_price}</strong></p>
        </div>
      ))}
    </div>
  );
}

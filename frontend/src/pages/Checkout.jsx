import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

export default function Checkout() {
  const { cart, fetchCart } = useCart();
  const { user } = useAuth();
  const [address, setAddress] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('cod'); // 'cod' | 'razorpay'
  const [error, setError] = useState('');
  const [placing, setPlacing] = useState(false);
  const navigate = useNavigate();

  const handleCodOrder = async () => {
    const { data } = await api.post('/orders/checkout/', { shipping_address: address });
    return data;
  };

  const handleRazorpayOrder = async () => {
    // Step 1: ask our backend to create a Razorpay order for the current cart total
    const { data: rpOrder } = await api.post('/orders/razorpay/create/', {
      shipping_address: address,
    });

    // Step 2: open Razorpay's checkout popup
    return new Promise((resolve, reject) => {
      const options = {
        key: rpOrder.key_id,
        amount: rpOrder.amount,
        currency: rpOrder.currency,
        name: 'ShopEase',
        description: 'Order payment',
        order_id: rpOrder.razorpay_order_id,
        prefill: { name: user?.username },
        theme: { color: '#1a1a2e' },
        handler: async (response) => {
          // Step 3: payment succeeded in the popup - verify it with our backend
          try {
            const { data: order } = await api.post('/orders/razorpay/verify/', {
              shipping_address: address,
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
            });
            resolve(order);
          } catch (err) {
            reject(err);
          }
        },
        modal: {
          ondismiss: () => reject(new Error('Payment popup closed before completing payment.')),
        },
      };
      const rzp = new window.Razorpay(options);
      rzp.on('payment.failed', () => reject(new Error('Payment failed. Please try again.')));
      rzp.open();
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setPlacing(true);
    try {
      const order =
        paymentMethod === 'cod' ? await handleCodOrder() : await handleRazorpayOrder();
      await fetchCart(); // cart is now empty on the server
      navigate('/orders', { state: { justPlacedOrderId: order.id } });
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Something went wrong. Please try again.');
    } finally {
      setPlacing(false);
    }
  };

  return (
    <div className="container narrow">
      <h2>Checkout</h2>
      <p>Order total: <strong>₹{cart.total_price}</strong> ({cart.total_items} items)</p>

      <form onSubmit={handleSubmit} className="form">
        <label>Shipping Address</label>
        <textarea
          required
          rows="4"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder="House name, street, city, state, PIN code"
        />

        <label>Payment Method</label>
        <div className="payment-options">
          <label className="payment-option">
            <input
              type="radio"
              name="paymentMethod"
              value="cod"
              checked={paymentMethod === 'cod'}
              onChange={() => setPaymentMethod('cod')}
            />
            Cash on Delivery
          </label>
          <label className="payment-option">
            <input
              type="radio"
              name="paymentMethod"
              value="razorpay"
              checked={paymentMethod === 'razorpay'}
              onChange={() => setPaymentMethod('razorpay')}
            />
            Pay Online (Card / UPI / Netbanking - Razorpay)
          </label>
        </div>

        {error && <p className="error-msg">{error}</p>}
        <button className="btn-primary" type="submit" disabled={placing}>
          {placing
            ? 'Processing...'
            : paymentMethod === 'cod'
            ? 'Place Order'
            : 'Pay & Place Order'}
        </button>
      </form>
    </div>
  );
}

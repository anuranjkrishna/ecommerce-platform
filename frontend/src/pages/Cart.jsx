import { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

export default function Cart() {
  const { cart, fetchCart, updateQuantity, removeItem } = useCart();
  const navigate = useNavigate();

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  if (!cart.items.length) {
    return (
      <div className="container">
        <h2>Your Cart</h2>
        <p>Your cart is empty. <Link to="/">Browse products</Link></p>
      </div>
    );
  }

  return (
    <div className="container">
      <h2>Your Cart</h2>
      <div className="cart-list">
        {cart.items.map((item) => (
          <div className="cart-item" key={item.id}>
            <img src={item.product.image || '/placeholder.png'} alt={item.product.name} />
            <div className="cart-item-info">
              <h4>{item.product.name}</h4>
              <p>₹{item.product.price} each</p>
            </div>
            <input
              type="number"
              min="1"
              value={item.quantity}
              onChange={(e) => updateQuantity(item.id, Number(e.target.value))}
            />
            <p className="cart-item-subtotal">₹{item.subtotal}</p>
            <button className="btn-link" onClick={() => removeItem(item.id)}>Remove</button>
          </div>
        ))}
      </div>

      <div className="cart-summary">
        <h3>Total: ₹{cart.total_price}</h3>
        <button className="btn-primary" onClick={() => navigate('/checkout')}>
          Proceed to Checkout
        </button>
      </div>
    </div>
  );
}

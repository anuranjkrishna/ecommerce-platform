import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const { cart, clearCartState } = useCart();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    clearCartState();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">ShopEase</Link>
      <div className="navbar-links">
        <Link to="/">Products</Link>
        {user && <Link to="/orders">My Orders</Link>}
        <Link to="/cart" className="cart-link">
          Cart
          {cart.total_items > 0 && <span className="cart-badge">{cart.total_items}</span>}
        </Link>
        {user ? (
          <>
            <span className="navbar-user">Hi, {user.username}</span>
            <button className="btn-link" onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

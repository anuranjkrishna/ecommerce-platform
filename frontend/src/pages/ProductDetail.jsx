import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

export default function ProductDetail() {
  const { slug } = useParams();
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [message, setMessage] = useState('');
  const { user } = useAuth();
  const { addToCart } = useCart();
  const navigate = useNavigate();

  useEffect(() => {
    api.get(`/products/${slug}/`).then(({ data }) => setProduct(data));
  }, [slug]);

  const handleAddToCart = async () => {
    if (!user) {
      navigate('/login');
      return;
    }
    await addToCart(product.id, quantity);
    setMessage('Added to cart!');
    setTimeout(() => setMessage(''), 2000);
  };

  if (!product) return <div className="container"><p>Loading...</p></div>;

  return (
    <div className="container product-detail">
      <img src={product.image || '/placeholder.png'} alt={product.name} className="product-detail-img" />
      <div className="product-detail-info">
        <h2>{product.name}</h2>
        <p className="product-card-category">{product.category?.name}</p>
        <p className="product-detail-price">₹{product.price}</p>
        <p>{product.description}</p>
        <p>{product.in_stock ? `${product.stock} in stock` : 'Out of stock'}</p>

        {product.in_stock && (
          <div className="add-to-cart-row">
            <input
              type="number"
              min="1"
              max={product.stock}
              value={quantity}
              onChange={(e) => setQuantity(Number(e.target.value))}
            />
            <button className="btn-primary" onClick={handleAddToCart}>Add to Cart</button>
          </div>
        )}
        {message && <p className="success-msg">{message}</p>}
      </div>
    </div>
  );
}

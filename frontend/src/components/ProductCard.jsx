import { Link } from 'react-router-dom';

export default function ProductCard({ product }) {
  return (
    <Link to={`/products/${product.slug}`} className="product-card">
      <img src={product.image || '/placeholder.png'} alt={product.name} className="product-card-img" />
      <div className="product-card-body">
        <h3>{product.name}</h3>
        <p className="product-card-category">{product.category?.name}</p>
        <p className="product-card-price">₹{product.price}</p>
        {!product.in_stock && <span className="badge-out">Out of stock</span>}
      </div>
    </Link>
  );
}

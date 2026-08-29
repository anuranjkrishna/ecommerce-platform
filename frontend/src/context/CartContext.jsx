import { createContext, useContext, useState, useCallback } from 'react';
import api from '../api/axios';
import { useAuth } from './AuthContext';

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const { user } = useAuth();
  const [cart, setCart] = useState({ items: [], total_price: '0.00', total_items: 0 });
  const [loading, setLoading] = useState(false);

  const fetchCart = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    try {
      const { data } = await api.get('/cart/');
      setCart(data);
    } finally {
      setLoading(false);
    }
  }, [user]);

  const addToCart = async (productId, quantity = 1) => {
    const { data } = await api.post('/cart/add/', { product_id: productId, quantity });
    setCart(data);
  };

  const updateQuantity = async (itemId, quantity) => {
    const { data } = await api.put(`/cart/update/${itemId}/`, { quantity });
    setCart(data);
  };

  const removeItem = async (itemId) => {
    const { data } = await api.delete(`/cart/remove/${itemId}/`);
    setCart(data);
  };

  const clearCartState = () => setCart({ items: [], total_price: '0.00', total_items: 0 });

  return (
    <CartContext.Provider
      value={{ cart, loading, fetchCart, addToCart, updateQuantity, removeItem, clearCartState }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  return useContext(CartContext);
}

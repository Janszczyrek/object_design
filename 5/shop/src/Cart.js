import React, { useState, useContext, createContext, useMemo } from 'react';
import Payment from './Payment';
import PropTypes from 'prop-types';

export const CartContext = createContext({ cart: [], setCart: () => {} });
export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);
  const contextValue = useMemo(() => ({ cart, setCart }), [cart, setCart]);
  return (
    <CartContext.Provider value={contextValue}>
      {children}
    </CartContext.Provider>
  );
}

CartProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

function Cart() {
    const contextValue = useContext(CartContext);
    const { cart, setCart } = contextValue;

    const increaseQuantity = (productId) => {
        setCart(prevCart =>
          prevCart.map(item =>
            item.product.id === productId
              ? { ...item, quantity: item.quantity + 1 }
              : item
          )
        );
      };
      const decreaseQuantity = (productId) => {
        setCart(prevCart =>
          prevCart.map(item =>
            item.product.id === productId && item.quantity > 1
              ? { ...item, quantity: item.quantity - 1 }
              : item
          )
        );
      };
      const removeFromCart = (productId) => {
        setCart(prevCart => prevCart.filter(item => item.product.id !== productId));
      };

  return (
    <div>
      <h1>Cart</h1>
      <ul>
        {cart.map(item => (
          <li key={item.product.id}>
            {item.product.name} - ${item.product.price} x {item.quantity}
            <button onClick={() => { increaseQuantity(item.product.id)}} >+</button>
            <button onClick={() => { decreaseQuantity(item.product.id)}} >-</button>
            <button onClick={() => { removeFromCart(item.product.id)}} >Remove</button>
          </li>
        ))}
      </ul>
      <Payment cart={cart} />
    </div>
  );
}

export default Cart;
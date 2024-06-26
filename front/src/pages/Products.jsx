import React, { useState } from 'react';
import axios from 'axios';
import './Account.css';

const Products = () => {
    const [activeTab, setActiveTab] = useState('createProduct');

    // New state for product management
    const [tipo, setTipo] = useState('');
    const [limiteCredito, setLimiteCredito] = useState('');
    const [condiciones, setCondiciones] = useState('');
    const [productBankId, setProductBankId] = useState('');
    const [productId, setProductId] = useState('');

    // Existing handlers...

    // Handler for creating a product
    const handleCreateProduct = async (event) => {
        event.preventDefault();
        const payload = {
            tipo, 
            limite_credito: limiteCredito, 
            condiciones, 
            bank_id: productBankId
        };
        try {
            const response = await axios.post('http://localhost:8001/bankpal/product/', payload);
            alert('Product created successfully: ' + JSON.stringify(response.data.data));
        } catch (error) {
            console.error('Error creating product:', error);
        }
    };

    // Handler for deleting products
    const handleDeleteProduct = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.delete(`http://localhost:8001/bankpal/product/${productId}`);
            alert('Products deleted successfully');
        } catch (error) {
            console.error('Error deleting products:', error);
        }
    };

    // Handler for getting products by bank
    const handleGetProducts = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.get(`http://localhost:8001/bankpal/product/${productBankId}`);
            if (response.data.status === 404) {
                alert('No products found for this bank');
            } else {
                alert('Products found: ' + JSON.stringify(response.data.data));
            }
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    };

    return (
        <div className="bank-container">
            <h1>Product Management</h1>
            <div className="tabs">
                <button onClick={() => setActiveTab('createProduct')}>Create Product</button>
                <button onClick={() => setActiveTab('deleteProduct')}>Delete Products</button>
                <button onClick={() => setActiveTab('getProducts')}>Get Products By Bank</button>
            </div>

            {activeTab === 'createProduct' && (
                <form onSubmit={handleCreateProduct}>
                    <h2>Create Product</h2>
                    <input type="text" placeholder="Product Type" value={tipo} onChange={e => setTipo(e.target.value)} />
                    <input type="number" placeholder="Credit Limit" value={limiteCredito} onChange={e => setLimiteCredito(e.target.value)} />
                    <input type="text" placeholder="Conditions" value={condiciones} onChange={e => setCondiciones(e.target.value)} />
                    <input type="text" placeholder="Bank ID" value={productBankId} onChange={e => setProductBankId(e.target.value)} />
                    <button type="submit">Create Product</button>
                </form>
            )}

            {activeTab === 'deleteProduct' && (
                <form onSubmit={handleDeleteProduct}>
                    <h2>Delete Product</h2>
                    <input type="text" placeholder="Product ID" value={productId} onChange={e => setProductId(e.target.value)} />
                    <button type="submit">Delete Product</button>
                </form>
            )}

            {activeTab === 'getProducts' && (
                <form onSubmit={handleGetProducts}>
                    <h2>Get Products By Bank</h2>
                    <input type="text" placeholder="Bank ID" value={productBankId} onChange={e => setProductBankId(e.target.value)} />
                    <button type="submit">Get Products</button>
                </form>
            )}
        </div>
    );
};

export default Products;

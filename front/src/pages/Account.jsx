import React, { useState } from 'react';
import axios from 'axios';

const Account = () => {
    // State for creating accounts
    const [tipo, setTipo] = useState('');
    const [saldo, setSaldo] = useState('');
    const [bankId, setBankId] = useState('');
    const [clienteId, setClienteId] = useState('');

    // State for other actions
    const [accountNumber, setAccountNumber] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [accountNumb, setAccountNumb] = useState('');
    const [accountDetails, setAccountDetails] = useState(null);
    const [accountNumbers, setAccountNumbers] = useState('');
    const [isPremium, setIsPremium] = useState(false);

    // Handlers for actions
    const handleCreate = async (event) => {
        event.preventDefault();
        const payload = { tipo, saldo, bank_id: bankId, cliente_id: clienteId };
        try {
            const response = await axios.post('http://localhost:8001/bankpal/account', payload);
            alert('Account Created: ' + JSON.stringify(response.data));
        } catch (error) {
            console.error('Error creating account:', error);
        }
    };

    const handleGet = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.get(`http://localhost:8001/bankpal/account/${accountNumber}`);
            if (response.data.status === 404) {  // Assuming your backend sends 404 status for not found
                setAccountDetails(null);
                setErrorMessage('Account not found');
            } else {
                setAccountDetails(response.data.data);
                setErrorMessage('');
            }
        } catch (error) {
            console.error('Error fetching account:', error);
            setAccountDetails(null);
            setErrorMessage('Failed to fetch account details. Please try again.');
        }
    };

    const handleDelete = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.delete(`http://localhost:8001/bankpal/account/${accountNumber}`);
            alert('Account Deleted: ' + JSON.stringify(response.data));
        } catch (error) {
            console.error('Error deleting account:', error);
        }
    };

    const handleUpgrade = async (event) => {
        event.preventDefault();
        const payload = {
            account_numbers: accountNumbers.split(','),
            is_premium: isPremium
        };
        try {
            const response = await axios.post('http://localhost:8001/bankpal/account/upgrade', payload);
            alert('Accounts Updated: ' + JSON.stringify(response.data.data));
        } catch (error) {
            console.error('Error upgrading accounts:', error);
        }
    };

    return (
        <div>
            {/* Form for creating an account */}
            <form onSubmit={handleCreate}>
                <h2>Create Account</h2>
                <input type="text" placeholder="Account Type" value={tipo} onChange={e => setTipo(e.target.value)} />
                <input type="number" placeholder="Balance" value={saldo} onChange={e => setSaldo(e.target.value)} />
                <input type="text" placeholder="Bank ID" value={bankId} onChange={e => setBankId(e.target.value)} />
                <input type="text" placeholder="Client ID" value={clienteId} onChange={e => setClienteId(e.target.value)} />
                <button type="submit">Create Account</button>
            </form>

            {/* Form for getting an account */}
            <div>
                <form onSubmit={handleGet}>
                    <h2>Get Account</h2>
                    <input type="text" placeholder="Account Number" value={accountNumber} onChange={e => setAccountNumber(e.target.value)} />
                    <button type="submit">Get Account</button>
                </form>
                {accountDetails && (
                <div className="account-card">
                    <h3>Account Details:</h3>
                    <p><strong>Account Type:</strong> {accountDetails.cuenta.tipoCuenta}</p>
                    <p><strong>Balance:</strong> ${accountDetails.cuenta.saldo.toFixed(2)}</p>
                    <p><strong>Client Name:</strong> {accountDetails.cliente.nombre}</p>
                    <p><strong>Bank Name:</strong> {accountDetails.banco.nombre}</p>
                    <p><strong>Bank Rating:</strong> {accountDetails.banco.calificacion} stars</p>
                    <p><strong>Is Premium:</strong> {accountDetails.cliente.esPremium ? 'Yes' : 'No'}</p>
                </div>
                )}
                {errorMessage && (
                    <div className="error-message">
                        <p>{errorMessage}</p>
                    </div>
                )}
            </div>
            {/* Form for deleting an account */}
            <form onSubmit={handleDelete}>
                <h2>Delete Account</h2>
                <input type="text" placeholder="Account Number" value={accountNumb} onChange={e => setAccountNumb(e.target.value)} />
                <button type="submit">Delete Account</button>
            </form>

            {/* Form for upgrading accounts */}
            <form onSubmit={handleUpgrade}>
                <h2>Upgrade Accounts</h2>
                <input type="text" placeholder="Account Numbers (comma-separated)" value={accountNumbers} onChange={e => setAccountNumbers(e.target.value)} />
                <label>
                    <input type="checkbox" checked={isPremium} onChange={e => setIsPremium(e.target.checked)} />
                    Premium Status
                </label>
                <button type="submit">Upgrade Account</button>
            </form>
        </div>
    );
};

export default Account;
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function AccountsGrid() {
    const [accounts, setAccounts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchAccounts = async () => {
            setLoading(true);
            try {
                const response = await axios.get('http://localhost:8001/bankpal/accounts');
                setAccounts(response.data.data);
            } catch (error) {
                console.error('Error fetching accounts:', error);
                setError('Failed to fetch accounts');
            }
            setLoading(false);
        };

        fetchAccounts();
    }, []);

    return (
        <div>
            {loading ? <p>Loading accounts...</p> : (
                <table>
                    <thead>
                        <tr>
                            <th>Account Type</th>
                            <th>Balance</th>
                            <th>Client Names</th>
                            <th>Bank Names</th>
                        </tr>
                    </thead>
                    <tbody>
                        {accounts.map(account => (
                            <tr key={account.id}>
                                <td>{account.tipoCuenta}</td>
                                <td>${account.saldo}</td>
                                <td>{account.clientes.map(client => client.nombre).join(", ")}</td>
                                <td>{account.bancos.map(bank => bank.nombre).join(", ")}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
            {error && <p className="error">{error}</p>}
        </div>
    );
}

export default AccountsGrid;

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './AllAccounts.css';

function AccountsGrid() {
    const [currentPage, setCurrentPage] = useState(1);
    const [accountsPerPage, setAccountsPerPage] = useState(10);
    const [accounts, setAccounts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const indexOfLastAccount = currentPage * accountsPerPage;
    const indexOfFirstAccount = indexOfLastAccount - accountsPerPage;
    const currentAccounts = accounts.slice(indexOfFirstAccount, indexOfLastAccount);

    const paginate = pageNumber => setCurrentPage(pageNumber);
    const nextPage = () => setCurrentPage(prev => prev + 1);
    const prevPage = () => setCurrentPage(prev => (prev - 1 > 0 ? prev - 1 : 1));

    useEffect(() => {
        const fetchAccounts = async () => {
            setLoading(true);
            try {
                const response = await axios.get('http://localhost:8001/bankpal/account/accounts');
                console.log("response", response)
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
        <div  className="allaccounts-container">
            {loading ? <p>Loading accounts...</p> : (
                <>
                    <table>
                        <thead>
                            <tr>
                                <th>Account Name</th>
                                <th>Account Type</th>
                                <th>Balance</th>
                                <th>Client Names</th>
                                <th>Bank Names</th>
                            </tr>
                        </thead>
                        <tbody>
                            {currentAccounts.map(account => (
                                <tr key={account.id}>
                                    <td>{account.numeroCuenta}</td>
                                    <td>{account.tipoCuenta}</td>
                                    <td>${account.saldo}</td>
                                    <td>{account.clientes.map(client => client.nombre).join(", ")}</td>
                                    <td>{account.bancos.map(bank => bank.nombre).join(", ")}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <div>
                        <button onClick={prevPage}>Prev</button>
                        <button onClick={nextPage}>Next</button>
                    </div>
                </>
            )}
            {error && <p className="error">{error}</p>}
        </div>
    );
}

export default AccountsGrid;

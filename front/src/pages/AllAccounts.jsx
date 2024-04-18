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

    const [orderBy, setOrderBy] = useState('balance');
    const [orderDirection, setOrderDirection] = useState('asc');

    useEffect(() => {
        const fetchAccounts = async () => {
            const payload = {
                order_by: orderBy,
                order: orderDirection
            };
            setLoading(true);
            console.log(payload);
            try {
                const response = await axios.post('http://localhost:8001/bankpal/account/accounts', payload);
                setAccounts(response.data.data);
            } catch (error) {
                console.error('Error fetching accounts:', error);
                setError('Failed to fetch accounts');
            }
            setLoading(false);
        };
    
        fetchAccounts();
    }, [orderBy, orderDirection]);

    return (
        <div  className="allaccounts-container">
            <div>
            <label>Order By: </label>
            <select value={orderBy} onChange={(e) => setOrderBy(e.target.value)}>
                <option value="date">Date</option>
                <option value="balance">Balance</option>
            </select>

            <label> Order Direction: </label>
            <select value={orderDirection} onChange={(e) => setOrderDirection(e.target.value)}>
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
            </select>
        </div>
        
            {loading ? <p>Loading accounts...</p> : (
                <>
                    <table>
                        <thead>
                            <tr>
                                <th>Account Name</th>
                                <th>Account Type</th>
                                <th>Balance</th>
                                <th>Client Names</th>
                                <th>Date</th>
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
                                    <td>{account.fechaCreacion}</td>
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
        </div>
    );
}

export default AccountsGrid;

import React, { useState } from 'react';
import './FraudDetection.css';
import axios from 'axios';

function FraudDetectionPage() {
    const [transactionData, setTransactionData] = useState({
        metodo: '',
        monto: 0,
        to_account_number: '',
        from_account_number: ''
    });
    const [evaluationResult, setEvaluationResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setTransactionData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        if (!transactionData.to_account_number.trim() || !transactionData.from_account_number.trim()) {
            setError('Please enter all account numbers.');
            setLoading(false);
            return;
        }

        if (!transactionData.monto || transactionData.monto <= 0) {
            setError('Please enter a valid amount.');
            setLoading(false);
            return;
        }

        // Prepare payload
        const payload = {
            metodo: transactionData.metodo,
            monto: transactionData.monto,
            to_account_number: transactionData.to_account_number,
            from_account_number: transactionData.from_account_number
        };

        try {
            const response = await axios.post('http://localhost:8001/bankpal/transaction', payload);
            if (response.status === 200) {
                setEvaluationResult(response.data.data);
            } else {
                throw new Error(response.data.message || 'Unexpected error occurred');
            }
        } catch (e) {
            setError(`Error: ${e.response?.data?.message || e.message}`);
        }
        finally {
            setLoading(false);
        }
}

    return (
        <div className="fraud-detection-container">
            <h1>Fraud Detection System</h1>
            <form onSubmit={handleSubmit} className="transaction-form">
                <label>
                    Method:
                    <input
                        type="text"
                        name="metodo"
                        value={transactionData.metodo}
                        onChange={handleChange}
                    />
                </label>
                <label>
                    Amount:
                    <input
                        type="number"
                        name="monto"
                        value={transactionData.monto}
                        onChange={handleChange}
                    />
                </label>
                <label>
                    To Account Number:
                    <input
                        type="text"
                        name="to_account_number"
                        value={transactionData.to_account_number}
                        onChange={handleChange}
                    />
                </label>
                <label>
                    From Account Number:
                    <input
                        type="text"
                        name="from_account_number"
                        value={transactionData.from_account_number}
                        onChange={handleChange}
                    />
                </label>
                <button type="submit" disabled={loading}>Evaluate Transaction</button>
            </form>
            {evaluationResult && (
                <div className="result-section">
                    <h2>Results:</h2>
                    <p>{evaluationResult.is_fraudulent ? "This transaction is fraudulent." : "This transaction is not fraudulent."}</p>
                </div>
            )}
            {error && <p className="error">{error}</p>}
        </div>
    );
}

export default FraudDetectionPage;


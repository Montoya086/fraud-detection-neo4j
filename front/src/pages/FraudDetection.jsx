import React, { useState } from 'react';
import './FraudDetection.css';

function FraudDetectionPage() {
    const [transactionData, setTransactionData] = useState({
        metodo: '',
        monto: '',
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

        try {
            const response = await fetch('/api/evaluate-transaction', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(transactionData)
            });
            const data = await response.json();
            if (response.status === 200) {
                setEvaluationResult(data.data);
            } else {
                throw new Error(data.message || 'Unexpected error occurred');
            }
        } catch (e) {
            if (e.name === 'SyntaxError') {
                setError('Failed to process the server response. Please try again later.');
            } else {
                setError(`Error: ${e.message}`);
            }
        }
        setLoading(false);
    };

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


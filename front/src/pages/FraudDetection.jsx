import React, { useState } from 'react';
import './FraudDetection.css';

function FraudDetectionPage() {
    const [transactionData, setTransactionData] = useState({
        to_account_number: '',
        monto: 0
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
        
        // Verificar que el número de cuenta no esté vacío
        if (!transactionData.to_account_number.trim()) {
            setError('Please enter an account number.');
            setLoading(false);
            return;
        }
    
        try {
            const response = await fetch('/api/evaluate-transaction', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ transaction: transactionData })
            });
            const data = await response.json();
            if (response.status === 200) {
                setEvaluationResult(data.data);
            } else {
                throw new Error(data.message || 'Unexpected error occurred');
            }
        } catch (e) {
            // Manejo de errores cuando la respuesta no se puede procesar
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
                    Account Number:
                    <input
                        type="text"
                        name="to_account_number"
                        value={transactionData.to_account_number}
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

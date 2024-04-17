import React, { useState } from 'react';
import axios from 'axios';
import './Account.css';

const Bank = () => {
    const [activeTab, setActiveTab] = useState('hire');
    const [clientIds, setClientIds] = useState('');
    const [workerIds, setWorkerIds] = useState('');

    // Existing state and handlers remain unchanged...

    const handleHire = async (event) => {
        event.preventDefault();
        try {
            const payload = { client_ids: clientIds.split(',').map(id => id.trim()) };
            const response = await axios.post('http://localhost:8001/bankpal/bank/hire', payload);
            alert('Clients hired successfully');
        } catch (error) {
            console.error('Error hiring clients:', error);
        }
    };

    const handleFire = async (event) => {
        event.preventDefault();
        try {
            const payload = { worker_ids: workerIds.split(',').map(id => id.trim()) };
            const response = await axios.post('http://localhost:8001/bankpal/bank/fire', payload);
            alert('Workers fired successfully');
        } catch (error) {
            console.error('Error firing workers:', error);
        }
    };

    return (
        <div className="bank-container">
            <h1>Bank Management</h1>
            <div className="tabs">
                <button onClick={() => setActiveTab('hire')}>Hire Clients</button>
                <button onClick={() => setActiveTab('fire')}>Fire Workers</button>
            </div>

            {activeTab === 'hire' && (
                <form onSubmit={handleHire}>
                    <h2>Hire Clients as Employees</h2>
                    <input
                        type="text"
                        placeholder="Client IDs (comma-separated)"
                        value={clientIds}
                        onChange={e => setClientIds(e.target.value)}
                    />
                    <button type="submit">Hire Client(s)</button>
                </form>
            )}

            {activeTab === 'fire' && (
                <form onSubmit={handleFire}>
                    <h2>Fire Workers</h2>
                    <input
                        type="text"
                        placeholder="Worker IDs (comma-separated)"
                        value={workerIds}
                        onChange={e => setWorkerIds(e.target.value)}
                    />
                    <button type="submit">Fire Worker(s)</button>
                </form>
            )}
        </div>
    );
};

export default Bank;

import React from 'react';
import './navbar.css';
import { Link } from 'react-router-dom';
import logo from '../assets/logo.png';

const Navbar = () => {
    return (
        <div className="navbar">
            <div className="left-side">
                <div className="navbar-links">
                    <Link className="navbar-link" to="/">Home</Link>
                    <Link className="navbar-link" to="/create">Accounts</Link>
                    <Link className="navbar-link" to="/fraud-detection">Fraud Detection</Link>
                    <Link className="navbar-link" to="/all-accounts">All Accounts</Link>
                    <Link className="navbar-link" to="/banks">Banks</Link>
                    <Link className="navbar-link" to="/products">Products</Link>
                </div>
            </div>
            <div className="right-side">
                <img src={logo} alt="Logo" className="navbar-logo" />
            </div>
        </div>
    );
};

export default Navbar;

import { Routes, Route  } from 'react-router-dom';
import Account from './pages/Account';
import FraudDetection from './pages/FraudDetection';
import Home from './pages/Home';
import AccountsGrid from './pages/AllAccounts';
import './App.css'
import Navbar from './components/navbar';
import Bank from './pages/Bank';

function App() {

  return (
    <div className="App">
      <Navbar />
      <div className="cont">
        <Routes>
          <Route path="/" element={< Home />}/>
          <Route path="/create" element={< Account />} />
          <Route path="/fraud-detection" element={< FraudDetection />} />
          <Route path="/all-accounts" element={< AccountsGrid />} />
          <Route path="/bank" element={< Bank />} />
        </Routes>
      </div>
    </div>
  );
}

export default App

import { Routes, Route  } from 'react-router-dom';
import Account from './pages/Account';
import FraudDetection from './pages/FraudDetection';
import Home from './pages/Home';
import './App.css'
import Navbar from './components/navbar';

function App() {

  return (
    <div className="App">
      <Navbar />
      <div className="cont">
        <Routes>
          <Route path="/" element={< Home />}/>
          <Route path="/create" element={< Account />} />
          <Route path="/fraud-detection" element={< FraudDetection />} />
        </Routes>
      </div>
    </div>
  );
}

export default App

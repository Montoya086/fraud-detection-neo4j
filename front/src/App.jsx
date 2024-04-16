import { Routes, Route  } from 'react-router-dom';
import Account from './pages/Account';
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
        </Routes>
      </div>
    </div>
  );
}

export default App

import { Routes, Route  } from 'react-router-dom';
import Account from './pages/Account';
import Home from './pages/Home';
import './App.css'

function App() {

  return (

  <div className="cont">
    <Routes>
      <Route path="/" element={< Home />}/>
      <Route path="/create" element={< Account />} />
    </Routes>
  </div>
  )
}

export default App

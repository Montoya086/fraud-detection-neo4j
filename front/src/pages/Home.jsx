import React from 'react';
import './Home.css';

const Home = () => {
  return (
    <div className='home-container'>
      <div className="title-container">
        <h1>Bienvenido al sistema de seguridad bancaria AFD</h1>
      </div>
      <div className="view">
        <div className="plane main">
          {Array.from({ length: 5 }, (_, i) => (
            <div key={i} className="circle" style={{ transform: `rotateZ(${i / 5 * 360}deg) rotateX(63.435deg)` }} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;

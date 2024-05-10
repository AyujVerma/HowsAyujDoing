import React, { useState, useEffect } from 'react';
import './App.css';

const App = () => {
  const [currentInfo, setCurrentInfo] = useState({
    type: null,
    id: null,
    name: 'Offline',
    link: null,
    duration: null,
    progress: null,
    image: 'https://blog.namarora.me/images/ayuj_sleeping.jpeg',
    artists: ['Ayuj'],
    mood: 'Asleep'
  });
  const [innerSquareColor, setInnerSquareColor] = useState('');
  const [prevTrackInfo, setPrevTrackInfo] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('https://hows-ayuj-doing.onrender.com/api/current-track');
        // const response = await fetch('http://localhost:5000/api/current-track'); // Debugging purposes.
        const data = await response.json();
        setCurrentInfo(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const intervalTime = 15 * 1000; // Default: 15 seconds
    const refreshInterval = setInterval(fetchData, intervalTime);

    return () => {
      clearInterval(refreshInterval);
    };
  }, []);

  useEffect(() => {
    if (prevTrackInfo && currentInfo.id === prevTrackInfo.id) 
    {
      return;
    }
    switch (currentInfo.type) {
      case 'track':
        let hexColor = null
        if(currentInfo.mood == 'Happy')
        {
          hexColor = '#F8D664'
        }
        else if(currentInfo.mood == 'Sad')
        {
          hexColor = '#004b90'
        }
        setInnerSquareColor(hexColor);
        break;
      case 'ad':
        setInnerSquareColor('#D3D3D3');
        break;
      default:
        setInnerSquareColor('#999AC6');
    }
    
    setPrevTrackInfo(currentInfo);
  }, [currentInfo, prevTrackInfo]);

  return (
    <div className="App">
      <div className="outer-square" style={{ backgroundColor: innerSquareColor }}>
        <div className="inner-square">
          <img src={currentInfo.image} className="album-cover" alt="Album Cover" />
        </div>
        <div className="text-below">
          <div className="title">
            <label>{currentInfo.name}</label>
          </div>
          <div className="artists">
            <div>{currentInfo.artists}</div>
          </div>
          <div className="mood">
            <div>Mood: {currentInfo.mood}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
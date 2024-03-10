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
  });
  const moods = ['Joy', 'Trust', 'Fear', 'Surprise', 'Sadness', 'Anticipation', 'Anger', 'Disgust']; // Taken from Plutchik's eight basic emotions
  const [mood, setMood] = useState('');
  const [innerSquareColor, setInnerSquareColor] = useState('');
  const [prevTrackInfo, setPrevTrackInfo] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('https://hows-ayuj-doing.onrender.com/api/current-track');
        // const response = await fetch('http://localhost:5000/api/current-track'); Debugging purposes.
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
        const randomMood = getRandomMood();
        const randomHexColor = getRandomHexColor();
        setMood(randomMood);
        setInnerSquareColor(randomHexColor);
        break;
      case 'ad':
        setMood('Impatient');
        setInnerSquareColor('#D3D3D3');
        break;
      default:
        setMood('Asleep');
        setInnerSquareColor('#999AC6');
    }
    
    setPrevTrackInfo(currentInfo);
  }, [currentInfo, prevTrackInfo]);

  const getRandomMood = () => {
    const randomIndex = Math.floor(Math.random() * moods.length);
    return moods[randomIndex];
  };

  const getRandomHexColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  };

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
            <div>Mood: {mood}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
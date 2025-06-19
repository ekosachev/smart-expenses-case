import React from 'react';
import car1 from '../img_cars/car1.png';
import car2 from '../img_cars/car2.png';
import car3 from '../img_cars/car3.png';
const car4 = car1;
const car5 = car2;
const car6 = car3;
const car7 = car1;
const car8 = car2;
import inactiveLikeIcon from '../assets/inactive like.svg';
import likePlacedIcon from '../assets/like placed.svg';
import linealDisplayIcon from '../assets/lineal display.svg';
import editProfileIcon from '../assets/edit profile.svg';
import otherThreeDotsIcon from '../assets/other three dots.svg';
import manualIcon from '../assets/manual.svg';
import passengerIcon from '../assets/passenger.svg';

const Autopark = ({ onSelectCar }) => {
  const carImages = [car1, car2, car3, car4, car5, car6, car7, car8];

  const carData = Array.from({ length: 9 }).map((_, i) => ({
    id: i,
    model: 'Porsche 718 Cayman S',
    type: 'Купе',
    seats: 4,
    transmission: 'Manual',
    price: '₽20k/д',
    image: carImages[i % carImages.length], // Use modulo to cycle through images
  }));

  const [favorites, setFavorites] = React.useState([]);

  return (
    <div className="autopark-page">
      <div className="autopark-header">
        <h2>Автопарк</h2>
        <div className="controls">
          <div className="filters">
            <button className="filter-btn">Новые</button>
            <button className="filter-btn">Porsh</button>
          </div>
          <div className="view-options">
            <img src={otherThreeDotsIcon} alt="Filter" className="view-icon active" />
          </div>
        </div>
      </div>

      <div className="car-grid">
        {carData.map(car => (
          <div className="car-card" key={car.id} onClick={() => onSelectCar(car)}>
            <div className="card-header">
              <h3 className="car-model">{car.model}</h3>
              <img src={favorites.includes(car.id) ? likePlacedIcon : inactiveLikeIcon} alt="Add to Favorites" className="heart-icon" onClick={e => {e.stopPropagation(); setFavorites(favs => favs.includes(car.id) ? favs.filter(id => id !== car.id) : [...favs, car.id]);}} />
            </div>
            <p className="car-type">{car.type}</p>
            <div className="car-image-container">
              <img src={car.image} alt={car.model} className="car-image" />
            </div>
            <div className="car-details">
              <div className="detail-item">
                <img src={passengerIcon} alt="Seats" className="detail-icon" />
                <span>{car.seats}</span>
              </div>
              <div className="detail-item">
                <img src={manualIcon} alt="Transmission" className="detail-icon" />
                <span>{car.transmission}</span>
              </div>
              <div className="detail-item price">
                <span>{car.price}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Autopark; 
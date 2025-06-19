import React from 'react';
import car1 from '../img_cars/2014-mercedes-benz-m-class-2012-mercedes-benz-m-class-2008-mercedes-benz-m-class-sport-utility-vehicle-mercedes-car-png-image-8230b0372dd015bcf5312eb17e2751ee-1.png';
import car2 from '../img_cars/car-audi-a3-audi-a4-car-3822c2bc08e2c2bce1d8ead0e70c7ddb-1.png';
import car3 from '../img_cars/maruti-suzuki-dzire-car-suzuki-ertiga-swift-dzire-f8a7d4ae19bd1c349dc080d9081ffd31.png';
import car4 from '../img_cars/suzuki-ertiga-maruti-car-suzuki-ciaz-suzuki-dcac04d3f676c91c7ca6f2d195b86ff3.png';
import car5 from '../img_cars/toyota-innova-toyota-avanza-car-rush-toyota-seven-cars-a3650fca54041ac1aaae4fe013ac79ca 1.png';
import car6 from '../img_cars/white car.png';
import car7 from '../img_cars/2014-mercedes-benz-m-class-2012-mercedes-benz-m-class-2008-mercedes-benz-m-class-sport-utility-vehicle-mercedes-car-png-image-8230b0372dd015bcf5312eb17e2751ee.png';
import car8 from '../img_cars/car-audi-a3-audi-a4-car-3822c2bc08e2c2bce1d8ead0e70c7ddb.png';
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
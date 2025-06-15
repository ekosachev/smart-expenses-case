import React from 'react';

const Autopark = ({ onSelectCar }) => {
  const carData = Array.from({ length: 9 }).map((_, i) => ({
    id: i,
    model: 'Porsche 718 Cayman S',
    type: 'Купе',
    seats: 4,
    transmission: 'Manual',
    price: '₽20k/д',
    image: '/placeholder-car.svg', // Placeholder image
  }));

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
            <img src="/placeholder-grid.svg" alt="Grid View" className="view-icon active" />
            <img src="/placeholder-filter.svg" alt="Filter" className="view-icon" />
          </div>
        </div>
      </div>

      <div className="car-grid">
        {carData.map(car => (
          <div className="car-card" key={car.id} onClick={() => onSelectCar(car.id)}>
            <div className="card-header">
              <h3 className="car-model">{car.model}</h3>
              <img src="/placeholder-heart.svg" alt="Add to Favorites" className="heart-icon" />
            </div>
            <p className="car-type">{car.type}</p>
            <div className="car-image-container">
              <img src={car.image} alt={car.model} className="car-image" />
            </div>
            <div className="car-details">
              <div className="detail-item">
                <img src="/placeholder-seat.svg" alt="Seats" className="detail-icon" />
                <span>{car.seats}</span>
              </div>
              <div className="detail-item">
                <img src="/placeholder-manual.svg" alt="Transmission" className="detail-icon" />
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
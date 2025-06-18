import React, { useState } from 'react';
import './Settings.css';
import emailIcon from '../assets/email.svg';
import genderIcon from '../assets/gender.svg';
import homeIcon from '../assets/home.svg';
import otherThreeDotsIcon from '../assets/other three dots.svg';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('profile'); // Default to Profile tab
  const [profileSettings, setProfileSettings] = useState({
    liveIn: 'Zuichi, Switzerland',
    streetAddress: '2445 Crosswind Drive',
    emailAddress: 'uihutofficial@gmail.com',
    dateOfBirth: '07.12.195',
    gender: 'Male',
    photo: '/placeholder-user.svg', // Placeholder for user photo
    facebook: 'facebook.com/',
    twitter: 'twitter.com/',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfileSettings(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePhotoUpdate = () => {
    // Logic to update photo
    console.log('Update photo');
  };

  const handlePhotoDelete = () => {
    // Logic to delete photo
    console.log('Delete photo');
    setProfileSettings(prev => ({
      ...prev,
      photo: '' // Clear photo or set to default placeholder
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Сохраненные настройки профиля:', profileSettings);
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'my-details':
        return <div>My Details Content (Not implemented yet)</div>;
      case 'profile':
        return (
          <div className="profile-tab-content">
            <h3>Profile</h3>
            <p className="subtitle">Update your photo and personal details here.</p>

            <form onSubmit={handleSubmit}>
              <div className="form-row">
                <div className="form-group with-icon">
                  <label htmlFor="liveIn">Live in</label>
                  <div className="input-wrapper">
                    <img src={homeIcon} alt="Home Icon" className="input-icon" />
                    <input
                      type="text"
                      id="liveIn"
                      name="liveIn"
                      value={profileSettings.liveIn}
                      onChange={handleChange}
                    />
                  </div>
                </div>
                <div className="form-group with-icon">
                  <label htmlFor="streetAddress">Street Address</label>
                  <div className="input-wrapper">
                    <img src={homeIcon} alt="Home Icon" className="input-icon" />
                    <input
                      type="text"
                      id="streetAddress"
                      name="streetAddress"
                      value={profileSettings.streetAddress}
                      onChange={handleChange}
                    />
                  </div>
                </div>
              </div>

              <div className="form-group with-icon">
                <label htmlFor="emailAddress">Email Address</label>
                <div className="input-wrapper">
                  <img src={emailIcon} alt="Mail Icon" className="input-icon" />
                  <input
                    type="email"
                    id="emailAddress"
                    name="emailAddress"
                    value={profileSettings.emailAddress}
                    onChange={handleChange}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group with-icon">
                  <label htmlFor="dateOfBirth">Date Of Birth</label>
                  <div className="input-wrapper">
                    <img src={otherThreeDotsIcon} alt="Birthday Icon" className="input-icon" />
                    <input
                      type="text"
                      id="dateOfBirth"
                      name="dateOfBirth"
                      value={profileSettings.dateOfBirth}
                      onChange={handleChange}
                    />
                  </div>
                </div>
                <div className="form-group with-icon">
                  <label htmlFor="gender">Gender</label>
                  <div className="input-wrapper">
                    <img src={genderIcon} alt="Gender Icon" className="input-icon" />
                    <select
                      id="gender"
                      name="gender"
                      value={profileSettings.gender}
                      onChange={handleChange}
                    >
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="form-group photo-upload-section">
                <label>Your photo</label>
                <p className="subtitle">This will be displayed on your profile.</p>
                <div className="photo-content">
                  <img src={profileSettings.photo} alt="Your Photo" className="profile-photo" />
                  <div className="photo-actions">
                    <span onClick={handlePhotoDelete}>Delete</span>
                    <span onClick={handlePhotoUpdate}>Update</span>
                  </div>
                </div>
              </div>

              <div className="form-group social-profiles">
                <label>Social Profiles</label>
                <div className="input-wrapper">
                  <input
                    type="text"
                    name="facebook"
                    placeholder="facebook.com/"
                    value={profileSettings.facebook}
                    onChange={handleChange}
                  />
                </div>
                <div className="input-wrapper">
                  <input
                    type="text"
                    name="twitter"
                    placeholder="twitter.com/"
                    value={profileSettings.twitter}
                    onChange={handleChange}
                  />
                </div>
              </div>

              {/* No explicit save button shown in image for profile tab, but keep for functionality */}
              {/* <button type="submit" className="save-button">Save Settings</button> */}
            </form>
          </div>
        );
      case 'password':
        return <div>Password Content (Not implemented yet)</div>;
      case 'email':
        return <div>Email Content (Not implemented yet)</div>;
      case 'notification':
        return <div>Notification Content (Not implemented yet)</div>;
      default:
        return null;
    }
  };

  return (
    <div className="settings-container">
      <h2>Settings</h2>
      <div className="tabs-navigation">
        <button className={activeTab === 'my-details' ? 'active' : ''} onClick={() => setActiveTab('my-details')}>My details</button>
        <button className={activeTab === 'profile' ? 'active' : ''} onClick={() => setActiveTab('profile')}>Profile</button>
        <button className={activeTab === 'password' ? 'active' : ''} onClick={() => setActiveTab('password')}>Password</button>
        <button className={activeTab === 'email' ? 'active' : ''} onClick={() => setActiveTab('email')}>Email</button>
        <button className={activeTab === 'notification' ? 'active' : ''} onClick={() => setActiveTab('notification')}>Notification</button>
      </div>
      {renderContent()}
    </div>
  );
};

export default Settings; 
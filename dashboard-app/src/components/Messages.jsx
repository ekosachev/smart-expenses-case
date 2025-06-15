import React, { useState } from 'react';
import './Messages.css';

const Messages = () => {
  const [activeChat, setActiveChat] = useState({
    id: 1,
    name: 'Killian James',
    status: 'Active Now',
    avatar: '/placeholder-user.svg',
    messages: [
      { id: 1, sender: 'other', content: 'Hi, i hope you are doing well, yesterday you have gave a pen This very nice, i am very happy for this.yesterday you have gave a pen This very nice', time: '4:30 PM' },
      { id: 2, sender: 'self', content: 'yea i\'m well, Thank you, i am very happy for this.yesterday you have gave a pen This very nice', time: '4:30 PM' },
      { id: 3, sender: 'other', content: 'Hi, i hope you are doing well, yesterday you have gave a pen This very nice 🤩', time: '4:30 PM' },
      { id: 4, sender: 'self', content: 'yea i\'m well, Thank you, i am very happy for this.yesterday you have gave a pen This very nice', time: '4:30 PM' },
      { id: 5, sender: 'other', content: 'voice', time: '1:25' }, // Placeholder for voice message
    ],
  });

  const pinnedContacts = [
    { id: 1, name: 'Killian James', status: 'Typing...', avatar: '/placeholder-user.svg', time: '4:30 PM', unread: 2, online: true },
  ];

  const allMessageContacts = [
    { id: 2, name: 'Desian Tam', message: 'Hello! Everyone', avatar: '/placeholder-user2.svg', time: '9:36 AM', unread: 0, delivered: true },
    { id: 3, name: 'Ahmed Medi', message: 'Wow really Cool 🔥', avatar: '/placeholder-user3.svg', time: '1:15 AM', unread: 0 },
    { id: 4, name: 'Claudia Maudi', message: 'Nice', avatar: '/placeholder-user4.svg', time: '4:30 PM', unread: 0 },
    { id: 5, name: 'Novita', message: 'yah, nice design', avatar: '/placeholder-user5.svg', time: '4:30 PM', unread: 2 },
    { id: 6, name: 'Milie Nose', message: 'Awesome 🔥', avatar: '/placeholder-user6.svg', time: '8:20 PM', unread: 1 },
    { id: 7, name: 'Ikhsan SD', message: 'Voice message', avatar: '/placeholder-user7.svg', time: 'yesterday', unread: 0, voice: true },
    { id: 8, name: 'Aditya', message: 'publish now', avatar: '/placeholder-user8.svg', time: 'yesterday', unread: 0, delivered: true },
  ];

  return (
    <div className="messages-container">
      <h2>Messages
        <img src="/placeholder-pencil.svg" alt="New message" className="new-message-icon" />
      </h2>

      <div className="messages-content">
        <div className="contacts-panel">
          <div className="search-bar-contacts">
            <img src="/placeholder-search.svg" alt="Search" />
            <input type="text" placeholder="Search..." />
          </div>

          <div className="contacts-list">
            <div className="contacts-group">
              <span className="group-title">PINNED</span>
              {pinnedContacts.map(contact => (
                <div key={contact.id} className="contact-item active">
                  <div className="contact-avatar-wrapper">
                    <img src={contact.avatar} alt={contact.name} className="contact-avatar" />
                    {contact.online && <span className="online-dot"></span>}
                  </div>
                  <div className="contact-info">
                    <div className="contact-name">{contact.name}</div>
                    <div className="contact-status">{contact.status}</div>
                  </div>
                  <div className="contact-meta">
                    <div className="contact-time">{contact.time}</div>
                    {contact.unread > 0 && <div className="unread-count">{contact.unread}</div>}
                  </div>
                </div>
              ))}
            </div>

            <div className="contacts-group">
              <span className="group-title">All Message</span>
              {allMessageContacts.map(contact => (
                <div key={contact.id} className="contact-item">
                  <div className="contact-avatar-wrapper">
                    <img src={contact.avatar} alt={contact.name} className="contact-avatar" />
                  </div>
                  <div className="contact-info">
                    <div className="contact-name">{contact.name}</div>
                    <div className="contact-message">{contact.message}</div>
                  </div>
                  <div className="contact-meta">
                    <div className="contact-time">{contact.time}</div>
                    {contact.unread > 0 && <div className="unread-count">{contact.unread}</div>}
                    {contact.delivered && <img src="/placeholder-delivered.svg" alt="Delivered" className="delivered-icon" />}
                    {contact.voice && <img src="/placeholder-microphone-small.svg" alt="Voice message" className="voice-icon" />}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="chat-panel">
          <div className="chat-header">
            <div className="chat-contact-info">
              <img src={activeChat.avatar} alt={activeChat.name} className="chat-avatar" />
              <div>
                <div className="chat-contact-name">{activeChat.name}</div>
                <div className="chat-contact-status">{activeChat.status}</div>
              </div>
            </div>
            <div className="chat-actions">
              <img src="/placeholder-video-call.svg" alt="Video call" />
              <img src="/placeholder-phone-call.svg" alt="Voice call" />
              <img src="/placeholder-more-vertical.svg" alt="More options" />
            </div>
          </div>

          <div className="chat-messages">
            {activeChat.messages.map(message => (
              <div key={message.id} className={`message-bubble ${message.sender}`}>
                {message.sender === 'other' && <img src={activeChat.avatar} alt="Avatar" className="message-avatar" />}
                <div className="message-content-wrapper">
                  {message.content === 'voice' ? (
                    <div className="voice-message">
                      <img src="/placeholder-pause.svg" alt="Pause" className="voice-control-icon" />
                      <div className="waveform"></div> {/* Placeholder for waveform */}
                      <span>{message.time}</span>
                    </div>
                  ) : (
                    <p>{message.content}</p>
                  )}
                  {message.sender === 'self' && <span className="message-time">{message.time}</span>}
                </div>
                {message.sender === 'self' && <img src={activeChat.avatar} alt="Avatar" className="message-avatar" />}
              </div>
            ))}
          </div>

          <div className="chat-input-area">
            <img src="/placeholder-attachment.svg" alt="Attachment" className="input-icon" />
            <input type="text" placeholder="Type Something..." />
            <img src="/placeholder-send.svg" alt="Send" className="input-icon send-icon" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Messages; 
import React, { useState } from 'react';
import './Messages.css';

const Messages = () => {
  const [activeChat, setActiveChat] = useState({
    id: 1,
    name: 'Иван Петров',
    status: 'В сети',
    avatar: '/placeholder-user.svg',
    messages: [
      { id: 1, sender: 'other', content: 'Привет, надеюсь, у тебя все хорошо, вчера ты дал мне эту ручку, она очень красивая, я очень этому рад. Вчера ты дал мне эту ручку, она очень красивая', time: '16:30' },
      { id: 2, sender: 'self', content: 'Да, у меня все хорошо, спасибо, я очень этому рад. Вчера ты дал мне эту ручку, она очень красивая', time: '16:30' },
      { id: 3, sender: 'other', content: 'Привет, надеюсь, у тебя все хорошо, вчера ты дал мне эту ручку, она очень красивая 🤩', time: '16:30' },
      { id: 4, sender: 'self', content: 'Да, у меня все хорошо, спасибо, я очень этому рад. Вчера ты дал мне эту ручку, она очень красивая', time: '16:30' },
      { id: 5, sender: 'other', content: 'голосовое', time: '1:25' }, // Placeholder for voice message
    ],
  });

  const pinnedContacts = [
    { id: 1, name: 'Иван Петров', status: 'Печатает...', avatar: '/placeholder-user.svg', time: '16:30', unread: 2, online: true },
  ];

  const allMessageContacts = [
    { id: 2, name: 'Денис Тамов', message: 'Привет всем!', avatar: '/placeholder-user2.svg', time: '9:36', unread: 0, delivered: true },
    { id: 3, name: 'Ахмед Медведев', message: 'Вау, круто 🔥', avatar: '/placeholder-user3.svg', time: '1:15', unread: 0 },
    { id: 4, name: 'Клавдия Маслова', message: 'Отлично', avatar: '/placeholder-user4.svg', time: '16:30', unread: 0 },
    { id: 5, name: 'Новита Смирнова', message: 'да, хороший дизайн', avatar: '/placeholder-user5.svg', time: '16:30', unread: 2 },
    { id: 6, name: 'Мила Носова', message: 'Потрясающе 🔥', avatar: '/placeholder-user6.svg', time: '20:20', unread: 1 },
    { id: 7, name: 'Ихсан Салимов', message: 'Голосовое сообщение', avatar: '/placeholder-user7.svg', time: 'вчера', unread: 0, voice: true },
    { id: 8, name: 'Адиль Иванов', message: 'опубликовать сейчас', avatar: '/placeholder-user8.svg', time: 'вчера', unread: 0, delivered: true },
  ];

  return (
    <div className="messages-container">
      <h2>Сообщения
        <img src="/placeholder-pencil.svg" alt="Новое сообщение" className="new-message-icon" />
      </h2>

      <div className="messages-content">
        <div className="contacts-panel">
          <div className="search-bar-contacts">
            <img src="/placeholder-search.svg" alt="Поиск" />
            <input type="text" placeholder="Поиск..." />
          </div>

          <div className="contacts-list">
            <div className="contacts-group">
              <span className="group-title">ЗАКРЕПЛЕННЫЕ</span>
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
              <span className="group-title">Все сообщения</span>
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
                    {contact.delivered && <img src="/placeholder-delivered.svg" alt="Доставлено" className="delivered-icon" />}
                    {contact.voice && <img src="/placeholder-microphone-small.svg" alt="Голосовое сообщение" className="voice-icon" />}
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
              <img src="/placeholder-video-call.svg" alt="Видеозвонок" />
              <img src="/placeholder-phone-call.svg" alt="Голосовой вызов" />
              <img src="/placeholder-more-vertical.svg" alt="Дополнительные опции" />
            </div>
          </div>

          <div className="chat-messages">
            {activeChat.messages.map(message => (
              <div key={message.id} className={`message-bubble ${message.sender}`}>
                {message.sender === 'other' && <img src={activeChat.avatar} alt="Аватар" className="message-avatar" />}
                <div className="message-content-wrapper">
                  {message.content === 'voice' ? (
                    <div className="voice-message">
                      <img src="/placeholder-pause.svg" alt="Пауза" className="voice-control-icon" />
                      <div className="waveform"></div> {/* Placeholder for waveform */}
                      <span>{message.time}</span>
                    </div>
                  ) : (
                    <p>{message.content}</p>
                  )}
                  {message.sender === 'self' && <span className="message-time">{message.time}</span>}
                </div>
                {message.sender === 'self' && <img src={activeChat.avatar} alt="Аватар" className="message-avatar" />}
              </div>
            ))}
          </div>

          <div className="chat-input-area">
            <img src="/placeholder-attachment.svg" alt="Вложение" className="input-icon" />
            <input type="text" placeholder="Напишите что-нибудь..." />
            <img src="/placeholder-send.svg" alt="Отправить" className="input-icon send-icon" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Messages; 
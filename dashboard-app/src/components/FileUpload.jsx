import React, { useState, useRef } from 'react';
import './FileUpload.css';

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [companyId, setCompanyId] = useState(1);
  const [apiKey, setApiKey] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setUploadStatus(null);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
      setUploadStatus(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus({ type: 'error', message: 'Пожалуйста, выберите файл' });
      return;
    }

    setIsUploading(true);
    setUploadStatus({ type: 'info', message: 'Загрузка файла...' });

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('company_id', companyId);
      formData.append('api_key', apiKey);

      const response = await fetch(`http://localhost:8000/import/all`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setUploadStatus({ 
          type: 'success', 
          message: `Успешно импортировано: ${result.imported_count || ''}` 
        });
        setSelectedFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      } else {
        const errorData = await response.json();
        setUploadStatus({ 
          type: 'error', 
          message: `Ошибка: ${errorData.detail || 'Неизвестная ошибка'}` 
        });
      }
    } catch (error) {
      setUploadStatus({ 
        type: 'error', 
        message: `Ошибка соединения: ${error.message}` 
      });
    } finally {
      setIsUploading(false);
    }
  };

  const getFileIcon = (filename) => {
    if (!filename) return '📄';
    if (filename.endsWith('.csv')) return '📊';
    if (filename.endsWith('.xlsx') || filename.endsWith('.xls')) return '📈';
    if (filename.endsWith('.json')) return '🟦';
    return '📄';
  };

  return (
    <div className="file-upload-container">
      <div className="file-upload-header">
        <h3>📁 Импорт данных</h3>
        <p>Загрузите файл (транспорт + расходы) для импорта в базу данных</p>
      </div>

      <div className="company-selector">
        <label>ID компании:</label>
        <input
          type="number"
          value={companyId}
          onChange={(e) => setCompanyId(parseInt(e.target.value) || 1)}
          min="1"
        />
      </div>

      <div className="api-key-input pretty">
        <label htmlFor="api-key-input-field">API-ключ:</label>
        <div className="api-key-input-wrapper">
          <span className="api-key-icon">🔑</span>
          <input
            id="api-key-input-field"
            type="text"
            value={apiKey}
            onChange={e => setApiKey(e.target.value)}
            placeholder="Введите ваш API-ключ"
            autoComplete="off"
          />
        </div>
      </div>

      <div 
        className={`file-drop-zone ${dragActive ? 'drag-active' : ''} ${selectedFile ? 'has-file' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.xls,.json"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        
        {selectedFile ? (
          <div className="selected-file">
            <span className="file-icon">{getFileIcon(selectedFile.name)}</span>
            <div className="file-info">
              <span className="file-name">{selectedFile.name}</span>
              <span className="file-size">
                {(selectedFile.size / 1024).toFixed(1)} KB
              </span>
            </div>
            <button 
              className="remove-file"
              onClick={(e) => {
                e.stopPropagation();
                setSelectedFile(null);
                setUploadStatus(null);
                if (fileInputRef.current) {
                  fileInputRef.current.value = '';
                }
              }}
            >
              ✕
            </button>
          </div>
        ) : (
          <div className="drop-zone-content">
            <span className="upload-icon">📁</span>
            <p>Перетащите файл сюда или кликните для выбора</p>
            <p className="file-types">Поддерживаемые форматы: CSV, XLSX, JSON</p>
          </div>
        )}
      </div>

      {uploadStatus && (
        <div className={`upload-status ${uploadStatus.type}`}>
          <span className="status-icon">
            {uploadStatus.type === 'success' ? '✅' : 
             uploadStatus.type === 'error' ? '❌' : '⏳'}
          </span>
          <span className="status-message">{uploadStatus.message}</span>
        </div>
      )}

      <div className="upload-actions">
        <button
          className="upload-btn"
          onClick={handleUpload}
          disabled={!selectedFile || isUploading}
        >
          {isUploading ? (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <span>Загрузка...</span>
            </div>
          ) : (
            '📤 Загрузить файл'
          )}
        </button>
      </div>

      <div className="upload-info">
        <h4>Информация об импорте:</h4>
        <ul>
          <li>• Файл может содержать транспорт и расходы одновременно</li>
          <li>• Поддерживаются форматы CSV, Excel, JSON</li>
          <li>• Максимальный размер файла: 10MB</li>
          <li>• Данные будут добавлены в базу PostgreSQL</li>
        </ul>
      </div>
    </div>
  );
};

export default FileUpload; 
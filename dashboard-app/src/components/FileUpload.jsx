import React, { useState, useRef } from 'react';
import './FileUpload.css';

const FileUpload = () => {
  const [mode, setMode] = useState('separate'); // 'separate' | 'mixed'
  const [vehicleFile, setVehicleFile] = useState(null);
  const [expenseFile, setExpenseFile] = useState(null);
  const [mixedFile, setMixedFile] = useState(null);
  const [companyId, setCompanyId] = useState(1);
  const [apiKey, setApiKey] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const vehicleInputRef = useRef(null);
  const expenseInputRef = useRef(null);
  const mixedInputRef = useRef(null);

  const handleFileSelect = (event, type) => {
    const file = event.target.files[0];
    if (!file) return;
    if (type === 'vehicle') setVehicleFile(file);
    if (type === 'expense') setExpenseFile(file);
    if (type === 'mixed') setMixedFile(file);
    setUploadStatus(null);
  };

  const handleRemoveFile = (type) => {
    if (type === 'vehicle') {
      setVehicleFile(null);
      if (vehicleInputRef.current) vehicleInputRef.current.value = '';
    }
    if (type === 'expense') {
      setExpenseFile(null);
      if (expenseInputRef.current) expenseInputRef.current.value = '';
    }
    if (type === 'mixed') {
      setMixedFile(null);
      if (mixedInputRef.current) mixedInputRef.current.value = '';
    }
    setUploadStatus(null);
  };

  const getFileIcon = (filename) => {
    if (!filename) return '📄';
    if (filename.endsWith('.csv')) return '📊';
    if (filename.endsWith('.xlsx') || filename.endsWith('.xls')) return '📈';
    if (filename.endsWith('.json')) return '🟦';
    return '📄';
  };

  const handleUpload = async () => {
    setIsUploading(true);
    setUploadStatus({ type: 'info', message: 'Загрузка файла...' });
    try {
      if (mode === 'separate') {
        let results = [];
        if (vehicleFile) {
          const formData = new FormData();
          formData.append('file', vehicleFile);
          formData.append('company_id', companyId);
          formData.append('api_key', apiKey);
          const response = await fetch('http://localhost:8000/import/vehicles', {
            method: 'POST',
            body: formData,
          });
          const result = await response.json();
          results.push({ type: 'ТС', ...result, ok: response.ok });
        }
        if (expenseFile) {
          const formData = new FormData();
          formData.append('file', expenseFile);
          formData.append('company_id', companyId);
          formData.append('api_key', apiKey);
          const response = await fetch('http://localhost:8000/import/expenses', {
            method: 'POST',
            body: formData,
          });
          const result = await response.json();
          results.push({ type: 'Расходы', ...result, ok: response.ok });
        }
        if (results.length === 0) {
          setUploadStatus({ type: 'error', message: 'Выберите хотя бы один файл' });
        } else if (results.some(r => !r.ok)) {
          setUploadStatus({ type: 'error', message: results.map(r => r.ok ? '' : `Ошибка (${r.type}): ${r.detail || 'Неизвестная ошибка'}`).join(' ') });
        } else {
          setUploadStatus({ type: 'success', message: results.map(r => `Импортировано (${r.type}): ${r.imported_count || 0}`).join(' | ') });
          setVehicleFile(null);
          setExpenseFile(null);
          if (vehicleInputRef.current) vehicleInputRef.current.value = '';
          if (expenseInputRef.current) expenseInputRef.current.value = '';
        }
      } else if (mode === 'mixed') {
        if (!mixedFile) {
          setUploadStatus({ type: 'error', message: 'Выберите файл' });
          setIsUploading(false);
          return;
        }
        const formData = new FormData();
        formData.append('file', mixedFile);
        formData.append('company_id', companyId);
        formData.append('api_key', apiKey);
        const response = await fetch('http://localhost:8000/import/all', {
          method: 'POST',
          body: formData,
        });
        const result = await response.json();
        if (response.ok) {
          setUploadStatus({ type: 'success', message: `Импортировано: ${result.imported_count || 0}` });
          setMixedFile(null);
          if (mixedInputRef.current) mixedInputRef.current.value = '';
        } else {
          setUploadStatus({ type: 'error', message: `Ошибка: ${result.detail || 'Неизвестная ошибка'}` });
        }
      }
    } catch (error) {
      setUploadStatus({ type: 'error', message: `Ошибка соединения: ${error.message}` });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <div className="file-upload-header">
        <h3>📁 Импорт данных</h3>
        <p>Загрузите таблицы с транспортом и расходами или смешанный файл</p>
      </div>

      <div className="import-mode-switch">
        <button className={mode === 'separate' ? 'active' : ''} onClick={() => setMode('separate')}>Два файла</button>
        <button className={mode === 'mixed' ? 'active' : ''} onClick={() => setMode('mixed')}>Смешанный файл</button>
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

      {mode === 'separate' && (
        <>
          <div className="file-drop-zone" onClick={() => vehicleInputRef.current?.click()}>
            <input
              ref={vehicleInputRef}
              type="file"
              accept=".csv,.xlsx,.xls,.json"
              onChange={e => handleFileSelect(e, 'vehicle')}
              style={{ display: 'none' }}
            />
            {vehicleFile ? (
              <div className="selected-file">
                <span className="file-icon">{getFileIcon(vehicleFile.name)}</span>
                <div className="file-info">
                  <span className="file-name">{vehicleFile.name}</span>
                  <span className="file-size">{(vehicleFile.size / 1024).toFixed(1)} KB</span>
                </div>
                <button className="remove-file" onClick={e => { e.stopPropagation(); handleRemoveFile('vehicle'); }}>✕</button>
              </div>
            ) : (
              <div className="drop-zone-content">
                <span className="upload-icon">📁</span>
                <p>Таблица с транспортом (CSV, XLSX, JSON)</p>
              </div>
            )}
          </div>
          <div className="file-drop-zone" onClick={() => expenseInputRef.current?.click()}>
            <input
              ref={expenseInputRef}
              type="file"
              accept=".csv,.xlsx,.xls,.json"
              onChange={e => handleFileSelect(e, 'expense')}
              style={{ display: 'none' }}
            />
            {expenseFile ? (
              <div className="selected-file">
                <span className="file-icon">{getFileIcon(expenseFile.name)}</span>
                <div className="file-info">
                  <span className="file-name">{expenseFile.name}</span>
                  <span className="file-size">{(expenseFile.size / 1024).toFixed(1)} KB</span>
                </div>
                <button className="remove-file" onClick={e => { e.stopPropagation(); handleRemoveFile('expense'); }}>✕</button>
              </div>
            ) : (
              <div className="drop-zone-content">
                <span className="upload-icon">📁</span>
                <p>Таблица с расходами (CSV, XLSX, JSON)</p>
              </div>
            )}
          </div>
        </>
      )}
      {mode === 'mixed' && (
        <div className="file-drop-zone" onClick={() => mixedInputRef.current?.click()}>
          <input
            ref={mixedInputRef}
            type="file"
            accept=".json,.csv,.xlsx,.xls"
            onChange={e => handleFileSelect(e, 'mixed')}
            style={{ display: 'none' }}
          />
          {mixedFile ? (
            <div className="selected-file">
              <span className="file-icon">{getFileIcon(mixedFile.name)}</span>
              <div className="file-info">
                <span className="file-name">{mixedFile.name}</span>
                <span className="file-size">{(mixedFile.size / 1024).toFixed(1)} KB</span>
              </div>
              <button className="remove-file" onClick={e => { e.stopPropagation(); handleRemoveFile('mixed'); }}>✕</button>
            </div>
          ) : (
            <div className="drop-zone-content">
              <span className="upload-icon">📁</span>
              <p>Смешанный файл (JSON, CSV, XLSX)</p>
            </div>
          )}
        </div>
      )}

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
          disabled={isUploading}
        >
          {isUploading ? (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <span>Загрузка...</span>
            </div>
          ) : (
            '📤 Загрузить'
          )}
        </button>
      </div>

      <div className="upload-info">
        <h4>Информация об импорте:</h4>
        <ul>
          <li>• Можно загрузить транспорт и расходы по отдельности или смешанным файлом</li>
          <li>• Поддерживаются форматы CSV, Excel, JSON</li>
          <li>• Максимальный размер файла: 10MB</li>
          <li>• Данные будут добавлены в базу PostgreSQL</li>
        </ul>
      </div>
    </div>
  );
};

export default FileUpload; 
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const ProviderSelector = ({ onSelectionChange, selectedProviders }) => {
  const [availableProviders, setAvailableProviders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProviders = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/providers');
        if (!response.ok) {
          throw new Error('Failed to fetch providers');
        }
        const data = await response.json();
        setAvailableProviders(data);
        // Initialize selection with all providers if empty/first load
        if (selectedProviders.length === 0) {
            onSelectionChange(data);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProviders();
  }, []);

  const handleToggle = (provider) => {
    let newSelection;
    if (selectedProviders.includes(provider)) {
      newSelection = selectedProviders.filter((p) => p !== provider);
    } else {
      newSelection = [...selectedProviders, provider];
    }
    onSelectionChange(newSelection);
  };

  if (loading) return <div>Loading providers...</div>;
  if (error) return <div style={{ color: 'red' }}>Error loading providers: {error}</div>;

  return (
    <div style={{ marginTop: '20px' }}>
        <h3 style={{ fontSize: '1.1rem', marginBottom: '10px', color: '#444' }}>Select Search Sources:</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
        {availableProviders.map((provider) => (
            <motion.div
            key={provider}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleToggle(provider)}
            style={{
                padding: '8px 12px',
                borderRadius: '20px',
                cursor: 'pointer',
                backgroundColor: selectedProviders.includes(provider) ? '#667eea' : '#e0e0e0',
                color: selectedProviders.includes(provider) ? 'white' : '#333',
                fontSize: '0.9rem',
                fontWeight: '500',
                userSelect: 'none',
                transition: 'background-color 0.2s',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
            }}
            >
            <span>{selectedProviders.includes(provider) ? '✓' : '+'}</span>
            {provider.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </motion.div>
        ))}
        </div>
    </div>
  );
};

export default ProviderSelector;

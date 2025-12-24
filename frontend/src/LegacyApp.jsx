import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Header from './components/Header';
import ModuleSelector from './components/ModuleSelector';
import ResearchForm from './components/ResearchForm';
import ResultsDisplay from './components/ResultsDisplay';
import ProviderSelector from './components/ProviderSelector';
import { getModules, performResearch } from './utils/api';
import { Loader, AlertCircle } from 'lucide-react';

function LegacyApp() {
  const [modules, setModules] = useState([]);
  const [selectedModules, setSelectedModules] = useState([]);
  const [selectedProviders, setSelectedProviders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [entityName, setEntityName] = useState('');

  useEffect(() => {
    fetchModules();
  }, []);

  const fetchModules = async () => {
    try {
      const data = await getModules();
      setModules(data);
      // Select first 3 modules by default
      setSelectedModules(data.slice(0, 3).map(m => m.id));
    } catch (err) {
      console.error('Failed to fetch modules:', err);
      setError('Failed to load research modules. Please check if the backend is running.');
    }
  };

  const handleModuleToggle = (moduleId) => {
    setSelectedModules(prev =>
      prev.includes(moduleId)
        ? prev.filter(id => id !== moduleId)
        : [...prev, moduleId]
    );
  };

  const handleResearch = async (formData) => {
    if (selectedModules.length === 0) {
      setError('Please select at least one research module');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);
    setEntityName(formData.entity_name);

    try {
      const response = await performResearch({
        entity_name: formData.entity_name,
        entity_type: formData.entity_type,
        research_types: selectedModules,
        selected_providers: selectedProviders,
      });

      setResults(response);
    } catch (err) {
      console.error('Research failed:', err);
      setError(err.response?.data?.detail || 'Research failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', paddingBottom: '50px' }}>
      {/* Animated background particles */}
      <div className="particles">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="particle"
            style={{
              width: Math.random() * 20 + 10,
              height: Math.random() * 20 + 10,
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              x: [0, Math.random() * 100 - 50, 0],
              y: [0, Math.random() * 100 - 50, 0],
              opacity: [0.2, 0.5, 0.2],
            }}
            transition={{
              duration: Math.random() * 10 + 10,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
        ))}
      </div>

      <Header />

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          style={{
            margin: '20px',
            padding: '15px 20px',
            background: 'rgba(239, 68, 68, 0.1)',
            border: '2px solid #ef4444',
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            color: '#dc2626',
          }}
        >
          <AlertCircle size={24} />
          <span>{error}</span>
        </motion.div>
      )}

      {loading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '60px',
            gap: '20px',
          }}
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          >
            <Loader size={64} color="#fff" />
          </motion.div>
          <h2 style={{ color: '#fff', fontSize: '1.5rem' }}>
            AI is analyzing your request...
          </h2>
          <p style={{ color: 'rgba(255, 255, 255, 0.8)' }}>
            Processing {selectedModules.length} research modules
          </p>
        </motion.div>
      )}

      {!loading && !results && (
        <>
          <ResearchForm onSubmit={handleResearch} loading={loading} />
          <div style={{ maxWidth: '600px', margin: '0 auto' }}>
            <ProviderSelector
              selectedProviders={selectedProviders}
              onSelectionChange={setSelectedProviders}
            />
          </div>
          {modules.length > 0 && (
            <ModuleSelector
              modules={modules}
              selectedModules={selectedModules}
              onToggle={handleModuleToggle}
            />
          )}
        </>
      )}

      {results && (
        <>
          <ResultsDisplay
            results={results.results}
            entityName={results.entity_name}
            reportId={results.report_id}
          />
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            style={{
              display: 'flex',
              justifyContent: 'center',
              margin: '30px 20px',
            }}
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                setResults(null);
                setError(null);
              }}
              style={{
                padding: '15px 40px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: '#fff',
                border: 'none',
                borderRadius: '8px',
                fontSize: '1.1rem',
                fontWeight: 'bold',
                cursor: 'pointer',
              }}
            >
              Start New Research
            </motion.button>
          </motion.div>
        </>
      )}
    </div>
  );
}

export default LegacyApp;

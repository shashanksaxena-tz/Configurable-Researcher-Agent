import { motion, AnimatePresence } from 'framer-motion';
import { Download, ExternalLink, TrendingUp } from 'lucide-react';

const ResultsDisplay = ({ results, entityName, reportId }) => {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
      },
    },
  };

  const item = {
    hidden: { y: 20, opacity: 0 },
    show: { y: 0, opacity: 1 },
  };

  if (!results || results.length === 0) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      style={{ padding: '20px' }}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="glass-card"
        style={{
          padding: '30px',
          marginBottom: '30px',
          textAlign: 'center',
        }}
      >
        <h2 style={{ fontSize: '2rem', color: '#333', marginBottom: '15px' }}>
          Research Complete for <span style={{ color: '#667eea' }}>{entityName}</span>
        </h2>
        <p style={{ color: '#666', fontSize: '1.1rem', marginBottom: '20px' }}>
          {results.length} analysis modules completed successfully
        </p>

        {reportId && (
          <motion.a
            href={`http://localhost:8000/reports/${reportId}_${entityName.replace(' ', '_')}_report.pdf`}
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '10px',
              padding: '12px 24px',
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              color: '#fff',
              textDecoration: 'none',
              borderRadius: '8px',
              fontWeight: 'bold',
            }}
          >
            <Download size={20} />
            Download Full Report (PDF)
          </motion.a>
        )}
      </motion.div>

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
          gap: '20px',
        }}
      >
        <AnimatePresence>
          {results.map((result, index) => (
            <motion.div
              key={result.research_type}
              variants={item}
              className="glass-card"
              style={{
                padding: '25px',
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              {/* Animated background accent */}
              <motion.div
                initial={{ x: '-100%' }}
                animate={{ x: '100%' }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  repeatDelay: 3,
                  ease: 'easeInOut',
                }}
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  height: '100%',
                  width: '50%',
                  background: 'linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent)',
                  pointerEvents: 'none',
                }}
              />

              <div style={{ position: 'relative', zIndex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '15px' }}>
                  <h3 style={{ fontSize: '1.5rem', color: '#333', fontWeight: 'bold' }}>
                    {result.title}
                  </h3>
                  <motion.div
                    animate={{ rotate: [0, 360] }}
                    transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                  >
                    <TrendingUp size={24} color="#667eea" />
                  </motion.div>
                </div>

                <div
                  style={{
                    background: 'rgba(102, 126, 234, 0.1)',
                    padding: '15px',
                    borderRadius: '8px',
                    marginBottom: '15px',
                  }}
                >
                  <p style={{ color: '#555', lineHeight: '1.6' }}>{result.summary}</p>
                </div>

                <div style={{ marginBottom: '15px' }}>
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '10px',
                      marginBottom: '8px',
                    }}
                  >
                    <span style={{ color: '#666', fontWeight: '500' }}>Confidence Score:</span>
                    <span
                      style={{
                        background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                        color: '#fff',
                        padding: '4px 12px',
                        borderRadius: '12px',
                        fontWeight: 'bold',
                      }}
                    >
                      {(result.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                  
                  {/* Animated confidence bar */}
                  <div style={{ background: '#e0e0e0', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${result.confidence * 100}%` }}
                      transition={{ duration: 1, delay: index * 0.2 }}
                      style={{
                        height: '100%',
                        background: 'linear-gradient(90deg, #10b981, #059669)',
                      }}
                    />
                  </div>
                </div>

                <div style={{ borderTop: '1px solid #e0e0e0', paddingTop: '15px' }}>
                  <h4 style={{ fontSize: '1rem', color: '#666', marginBottom: '10px' }}>Key Data Points:</h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {Object.entries(result.data).slice(0, 4).map(([key, value]) => (
                      <div
                        key={key}
                        style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          padding: '8px',
                          background: 'rgba(0, 0, 0, 0.02)',
                          borderRadius: '4px',
                        }}
                      >
                        <span style={{ color: '#666', fontSize: '0.9rem' }}>
                          {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </span>
                        <span style={{ color: '#333', fontSize: '0.9rem', fontWeight: '500' }}>
                          {typeof value === 'object' ? JSON.stringify(value).slice(0, 30) + '...' : String(value).slice(0, 50)}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
};

export default ResultsDisplay;

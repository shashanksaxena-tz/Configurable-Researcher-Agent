import { motion, AnimatePresence } from 'framer-motion';
import { Download, TrendingUp, ShieldCheck } from 'lucide-react';
import ExecutiveSummary from './ExecutiveSummary';
import SourceList from './SourceList';

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
      style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        style={{
          padding: '40px 0',
          textAlign: 'center',
          marginBottom: '40px'
        }}
      >
        <h2 style={{ fontSize: '2.5rem', fontFamily: 'Merriweather, serif', color: '#111827', marginBottom: '10px' }}>
          Research Dossier: <span style={{ color: '#059669', borderBottom: '3px solid #059669' }}>{entityName}</span>
        </h2>
        <p style={{ color: '#6b7280', fontSize: '1.1rem' }}>
          Intelligence gathered from {results.length} distinct analysis vectors
        </p>

        {reportId && (
          <motion.a
            href={`http://localhost:8000/reports/${reportId}_${entityName.replace(' ', '_')}_report.pdf`}
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            style={{
              marginTop: '20px',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '10px',
              padding: '12px 24px',
              background: '#1f2937',
              color: '#fff',
              textDecoration: 'none',
              borderRadius: '6px',
              fontWeight: '600',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
            }}
          >
            <Download size={18} />
            Download Executive Report (PDF)
          </motion.a>
        )}
      </motion.div>

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '40px',
        }}
      >
        <AnimatePresence>
          {results.map((result) => (
            <motion.div
              key={result.research_type}
              variants={item}
              style={{
                background: '#fff',
                borderRadius: '12px',
                boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                overflow: 'hidden',
                border: '1px solid #f3f4f6'
              }}
            >
              {/* Header Strip */}
              <div style={{
                background: '#f8fafc',
                padding: '20px 30px',
                borderBottom: '1px solid #e5e7eb',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <h3 style={{ fontSize: '1.5rem', color: '#1e293b', fontWeight: 'bold', margin: 0 }}>
                  {result.title}
                </h3>

                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.9rem', color: '#64748b' }}>
                    <ShieldCheck size={18} />
                    <span>Confidence: <strong>{(result.confidence * 100).toFixed(0)}%</strong></span>
                  </div>
                </div>
              </div>

              <div style={{ padding: '30px' }}>
                {/* Executive Summary Section */}
                {result.data.narrative_summary ? (
                   <ExecutiveSummary summary={result.data.narrative_summary} />
                ) : (
                  <div style={{ padding: '20px', background: '#f0fdf4', borderLeft: '4px solid #10b981', marginBottom: '20px', color: '#374151' }}>
                    {result.summary}
                  </div>
                )}

                {/* Structured Data Grid */}
                <h4 style={{ fontSize: '1rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '15px' }}>Key Metrics & Data</h4>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
                  gap: '15px',
                  marginBottom: '30px'
                }}>
                  {Object.entries(result.data)
                    .filter(([key]) => !['narrative_summary', 'confidence_score', 'key_sources', '_raw_search_results'].includes(key))
                    .map(([key, value]) => (
                      <div
                        key={key}
                        style={{
                          padding: '15px',
                          background: '#f8fafc',
                          borderRadius: '8px',
                          border: '1px solid #f1f5f9'
                        }}
                      >
                        <div style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '5px', textTransform: 'capitalize' }}>
                          {key.replace(/_/g, ' ')}
                        </div>
                        <div style={{ fontSize: '1.1rem', color: '#0f172a', fontWeight: '600' }}>
                           {Array.isArray(value)
                             ? value.join(", ")
                             : (typeof value === 'object' ? JSON.stringify(value).slice(0, 30) + '...' : String(value))}
                        </div>
                      </div>
                  ))}
                </div>

                {/* Sources Section */}
                <SourceList sources={result.data._raw_search_results || result.data.key_sources} />

              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
};

export default ResultsDisplay;

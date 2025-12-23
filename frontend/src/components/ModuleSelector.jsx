import { motion } from 'framer-motion';
import { Check } from 'lucide-react';

const ModuleSelector = ({ modules, selectedModules, onToggle }) => {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const item = {
    hidden: { y: 20, opacity: 0 },
    show: { y: 0, opacity: 1 },
  };

  return (
    <div style={{ padding: '20px' }}>
      <motion.h2
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        style={{
          fontSize: '1.8rem',
          marginBottom: '20px',
          color: '#fff',
          textAlign: 'center',
        }}
      >
        Select Research Modules
      </motion.h2>

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '15px',
        }}
      >
        {modules.map((module) => {
          const isSelected = selectedModules.includes(module.id);
          
          return (
            <motion.div
              key={module.id}
              variants={item}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onToggle(module.id)}
              className="glass-card"
              style={{
                padding: '20px',
                cursor: 'pointer',
                position: 'relative',
                border: isSelected ? `2px solid ${module.color}` : '1px solid rgba(255, 255, 255, 0.3)',
                transition: 'all 0.3s ease',
              }}
            >
              {isSelected && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  style={{
                    position: 'absolute',
                    top: '10px',
                    right: '10px',
                    background: module.color,
                    borderRadius: '50%',
                    width: '30px',
                    height: '30px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <Check size={20} color="#fff" />
                </motion.div>
              )}

              <div style={{ fontSize: '2.5rem', marginBottom: '10px' }}>
                {module.icon}
              </div>

              <h3
                style={{
                  fontSize: '1.2rem',
                  marginBottom: '8px',
                  color: module.color,
                  fontWeight: 'bold',
                }}
              >
                {module.name}
              </h3>

              <p
                style={{
                  fontSize: '0.9rem',
                  color: '#666',
                  lineHeight: '1.4',
                }}
              >
                {module.description}
              </p>

              <div style={{ marginTop: '10px', fontSize: '0.8rem', color: '#999' }}>
                {module.fields.length} data points
              </div>
            </motion.div>
          );
        })}
      </motion.div>
    </div>
  );
};

export default ModuleSelector;

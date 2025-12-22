import { motion } from 'framer-motion';
import { Sparkles, Brain, TrendingUp } from 'lucide-react';

const Header = () => {
  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="glass"
      style={{
        padding: '20px 40px',
        margin: '20px',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '15px' }}>
        <motion.div
          animate={{
            rotate: [0, 360],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Brain size={40} color="#fff" />
        </motion.div>
        
        <h1
          className="gradient-text"
          style={{
            fontSize: '2.5rem',
            fontWeight: 'bold',
            margin: 0,
          }}
        >
          Configurable Researcher Agent
        </h1>
        
        <motion.div
          animate={{
            y: [0, -10, 0],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Sparkles size={32} color="#fbbf24" />
        </motion.div>
      </div>
      
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        style={{
          textAlign: 'center',
          color: 'rgba(255, 255, 255, 0.9)',
          marginTop: '10px',
          fontSize: '1.1rem',
        }}
      >
        AI-Powered Multi-Dimensional Research Platform
      </motion.p>

      {/* Animated particles */}
      <motion.div
        style={{
          position: 'absolute',
          top: '20%',
          left: '10%',
          width: '10px',
          height: '10px',
          background: 'rgba(255, 255, 255, 0.5)',
          borderRadius: '50%',
        }}
        animate={{
          y: [0, -20, 0],
          opacity: [0.5, 1, 0.5],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      <motion.div
        style={{
          position: 'absolute',
          top: '60%',
          right: '15%',
          width: '8px',
          height: '8px',
          background: 'rgba(255, 255, 255, 0.4)',
          borderRadius: '50%',
        }}
        animate={{
          y: [0, 20, 0],
          opacity: [0.4, 0.8, 0.4],
        }}
        transition={{
          duration: 2.5,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 0.5,
        }}
      />
    </motion.header>
  );
};

export default Header;

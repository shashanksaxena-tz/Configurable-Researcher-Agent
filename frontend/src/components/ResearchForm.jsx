import { motion } from 'framer-motion';

const ResearchForm = ({ onSubmit, loading }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    onSubmit({
      entity_name: formData.get('entity_name'),
      entity_type: formData.get('entity_type'),
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card"
      style={{
        padding: '30px',
        margin: '20px',
        maxWidth: '600px',
        marginLeft: 'auto',
        marginRight: 'auto',
      }}
    >
      <h2
        style={{
          fontSize: '1.5rem',
          marginBottom: '20px',
          color: '#333',
          textAlign: 'center',
        }}
      >
        Enter Research Target
      </h2>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div>
          <label
            htmlFor="entity_name"
            style={{
              display: 'block',
              marginBottom: '8px',
              color: '#555',
              fontWeight: '500',
            }}
          >
            Name
          </label>
          <input
            type="text"
            id="entity_name"
            name="entity_name"
            required
            placeholder="Enter person or company name"
            style={{
              width: '100%',
              padding: '12px',
              border: '2px solid #e0e0e0',
              borderRadius: '8px',
              fontSize: '1rem',
              transition: 'border 0.3s ease',
            }}
            onFocus={(e) => (e.target.style.borderColor = '#667eea')}
            onBlur={(e) => (e.target.style.borderColor = '#e0e0e0')}
          />
        </div>

        <div>
          <label
            htmlFor="entity_type"
            style={{
              display: 'block',
              marginBottom: '8px',
              color: '#555',
              fontWeight: '500',
            }}
          >
            Type
          </label>
          <select
            id="entity_type"
            name="entity_type"
            required
            style={{
              width: '100%',
              padding: '12px',
              border: '2px solid #e0e0e0',
              borderRadius: '8px',
              fontSize: '1rem',
              backgroundColor: '#fff',
              cursor: 'pointer',
            }}
          >
            <option value="company">Company</option>
            <option value="individual">Individual</option>
          </select>
        </div>

        <motion.button
          type="submit"
          disabled={loading}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          style={{
            padding: '15px',
            background: loading
              ? '#ccc'
              : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1.1rem',
            fontWeight: 'bold',
            cursor: loading ? 'not-allowed' : 'pointer',
            marginTop: '10px',
          }}
        >
          {loading ? 'Researching...' : 'Start Research'}
        </motion.button>
      </form>
    </motion.div>
  );
};

export default ResearchForm;

import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Quote } from 'lucide-react';

const ExecutiveSummary = ({ summary }) => {
  if (!summary) return null;

  return (
    <div style={{
      marginBottom: '30px',
      padding: '30px',
      background: 'white',
      borderRadius: '8px',
      boxShadow: '0 4px 20px rgba(0,0,0,0.05)',
      borderLeft: '4px solid #10b981'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
        <Quote size={24} color="#10b981" style={{ opacity: 0.8 }} />
        <h3 style={{
          fontSize: '1.4rem',
          fontFamily: '"Merriweather", serif',
          color: '#1f2937',
          margin: 0
        }}>
          Executive Summary
        </h3>
      </div>

      <div className="prose prose-lg" style={{
        color: '#374151',
        lineHeight: '1.8',
        fontSize: '1.05rem',
        fontFamily: '"Georgia", serif'
      }}>
        <ReactMarkdown>{summary}</ReactMarkdown>
      </div>
    </div>
  );
};

export default ExecutiveSummary;

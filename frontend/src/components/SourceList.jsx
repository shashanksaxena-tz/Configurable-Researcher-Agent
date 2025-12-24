import React from 'react';
import { ExternalLink, Link2 } from 'lucide-react';

const SourceList = ({ sources }) => {
  if (!sources || sources.length === 0) return null;

  return (
    <div style={{
      marginTop: '20px',
      padding: '20px',
      background: '#f9fafb',
      borderRadius: '8px',
      border: '1px solid #e5e7eb'
    }}>
      <h4 style={{
        fontSize: '0.9rem',
        textTransform: 'uppercase',
        letterSpacing: '0.05em',
        color: '#6b7280',
        marginBottom: '15px',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}>
        <Link2 size={16} />
        Verified Sources
      </h4>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
        {sources.map((source, index) => {
          // Handle various source formats (URL string or object)
          const url = typeof source === 'string' ? source : source.url;
          const title = typeof source === 'string' ? new URL(source).hostname : (source.title || new URL(source.url).hostname);

          if (!url) return null;

          return (
            <a
              key={index}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 12px',
                background: 'white',
                border: '1px solid #d1d5db',
                borderRadius: '20px',
                color: '#4b5563',
                fontSize: '0.8rem',
                textDecoration: 'none',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#10b981';
                e.currentTarget.style.color = '#10b981';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = '#d1d5db';
                e.currentTarget.style.color = '#4b5563';
              }}
            >
              <ExternalLink size={12} />
              {title}
            </a>
          );
        })}
      </div>
    </div>
  );
};

export default SourceList;

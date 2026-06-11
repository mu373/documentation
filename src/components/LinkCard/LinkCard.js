import React from 'react';
import Link from '@docusaurus/Link';

import styles from './LinkCard.module.css';

function getDomain(href) {
  try {
    return new URL(href).hostname.replace(/^www\./, '');
  } catch {
    return '';
  }
}

export default function LinkCard({
  href,
  title,
  description,
  favicon = true,
  faviconSrc,
}) {
  const domain = getDomain(href);
  const faviconUrl =
    typeof favicon === 'string'
      ? favicon
      : faviconSrc || `https://www.google.com/s2/favicons?domain=${encodeURIComponent(domain || href)}&sz=32`;
  const showDescription = description !== false && description != null && description !== '';

  return (
    <Link className={styles.card} to={href} target="_blank" rel="noopener noreferrer">
      <span className={styles.title}>{title || domain || href}</span>
      {showDescription && <span className={styles.description}>{description}</span>}
      <span className={styles.origin}>
        {favicon !== false && (
          <img className={styles.favicon} src={faviconUrl} alt="" width="14" height="14" />
        )}
        <span className={styles.domain}>{domain || href}</span>
      </span>
    </Link>
  );
}

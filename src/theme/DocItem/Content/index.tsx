import React, {type ReactNode} from 'react';
import clsx from 'clsx';
import {ThemeClassNames} from '@docusaurus/theme-common';
import {useDoc} from '@docusaurus/plugin-content-docs/client';
import Heading from '@theme/Heading';
import MDXContent from '@theme/MDXContent';
import type {Props} from '@theme/DocItem/Content';

import styles from './styles.module.scss';

/**
 Title can be declared inside md content or declared through
 front matter and added manually. To make both cases consistent,
 the added title is added under the same div.markdown block
 See https://github.com/facebook/docusaurus/pull/4882#issuecomment-853021120

 We render a "synthetic title" if:
 - user doesn't ask to hide it with front matter
 - the markdown content does not already contain a top-level h1 heading
*/
function useSyntheticTitle(): string | null {
  const {metadata, frontMatter, contentTitle} = useDoc();

  const hasCustomTitle = frontMatter.custom_title && frontMatter.custom_title.trim() !== '';

  if (frontMatter.hide_title) {
    // If there is no content title and no custom title, return null
    return null;
  }

  if (hasCustomTitle) {
    // If "custom_title" is provided in front matter, use it
    // This precedes the "title"
    return frontMatter.custom_title;
  } else if ( frontMatter.title && frontMatter.title.trim() !== '' ) {
    // If a title is provided in front matter, use it
    return frontMatter.title;
  } else {
    return contentTitle
  }
}

function stringify(value: any): string {
  if (typeof value === 'string') {
    return value;
  } else if (typeof value === 'number') {
    return value.toString();
  } else if (Array.isArray(value)) {
    return value.map(stringify).join(', ');
  } else if (value instanceof Date) {
    return value.toISOString().split('T')[0]; // Format as YYYY-MM-DD
  } else if (value && typeof value === 'object') {
    return JSON.stringify(value, null, 2);
  }
  return '';
}

export function DocItemContentHeader(): ReactNode {
  const syntheticTitle = useSyntheticTitle();
  const {metadata, frontMatter, contentTitle} = useDoc();

  const notebookLanguage = frontMatter.language
  const lastUpdatedAt = metadata.lastUpdatedAt 
  const header = frontMatter.header;

  return (
    <header className={clsx(styles.docItemContentHeader)}>
      { syntheticTitle && ( <Heading as="h1">{syntheticTitle}</Heading> ) }
      {notebookLanguage || lastUpdatedAt || header && (
      <div className={clsx(styles.metadata)}>
        <ul>
          {notebookLanguage && (<li>Language coded: {notebookLanguage}</li>) }
          {lastUpdatedAt && (<li>Last updated: {lastUpdatedAt}</li>) }
          {header && Object.entries(header).map(([key, value]) => (
            <li>{key}: {stringify(value)}</li>
          ))}
        </ul>
      </div>
      )}
    </header>
  );
}

export default function DocItemContent({children}: Props): ReactNode {
  return (
    <div className={clsx(ThemeClassNames.docs.docMarkdown, 'markdown')}>
      <DocItemContentHeader></DocItemContentHeader>
      <MDXContent>{children}</MDXContent>
    </div>
  );
}

import React from 'react';
// Import the original mapper
import MDXComponents from '@theme-original/MDXComponents';

// For rendering Markdown from nbdocs
import CodeOutputBlock from '@site/src/components/CodeOutputBlock/CodeOutputBlock.js';
import HTMLOutputBlock from '@site/src/components/HTMLOutputBlock/HTMLOutputBlock.js';

export default {
  ...MDXComponents,
  CodeOutputBlock,
  HTMLOutputBlock
};
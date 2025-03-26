import React from 'react';
import { isValidElement } from "react";
import Head from "@docusaurus/Head";
import Link from "@docusaurus/Link";
import CodeBlock from "@theme/CodeBlock";
import CodeBlockContainer from "@theme/CodeBlock/Container";
import Heading from "@theme/Heading";
import Details from "@theme/Details";
import CodeOutputBlock from '@site/src/components/CodeOutputBlock/CodeOutputBlock.js';
import CodeOutputImageBlock from '@site/src/components/CodeOutputImageBlock/CodeOutputImageBlock.js';
import HTMLOutputBlock from '@site/src/components/HTMLOutputBlock/HTMLOutputBlock.js';

const MDXComponents = {
  head: (props) => <Head {...props} />,
  
  code: (props) => {

    // If it's inline code (no newlines), render as code
    if (typeof props.children === 'string' && !props.children.includes('\n')) {
      return <code {...props} />;
    }
    
    // Otherwise render as CodeBlock
    // return <CodeBlock {...props} />;
    return <CodeBlock {...props} />;
  },
  
  pre: (props) => {
    // // Handle code-output class
    // if (props.className === 'code-output') {
    //   const content = props.children?.props?.children;
    //   if (typeof content === 'string' && content.includes('![png]')) {
    //     const imgMatch = content.match(/!\[png\]\((.*?)\)/);
    //     if (imgMatch) {
    //       return <img src={imgMatch[1]} alt="output" />;
    //     }
    //   }
    //   return <pre {...props} />;
    // }

    // Handle empty codeblocks or codeblocks with language
    if (isValidElement(props.children)) {
      // If it has a language class
      if (props.children.props.className?.includes('language-')) {
        const { className, children } = props.children.props;
        return <CodeBlock language={className.replace('language-', '')}>{children}</CodeBlock>;
      }
    }
    
    return <pre {...props} />;
  },
  
  // その他のコンポーネント
  a: (props) => <Link {...props} />,
  h1: (props) => <Heading as="h1" {...props} />,
  h2: (props) => <Heading as="h2" {...props} />,
  h3: (props) => <Heading as="h3" {...props} />,
  h4: (props) => <Heading as="h4" {...props} />,
  h5: (props) => <Heading as="h5" {...props} />,
  h6: (props) => <Heading as="h6" {...props} />,
  Details: (props) => {
    let summaryContent = null;
    // 子要素を配列に変換
    const childrenArray = React.Children.toArray(props.children);
    // <summary> タグを検出して内容を取り出し、他の子要素からは除外する
    const childrenWithoutSummary = childrenArray.filter(child => {
      if (isValidElement(child) && child.type === 'summary') {
        summaryContent = child.props.children;
        return false;
      }
      return true;
    });
  
    return <Details summary={summaryContent} {...props}>{childrenWithoutSummary}</Details>;
  },
  
  CodeOutputBlock,
  CodeOutputImageBlock,
  HTMLOutputBlock,
};

export default MDXComponents;
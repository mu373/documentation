import React from 'react';
import styles from "./CodeOutputBlock.module.css";

const CodeOutputBlock = ({ children, lang }) => {
  
  // 最も深い要素のテキストコンテンツを抽出
  const extractDeepestContent = (element) => {
    if (typeof element === 'string') {
      return element.replace(/^```.*\n|```$/g, '').trim();
    }

    if (React.isValidElement(element)) {
      if (element.props.className === 'token-line') {
        return element.props.children.map(child => 
          typeof child === 'string' ? child : child.props?.children || ''
        ).join('');
      }
      
      const childContent = React.Children.map(element.props.children, child => 
        extractDeepestContent(child)
      );
      return childContent ? childContent.join('') : '';
    }

    if (Array.isArray(element)) {
      return element.map(extractDeepestContent).join('');
    }

    return '';
  };

  const content = children;
  
  // 画像マークダウンの場合は jupyter-output-image でラップした img 要素を返す
  // const imageElement = checkForImage(content);
  // if (imageElement) {
  //   return imageElement;
  // }

  // その他のコンテンツは pre/code でラップ
  return (
    <div className={styles['jupyter-output']}>
    <pre className={styles['jupyter-output-code']}>
      <code className={lang ? `language-${lang}` : ''}>
        {extractDeepestContent(content)}
      </code>
    </pre>
    </div>
  );
};

export default CodeOutputBlock;
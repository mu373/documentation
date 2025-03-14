import React from 'react';

const CodeOutputImageBlock = ({ children, lang }) => {
  
  const content = children;

  // Extract the image URL from the content
  const imageUrl = content.props.children.props.src
  
  return (
    <div className="jupyter-output-image">
      <img src={imageUrl} alt="output plot" width="50%"/>
    </div>
  );
};

export default CodeOutputImageBlock;
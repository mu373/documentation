import React from 'react';

const CodeOutputImageBlock = ({ children }) => {
  
  const content = children;

  // Extract the image URL from the content
  const imageUrl = content.props.children.props.src
  let imageClass = ""

  if (imageUrl.endsWith('.svg')) {
    imageClass += "svg "
  }
  
  return (
    <div className="jupyter-output-image">
      <img src={imageUrl} className={imageClass} alt="output plot"/>
    </div>
  );
};

export default CodeOutputImageBlock;
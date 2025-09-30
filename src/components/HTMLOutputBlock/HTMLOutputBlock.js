import React from "react";
import styles from "./HTMLOutputBlock.module.css";
import Helmet from "react-helmet";

/**
 * Renders HTML within MDX
 *
 * Include the HTML code within a block so that the MDX parser ignores it and doesn't give errors.
 * This will work with a single <script> tag and will execute the code within. BE CAREFUL!
 *
 * Attributes:
 *
 * center: centers the output horizontally
 *
 * Usage:
 * <HTMLOutputBlock>
 *
 * ```
 * <strong>bad</strong>
 * ```
 *
 * </HTMLOutputBlock
 *
 */
export const HTMLOutputBlock = ({ children, center = false }) => {
  console.log("center: ", center);
  const html = children.props.children.props.children;

  const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
  const matches = Array.from(html.matchAll(scriptRegex));

  // Extract script tags with src attribute
  const srcScriptRegex = /<script[^>]*src=["']([^"']+)["'][^>]*><\/script>/gi;
  const srcMatches = Array.from(html.matchAll(srcScriptRegex));
  
  // Extract inline scripts (without src)
  const inlineScriptRegex = /<script[^>]*(?!src=)>([\s\S]*?)<\/script>/gi;
  const inlineMatches = Array.from(html.matchAll(inlineScriptRegex));

  
  return (
    <>
      <div
        className={styles.wrapper + (center ? " " + styles.center : "")}
        dangerouslySetInnerHTML={{ __html: html }}
      />
      {(inlineMatches.length > 0 || srcMatches.length > 0) && (
        <Helmet>
          {inlineMatches.map((m, idx) => (
            <script key={`inline-${idx}`}>{m[1]}</script>
          ))}
          {srcMatches.map((m, idx) => (
            <script key={`src-${idx}`} src={m[1]}></script>
          ))}
        </Helmet>
      )}
    </>
  );
};

export default HTMLOutputBlock;

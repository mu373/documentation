import React from "react";
import styles from "./HTMLOutputBlock.module.css";
import Helmet from "react-helmet";
import VideoJSPlayer from "../VideoJSPlayer/VideoJSPlayer";

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
function extractAttribute(tag, name) {
  const doubleQuoted = tag.match(new RegExp(`${name}="([^"]*)"`, "i"));
  if (doubleQuoted) {
    return doubleQuoted[1];
  }

  const singleQuoted = tag.match(new RegExp(`${name}='([^']*)'`, "i"));
  if (singleQuoted) {
    return singleQuoted[1];
  }

  const unquoted = tag.match(new RegExp(`${name}=([^\\s>]+)`, "i"));
  if (unquoted) {
    return unquoted[1];
  }

  return "";
}

function hasBooleanAttribute(tag, name) {
  return new RegExp(`(^|\\s)${name}(\\s|>|=)`, "i").test(tag);
}

function extractVideo(html) {
  const videoMatch = html.match(/<video\b([^>]*)>([\s\S]*?)<\/video>/i);
  if (!videoMatch) {
    return null;
  }

  const videoAttributes = videoMatch[1];
  const videoBody = videoMatch[2];
  const sourceMatch = videoBody.match(/<source\b([^>]*)>/i);
  const sourceAttributes = sourceMatch ? sourceMatch[1] : "";
  const src = extractAttribute(sourceAttributes, "src") || extractAttribute(videoAttributes, "src");

  if (!src) {
    return null;
  }

  return {
    src,
    type: extractAttribute(sourceAttributes, "type") || "video/mp4",
    className: extractAttribute(videoAttributes, "class"),
    autoplay: hasBooleanAttribute(videoAttributes, "autoplay"),
    muted: hasBooleanAttribute(videoAttributes, "muted"),
    loop: hasBooleanAttribute(videoAttributes, "loop"),
  };
}

export const HTMLOutputBlock = ({ children, center = false }) => {
  const html = children.props.children.props.children;
  const video = extractVideo(html);

  const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
  const matches = Array.from(html.matchAll(scriptRegex));

  // Extract script tags with src attribute
  const srcScriptRegex = /<script[^>]*src=["']([^"']+)["'][^>]*><\/script>/gi;
  const srcMatches = Array.from(html.matchAll(srcScriptRegex));
  
  // Extract inline scripts (without src)
  const inlineScriptRegex = /<script[^>]*(?!src=)>([\s\S]*?)<\/script>/gi;
  const inlineMatches = Array.from(html.matchAll(inlineScriptRegex));

  if (video) {
    return (
      <div className={styles.videoWrapper + (center ? " " + styles.center : "")}>
        <VideoJSPlayer {...video} />
      </div>
    );
  }
  
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

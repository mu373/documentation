import React, { useEffect, useRef } from 'react';
import styles from './P5Sketch.module.css';

/**
 * Simple P5.js sketch component - optimized for Docusaurus
 * @param {Object} props - Component properties
 * @param {function} props.sketch - Sketch function that receives the P5 instance
 * @param {number} props.width - Canvas width (default: 600)
 * @param {number} props.height - Canvas height (default: 400)
 * @param {string} props.containerWidth - Container width ('100%' or '500px', etc. default: '100%')
 * @param {Object} props.params - Additional parameters to pass to the sketch function
 * @returns {JSX.Element} div that displays the P5 animation
 */

export function P5Sketch({
  sketch = defaultSketch,
  width = 1000,
  height = 600,
  containerWidth = '100%',
  params = {}
}) {
  const containerRef = useRef(null);
  const p5InstanceRef = useRef(null);
  
  // Process containerWidth - convert number to px
  const processedWidth = typeof containerWidth === 'number' 
    ? `${containerWidth}px` 
    : containerWidth;
    
  useEffect(() => {
    // Execute only on client-side
    if (typeof window === 'undefined') return;
    // Execute only once when the component mounts
    let p5Instance = null;
    
    const initP5 = async () => {
      try {
        // Import P5.js
        const p5Module = await import('p5');
        const p5 = p5Module.default;
        
        // Function to initialize the sketch
        const p5Sketch = (p) => {
          // Wrap the original sketch and provide new setup and draw
          const originalSketch = sketch(p, { width, height, ...params });
          const originalSetup = originalSketch.setup || (() => {});
          const originalDraw = originalSketch.draw || (() => {});
          
          // Save other event handlers
          const eventHandlers = {};
          const events = [
            'mousePressed', 'mouseReleased', 'mouseMoved', 'mouseDragged', 'mouseClicked',
            'doubleClicked', 'mouseWheel', 'keyPressed', 'keyReleased', 'keyTyped',
            'touchStarted', 'touchMoved', 'touchEnded', 'windowResized'
          ];
          
          events.forEach(event => {
            if (originalSketch[event]) {
              eventHandlers[event] = originalSketch[event];
              p[event] = originalSketch[event];
            }
          });
          
          // Define setup function
          p.setup = () => {
            // Create canvas and add to container
            const canvas = p.createCanvas(width, height);
            
            if (containerRef.current) {
              canvas.parent(containerRef.current);
              
              // Set canvas CSS to width: 100%
              const canvasElement = canvas.elt;
              if (canvasElement) {
                canvasElement.style.width = '100%';
                canvasElement.style.height = 'auto';
              }
            }
            
            // Execute original setup function
            originalSetup();
          };
          
          // Define draw function
          p.draw = () => {
            originalDraw();
          };
        };
        
        // Create P5 instance
        p5Instance = new p5(p5Sketch);
        p5InstanceRef.current = p5Instance;
        
      } catch (error) {
        console.error('Failed to initialize P5:', error);
      }
    };
    
    initP5();
    
    // Cleanup function
    return () => {
      if (p5InstanceRef.current) {
        p5InstanceRef.current.remove();
        p5InstanceRef.current = null;
      }
    };
  }, [sketch, width, height, params]); // Update dependency array to reinitialize when properties change
  
  return (
    <div 
      ref={containerRef} 
      className={styles['p5-container']}
    />
  );
}

// Default sketch implementation
function defaultSketch(p, props) {
  return {
    setup() {
      // Note: Canvas creation is handled by the component, so don't create it here
      p.background(220);
    },
    
    draw() {
      p.background(220);
      p.fill(0, 102, 153);
      p.textSize(24);
      p.textAlign(p.CENTER, p.CENTER);
      p.text('P5.js Sketch', props.width/2, props.height/2 - 20);
      
      p.fill(255, 102, 0);
      p.noStroke();
      const size = 50 + p.sin(p.frameCount * 0.05) * 15;
      p.ellipse(props.width/2, props.height/2 + 30, size, size);
    }
  };
}
import React, {useEffect, useRef} from 'react';
import clsx from 'clsx';
import 'video.js/dist/video-js.css';

import styles from './VideoJSPlayer.module.css';

export default function VideoJSPlayer({
  src,
  type = 'video/mp4',
  className = '',
  autoplay = false,
  muted = false,
  loop = false,
}) {
  const videoRef = useRef(null);
  const playerRef = useRef(null);
  const isRetina = className.split(/\s+/).includes('retina');
  const isRetinaHalf = className.split(/\s+/).includes('retina-half');

  useEffect(() => {
    let disposed = false;

    async function setupPlayer() {
      const videojs = (await import('video.js')).default;

      if (disposed || !videoRef.current || playerRef.current) {
        return;
      }

      playerRef.current = videojs(videoRef.current, {
        autoplay,
        controls: true,
        fluid: true,
        loop,
        muted,
        preload: 'auto',
        responsive: true,
        sources: [{src, type}],
        controlBar: {
          pictureInPictureToggle: false,
        },
      });
    }

    setupPlayer();

    return () => {
      disposed = true;
      if (playerRef.current && !playerRef.current.isDisposed()) {
        playerRef.current.dispose();
        playerRef.current = null;
      }
    };
  }, [autoplay, loop, muted, src, type]);

  return (
    <div className={clsx(styles.player, isRetina && styles.retina, isRetinaHalf && styles.retinaHalf)}>
      <div data-vjs-player>
        <video ref={videoRef} className="video-js vjs-big-play-centered" playsInline />
      </div>
    </div>
  );
}

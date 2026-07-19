'use client';

import { useEffect, useRef, useState } from 'react';

interface ScrollSequenceProps {
  progress: number; // 0.0 to 1.0
  frameCount: number;
  basePath?: string; // Directory containing the frames, defaults to "/frames"
  imagePrefix?: string; // Prefix for the image files, defaults to "ezgif-frame-"
}

export function ScrollSequence({ progress, frameCount, basePath = "/frames", imagePrefix = "ezgif-frame-" }: ScrollSequenceProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [images, setImages] = useState<HTMLImageElement[]>([]);
  const [loadedCount, setLoadedCount] = useState(0);

  // Preload images
  useEffect(() => {
    const loadedImages: HTMLImageElement[] = [];
    let loaded = 0;
    setLoadedCount(0);

    for (let i = 1; i <= frameCount; i++) {
      const img = new Image();
      // Format number to 3 digits, e.g., 001, 002...
      const frameIndex = i.toString().padStart(3, '0');
      img.src = `${basePath}/${imagePrefix}${frameIndex}.jpg`;
      
      img.onload = () => {
        loaded++;
        setLoadedCount(loaded);
      };
      
      loadedImages.push(img);
    }
    setImages(loadedImages);
  }, [frameCount, basePath]);

  // Draw current frame to canvas
  useEffect(() => {
    if (images.length === 0 || !canvasRef.current) return;
    
    // Ensure we don't try to render an image that hasn't loaded yet
    if (loadedCount < frameCount * 0.1) return; // Wait until at least 10% are loaded to start rendering to avoid flashes

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Calculate current frame index based on progress
    // Progress 0.0 = Frame 0, Progress 1.0 = Frame 79
    const frameIndex = Math.min(
      Math.floor(progress * frameCount),
      frameCount - 1
    );

    const img = images[frameIndex];
    if (!img || !img.complete) return;

    // Maintain aspect ratio while filling canvas (object-fit: cover equivalent)
    const canvasRatio = canvas.width / canvas.height;
    const imgRatio = img.width / img.height;
    
    let renderWidth, renderHeight, xOffset, yOffset;
    
    if (canvasRatio > imgRatio) {
      renderWidth = canvas.width;
      renderHeight = canvas.width / imgRatio;
      xOffset = 0;
      yOffset = (canvas.height - renderHeight) / 2;
    } else {
      renderWidth = canvas.height * imgRatio;
      renderHeight = canvas.height;
      xOffset = (canvas.width - renderWidth) / 2;
      yOffset = 0;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(img, xOffset, yOffset, renderWidth, renderHeight);

  }, [progress, images, loadedCount, frameCount]);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      if (canvasRef.current) {
        // High DPI support
        const dpr = window.devicePixelRatio || 1;
        canvasRef.current.width = window.innerWidth * dpr;
        canvasRef.current.height = window.innerHeight * dpr;
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="relative w-full h-full overflow-hidden bg-[#0a0a0a]">
      <canvas
        ref={canvasRef}
        className="w-full h-full object-cover"
        style={{ width: '100vw', height: '100vh', transform: 'scale(1.02)' }}
      />
      {/* Optional: Minimal loading indicator if connection is slow */}
      {loadedCount < frameCount * 0.5 && (
        <div className="absolute inset-0 flex items-center justify-center bg-black z-50 transition-opacity duration-1000" style={{ opacity: loadedCount > 0 ? 1 - (loadedCount / (frameCount * 0.5)) : 1 }}>
          <div className="text-[#E1D4C0] text-[10px] tracking-widest opacity-50">
            LOADING ASSETS [{Math.round((loadedCount / frameCount) * 100)}%]
          </div>
        </div>
      )}
    </div>
  );
}

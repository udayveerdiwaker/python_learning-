import React, { useEffect } from 'react'
import { X, ChevronLeft, ChevronRight, Download } from 'lucide-react'

export default function ImageLightbox({ images, currentIndex, isOpen, onClose, onPrev, onNext }) {
  
  // Close on Esc, navigate on Left/Right keys
  useEffect(() => {
    if (!isOpen) return

    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 'ArrowLeft') onPrev()
      if (e.key === 'ArrowRight') onNext()
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, onClose, onPrev, onNext])

  if (!isOpen || !images || images.length === 0) return null

  const activeImage = images[currentIndex]

  return (
    <div className="lightbox-overlay" onClick={onClose}>
      {/* Close button */}
      <button className="lightbox-btn lightbox-close" onClick={onClose} aria-label="Close Lightbox">
        <X size={24} />
      </button>

      {/* Navigation - Left */}
      {images.length > 1 && (
        <button 
          className="lightbox-btn lightbox-nav-left" 
          onClick={(e) => { e.stopPropagation(); onPrev(); }}
          aria-label="Previous Image"
        >
          <ChevronLeft size={28} />
        </button>
      )}

      {/* Main Image View */}
      <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>
        <img 
          src={activeImage} 
          alt={`Active view ${currentIndex + 1}`} 
          className="lightbox-img" 
        />
        
        {/* Caption bar */}
        <div className="lightbox-caption">
          <span>Image {currentIndex + 1} of {images.length}</span>
          <a 
            href={activeImage} 
            download 
            target="_blank" 
            rel="noopener noreferrer" 
            className="lightbox-download-link"
            title="Open original in new tab"
          >
            <Download size={14} />
            <span>Open Original</span>
          </a>
        </div>
      </div>

      {/* Navigation - Right */}
      {images.length > 1 && (
        <button 
          className="lightbox-btn lightbox-nav-right" 
          onClick={(e) => { e.stopPropagation(); onNext(); }}
          aria-label="Next Image"
        >
          <ChevronRight size={28} />
        </button>
      )}
    </div>
  )
}

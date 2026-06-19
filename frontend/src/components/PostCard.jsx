import React, { useState } from 'react'
import { User, Calendar, Heart, Clock } from 'lucide-react'

export default function PostCard({ post, onLike, isLiked }) {
  const [likeAnimating, setLikeAnimating] = useState(false)

  // Format the ISO timestamp nicely
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch (e) {
      return dateString
    }
  }

  // Calculate estimated read time
  const getReadTime = (text) => {
    if (!text) return '1 min read'
    const wordsPerMinute = 200
    const words = text.trim().split(/\s+/).length
    const minutes = Math.ceil(words / wordsPerMinute)
    return `${minutes} min read`
  }

  const handleLikeClick = () => {
    setLikeAnimating(true)
    onLike(post.id)
    setTimeout(() => setLikeAnimating(false), 300)
  }

  // Cover image fallback hierarchy
  const coverImage = post.medium_cover_image || post.large_cover_image || post.small_cover_image

  // Define badge class dynamically based on category
  const badgeClass = `badge badge-${(post.category || 'General').toLowerCase()}`

  return (
    <article className="glass-panel post-card" style={{ padding: coverImage ? '0 0 1.5rem 0' : '2rem', display: 'flex', flexDirection: 'column' }}>
      {coverImage && (
        <div className="post-image-wrapper" style={{ margin: 0, width: '100%', height: '220px' }}>
          <img 
            src={coverImage} 
            alt={post.title} 
            className="post-image" 
            loading="lazy"
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>
      )}
      
      <div style={{ padding: coverImage ? '1.25rem 1.5rem 0 1.5rem' : 0, display: 'flex', flexDirection: 'column', flex: 1 }}>
        <div className="post-header">
          <h3 className="post-title" style={{ fontSize: '1.15rem', fontWeight: '700' }}>{post.title}</h3>
          <span className={badgeClass}>{post.category || 'General'}</span>
        </div>
        
        <p className="post-content" style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>
          {post.content}
        </p>

        {/* Screenshots gallery */}
        {post.screenshots && post.screenshots.length > 0 && (
          <div style={{ display: 'flex', gap: '0.35rem', marginTop: '1rem', overflowX: 'auto', paddingBottom: '0.25rem' }}>
            {post.screenshots.map((src, i) => (
              <a 
                key={i} 
                href={src} 
                target="_blank" 
                rel="noopener noreferrer" 
                style={{ flexShrink: 0 }}
              >
                <img 
                  src={src} 
                  alt={`Screenshot ${i + 1}`}
                  style={{ 
                    width: '70px', 
                    height: '46px', 
                    objectFit: 'cover', 
                    borderRadius: '0.25rem', 
                    border: '1px solid rgba(255,255,255,0.08)',
                    transition: 'all 0.2s'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.borderColor = '#c084fc'
                    e.currentTarget.style.opacity = '0.8'
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'
                    e.currentTarget.style.opacity = '1'
                  }}
                />
              </a>
            ))}
          </div>
        )}
        
        <div className="post-meta" style={{ marginTop: '1.25rem', borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '0.75rem' }}>
          <span className="meta-item">
            <User size={13} />
            <span>{post.author}</span>
          </span>
          
          <span className="meta-item">
            <Calendar size={13} />
            <span>{formatDate(post.created_at)}</span>
          </span>

          <span className="meta-item" style={{ marginLeft: '0.25rem' }}>
            <Clock size={12} />
            <span>{getReadTime(post.content)}</span>
          </span>
          
          <button 
            onClick={handleLikeClick}
            className={`like-button ${isLiked ? 'liked' : ''} ${likeAnimating ? 'pop' : ''}`}
            title={isLiked ? 'Liked' : 'Like this post'}
          >
            <Heart size={14} fill={isLiked ? '#ef4444' : 'none'} />
            <span>{post.likes || 0}</span>
          </button>
        </div>
      </div>
    </article>
  )
}

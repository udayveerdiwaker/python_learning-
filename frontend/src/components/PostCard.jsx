import React, { useState } from 'react'
import { User, Calendar, Heart, Clock, MessageSquare, Trash2, Send, Loader2, Bookmark } from 'lucide-react'

export default function PostCard({ 
  post, 
  onLike, 
  onDelete, 
  isLiked, 
  isBookmarked, 
  onBookmark, 
  onOpenLightbox, 
  token 
}) {
  const [likeAnimating, setLikeAnimating] = useState(false)
  const [showComments, setShowComments] = useState(false)
  const [comments, setComments] = useState([])
  const [loadingComments, setLoadingComments] = useState(false)
  const [commentAuthor, setCommentAuthor] = useState('')
  const [commentContent, setCommentContent] = useState('')
  const [submittingComment, setSubmittingComment] = useState(false)

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

  const fetchComments = async () => {
    setLoadingComments(true)
    try {
      const response = await fetch(`/v1/api/posts/${post.id}/comments`)
      if (response.ok) {
        const data = await response.json()
        setComments(data)
      }
    } catch (e) {
      console.error("Error loading comments:", e)
    } finally {
      setLoadingComments(false)
    }
  }

  const handleToggleComments = () => {
    const nextShow = !showComments
    setShowComments(nextShow)
    if (nextShow) {
      fetchComments()
    }
  }

  const handleCommentSubmit = async (e) => {
    e.preventDefault()
    if (!commentAuthor.trim() || !commentContent.trim()) return

    setSubmittingComment(true)
    try {
      const response = await fetch(`/v1/api/posts/${post.id}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          author: commentAuthor.trim(),
          content: commentContent.trim()
        })
      })

      if (response.status === 401) {
        alert("Unauthorized: Invalid session token. Please update/generate your security session key on the Dashboard.")
        return
      }

      if (response.ok) {
        const newComment = await response.json()
        setComments((prev) => [...prev, newComment])
        setCommentContent('')
        post.comment_count = (post.comment_count || 0) + 1
      } else {
        alert("Failed to submit comment. Please verify the backend is running.")
      }
    } catch (err) {
      console.error(err)
      alert("Error submitting comment.")
    } finally {
      setSubmittingComment(false)
    }
  }

  // Cover image fallback hierarchy
  const coverImage = post.medium_cover_image || post.large_cover_image || post.small_cover_image

  // Define badge class dynamically based on category
  const badgeClass = `badge badge-${(post.category || 'General').toLowerCase()}`

  // Gather all unique images for lightbox zoom
  const getAllImages = () => {
    const allImages = []
    if (post.large_cover_image) allImages.push(post.large_cover_image)
    if (post.medium_cover_image && !allImages.includes(post.medium_cover_image)) allImages.push(post.medium_cover_image)
    if (post.small_cover_image && !allImages.includes(post.small_cover_image)) allImages.push(post.small_cover_image)
    
    let screenshotUrls = []
    try {
      if (post.screenshots) {
        screenshotUrls = typeof post.screenshots === 'string' 
          ? JSON.parse(post.screenshots) 
          : post.screenshots
      }
    } catch (e) {}
    
    screenshotUrls.forEach(url => {
      if (url && !allImages.includes(url)) allImages.push(url)
    })
    return allImages
  }

  const handleOpenImage = (clickedUrl) => {
    if (!onOpenLightbox) return
    const images = getAllImages()
    const startIdx = images.indexOf(clickedUrl)
    onOpenLightbox(images, startIdx >= 0 ? startIdx : 0)
  }

  return (
    <article className="glass-panel post-card" style={{ padding: coverImage ? '0 0 1.5rem 0' : '2rem', display: 'flex', flexDirection: 'column' }}>
      {coverImage && (
        <div 
          className="post-image-wrapper" 
          style={{ margin: 0, width: '100%', height: '220px', cursor: 'zoom-in' }}
          onClick={() => handleOpenImage(coverImage)}
        >
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
              <div 
                key={i} 
                style={{ flexShrink: 0, cursor: 'zoom-in' }}
                onClick={() => handleOpenImage(src)}
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
              </div>
            ))}
          </div>
        )}
        
        {/* Post Metadata, Like, Comment Toggle, and Delete */}
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
          
          <div style={{ display: 'flex', gap: '0.35rem', alignItems: 'center', marginLeft: 'auto' }}>
            {/* Like button */}
            <button 
              onClick={handleLikeClick}
              className={`like-button ${isLiked ? 'liked' : ''} ${likeAnimating ? 'pop' : ''}`}
              title={isLiked ? 'Liked' : 'Like this post'}
            >
              <Heart size={14} fill={isLiked ? '#ef4444' : 'none'} />
              <span>{post.likes || 0}</span>
            </button>

            {/* Bookmark button */}
            <button 
              onClick={() => onBookmark(post.id)}
              className={`like-button ${isBookmarked ? 'liked' : ''}`}
              style={{ color: isBookmarked ? '#f59e0b' : 'var(--text-muted)' }}
              title={isBookmarked ? 'Bookmarked' : 'Bookmark this post'}
            >
              <Bookmark size={14} fill={isBookmarked ? '#f59e0b' : 'none'} />
            </button>

            {/* Comment toggler */}
            <button 
              onClick={handleToggleComments}
              className={`like-button ${showComments ? 'liked' : ''}`}
              style={{ color: showComments ? '#c084fc' : 'var(--text-muted)' }}
              title="View comments"
            >
              <MessageSquare size={14} fill={showComments ? 'rgba(192, 132, 252, 0.15)' : 'none'} />
              <span>{post.comment_count || 0}</span>
            </button>

            {/* Delete button (authenticated) */}
            {onDelete && (
              <button 
                onClick={() => onDelete(post.id)}
                className="btn-delete-post"
                title="Delete this post"
              >
                <Trash2 size={14} />
              </button>
            )}
          </div>
        </div>

        {/* Collapsible Comments Section */}
        {showComments && (
          <div className="comments-section">
            <h4 className="comments-title">
              <MessageSquare size={14} />
              <span>Discussion ({comments.length})</span>
            </h4>

            {loadingComments ? (
              <div style={{ display: 'flex', justifyContent: 'center', padding: '1rem' }}>
                <Loader2 className="spinner" size={18} />
              </div>
            ) : (
              <div className="comments-list">
                {comments.length === 0 ? (
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textAlign: 'center', padding: '0.5rem 0' }}>
                    No comments yet. Be the first to start the conversation!
                  </p>
                ) : (
                  comments.map((comment) => (
                    <div key={comment.id} className="comment-item">
                      <div className="comment-header">
                        <span className="comment-author">{comment.author}</span>
                        <span className="comment-date">{formatDate(comment.created_at)}</span>
                      </div>
                      <p className="comment-body">{comment.content}</p>
                    </div>
                  ))
                )}
              </div>
            )}

            {/* Add Comment Form */}
            <form onSubmit={handleCommentSubmit} className="comment-form">
              <div className="comment-form-row">
                <input 
                  type="text" 
                  placeholder="Your Name"
                  className="form-input comment-input-author"
                  value={commentAuthor}
                  onChange={(e) => setCommentAuthor(e.target.value)}
                  disabled={submittingComment}
                  maxLength={50}
                  required
                />
                <input 
                  type="text" 
                  placeholder="Add a comment..."
                  className="form-input comment-input-content"
                  value={commentContent}
                  onChange={(e) => setCommentContent(e.target.value)}
                  disabled={submittingComment}
                  required
                />
                <button 
                  type="submit" 
                  className="btn btn-primary btn-comment-submit"
                  disabled={!commentAuthor.trim() || !commentContent.trim() || submittingComment}
                >
                  {submittingComment ? <Loader2 size={12} className="spinner" /> : <Send size={12} />}
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </article>
  )
}

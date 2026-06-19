import React, { useState } from 'react'
import { PenSquare, Send, Loader2 } from 'lucide-react'

const CATEGORIES = ['General', 'Tech', 'Idea', 'Life']

export default function PostForm({ onSubmit, isSubmitting }) {
  const [title, setTitle] = useState('')
  const [author, setAuthor] = useState('')
  const [content, setContent] = useState('')
  const [category, setCategory] = useState('General')
  const [coverUrl, setCoverUrl] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!title.trim() || !author.trim() || !content.trim()) return
    
    onSubmit({
      title: title.trim(),
      author: author.trim(),
      content: content.trim(),
      category,
      medium_cover_image: coverUrl.trim() || null,
      large_cover_image: coverUrl.trim() || null,
      small_cover_image: coverUrl.trim() || null
    }, () => {
      // Clear form on success
      setTitle('')
      setAuthor('')
      setContent('')
      setCategory('General')
      setCoverUrl('')
    })
  }

  const isValid = title.trim() && author.trim() && content.trim()

  return (
    <div className="glass-panel">
      <h2 className="section-title">
        <PenSquare size={22} />
        <span>Create Post</span>
      </h2>
      
      <form onSubmit={handleSubmit}>
        {/* Author */}
        <div className="form-group">
          <label htmlFor="author">Author Name</label>
          <input
            id="author"
            type="text"
            className="form-input"
            placeholder="Your name or handle"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            disabled={isSubmitting}
            maxLength={50}
            required
          />
        </div>

        {/* Title */}
        <div className="form-group">
          <label htmlFor="title">Post Title</label>
          <input
            id="title"
            type="text"
            className="form-input"
            placeholder="Give your post a catchy title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            disabled={isSubmitting}
            maxLength={100}
            required
          />
        </div>

        {/* Content */}
        <div className="form-group">
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            className="form-textarea"
            placeholder="What's on your mind?"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            disabled={isSubmitting}
            required
          />
        </div>

        {/* Cover Image URL */}
        <div className="form-group">
          <label htmlFor="coverUrl">Cover Image URL (Optional)</label>
          <input
            id="coverUrl"
            type="url"
            className="form-input"
            placeholder="https://... (or blank for random seed cover)"
            value={coverUrl}
            onChange={(e) => setCoverUrl(e.target.value)}
            disabled={isSubmitting}
          />
        </div>

        {/* Category */}
        <div className="form-group">
          <label>Category</label>
          <div className="category-picker">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                type="button"
                className={`category-pill ${category === cat ? 'selected' : ''}`}
                data-category={cat}
                onClick={() => setCategory(cat)}
                disabled={isSubmitting}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={!isValid || isSubmitting}
          style={{ marginTop: '0.7rem' }}
        >
          {isSubmitting ? (
            <>
              <Loader2 className="spinner" size={18} style={{ width: 18, height: 18 }} />
              <span>Publishing...</span>
            </>
          ) : (
            <>
              <Send size={18} />
              <span>Publish Post</span>
            </>
          )}
        </button>
      </form>
    </div>
  )
}

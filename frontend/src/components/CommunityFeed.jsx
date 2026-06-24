import React, { useEffect } from 'react'
import { Search, MessageSquare, RefreshCw, FileText, ChevronLeft, ChevronRight, AlertCircle, Heart, Bookmark } from 'lucide-react'
import PostCard from './PostCard'

export default function CommunityFeed({ 
  posts, 
  onLike, 
  onDelete, 
  likedPosts, 
  bookmarkedPosts,
  onBookmark,
  onOpenLightbox,
  token,
  loading, 
  error, 
  onRefresh,
  currentPage,
  setCurrentPage,
  totalPages,
  searchQuery,
  setSearchQuery,
  selectedFilter,
  setSelectedFilter
}) {
  
  // Scroll to top of feed when page changes
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [currentPage])

  // Local client-side filtering for user Bookmarks and Likes
  const displayedPosts = selectedFilter === 'Liked'
    ? posts.filter((post) => likedPosts.has(post.id))
    : selectedFilter === 'Bookmarked'
      ? posts.filter((post) => bookmarkedPosts.has(post.id))
      : posts

  // Generate page numbers range helper with ellipsis
  const getPageNumbers = () => {
    const pages = []
    
    if (totalPages <= 7) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1) // Always show first page
      
      if (currentPage > 3) {
        pages.push('...')
      }
      
      let start = Math.max(2, currentPage - 1)
      let end = Math.min(totalPages - 1, currentPage + 1)
      
      if (currentPage <= 3) {
        end = 4
      } else if (currentPage >= totalPages - 2) {
        start = totalPages - 3
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      if (currentPage < totalPages - 2) {
        pages.push('...')
      }
      
      pages.push(totalPages) // Always show last page
    }
    
    return pages
  }

  const CATEGORIES = ['All', 'General', 'Tech', 'Idea', 'Life', 'Liked', 'Bookmarked']

  return (
    <div className="community-feed-view">
      {/* Search and Filters panel */}
      <div className="feed-controls">
        {/* Search */}
        <div className="search-wrapper">
          <Search size={18} className="search-icon" />
          <input
            type="text"
            className="form-input search-input"
            placeholder="Search 10,000+ posts by title, author, or content..."
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value)
              setCurrentPage(1) // reset page on search
            }}
          />
        </div>

        {/* Filter Pills */}
        <div className="filter-pills">
          <span className="filter-pills-label">Category:</span>
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => {
                setSelectedFilter(cat)
                setCurrentPage(1) // reset page on filter change
              }}
              className={`filter-pill ${selectedFilter === cat ? 'active' : ''}`}
              data-category={cat}
              style={(cat === 'Liked' || cat === 'Bookmarked') ? { display: 'inline-flex', alignItems: 'center', gap: '0.35rem' } : {}}
            >
              {cat === 'Liked' && (
                <Heart 
                  size={12} 
                  fill={selectedFilter === 'Liked' ? '#ef4444' : 'none'} 
                  color={selectedFilter === 'Liked' ? '#ef4444' : 'currentColor'} 
                />
              )}
              {cat === 'Bookmarked' && (
                <Bookmark 
                  size={12} 
                  fill={selectedFilter === 'Bookmarked' ? '#f59e0b' : 'none'} 
                  color={selectedFilter === 'Bookmarked' ? '#f59e0b' : 'currentColor'} 
                />
              )}
              <span>
                {cat === 'Liked' ? 'My Likes' : cat === 'Bookmarked' ? 'Bookmarks' : cat}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Title & Refresh */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
        <h2 className="section-title" style={{ margin: 0 }}>
          <MessageSquare size={22} />
          <span>Community Feed</span>
        </h2>
        
        <button 
          onClick={onRefresh} 
          className="btn" 
          style={{ width: 'auto', padding: '0.5rem 1rem', background: 'rgba(255,255,255,0.05)', fontSize: '0.85rem' }}
          disabled={loading}
          title="Refresh feed"
        >
          <RefreshCw size={14} className={loading ? 'spinner' : ''} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Feed list */}
      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading database feed...</p>
        </div>
      ) : displayedPosts.length === 0 ? (
        <div className="empty-state">
          <FileText size={48} />
          <h3>No posts matched</h3>
          <p>Try resetting filters, searching something else, or creating a new post!</p>
        </div>
      ) : (
        <>
          <div className="feed-container">
            {displayedPosts.map((post) => (
              <PostCard 
                key={post.id} 
                post={post} 
                onLike={onLike}
                onDelete={onDelete}
                isLiked={likedPosts.has(post.id)}
                isBookmarked={bookmarkedPosts.has(post.id)}
                onBookmark={onBookmark}
                onOpenLightbox={onOpenLightbox}
                token={token}
              />
            ))}
          </div>

          {/* Numbered Pagination controls */}
          {selectedFilter !== 'Liked' && selectedFilter !== 'Bookmarked' && totalPages > 1 && (
            <div className="pagination-bar">
              <button 
                className="pagination-btn"
                disabled={currentPage === 1}
                onClick={() => setCurrentPage((prev) => prev - 1)}
                title="Previous Page"
              >
                <ChevronLeft size={16} />
              </button>
              
              {getPageNumbers().map((pageNum, idx) => (
                pageNum === '...' ? (
                  <span key={`ellipsis-${idx}`} className="pagination-ellipsis">&bull;&bull;&bull;</span>
                ) : (
                  <button
                    key={`page-${pageNum}`}
                    className={`pagination-btn ${currentPage === pageNum ? 'active' : ''}`}
                    onClick={() => setCurrentPage(pageNum)}
                  >
                    {pageNum}
                  </button>
                )
              ))}
              
              <button 
                className="pagination-btn"
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage((prev) => prev + 1)}
                title="Next Page"
              >
                <ChevronRight size={16} />
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

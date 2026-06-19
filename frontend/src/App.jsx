import React, { useState, useEffect } from 'react'
import { 
  FileText, 
  Heart, 
  Users, 
  Key, 
  ShieldAlert, 
  CheckCircle2, 
  Home, 
  MessageSquare,
  Code,
  Copy
} from 'lucide-react'
import PostForm from './components/PostForm'
import CommunityFeed from './components/CommunityFeed'

export default function App() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [toastMessage, setToastMessage] = useState(null)

  // Navigation tab state
  const [activeTab, setActiveTab] = useState('home')

  // Auth/Token State
  const [token, setToken] = useState(() => {
    return localStorage.getItem('api_token') || 'demo-secret-key-2026'
  })
  const [isTokenValid, setIsTokenValid] = useState(true)
  const [authError, setAuthError] = useState(null)

  // Code Snippet state toggle
  const [activeSnippet, setActiveSnippet] = useState('get')

  // Liked Posts local state tracker
  const [likedPosts, setLikedPosts] = useState(() => {
    try {
      const stored = localStorage.getItem('liked_posts')
      return stored ? new Set(JSON.parse(stored)) : new Set()
    } catch {
      return new Set()
    }
  })

  // Fetch posts from API (public endpoint)
  const fetchPosts = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/v1/api/get_posts')
      if (!response.ok) {
        throw new Error('Failed to fetch posts. Please try again.')
      }
      const data = await response.json()
      setPosts(data)
    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  // Fetch on mount
  useEffect(() => {
    fetchPosts()
  }, [])

  // Sync liked posts to local storage
  useEffect(() => {
    localStorage.setItem('liked_posts', JSON.stringify(Array.from(likedPosts)))
  }, [likedPosts])

  // Generate new random API token from backend
  const handleGenerateToken = async () => {
    setAuthError(null)
    try {
      const response = await fetch('/api/auth/token')
      if (!response.ok) {
        throw new Error('Failed to generate token from API.')
      }
      const data = await response.json()
      setToken(data.token)
      localStorage.setItem('api_token', data.token)
      setIsTokenValid(true)
      showToast('New API Token Generated!')
    } catch (err) {
      setAuthError(err.message || 'Could not fetch token.')
    }
  }

  // Show Toast helper
  const showToast = (message) => {
    setToastMessage(message)
    setTimeout(() => {
      setToastMessage(null)
    }, 3000)
  }

  // Copy helper
  const copyToClipboard = (text, label) => {
    navigator.clipboard.writeText(text)
    showToast(`${label} copied to clipboard!`)
  }

  // Handle post creation (authenticated)
  const handleCreatePost = async (newPostData, onSuccess) => {
    setSubmitting(true)
    setError(null)
    setAuthError(null)
    try {
      const response = await fetch('/v1/api/create_posts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(newPostData),
      })
      
      if (response.status === 401) {
        setIsTokenValid(false)
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Unauthorized: Invalid token.')
      }

      if (!response.ok) {
        throw new Error('Failed to publish post. Please check inputs.')
      }
      
      const savedPost = await response.json()
      
      // Update local state
      setPosts((prevPosts) => [savedPost, ...prevPosts])
      setIsTokenValid(true)
      showToast('Post published successfully!')
      
      if (onSuccess) onSuccess()

      // Redirect user to the feed tab to see their new post
      setTimeout(() => setActiveTab('feed'), 800)
    } catch (err) {
      if (err.message.includes('Unauthorized') || err.message.includes('token')) {
        setAuthError(err.message)
      } else {
        setError(err.message || 'Could not save post.')
      }
    } finally {
      setSubmitting(false)
    }
  }

  // Handle post liking (authenticated)
  const handleLikePost = async (postId) => {
    setAuthError(null)
    
    const isAlreadyLiked = likedPosts.has(postId)
    if (isAlreadyLiked) {
      showToast('You already liked this post!')
      return
    }

    try {
      const response = await fetch(`/v1/api/like_post/${postId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.status === 401) {
        setIsTokenValid(false)
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Unauthorized: Invalid token.')
      }

      if (!response.ok) {
        throw new Error('Failed to record like.')
      }

      const updatedPost = await response.json()

      // Update posts array in state
      setPosts((prevPosts) => 
        prevPosts.map((p) => p.id === postId ? updatedPost : p)
      )

      // Add to liked set
      setLikedPosts((prev) => {
        const next = new Set(prev)
        next.add(postId)
        return next
      })

      setIsTokenValid(true)
    } catch (err) {
      if (err.message.includes('Unauthorized') || err.message.includes('token')) {
        setAuthError(err.message)
      } else {
        showToast('Error liking post.')
      }
    }
  }

  // Dashboard Stats Calculations
  const totalPosts = posts.length
  const totalLikes = posts.reduce((sum, p) => sum + (p.likes || 0), 0)
  const uniqueAuthors = new Set(posts.map((p) => p.author.trim().toLowerCase())).size

  // Javascript code snippets for developer integration
  const jsGetSnippet = `// Fetch community feed posts from your website
fetch('http://localhost:8000/v1/api/get_posts')
  .then(response => response.json())
  .then(posts => {
    console.log("Loaded " + posts.length + " posts!");
    // Render posts dynamically on your website
  })
  .catch(err => console.error("Error loading feed:", err));`

  const jsPostSnippet = `// Submit a new post from your external website
fetch('http://localhost:8000/v1/api/create_posts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ${token}'
  },
  body: JSON.stringify({
    title: 'Hello World from my site',
    content: 'This post was sent using the API Developer Hub!',
    author: 'External Developer',
    category: 'Tech'
  })
})
  .then(res => res.json())
  .then(newPost => console.log("Published post:", newPost))
  .catch(err => console.error("Authentication failed:", err));`

  return (
    <div className="app-container">
      {/* Background glow effects */}
      <div className="glow-bg">
        <div className="glow-circle glow-circle-1"></div>
        <div className="glow-circle glow-circle-2"></div>
      </div>

      {/* Header */}
      <header>
        <h1>Post &amp; Get Feed</h1>
        <p>A high-performance modern dashboard built with React and FastAPI</p>
      </header>

      {/* Navigation tabs */}
      <nav className="nav-tabs">
        <button 
          className={`nav-tab ${activeTab === 'home' ? 'active' : ''}`}
          onClick={() => setActiveTab('home')}
        >
          <Home size={16} />
          <span>Dashboard</span>
        </button>
        <button 
          className={`nav-tab ${activeTab === 'feed' ? 'active' : ''}`}
          onClick={() => setActiveTab('feed')}
        >
          <MessageSquare size={16} />
          <span>Community Feed</span>
        </button>
      </nav>

      {/* Stats Widgets */}
      <section className="stats-grid">
        <div className="glass-panel stat-card">
          <div className="stat-icon" style={{ color: '#c084fc' }}>
            <FileText size={24} />
          </div>
          <div className="stat-info">
            <span className="stat-value">{totalPosts}</span>
            <span className="stat-label">Total Posts</span>
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-icon" style={{ color: '#ef4444' }}>
            <Heart size={24} fill="#ef4444" style={{ opacity: 0.15 }} />
          </div>
          <div className="stat-info">
            <span className="stat-value">{totalLikes}</span>
            <span className="stat-label">Total Likes</span>
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-icon" style={{ color: '#60a5fa' }}>
            <Users size={24} />
          </div>
          <div className="stat-info">
            <span className="stat-value">{uniqueAuthors}</span>
            <span className="stat-label">Active Authors</span>
          </div>
        </div>
      </section>

      {/* Tab Switcher Content */}
      <main>
        {activeTab === 'home' ? (
          /* Dashboard Home view */
          <div className="dashboard-grid">
            <section>
              {/* Auth Panel / Security Session widget (preserved) */}
              <div className="glass-panel auth-panel">
                <div className="auth-header">
                  <h2 className="section-title" style={{ margin: 0, fontSize: '1.25rem' }}>
                    <Key size={18} />
                    <span>Security Session</span>
                  </h2>
                  <div className="auth-status">
                    <span className={`status-indicator ${isTokenValid ? 'status-active' : 'status-inactive'}`}></span>
                    <span style={{ color: isTokenValid ? '#10b981' : '#ef4444' }}>
                      {isTokenValid ? 'Active' : 'Invalid Session'}
                    </span>
                  </div>
                </div>

                {authError && (
                  <div className="error-message" style={{ fontSize: '0.85rem', padding: '0.75rem', marginBottom: '0.75rem' }}>
                    <ShieldAlert size={16} />
                    <span>{authError}</span>
                  </div>
                )}

                <div className="token-container">
                  <input
                    type="text"
                    className="form-input token-input"
                    value={token}
                    onChange={(e) => {
                      setToken(e.target.value)
                      localStorage.setItem('api_token', e.target.value)
                      setIsTokenValid(true)
                      setAuthError(null)
                    }}
                    placeholder="Enter API token key"
                  />
                  <button 
                    onClick={handleGenerateToken}
                    className="btn btn-primary"
                    style={{ width: 'auto', padding: '0.5rem 1rem', fontSize: '0.85rem' }}
                  >
                    Generate Key
                  </button>
                </div>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem', lineHeight: '1.4' }}>
                  A valid authorization token header is required to submit posts and likes to the database.
                </p>
              </div>

              {/* Developer API Integration Hub */}
              <div className="glass-panel dev-hub-panel">
                <h2 className="section-title" style={{ fontSize: '1.15rem' }}>
                  <Code size={18} />
                  <span>Developer API Hub</span>
                </h2>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                  Use this backend API directly in your own websites or applications. CORS is enabled globally.
                </p>

                {/* Developer Key Generator (synced in real-time) */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', background: 'rgba(255,255,255,0.02)', padding: '0.65rem 0.85rem', borderRadius: '0.5rem', border: '1px dashed var(--glass-border)' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Active API Key Token:</span>
                    <span style={{ fontSize: '0.8rem', fontFamily: 'monospace', color: '#c084fc', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '170px' }} title={token}>
                      {token}
                    </span>
                  </div>
                  <button 
                    onClick={handleGenerateToken}
                    className="btn btn-primary"
                    style={{ width: 'auto', padding: '0.4rem 0.85rem', fontSize: '0.75rem' }}
                  >
                    Generate API Key
                  </button>
                </div>

                {/* API Route Targets */}
                <div className="api-endpoint-card">
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span className="api-route-tag route-get">GET</span>
                    <button 
                      className="btn" 
                      style={{ width: 'auto', padding: '0.2rem 0.5rem', fontSize: '0.7rem', background: 'rgba(255,255,255,0.03)' }}
                      onClick={() => copyToClipboard('http://localhost:8000/v1/api/get_posts', 'API GET URL')}
                    >
                      <Copy size={11} />
                      <span>Copy URL</span>
                    </button>
                  </div>
                  <span className="api-route-url">http://localhost:8000/v1/api/get_posts</span>
                </div>

                <div className="api-endpoint-card">
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span className="api-route-tag route-post">POST</span>
                    <button 
                      className="btn" 
                      style={{ width: 'auto', padding: '0.2rem 0.5rem', fontSize: '0.7rem', background: 'rgba(255,255,255,0.03)' }}
                      onClick={() => copyToClipboard('http://localhost:8000/v1/api/create_posts', 'API POST URL')}
                    >
                      <Copy size={11} />
                      <span>Copy URL</span>
                    </button>
                  </div>
                  <span className="api-route-url">http://localhost:8000/v1/api/create_posts</span>
                </div>

                {/* Integration Code Switcher */}
                <div style={{ display: 'flex', gap: '0.35rem', marginTop: '1rem', borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.5rem' }}>
                  <button 
                    className={`filter-pill ${activeSnippet === 'get' ? 'active' : ''}`}
                    onClick={() => setActiveSnippet('get')}
                    style={{ fontSize: '0.75rem', padding: '0.25rem 0.65rem' }}
                  >
                    Fetch Feed JS
                  </button>
                  <button 
                    className={`filter-pill ${activeSnippet === 'post' ? 'active' : ''}`}
                    onClick={() => setActiveSnippet('post')}
                    style={{ fontSize: '0.75rem', padding: '0.25rem 0.65rem' }}
                  >
                    Submit Post JS
                  </button>
                </div>

                <div className="code-snippet-box">
                  <button 
                    className="btn-copy-code"
                    onClick={() => copyToClipboard(activeSnippet === 'get' ? jsGetSnippet : jsPostSnippet, 'Code snippet')}
                  >
                    <Copy size={12} />
                  </button>
                  {activeSnippet === 'get' ? jsGetSnippet : jsPostSnippet}
                </div>
              </div>
            </section>

            <section>
              {/* Form panel */}
              <PostForm onSubmit={handleCreatePost} isSubmitting={submitting} />
            </section>
          </div>
        ) : (
          /* Separate Community Feed view with Pagination */
          <CommunityFeed 
            posts={posts}
            onLike={handleLikePost}
            likedPosts={likedPosts}
            loading={loading}
            error={error}
            onRefresh={fetchPosts}
          />
        )}
      </main>

      {/* Toast Alert Notification */}
      {toastMessage && (
        <div className="toast">
          <CheckCircle2 size={18} color="#14b8a6" />
          <span>{toastMessage}</span>
        </div>
      )}
    </div>
  )
}

# Import FastAPI, HTTPException, HTMLResponse, and Pydantic
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Initialize the FastAPI application
app = FastAPI(title="User Manager Portal")

# A simple in-memory database (a list) to store user data temporarily
users = []

# Define the structure of the data we expect from the client (data validation)
class User(BaseModel):
    name: str   # The user's name must be a string
    email: str  # The user's email must be a string

# Root Endpoint: Serves a beautiful, interactive Single Page UI
@app.get("/", response_class=HTMLResponse)
def get_ui():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Manager Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            /* Premium Glassmorphic Dark UI */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Outfit', sans-serif;
            }
            body {
                background: radial-gradient(circle at top right, #1e1b4b, #0f172a);
                color: #f8fafc;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 2rem 1rem;
            }
            .header-container {
                text-align: center;
                margin-bottom: 2rem;
            }
            h1 {
                font-size: 2.5rem;
                font-weight: 700;
                background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            }
            .subtitle {
                color: #94a3b8;
                font-size: 1rem;
            }
            .container {
                width: 100%;
                max-width: 1000px;
                display: grid;
                grid-template-columns: 1fr 1.3fr;
                gap: 2rem;
            }
            @media (max-width: 768px) {
                .container {
                    grid-template-columns: 1fr;
                }
            }
            .card {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
                transition: border-color 0.3s ease, box-shadow 0.3s ease;
            }
            .card:hover {
                border-color: rgba(99, 102, 241, 0.25);
                box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.05);
            }
            h2 {
                font-size: 1.3rem;
                margin-bottom: 1.5rem;
                color: #f1f5f9;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                padding-bottom: 0.75rem;
            }
            .form-group {
                margin-bottom: 1.25rem;
            }
            label {
                display: block;
                font-size: 0.85rem;
                color: #94a3b8;
                margin-bottom: 0.5rem;
                font-weight: 500;
            }
            input {
                width: 100%;
                padding: 0.8rem 1rem;
                background: rgba(0, 0, 0, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                color: #fff;
                font-size: 0.95rem;
                transition: all 0.2s ease;
            }
            input:focus {
                outline: none;
                border-color: #6366f1;
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
                background: rgba(0, 0, 0, 0.35);
            }
            .btn {
                width: 100%;
                padding: 0.8rem 1rem;
                background: linear-gradient(135deg, #6366f1, #4f46e5);
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 0.95rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 0.5rem;
            }
            .btn:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            }
            .btn-secondary {
                background: rgba(255, 255, 255, 0.08);
                color: #e2e8f0;
                margin-top: 0.5rem;
            }
            .btn-secondary:hover {
                background: rgba(255, 255, 255, 0.15);
                box-shadow: none;
                transform: none;
            }
            .users-list {
                display: flex;
                flex-direction: column;
                gap: 1rem;
                max-height: 480px;
                overflow-y: auto;
                padding-right: 0.5rem;
            }
            .users-list::-webkit-scrollbar {
                width: 6px;
            }
            .users-list::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.1);
            }
            .users-list::-webkit-scrollbar-thumb {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 3px;
            }
            .user-item {
                background: rgba(255, 255, 255, 0.015);
                border: 1px solid rgba(255, 255, 255, 0.04);
                padding: 1.1rem;
                border-radius: 14px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: all 0.2s ease;
            }
            .user-item:hover {
                background: rgba(255, 255, 255, 0.04);
                border-color: rgba(255, 255, 255, 0.08);
                transform: translateX(2px);
            }
            .user-info h3 {
                font-size: 1.05rem;
                color: #f1f5f9;
                margin-bottom: 0.2rem;
            }
            .user-info p {
                font-size: 0.85rem;
                color: #64748b;
            }
            .user-actions {
                display: flex;
                gap: 0.4rem;
            }
            .action-btn {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.06);
                cursor: pointer;
                padding: 0.5rem;
                border-radius: 8px;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .action-btn.edit {
                color: #38bdf8;
            }
            .action-btn.edit:hover {
                background: rgba(56, 189, 248, 0.15);
                border-color: rgba(56, 189, 248, 0.3);
            }
            .action-btn.delete {
                color: #f87171;
            }
            .action-btn.delete:hover {
                background: rgba(248, 113, 113, 0.15);
                border-color: rgba(248, 113, 113, 0.3);
            }
            .empty-state {
                text-align: center;
                color: #64748b;
                padding: 3rem 0;
                font-style: italic;
            }
            .toast {
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                background: #10b981;
                color: white;
                font-weight: 500;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
                transform: translateY(150%);
                transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                z-index: 1000;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .toast.error {
                background: #ef4444;
            }
            .toast.show {
                transform: translateY(0);
            }
        </style>
    </head>
    <body>
        <div class="header-container">
            <h1>User Manager</h1>
            <p class="subtitle">Interactive Live FastAPI Sandbox Dashboard</p>
        </div>

        <div class="container">
            <!-- Left Side: Manage User Form -->
            <div class="card">
                <h2 id="form-title">➕ Add New User</h2>
                <form id="user-form">
                    <div class="form-group">
                        <label for="user-name">Full Name</label>
                        <input type="text" id="user-name" placeholder="John Doe" required>
                    </div>
                    <div class="form-group">
                        <label for="user-email">Email Address</label>
                        <input type="email" id="user-email" placeholder="john@example.com" required>
                    </div>
                    <button type="submit" class="btn" id="submit-btn">Add User</button>
                    <button type="button" class="btn btn-secondary" id="cancel-btn" style="display: none;">Cancel</button>
                </form>
            </div>

            <!-- Right Side: Live Directory List -->
            <div class="card">
                <h2>👥 User Directory (<span id="user-count">0</span>)</h2>
                <div class="users-list" id="users-list">
                    <div class="empty-state">No users registered yet.</div>
                </div>
            </div>
        </div>

        <!-- Toast Notifications -->
        <div class="toast" id="toast">Notification Message</div>

        <script>
            const userForm = document.getElementById('user-form');
            const submitBtn = document.getElementById('submit-btn');
            const cancelBtn = document.getElementById('cancel-btn');
            const formTitle = document.getElementById('form-title');
            const userNameInput = document.getElementById('user-name');
            const userEmailInput = document.getElementById('user-email');
            const usersList = document.getElementById('users-list');
            const userCount = document.getElementById('user-count');
            const toast = document.getElementById('toast');

            let editingEmail = null; // Track if we are in Edit Mode

            // Show Toast Alert Helper
            function showToast(message, isError = false) {
                toast.textContent = message;
                if (isError) {
                    toast.classList.add('error');
                } else {
                    toast.classList.remove('error');
                }
                toast.classList.add('show');
                setTimeout(() => {
                    toast.classList.remove('show');
                }, 3000);
            }

            // Fetch and render the users list
            async function fetchUsers() {
                try {
                    const response = await fetch('/users_read');
                    const users = await response.json();
                    
                    userCount.textContent = users.length;
                    
                    if (users.length === 0) {
                        usersList.innerHTML = '<div class="empty-state">No users registered yet.</div>';
                        return;
                    }
                    
                    usersList.innerHTML = users.map(user => `
                        <div class="user-item">
                            <div class="user-info">
                                <h3>${escapeHtml(user.name)}</h3>
                                <p>${escapeHtml(user.email)}</p>
                            </div>
                            <div class="user-actions">
                                <button class="action-btn edit" onclick="startEdit('${escapeHtml(user.name)}', '${escapeHtml(user.email)}')" title="Edit User">
                                    ✏️
                                </button>
                                <button class="action-btn delete" onclick="deleteUser('${escapeHtml(user.email)}')" title="Delete User">
                                    🗑️
                                </button>
                            </div>
                        </div>
                    `).join('');
                } catch (error) {
                    showToast('Failed to load users list.', true);
                }
            }

            // Simple HTML escape to prevent XSS
            function escapeHtml(str) {
                return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
            }

            // Handle Form Submit (Create or Update)
            userForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const name = userNameInput.value.trim();
                const email = userEmailInput.value.trim();

                const userData = { name, email };

                try {
                    if (editingEmail) {
                        // PUT Request to Update User
                        const response = await fetch(`/users_update/${encodeURIComponent(editingEmail)}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(userData)
                        });

                        if (response.ok) {
                            showToast('User updated successfully!');
                            resetForm();
                            fetchUsers();
                        } else {
                            const err = await response.json();
                            showToast(err.detail || 'Failed to update user.', true);
                        }
                    } else {
                        // POST Request to Create User
                        const response = await fetch('/users_create', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(userData)
                        });

                        if (response.ok) {
                            showToast('User added successfully!');
                            userForm.reset();
                            fetchUsers();
                        } else {
                            showToast('Failed to create user.', true);
                        }
                    }
                } catch (error) {
                    showToast('An error occurred. Please try again.', true);
                }
            });

            // Enter Edit Mode
            window.startEdit = function(name, email) {
                editingEmail = email;
                userNameInput.value = name;
                userEmailInput.value = email;

                formTitle.textContent = '✏️ Edit User Details';
                submitBtn.textContent = 'Save Changes';
                cancelBtn.style.display = 'block';
                userNameInput.focus();
            };

            // Exit Edit Mode / Reset Form
            function resetForm() {
                editingEmail = null;
                userForm.reset();
                formTitle.textContent = '➕ Add New User';
                submitBtn.textContent = 'Add User';
                cancelBtn.style.display = 'none';
            }

            cancelBtn.addEventListener('click', resetForm);

            // Delete User (DELETE)
            window.deleteUser = async function(email) {
                if (!confirm(`Are you sure you want to delete user ${email}?`)) return;
                
                try {
                    const response = await fetch(`/users_delete/${encodeURIComponent(email)}`, {
                        method: 'DELETE'
                    });

                    if (response.ok) {
                        showToast('User deleted successfully.');
                        if (editingEmail === email) resetForm();
                        fetchUsers();
                    } else {
                        const err = await response.json();
                        showToast(err.detail || 'Failed to delete user.', true);
                    }
                } catch (error) {
                    showToast('An error occurred while deleting.', true);
                }
            };

            // Initial load
            fetchUsers();
        </script>
    </body>
    </html>
    """
    return html_content

# Endpoint to CREATE a new user (POST request)
@app.post("/users_create")
def create_user(user: User):
    # Convert the user data into a Python dictionary and add it to our list
    users.append(user.dict())
    # Return a success message back to the client
    return {"message": f"User created successfully name: {user.name}, email: {user.email}"}

# Endpoint to READ/GET all users (GET request)
@app.get("/users_read")
def get_users():
    # Return the list of all users we have saved so far
    return users

# Endpoint to UPDATE a user's details by their email (PUT request)
@app.put("/users_update/{email}")
def update_user(email: str, updated_user: User):
    for user in users:
        if user["email"] == email:
            user["name"] = updated_user.name
            user["email"] = updated_user.email
            return {"message": f"User with email {email} updated successfully"}
    # If user is not found, return a 404 error
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to DELETE a user by their email (DELETE request)
@app.delete("/users_delete/{email}")
def delete_user(email: str):
    for idx, user in enumerate(users):
        if user["email"] == email:
            users.pop(idx)
            return {"message": f"User with email {email} deleted successfully"}
    # If user is not found, return a 404 error
    raise HTTPException(status_code=404, detail="User not found")


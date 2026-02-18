# 🖥️ Medical Chatbot — Frontend

React + TypeScript frontend for the AI Medical Chatbot. Built with **Vite**, **Tailwind CSS**, **shadcn/ui**, and **Framer Motion** for a modern, Chat interface with full authentication support.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Directory Structure](#-directory-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Environment & Configuration](#-environment--configuration)
- [Running the App](#-running-the-app)
- [Pages & Routes](#-pages--routes)
- [Components Overview](#-components-overview)
- [Authentication](#-authentication)
- [API Service Layer](#-api-service-layer)
- [Theming](#-theming)


---

## ✨ Features

- 💬 **Real-time Chat Interface** — ChatGPT-inspired layout with sidebar and message thread
- 🗂️ **Conversation Sidebar** — Browse, select, and delete past conversations
- 📝 **Markdown Rendering** — AI responses rendered with full markdown support
- 🔐 **Full Auth Flow** — Login, Register, Email Verification, Forgot/Reset Password
- 🌗 **Dark / Light Mode** — System-aware with manual toggle (`next-themes`)
- ✨ **Smooth Animations** — Page transitions and micro-animations via Framer Motion
- 📱 **Responsive Design** — Collapsible sidebar, works on all screen sizes
- 🔔 **Toast Notifications** — Non-intrusive feedback via Sonner
- 🧩 **Component Library** — Built on shadcn/ui (Radix UI primitives)

---

## 🛠️ Tech Stack

| Category | Library / Tool |
|---|---|
| Framework | React 19 + TypeScript |
| Build Tool | Vite 7 |
| Styling | Tailwind CSS 3 |
| UI Components | shadcn/ui (Radix UI) |
| Icons | Lucide React |
| Routing | React Router v7 |
| Animations | Framer Motion 12 |
| Markdown | react-markdown |
| Auth State | React Context API + JWT Decode |
| Notifications | Sonner |
| Theme | next-themes |

---

## 📁 Directory Structure

```
frontend/
├── index.html                  # HTML entry point
├── vite.config.ts              # Vite configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
├── components.json             # shadcn/ui configuration
├── package.json
└── src/
    ├── main.tsx                # React entry point
    ├── App.tsx                 # Root component with routing
    ├── index.css               # Global styles and CSS variables
    │
    ├── components/
    │   ├── auth/               # Authentication dialog components
    │   │   ├── LoginDialog.tsx
    │   │   ├── RegisterDialog.tsx
    │   │   └── ForgotPasswordDialog.tsx
    │   │
    │   ├── chat/               # Core chat UI components
    │   │   ├── ChatInterface.tsx   # Main chat window
    │   │   ├── ChatSidebar.tsx     # Conversation list sidebar
    │   │   ├── ChatMessage.tsx     # Individual message bubble
    │   │   ├── ChatInput.tsx       # Message input bar
    │   │   └── ModeToggle.tsx      # Dark/light mode toggle
    │   │
    │   ├── ui/                 # shadcn/ui component library
    │   │   ├── button.tsx
    │   │   ├── dialog.tsx
    │   │   ├── sidebar.tsx
    │   │   ├── avatar.tsx
    │   │   ├── dropdown-menu.tsx
    │   │   ├── scroll-area.tsx
    │   │   ├── tooltip.tsx
    │   │   ├── sonner.tsx
    │   │   └── ...
    │   │
    │   ├── motion-primitives/  # Framer Motion animation wrappers
    │   └── theme-provider.tsx  # next-themes ThemeProvider wrapper
    │
    ├── context/
    │   └── AuthContext.tsx     # Global auth state (user, token, login/logout)
    │
    ├── hooks/
    │   └── use-mobile.tsx      # Responsive breakpoint hook
    │
    ├── pages/
    │   ├── Login.tsx           # Standalone login page
    │   ├── Register.tsx        # Standalone register page
    │   ├── VerifyEmail.tsx     # Email verification landing page
    │   └── ResetPassword.tsx   # Password reset page
    │
    └── services/
        └── api.ts              # All API calls (typed, centralized)
```

---

## ✅ Prerequisites

- **Node.js 18+**
- **npm** (or yarn/pnpm)
- The **backend server** running at `http://localhost:8000`

---

## 📦 Installation

```bash
cd frontend
npm install
```

---

## ⚙️ Environment & Configuration

The frontend connects to the backend API. The base URL is configured in `src/services/api.ts`.

By default it points to `http://localhost:8000`. If your backend runs on a different port or host, update the `BASE_URL` constant in `src/services/api.ts`.

To use Vite environment variables, create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Then reference it in `api.ts` as `import.meta.env.VITE_API_BASE_URL`.

---

## ▶️ Running the App

```bash
npm run dev
```

The app will be available at **`http://localhost:5173`**

> Make sure the backend is running at `http://localhost:8000` before starting the frontend.

---

## 🗺️ Pages & Routes

| Route | Component | Description |
|---|---|---|
| `/` | `Dashboard` (in App.tsx) | Main chat interface with sidebar |
| `/verify-email` | `VerifyEmail` | Email verification landing page |
| `/reset-password` | `ResetPassword` | Password reset page |
| `*` | Redirect to `/` | Catch-all redirect |

---

## 🧩 Components Overview

### `App.tsx`
Root component that sets up:
- `ThemeProvider` (dark/light mode)
- `BrowserRouter` + `Routes`
- `AuthProvider` (global auth state)
- `Toaster` (toast notifications)

### `Dashboard` (in App.tsx)
The main application shell:
- `SidebarProvider` + `ChatSidebar` — collapsible conversation list
- `SidebarInset` — main content area with header and chat
- Header with mode toggle, user avatar dropdown (login/logout)
- `ChatInterface` — the active chat window

### `ChatInterface`
- Displays the message thread for the active conversation
- Handles sending messages to the backend `/chat` endpoint
- Shows loading states and error handling
- Triggers login dialog if user is not authenticated

### `ChatSidebar`
- Lists all conversations fetched from `/conversations`
- Supports creating new chats and deleting existing ones
- Highlights the currently active conversation

### `ChatMessage`
- Renders individual messages (user or assistant)
- Markdown rendering for AI responses (code blocks, lists, bold, etc.)
- Shows source documents and confidence indicators

### Auth Dialogs
- **`LoginDialog`** — Email/password login form with links to Register and Forgot Password
- **`RegisterDialog`** — Registration form (name, email, password)
- **`ForgotPasswordDialog`** — Email input to trigger password reset

---

## 🔐 Authentication

Authentication state is managed globally via `AuthContext` (`src/context/AuthContext.tsx`).

**Context provides:**
- `user` — current user object (`{ email, full_name }`)
- `isAuthenticated` — boolean
- `login(email, password)` — calls `/auth/login`, stores JWT in `localStorage`
- `logout()` — clears token and user state
- `register(data)` — calls `/auth/register`

**Token storage:** JWT is stored in `localStorage` as `access_token` and automatically included in all API requests via the `Authorization: Bearer <token>` header.

**Protected routes:** The chat endpoint requires authentication. If the user is not logged in, the `ChatInterface` shows a prompt to log in, which opens the `LoginDialog`.

**Email verification flow:**
1. User registers → backend sends verification email
2. User clicks link → redirected to `/verify-email?token=...&status=success`
3. `VerifyEmail` page shows success/error state and prompts login

**Password reset flow:**
1. User clicks "Forgot Password" → enters email → backend sends reset email
2. User clicks link → redirected to `/reset-password?token=...`
3. `ResetPassword` page shows new password form

---

## 🌐 API Service Layer

All backend communication is centralized in `src/services/api.ts`.

**Key functions:**

```typescript
// Authentication
api.login(email, password)           // POST /auth/login
api.register(data)                   // POST /auth/register
api.getMe()                          // GET /auth/me
api.forgotPassword(email)            // POST /auth/forgot-password
api.resetPassword(token, password)   // POST /auth/reset-password
api.verifyEmail(token)               // GET /auth/verify/{token}

// Chat
api.sendMessage(message, conversationId?)  // POST /chat
api.getChatHistory(sessionId?)             // GET /chat/history

// Conversations
api.getConversations()               // GET /conversations
api.getConversation(id)              // GET /conversations/{id}
api.deleteConversation(id)           // DELETE /conversations/{id}
```

**TypeScript types exported from `api.ts`:**
- `Conversation` — `{ id, title, created_at }`
- `Message` — `{ id, role, content, created_at }`
- `ChatResponse` — full chat response with sources, confidence, etc.

---

## 🎨 Theming

The app uses **Tailwind CSS** with CSS custom properties for theming, following the shadcn/ui convention.

**Theme variables** are defined in `src/index.css`:
- `--background`, `--foreground`
- `--primary`, `--secondary`, `--muted`, `--accent`
- `--card`, `--border`, `--input`, `--ring`
- Separate values for `:root` (light) and `.dark` (dark mode)

**Toggle:** The `ModeToggle` component in the header switches between light, dark, and system modes using `next-themes`.

---

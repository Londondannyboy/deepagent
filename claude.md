# Fractional Quest v2 - Deep Agents Build

## Project Overview

This is a greenfield rebuild of [fractional.quest](https://fractional.quest) using LangChain Deep Agents instead of Pydantic AI. The goal is to solve persistent context/state management issues in the current app.

**Why the rebuild:**
- Current Pydantic AI agent loses user context between messages
- State sync between frontend and agent is unreliable
- Page context is forgotten after the first message
- Dual-write pattern (Neon + ZEP) causes memory divergence

**What this project does:**
- Helps fractional executives (CTO, CFO, CMO, etc.) find fractional/interim roles
- Onboards users through a 6-step profile building process
- Searches jobs and matches them to user profiles
- Connects users with executive coaches

---

## Tech Stack

### Backend (Agent)
- **LangGraph** - State machine for agent execution
- **Deep Agents** - Planning, subagents, and filesystem middleware on top of LangGraph
- **CopilotKit** - AG-UI protocol for streaming to frontend
- **FastAPI** - HTTP server
- **OpenAI GPT-4o** - LLM
- **Neon** - PostgreSQL database (same as current app)
- **ZEP** - Knowledge graph/memory (optional, may simplify to Neon-only)

### Frontend
- **Next.js 14+** - App Router
- **CopilotKit React** - Chat UI, state sync, tool rendering
- **Hume EVI** - Voice integration
- **Tailwind CSS** - Styling
- **MDX** - Content pages (pulled from Neon)

### Infrastructure
- **Railway** - Agent deployment
- **Vercel** - Frontend deployment
- **Neon** - Database (shared with current app during transition)

---

## Architecture

### Agent Architecture (Orchestrator + Subagents)

```
┌─────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                    │
│  - Routes requests to appropriate subagent               │
│  - Maintains global state (user, page context)           │
│  - Has no tools of its own (delegates everything)        │
└─────────────────────┬───────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ ONBOARDING  │ │ JOB SEARCH  │ │  COACHING   │
│   AGENT     │ │   AGENT     │ │   AGENT     │
│             │ │             │ │             │
│ - 6 HITL    │ │ - search    │ │ - connect   │
│   tools     │ │ - match     │ │ - schedule  │
│ - Profile   │ │ - save      │ │ - context   │
│   building  │ │ - like      │ │   handoff   │
└─────────────┘ └─────────────┘ └─────────────┘
```

### State Flow

```
Frontend (useCoAgent)
    ↓ setState()
CopilotKit Runtime (/api/copilotkit)
    ↓ AG-UI Protocol
Deep Agents (LangGraph StateGraph)
    ↓ State updates flow through graph
Tool execution
    ↓ Returns state_snapshot
CopilotKitMiddleware
    ↓ Streams state back
Frontend (state auto-updates)
```

---

## Project Structure

```
deepagent/
├── claude.md                    # This file
├── docs/
│   ├── PRD.md                   # Product requirements
│   └── RESTART.md               # Quick restart prompt
│
├── agent/                       # Python backend
│   ├── main.py                  # FastAPI entrypoint
│   ├── state.py                 # Pydantic state models
│   ├── agents/
│   │   ├── orchestrator.py      # Main routing agent
│   │   ├── onboarding.py        # Onboarding subagent
│   │   ├── job_search.py        # Job search subagent
│   │   └── coaching.py          # Coaching subagent
│   ├── tools/
│   │   ├── onboarding.py        # confirm_* HITL tools
│   │   ├── jobs.py              # search, match, save tools
│   │   └── coaching.py          # connect, schedule tools
│   ├── persistence/
│   │   ├── neon.py              # Database client
│   │   └── zep.py               # ZEP client (if keeping)
│   ├── pyproject.toml           # UV dependencies
│   └── .env                     # API keys (not committed)
│
├── frontend/                    # Next.js app
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # CopilotKit provider
│   │   │   ├── page.tsx         # Home page
│   │   │   ├── api/
│   │   │   │   └── copilotkit/
│   │   │   │       └── route.ts # CopilotKit runtime
│   │   │   └── [...slug]/
│   │   │       └── page.tsx     # Dynamic content pages
│   │   ├── components/
│   │   │   ├── chat/            # Chat UI components
│   │   │   ├── tools/           # Tool renderers
│   │   │   └── content/         # MDX renderers
│   │   └── lib/
│   │       ├── neon.ts          # Database client
│   │       └── content.ts       # Content fetching
│   ├── package.json
│   └── .env.local               # Environment variables
│
└── shared/                      # Shared types (optional)
    └── types.ts
```

---

## Database Schema (Existing Neon Tables)

### user_profile_items
```sql
CREATE TABLE user_profile_items (
  id SERIAL PRIMARY KEY,
  user_id TEXT NOT NULL,
  item_type TEXT NOT NULL,  -- 'location', 'role_preference', 'trinity', etc.
  value TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',
  confirmed BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, item_type, value)
);
```

### content_pages (for MDX content)
```sql
CREATE TABLE content_pages (
  id SERIAL PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,           -- MDX content
  page_type TEXT,                  -- 'service', 'jobs', 'article'
  role_type TEXT,                  -- 'cto', 'cfo', 'cmo', etc.
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### jobs (job listings)
```sql
CREATE TABLE jobs (
  session_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  company TEXT NOT NULL,
  location TEXT,
  description TEXT,
  url TEXT,
  engagement_type TEXT,            -- 'fractional', 'interim', 'advisory'
  role_category TEXT,              -- 'cto', 'cfo', 'cmo', etc.
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Key Patterns

### 1. State Updates from Tools

Every tool should return a state snapshot so the frontend stays in sync:

```python
@tool
def confirm_location(location: str, ctx: Context) -> dict:
    # Validate and normalize
    normalized = normalize_location(location)

    # Update state
    ctx.state.onboarding.location = normalized
    ctx.state.onboarding.current_step = 5

    # Persist to Neon
    save_to_neon(ctx.state.user.id, "location", normalized)

    # Return includes state snapshot
    return {
        "success": True,
        "message": f"Location set to {normalized}",
        "state_snapshot": ctx.state.model_dump()
    }
```

### 2. Subagent Delegation

Orchestrator routes to subagents based on context:

```python
ORCHESTRATOR_PROMPT = """
## Routing Rules
1. If onboarding.completed=False → delegate to onboarding-agent
2. If user asks about jobs → delegate to job-search-agent
3. If user asks about coaching → delegate to coaching-agent
4. For general questions → answer directly
"""
```

### 3. Content from Neon

Content pages are stored in Neon and rendered dynamically:

```typescript
// frontend/src/app/[...slug]/page.tsx
export default async function ContentPage({ params }) {
  const page = await sql`
    SELECT * FROM content_pages WHERE slug = ${params.slug.join('/')}
  `;
  return <MDXRemote source={page.content} />;
}
```

### 4. CopilotKit Tool Rendering

Tool results render as React components in the chat:

```typescript
useRenderToolCall({
  name: 'search_jobs',
  render: ({ result, status }) => {
    if (status !== 'complete') return <Loading />;
    return result.jobs.map(job => <JobCard key={job.id} job={job} />);
  }
});
```

---

## Development Workflow

### Starting the Agent
```bash
cd agent
uv run python main.py
# Runs on http://localhost:8123
```

### Starting the Frontend
```bash
cd frontend
npm run dev
# Runs on http://localhost:3000
```

### Environment Variables

**Agent (.env):**
```
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
ZEP_API_KEY=z_...  # Optional
```

**Frontend (.env.local):**
```
AGENT_URL=http://localhost:8123
DATABASE_URL=postgresql://...  # For content fetching
```

---

## Validation Criteria

The rebuild is successful when:

1. **Context persists between messages** - User says "London" on message 3, agent remembers on message 5
2. **State syncs automatically** - Agent updates step, frontend shows new step immediately
3. **Page context maintained** - Navigate pages, agent knows which page you're on
4. **Reconnection works** - Close browser, reopen, state persists
5. **Neon persistence works** - Complete onboarding, all values in DB
6. **Subagent routing works** - Jobs question → job agent, coaching → coaching agent

---

## Current Status

**Phase:** Project Setup
**Next:** Build onboarding subagent with 6 HITL tools

---

## References

### LangChain Documentation (Primary)
- [Deep Agents Overview](https://docs.langchain.com/oss/python/deepagents/overview) - Main docs
- [Deep Agents Reference](https://reference.langchain.com/python/deepagents/) - API reference
- [LangChain Academy: Deep Agents](https://academy.langchain.com/courses/deep-agents-with-langgraph) - Course
- [Deep Agents Blog Post](https://www.blog.langchain.com/deep-agents/) - Architecture explanation
- [Multi-Agent Applications](https://www.blog.langchain.com/building-multi-agent-applications-with-deep-agents/) - Subagent patterns
- [Evaluating Deep Agents](https://www.blog.langchain.com/evaluating-deep-agents-our-learnings/) - Testing patterns

### CopilotKit
- [CopilotKit Deep Agents Integration](https://docs.copilotkit.ai/langgraph/deep-agents)
- [AG-UI Protocol](https://docs.ag-ui.com)

### Project Reference
- [Current fractional.quest codebase](/Users/dankeegan/fractional.quest)

### Key Deep Agents Features (from docs)
1. **write_todos** - Built-in planning tool for breaking down complex tasks
2. **Filesystem tools** - ls, read_file, write_file, edit_file for context management
3. **task tool** - Spawn specialized subagents for context isolation
4. **Store** - Persistent memory across threads via LangGraph's Store

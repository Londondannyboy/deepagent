# Restart Prompt for Claude Sessions

Copy and paste this when starting a new Claude Code session on this project.

---

## Quick Context Prompt

```
I'm working on `deepagent` - a greenfield rebuild of fractional.quest using LangChain Deep Agents (built on LangGraph) instead of Pydantic AI.

## Why the Rebuild
The current app (in /Users/dankeegan/fractional.quest) has critical issues:
- User context lost between messages (custom middleware timing issues)
- Frontend/agent state doesn't sync reliably
- Page context forgotten after first message
- 27 tools in one bloated agent with 1,500+ line system prompt

## The Solution
Deep Agents provides:
- Explicit state management through LangGraph
- CopilotKitMiddleware for automatic state sync
- Subagent delegation (orchestrator → onboarding/job-search/coaching agents)
- Built-in planning and filesystem context

## Current Status
[UPDATE THIS SECTION AS YOU PROGRESS]

Phase: Project Setup
- Created project structure
- Created documentation (claude.md, PRD.md)
- Next: Initialize agent backend with Deep Agents

## Tech Stack
- Backend: FastAPI + Deep Agents + LangGraph + OpenAI
- Frontend: Next.js + CopilotKit + Tailwind
- Database: Neon PostgreSQL (same as current app)
- Voice: Hume EVI (to be ported)

## Key Files to Read First
1. /Users/dankeegan/deepagent/claude.md - Full project context
2. /Users/dankeegan/deepagent/docs/PRD.md - Requirements
3. /Users/dankeegan/fractional.quest/agent/src/agent.py - Current agent (for reference)

## Immediate Next Steps
1. Set up agent/ with uv and Deep Agents dependencies
2. Create state.py with Pydantic models
3. Create orchestrator.py with basic routing
4. Create onboarding.py subagent with first HITL tool
5. Test with CopilotKit frontend

## Success Criteria
The rebuild works if:
1. Context persists between messages (no re-asking)
2. State syncs to frontend automatically
3. Page context maintained across navigation
4. Reconnection preserves state
5. All profile data persists to Neon

Please read claude.md first, then help me with the next step.
```

---

## Full Restart (Include if Context is Very Limited)

```
I'm rebuilding fractional.quest (a job platform for fractional executives) using LangChain Deep Agents.

Current app uses Pydantic AI but has critical bugs:
- Agent forgets user context between messages
- State doesn't sync between frontend and agent
- 27 tools crammed into one agent

The new architecture:
- Orchestrator agent routes to specialized subagents
- Onboarding subagent: 6-step profile building
- Job search subagent: finding and matching jobs
- Coaching subagent: connecting with coaches

Stack: Deep Agents (LangGraph) + CopilotKit + Next.js + Neon PostgreSQL

Project is at /Users/dankeegan/deepagent
Reference codebase at /Users/dankeegan/fractional.quest

Read /Users/dankeegan/deepagent/claude.md for full context.
```

---

## Quick Status Update Template

After each session, update this section:

### Session Log

| Date | What Was Done | Next Steps |
|------|---------------|------------|
| 2026-01-22 | Created project structure and docs | Set up agent backend |
| | | |

### Known Issues/Blockers

- None yet

### Questions for Next Session

- None yet

---

## Useful Commands

```bash
# Start agent
cd /Users/dankeegan/deepagent/agent && uv run python main.py

# Start frontend
cd /Users/dankeegan/deepagent/frontend && npm run dev

# Check current app for reference
cd /Users/dankeegan/fractional.quest

# Database queries (via Neon console or psql)
# User profile: SELECT * FROM user_profile_items WHERE user_id = 'xxx';
# Content: SELECT * FROM content_pages WHERE slug = 'xxx';
```

---

## Reference Links

- [Deep Agents Docs](https://python.langchain.com/docs/langgraph)
- [CopilotKit Deep Agents](https://docs.copilotkit.ai/langgraph/deep-agents)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Current fractional.quest](https://fractional.quest)

# Product Requirements Document: Fractional Quest v2

## Document Info
- **Version:** 1.0
- **Last Updated:** 2026-01-22
- **Status:** Draft

---

## 1. Problem Statement

### Current State (fractional.quest v1)

The existing Fractional Quest application helps fractional executives find roles, but suffers from critical technical issues:

| Issue | Impact | Root Cause |
|-------|--------|------------|
| Context loss between messages | Agent asks questions user already answered | Custom middleware cache timing; `state.user` often `None` |
| Frontend/agent state divergence | UI shows step 1 after completing step 3 | `useCoAgent` doesn't reliably sync bidirectionally |
| Page context forgotten | Agent says "you're on homepage" when on /fractional-cto-jobs | Instructions only in first message |
| Memory inconsistency | Agent contradicts what profile panel shows | Dual-write to Neon + ZEP; ZEP writes fail silently |
| Bloated system prompt | 1,500+ lines, 27 tools in one agent | No separation of concerns |

### Desired State (v2)

A rebuild using Deep Agents that provides:
- Reliable context persistence across entire conversations
- Automatic state synchronization between frontend and agent
- Clean separation via orchestrator + specialized subagents
- Single source of truth for user data
- Maintainable, modular codebase

---

## 2. User Personas

### Primary: Fractional Executive

**Demographics:**
- Senior executives (VP, Director, C-suite experience)
- 40-60 years old
- Based in US, UK, or EU
- Seeking flexible/fractional work arrangements

**Goals:**
- Find fractional, interim, or advisory roles
- Build a profile that attracts relevant opportunities
- Get matched with companies that need their expertise
- Connect with coaches to navigate career transitions

**Pain Points (current app):**
- Has to repeat information multiple times
- Profile setup feels broken/incomplete
- Can't trust the agent remembers their preferences
- Confused by inconsistent responses

### Secondary: Executive Coach

**Goals:**
- Connect with executives seeking coaching
- Understand client background before calls
- Streamline booking process

---

## 3. Core User Journeys

### Journey 1: Onboarding (6 Steps)

**Trigger:** New user visits site or existing user has incomplete profile

**Steps:**
1. **Trinity** - "Why are you here?"
   - Options: job_search, coaching, lifestyle_change, just_curious
   - Determines subsequent experience focus

2. **Employment Status** - "What's your current situation?"
   - Options: employed, between_roles, freelancing, founder

3. **Professional Vertical** - "What's your domain?"
   - Options: technology, finance, marketing, operations, hr_people, sales, product

4. **Location** - "Where are you based?"
   - Free text with normalization
   - Validates against known locations

5. **Role Preference** - "What role are you targeting?"
   - Options: CTO, CFO, CMO, COO, CPO, CHRO, etc.

6. **Experience Level** - "What's your seniority?"
   - Options: c_suite, vp, director, senior_manager

**Success Criteria:**
- All 6 values persisted to Neon
- Frontend reflects completion state
- Agent remembers all values in subsequent conversation

### Journey 2: Job Search

**Trigger:** Onboarded user asks about jobs or navigates to job page

**Steps:**
1. Agent acknowledges user's profile (role, location, vertical)
2. Searches jobs matching profile
3. Returns job cards via tool (not in chat text)
4. User can like/save jobs
5. Agent explains match quality

**Success Criteria:**
- Jobs rendered as cards, not JSON in chat
- Likes persisted to user_profile_items
- Agent can reference previously liked jobs

### Journey 3: Coaching Connection

**Trigger:** User selects "coaching" in Trinity or asks about coaching

**Steps:**
1. Agent confirms coaching interest
2. Collects relevant context (goals, challenges)
3. Shows coach booking widget (Calendly)
4. Hands off context to coaching system

**Success Criteria:**
- Smooth transition from chat to booking
- Context preserved for coach

---

## 4. Functional Requirements

### FR1: Onboarding

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1.1 | System shall guide users through 6-step onboarding | P0 |
| FR1.2 | Each step shall use HITL (Human-in-the-Loop) confirmation | P0 |
| FR1.3 | System shall persist each answer immediately to Neon | P0 |
| FR1.4 | System shall allow out-of-order information (user says location before asked) | P1 |
| FR1.5 | System shall validate and normalize inputs (e.g., "london" → "London") | P1 |
| FR1.6 | System shall resume onboarding from last incomplete step on reconnection | P0 |

### FR2: Job Search

| ID | Requirement | Priority |
|----|-------------|----------|
| FR2.1 | System shall search jobs based on user profile | P0 |
| FR2.2 | System shall render jobs as cards via tool rendering | P0 |
| FR2.3 | System shall allow users to like/save jobs | P1 |
| FR2.4 | System shall explain why jobs match user profile | P1 |
| FR2.5 | System shall filter by location, role, engagement type | P1 |

### FR3: State Management

| ID | Requirement | Priority |
|----|-------------|----------|
| FR3.1 | Agent state shall persist across messages within a session | P0 |
| FR3.2 | Agent state shall sync to frontend automatically | P0 |
| FR3.3 | Agent state shall persist across browser sessions (reconnection) | P0 |
| FR3.4 | Agent shall maintain page context when user navigates | P0 |
| FR3.5 | User profile shall be single source of truth (Neon) | P0 |

### FR4: Subagent Routing

| ID | Requirement | Priority |
|----|-------------|----------|
| FR4.1 | Orchestrator shall route to onboarding-agent if profile incomplete | P0 |
| FR4.2 | Orchestrator shall route to job-search-agent for job queries | P0 |
| FR4.3 | Orchestrator shall route to coaching-agent for coaching queries | P1 |
| FR4.4 | Each subagent shall have isolated context and tools | P0 |

---

## 5. Non-Functional Requirements

### NFR1: Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR1.1 | First response latency | < 2 seconds |
| NFR1.2 | Tool execution latency | < 1 second |
| NFR1.3 | State sync to frontend | < 500ms |

### NFR2: Reliability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR2.1 | Context retention across messages | 100% |
| NFR2.2 | State sync success rate | > 99% |
| NFR2.3 | Database write success | > 99.9% |

### NFR3: Scalability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR3.1 | Concurrent users | 100+ |
| NFR3.2 | Messages per session | Unlimited |

---

## 6. Success Metrics

### Primary Metrics

| Metric | Current (v1) | Target (v2) |
|--------|--------------|-------------|
| Onboarding completion rate | ~40% | > 80% |
| Context retention (no re-asks) | ~60% | > 99% |
| State sync accuracy | ~70% | > 99% |
| User complaints about "forgetting" | Common | Rare |

### Secondary Metrics

| Metric | Target |
|--------|--------|
| Jobs discovered per session | > 5 |
| Profile completion rate | > 90% |
| Return user rate (7-day) | > 30% |

---

## 7. Out of Scope (v2.0)

The following are explicitly NOT in scope for the initial rebuild:

- **Analytics dashboards** - Will port later
- **Recruiter messaging** - Will port later
- **3D profile graph** - Will port later
- **Salary insights** - Will port later
- **Article/news content** - Will port later
- **A2UI widgets** - Will port later
- **Multi-language support** - Future consideration
- **Mobile app** - Not planned

---

## 8. Technical Constraints

### Must Use
- **Neon PostgreSQL** - Existing database with user data
- **CopilotKit** - Frontend integration requirement
- **OpenAI GPT-4o** - LLM for agent

### Should Use
- **Deep Agents** - Primary architectural choice
- **LangGraph** - Underlying execution framework
- **FastAPI** - Agent HTTP server

### May Use
- **ZEP** - Knowledge graph (evaluate if still needed)
- **Hume EVI** - Voice integration (port existing)

### Must Not Use
- **Pydantic AI** - Replacing with Deep Agents
- **Custom middleware for context** - Use CopilotKitMiddleware instead

---

## 9. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Deep Agents doesn't solve state issues | Low | High | Build onboarding first as proof of concept |
| Migration takes longer than expected | Medium | Medium | Keep current site running, swap when ready |
| Database schema changes needed | Low | Medium | Use same tables, add new ones if needed |
| CopilotKit integration issues | Low | Medium | Well-documented, proven to work with Deep Agents |
| Learning curve for LangGraph | Medium | Low | Team has Python experience, good docs available |

---

## 10. Timeline (Phases, No Dates)

### Phase 1: Foundation
- Project setup (repo, dependencies, structure)
- State models
- Basic orchestrator agent
- CopilotKit integration

### Phase 2: Onboarding
- Onboarding subagent
- 6 HITL tools
- Neon persistence
- Frontend onboarding UI

### Phase 3: Job Search
- Job search subagent
- Search and match tools
- Job card rendering
- Like/save functionality

### Phase 4: Content & Polish
- Content pages from Neon
- Page context handling
- Error handling
- Testing and validation

### Phase 5: Migration
- Side-by-side comparison
- Data verification
- DNS swap
- Deprecate v1

---

## 11. Approval

| Role | Name | Status |
|------|------|--------|
| Product Owner | Dan Keegan | Pending |
| Technical Lead | Claude | Draft |

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Fractional** | Part-time executive role, typically 1-3 days/week |
| **Interim** | Full-time temporary executive role |
| **Trinity** | User's primary reason for using the platform |
| **HITL** | Human-in-the-Loop - user confirmation before action |
| **Subagent** | Specialized agent that handles specific domain |
| **Orchestrator** | Main agent that routes to subagents |
| **AG-UI** | Agent-UI protocol for streaming agent state |

# Flip the Switch — Hackathon Product Track Brief

> **Core Mandate:** Build a collaborative workflow where at least one person and one AI agent solve a real-world task together through a **Switch Room**. Switch must be structurally essential to the solution (the workflow must not function without it).

---

## 1. Hackathon Constraints & Timeline

| Parameter | Detail |
|---|---|
| **Event Window** | November 4, 2026, 00:01 IST – November 7, 2026, 23:59 IST (18:29 UTC) |
| **Submission Deadline** | November 7, 2026, 23:59 IST |
| **Team Size** | 1 to 4 members (online, global, free) |
| **Scope of Work** | Pre-existing agents, libraries, and templates are allowed. The Switch setup, room configuration, and collaborative workflow must be built during the hackathon. |
| **Tooling & AI Policy** | AI coding tools are permitted; participants must understand and be able to explain all submitted code. |
| **Infrastructure Costs** | Switch is open source and self-hostable (bundled with local Mattermost via Docker). Participants provide their own model API keys or subscriptions. |

---

## 2. Target Product Tracks & Prizes

This project focuses exclusively on the **Product / Workflow Tracks**:

| Track | Core Requirement | Award |
|---|---|---|
| **Best Business Workflow** | A practical team workflow where people and agents collaborate on business tasks (engineering, operations, customer support, triage, etc.). Technical and non-technical participants welcome. | **$2,000** |
| **Best Personal or Creative Workflow** | Everyday productivity, personal projects, or creative tasks augmented through Switch rooms and agent collaboration. | **$2,000** |
| **Code with Wispr** *(Optional Side Track)* | Build by voice with Wispr Flow (prompts, agent instructions, documentation); submit a Wispr usage scorecard alongside the main workflow. | $500 |
| **Best Blog** *(Optional Side Track)* | A clear, practical tutorial explaining the build process, room setup, and lessons learned for first-time Switch users. | AirPods 5 |

*Total Prize Pool: $10,000 (including keyboards for top #HowISwitch posts, swag for 20 random entries, and finalist showcases).*

---

## 3. Judging Rubric & Evaluation Flow

### Evaluation Weights (Workflow Tracks)

| Criterion | Weight | Core Question for Judges |
|---|:---:|---|
| **Use of Switch** | **30%** | Is Switch central to the architecture? Would the workflow break down if Switch were removed? |
| **Technical Execution** | **25%** | Does the solution run reliably? Is the repository turnkey, reproducible, and easy to clone/test? |
| **Creativity & Impact** | **25%** | Does it address an acute problem faced by real teams? Is the interaction model novel and effective? |
| **Presentation** | **20%** | Do the demo video and README communicate the problem, Switch integration, and user-agent collaboration clearly? |

### Review Stages
1. **Initial Screening:** WeMakeDevs reviews all valid submissions.
2. **Shortlist Selection:** WeMakeDevs curates top candidate projects.
3. **Finalist Judging:** Panel of judges from Switch, DevTools Academy, and WeMakeDevs selects winners.

---

## 4. Switch Platform & Technical Capabilities

### Architectural Role of Switch
Switch serves as the coordination engine connecting human team chats with autonomous agents.

- **Team Chat Connectors:** Native bridge to Slack, Discord, Microsoft Teams, Telegram, and Mattermost.
- **Switch Rooms:** Persistent shared context containing conversation history, instructions, roles, tasks, and domain knowledge shared between humans and agents. Agents participate as distinct chat members with custom names and avatars.
- **Local Self-Hosted Stack:** Switch Console (desktop application) runs local Switch in Docker with a bundled Mattermost instance, removing dependencies on external corporate workspace permissions.
- **Supported Agent Frameworks:**
  - *Out of the Box:* Claude Code, Codex, and OpenCode via Switch Console.
  - *Custom Agents:* Any framework or language via the Switch Agent Protocol (inbound Server-Sent Events [SSE], outbound HTTP REST). Compatible with LangChain, OpenAI Agents SDK, Google ADK, or bespoke scripts.
- **OS Support:** macOS, Windows, and Linux (note: Windows/Linux builds are early access; validate local environment early).

### Reference Workflow Archetypes
- **Incident Response:** Human alerts incident → Triage agent queries logs and isolates commit → Release agent prepares rollback → Human reviews diff and approves execution.
- **Triage & Reproduce:** Routing agent parses issue ticket → Test agent generates and runs reproduction script → Human inspects script output in-thread to confirm bug.

---

## 5. Product Ideation & Validation Checklist

Every prospective idea must satisfy this validation checklist before implementation:

| Dimension | Qualification Criteria |
|---|---|
| **User & Problem** | Clear target user with an acute, recurring, time-consuming, or error-prone task. |
| **Workflow Trigger** | A concrete chat message, webhook, or event that initiates the room workflow. |
| **Human Contribution** | Meaningful human decision, domain input, policy review, or approval (not passive observation). |
| **Agent Execution** | Tangible, tool-augmented automated work (fetching data, querying APIs, running code, generating artifacts). |
| **Switch Dependency** | Hard requirement on Switch: shared context, multi-party visibility, human-in-the-loop handoff. *(Reject ideas where Switch is merely a passive notification webhook).* |
| **Verifiable Outcome** | A concrete completed artifact or state change (PR opened, service remediated, document drafted, issue closed)—never generic conversational chat alone. |
| **Feasibility** | Fully buildable, testable, and demonstrable within the hackathon window using available credentials and APIs. |

### Idea Definition Template
> *"For **[target user/team]**, a **[trigger event]** initiates a Switch room where **[agent]** executes **[automated tasks]**, **[human]** provides **[decision/review/input]**, producing **[verifiable finished outcome]**. Switch is indispensable because **[shared context / multi-party coordination reason]**."*

---

## 6. Submission Deliverables & Requirements

Plan repository and presentation assets around judging requirements:

1. **GitHub Repository:**
   - Clean, well-structured codebase.
   - Comprehensive `README.md` with problem statement, architecture diagram, Switch setup instructions, and step-by-step reproduction steps.
2. **Demo Video:**
   - Concise demonstration showcasing the trigger, live human-agent interaction inside the chat room, and the verified end-state outcome.
   - Clear explanation of why Switch is essential to the workflow.
3. **Turnkey Setup:**
   - Configuration files, environment variable templates (`.env.example`), and room templates/instructions included in the repository.

---

## 7. Open Uncertainties to Verify with Organizers

Verify these items with WeMakeDevs organizers via [Discord](https://discord.gg/E2rWw2Yhsm):

- **Submission Portal & Form Fields:** Confirm the exact submission URL (Devfolio, WeMakeDevs portal, or form) and all mandatory submission fields.
- **Demo Video Constraints:** Confirm exact time limit (e.g., strict 3-minute vs. 5-minute cap) and accepted hosting platforms (YouTube unlisted, Loom, etc.).
- **Repository Visibility:** Confirm whether the GitHub repository must be public at submission time or if private repositories with judge invitations are permitted.
- **Judge Reproduction Process:** Confirm whether judges will clone and run the stack locally (requiring automated Docker/Mattermost setup scripts and mock credentials) or evaluate primarily through code review and the video demo.

---

## 8. Essential Links & Documentation

- **Hackathon:** [Challenge & FAQ](https://www.wemakedevs.org/hackathons/switch) | [Resources Hub](https://www.wemakedevs.org/hackathons/switch/resources) | [Discord Support](https://discord.gg/E2rWw2Yhsm)
- **Switch Software:** [Switch Console Releases](https://github.com/sandbox-quantum/switch/releases/latest) | [Switch Core GitHub](https://github.com/sandbox-quantum/switch)
- **Documentation:** [10-Minute Quickstart](https://docs.switchagents.ai/switch-rooms/getting-started) | [Shared Context Guide](https://docs.switchagents.ai/switch-rooms/using/shared-context) | [Custom Agent Protocol](https://docs.switchagents.ai/switch-rooms/internals/agent-protocol) | [Chat Integrations](https://docs.switchagents.ai/switch-rooms/deploy/messaging-apps/index)
- **Examples:** [Official Repo Examples](https://github.com/sandbox-quantum/switch/tree/main/examples) | [Payments Room Walkthrough](https://docs.switchagents.ai/switch-rooms/building/payments-room)

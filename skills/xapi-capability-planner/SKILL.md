---
name: xapi-capability-planner
description: Discover, compare, and plan xAPI capability usage for an agent task. Use this skill when the user wants to find which xAPI API, action, capability, or endpoint can solve a goal; combine multiple xAPI calls into a workflow; estimate call risks or balance impact; or produce executable xapi CLI/API call examples without hand-searching the whole marketplace.
---

# xAPI Capability Planner

## Overview

Use xAPI discovery and catalog information to turn a user's goal into a concrete xAPI execution plan. Prefer existing xAPI actions and capabilities before proposing a custom API integration.

## Workflow

1. Restate the user's goal as one or more capability needs.
2. Search or list relevant xAPI services, actions, capabilities, or marketplace APIs.
3. Compare candidates by fit, input shape, authentication requirement, cost risk, freshness, and whether the result is suitable for agents.
4. Choose the smallest reliable call chain.
5. Produce an execution plan with endpoint/action names, required inputs, optional inputs, expected outputs, and failure handling.
6. Provide runnable examples with `xapi-to` commands or HTTP calls when the user asks to execute or integrate.

## Candidate Selection

Use this priority order:

1. A dedicated xAPI action matching the task.
2. A capability that already composes multiple APIs.
3. A public API endpoint already registered in xAPI.
4. A new provider registration or custom integration only when no existing xAPI capability fits.

## Output Format

For planning requests, return:

- Recommended xAPI capability or action
- Why it fits
- Required inputs
- Optional inputs
- Example call
- Expected output
- Cost or balance warning when relevant
- Fallback if the call fails

For multi-step workflows, include a numbered call sequence and say which output field feeds the next input.

## xAPI CLI Examples

Use the CLI shape when the user wants a runnable command:

```bash
npx xapi-to list
npx xapi-to search "twitter user profile"
npx xapi-to call twitter.user_by_screen_name --input '{"screen_name":"openai"}'
```

If the exact action name is uncertain, do not invent one. Search first, then explain the uncertainty.

## References

Read `references/planning-guide.md` when building a multi-step plan, comparing similar xAPI options, or writing a user-facing integration handoff.

## Safety

- Do not expose or request raw API keys in chat.
- Warn the user before any plan that can spend balance, mutate external state, trade assets, or process private data.
- Prefer read-only calls for discovery and research.
- Ask for explicit confirmation before executing a paid, state-changing, or long-running workflow.

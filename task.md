
**I need to refactor the `script_generator` agent to use the OpenAI Agents SDK, while keeping all other agents unchanged.**

**Key requirements:**

1. Replace the current implementation of the `script_generator` agent with the OpenAI Agents SDK.
2. Hardcode the use of the `"gpt-5"` model inside the refactored `script_generator` agent. This means **removing model selection from the Streamlit app** UI for this agent specifically.
3. Ensure seamless interoperability: the `script_generator` agent must still accept outputs (data/messages) from other agents in the pipeline, which may be using different models.
4. Read and follow the structure, methods, and conventions described in the **OpenAI Agents SDK documentation** provided in the markdown file @/Users/moe/script-gen-main/openai-agents.md.

**Please consider:**

* Performance: optimize agent invocation and avoid redundant operations.
* Best practices for using the OpenAI Agents SDK, including registration, task definition, and execution flow (as outlined in the documentation).
* Preserve all existing logic and code for the rest of the agents; only `script_generator` is to be refactored.

**Please do not unnecessarily remove any comments or code.**
**Generate the refactored code with clear comments explaining the logic.**



New Project Process

Create a prompt for Claude to use to create a Project Requirement Document.

Create a projectBrief.md/README.md with:
	Populate this file with a high-level overview of your project. This could include:
	The main goal or purpose of the project.
	Key features or components.
	Target audience or users.
	Overall architectural style or key technologies (if known).
	Any other foundational information that defines the project.

mkdir <project directory>
cd <project directory>

# Copy required files to new porject:
 rsync -av --progress \
  --include '.roo/' \
  --include '.roo/*' \
  --exclude '.roo/*/' \
  --exclude 'context_portal/' \
  --exclude '.git/' \
  /home/pwp/srv/roo_code_assets/ . 

# Intialize conport_portal:
Initialize according to custom instructions. Workspace path is ${workspaceFolder}  
First, call conport.get_conport_schema and then get_product_context with that absolute workspace_id.

# For Python Projects
  uv init

  uv venv



# For Javascript Projects>



This document outlines a repeatable workflow for kicking off a new project, including prompts, boilerplate files, and initialization steps for common stacks.

1) Create a prompt for Claude to generate a Project Requirements Document (PRD)
Use the following prompt verbatim:

You are a principal product manager and staff engineer collaborating to draft a crisp, actionable Project Requirements Document (PRD).

Context:
- Project name: <PROJECT_NAME>
- Problem to solve: <PROBLEM_STATEMENT>
- Target users: <TARGET_USERS>
- Business goals: <BUSINESS_GOALS>
- Constraints/assumptions: <CONSTRAINTS>
- Key technologies (if known): <TECHNOLOGIES>

Deliverables:
Produce a PRD with the following sections:
1. Summary: 3–5 sentence overview of the project and outcomes.
2. Goals & Non-Goals: Bullet points for what’s in scope vs. explicitly out of scope.
3. User Personas & Use Cases: 2–4 personas; 5–10 core use cases in Given/When/Then format.
4. Requirements:
   - Functional requirements (numbered, must/should/could).
   - Non-functional requirements (performance, security, privacy, reliability, accessibility, i18n).
   - Data requirements and retention.
5. Success Metrics / KPIs: Quantitative targets and measurement approach.
6. Dependencies & Risks: Internal/external dependencies, top risks, mitigations.
7. Milestones & Timeline: Phased plan (e.g., Alpha/Beta/GA), acceptance criteria per phase.
8. Open Questions: Specific decisions required, owners, and due dates.
9. Appendix: Glossary and references.

Constraints:
- Keep concise but unambiguous.
- Use tables where helpful (e.g., risks, metrics).
- Call out assumptions explicitly.
- Propose alternatives if there are major architectural choices.

Return the PRD in Markdown.
Ask up to 5 clarification questions if essential details are missing before producing the PRD.
2) Create projectBrief.md (or README.md)
Create a top-level brief to ground the project. Use this template:

# <Project Name>

## Overview
A short, high-level description of what the project is and why it exists.

## Goals
- Primary goal: ...
- Secondary goals: ...

## Target Users / Audience
- Who will use this?
- What problems are they trying to solve?

## Key Features
- Feature 1 — brief description
- Feature 2 — brief description
- Feature 3 — brief description

## Architecture / Technology (initial)
- Language(s): ...
- Frameworks: ...
- Data storage: ...
- Integrations: ...
- Hosting/deployment: ...

## Constraints & Assumptions
- Constraint 1
- Assumption 1

## Success Criteria
- KPI 1
- KPI 2

## Current Status
- Ideation / Discovery / Planning / In Progress / Alpha / Beta / GA

## Links
- PRD: <link>
- Designs: <link>
- Tracking board: <link>
3) Initialize a new project directory
	Create and enter the folder:
	mkdir <project directory>
	cd <project directory>
	
4) Copy required files to the new project (
	Copy .roo root without its children:
	rsync -av --progress \
	  --include '.roo/' \
	  --include '.roo/*' \
	  --exclude '.roo/*/' \
	  --exclude 'context_portal/' \
	  --exclude '.git/' \
	 /home/pwp/srv/roo_code_assets/ .
	 
5) Initialize conport_portal
	Initialize according to your custom instructions. Workspace path is ${workspaceFolder}.
	First, call: conport.get_conport_schema
	Then call: get_product_context with the absolute workspace_id obtained above.
	Capture or export any IDs/tokens required by your workflow.

6) Language-specific setup
	For Python projects:
	uv init
	uv venv

	For JavaScript projects:
	(Add your standard initialization steps here, e.g., npm init -y, pnpm dlx, bun init, etc.)
	Suggestions:

	If using Node + TypeScript:
	npm init -y
	npm pkg set type=module
	npm i -D typescript ts-node @types/node
	npx tsc --init --rootDir src --outDir dist --module esnext --moduleResolution bundler --target es2022 --resolveJsonModule --esModuleInterop
	If using package managers:
	pnpm dlx or bun init as preferred.
	7) Next steps checklist
	Complete projectBrief.md
	Run the Claude PRD prompt and link the PRD in the brief
	Define the initial milestone plan and create tracking issues
	Set up CI (lint, type check, tests)
	Add a LICENSE and CODE_OF_CONDUCT if public
	Create ENV templates (e.g., .env.example)
	Draft an initial ADR for key architectural choices
	This process ensures each project starts with clear intent, requirements, and repeatable scaffolding.
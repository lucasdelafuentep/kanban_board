# Frontend AGENTS.md

## Overview
This document describes the existing code in the frontend directory of the Project Management MVP web app.

### Main Features
- Kanban board with 5 fixed columns (Backlog, Discovery, In Progress, Review, Done)
- Columns can be renamed
- Cards can be added, edited, deleted, and moved between columns via drag-and-drop
- Backend API integration for persistence (`/api/board`)
- AI chat sidebar (`AiSidebar.tsx`) integrated with `/api/ai/chat`
- Login page with JWT-based authentication
- Unit and integration tests using Vitest and Playwright

### Key Components
- `src/components/KanbanBoard.tsx`: Main board component, manages board state, drag-and-drop, column renaming, and card operations
- `src/components/KanbanColumn.tsx`: Renders a single column, handles renaming and card listing
- `src/components/KanbanCard.tsx`: Renders a single card, supports drag-and-drop and delete
- `src/components/NewCardForm.tsx`: Form to add a new card to a column
- `src/components/KanbanCardPreview.tsx`: (Not detailed above, likely used for drag preview)

### State Management
- Board state is managed in `KanbanBoard` using React `useState`
- Board data structure is defined in `src/lib/kanban.ts` (types: BoardData, Column, Card)
- Initial board data is provided by `initialData` in `kanban.ts`
- Card movement logic is handled by `moveCard` in `kanban.ts`

### Testing
- Unit tests for board logic in `src/lib/kanban.test.ts`
- Component tests in `src/components/KanbanBoard.test.tsx`
- End-to-end tests in `tests/kanban.spec.ts` using Playwright

### Running and Testing
- `npm install` to install dependencies
- `npm run dev` to start the dev server
- `npm run test:unit` for unit tests
- `npm run test:e2e` for e2e tests

---
This document will be updated as the frontend evolves and integrates with the backend and AI features.

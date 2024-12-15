# Beta Flow Frontend

React-based frontend for the Beta Flow workflow management system.

## Features

- Create and manage workflows
- Drag-and-drop interface for workflow steps
- Execute workflows and view results
- Parallel and conditional workflow support

## Local Development

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Update `REACT_APP_API_URL` if needed.

3. Start development server:
   ```bash
   npm start
   ```

## Deployment to Vercel

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

4. Set environment variables in Vercel:
   - Go to your project settings
   - Add `REACT_APP_API_URL` pointing to your Railway backend

## Usage

### Creating a Workflow
1. Click "Create Workflow" in the navigation
2. Enter workflow name
3. Add steps using the "Add Step" button
4. Configure each step:
   - Step name
   - Action type
   - Parameters (prompt, model)
   - Optional group for parallel execution
5. Drag and drop steps to reorder
6. Click "Create Workflow" to save

### Executing a Workflow
1. Find your workflow in the home page list
2. Click "Execute" on the workflow
3. View results in the execution results page

## Folder Structure

```
frontend/
├── src/
│   ├── api/         # API integration
│   ├── components/  # Reusable components
│   ├── pages/       # Page components
│   └── theme.js     # MUI theme configuration
├── .env.example     # Environment variables template
└── vercel.json      # Vercel deployment config
```
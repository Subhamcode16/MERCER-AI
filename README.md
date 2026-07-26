# MERCER AI

MERCER AI is a cutting-edge visual intelligence and campaign generation platform built for the fashion industry. It seamlessly merges textile DNA analysis with state-of-the-art cinematic image generation to create hyper-realistic, brand-aligned fashion campaigns.

## Features

- **Campaign Studio**: A comprehensive workspace to orchestrate visual generation campaigns.
- **Material Intelligence**: Upload material specimens to extract textile DNA (weave type, fiber base) to accurately guide AI generation.
- **Cinematic Campaigns**: Configurable art direction (background environment, pose & movement, cinematic lighting) to produce high-end visual outputs.
- **Brand Archetypes**: Strict style enforcement ensuring that the generated assets align with luxury fashion standards.
- **High-Performance Architecture**: 
  - **Frontend**: Next.js 15, React, Tailwind CSS, Lucide Icons, featuring a premium dark-mode luxury aesthetic.
  - **Backend**: FastAPI, Python 3.13, orchestrating advanced image generation and visual reasoning models.

## Architecture

This repository contains the core software infrastructure for the MERCER AI platform:

- `/Visual-Intelligence/product/frontend/`: The Next.js web application interface.
- `/Visual-Intelligence/product/backend/`: The FastAPI Python backend serving AI models and logic.

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (3.13)
- Required AI Model API Keys (e.g., Gemini, etc.)

### Local Development

1. **Frontend Setup**
   ```bash
   cd Visual-Intelligence/product/frontend
   npm install
   npm run dev
   ```

2. **Backend Setup**
   ```bash
   cd Visual-Intelligence/product/backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

Alternatively, you can start both the frontend and backend simultaneously using the provided `start-app.bat` script in the root directory.

## License

All rights reserved.

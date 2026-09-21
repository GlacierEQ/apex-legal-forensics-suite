# 🏛️ APEX-LEGAL-FORENSICS-SUITE — APEX MEGA-REPOSITORY

> **Autonomous Full-Stack System** synthesized by the APEX Sovereign Mega-Repo Forge.  
> **Mission:** Autonomous Legal Discovery & Timeline Forensics Suite  
> **Lineage:** Synthesized from battle-tested open-source Lincoln Logs & APEX Holographic Mesh Doctrine.  
> **Operator:** Casey Barton / GlacierEQ (FRE 601/602 Testimonial Primacy Enforced)

---

## 🏗️ Architecture & Lincoln-Log Lineage

This Mega-Repository composes proven open-source primitives into a unified, high-performance organism:

* **Frontend:** Next.js 15 App Router, TypeScript, Tailwind CSS, WebSockets, Lucide Icons.
* **Backend:** FastAPI (Python 3.12), Pydantic v2, Async Event Bus, SQLite/DuckDB persistent store.
* **Middleware:** JWT Authentication, Role-Based Access Control, Rate Limiter, Structured JSON-RPC bridge.
* **Cloud Infrastructure:** Multi-stage Docker Compose and automated GitHub Actions (`.github/workflows/ci.yml`).

### Lincoln Logs Harvested:
{
  "legal tech python": [],
  "document forensics": [
    {
      "name": "oletools",
      "full_name": "decalage2/oletools",
      "html_url": "https://github.com/decalage2/oletools",
      "stars": 3418,
      "description": "oletools - python tools to analyze MS OLE2 files (Structured Storage, Compound File Binary Format) and MS Office documents, for malware analysis, forensics and debugging.",
      "topics": [
        "compound",
        "forensics",
        "macros",
        "malware-analysis",
        "ms-office-documents",
        "ole-files",
        "olefile",
        "parser",
        "pyparsing",
        "python",
        "python-library",
        "rtf",
        "security",
        "vba"
      ],
      "license": "NOASSERTION"
    },
    {
      "name": "StegoForge",
      "full_name": "Nour833/StegoForge",
      "html_url": "https://github.com/Nour833/StegoForge",
      "stars": 592,
      "description": "The ultimate steganography and digital forensics toolkit. Hide and extract data across images, audio, video, documents, and network packets, or run 11 advanced detection engines to uncover hidden payloads.",
      "topics": [
        "cryptography",
        "ctf",
        "ctf-tools",
        "cybersecurity",
        "forensics",
        "python",
        "security",
        "security-tools",
        "steganography"
      ],
      "license": "MIT"
    }
  ],
  "fastapi template": [
    {
      "name": "full-stack-fastapi-template",
      "full_name": "fastapi/full-stack-fastapi-template",
      "html_url": "https://github.com/fastapi/full-stack-fastapi-template",
      "stars": 45661,
      "description": "Full-stack web application template with FastAPI, React, SQLModel, PostgreSQL, Vite, Tailwind CSS, shadcn/ui, FastAPI Cloud, and Docker Compose.",
      "topics": [
        "docker",
        "docker-compose",
        "fastapi",
        "fastapi-cloud",
        "full-stack",
        "github-actions",
        "jwt",
        "openapi",
        "playwright",
        "postgresql",
        "pytest",
        "python",
        "react",
        "shadcn-ui",
        "sqlmodel",
        "tailwindcss",
        "tanstack-query",
        "tanstack-router",
        "typescript",
        "vite"
      ],
      "license": "MIT"
    },
    {
      "name": "FastAPI-template",
      "full_name": "s3rius/FastAPI-template",
      "html_url": "https://github.com/s3rius/FastAPI-template",
      "stars": 2828,
      "description": "Feature rich robust FastAPI template.",
      "topics": [
        "aerich",
        "alembic",
        "asynchronous",
        "asyncio",
        "cookiecutter",
        "cookiecutter-python3",
        "cookiecutter-template",
        "fastapi",
        "fastapi-boilerplate",
        "fastapi-template",
        "graphql",
        "opentelemetry",
        "ormar",
        "prometheus",
        "python3",
        "sentry",
        "sqlalchemy-orm",
        "strawberry-graphql",
        "tortoise-orm"
      ],
      "license": "MIT"
    }
  ],
  "nextjs dashboard": [
    {
      "name": "refine",
      "full_name": "refinedev/refine",
      "html_url": "https://github.com/refinedev/refine",
      "stars": 35702,
      "description": "A React Framework for building  internal tools, admin panels, dashboards & B2B apps with unmatched flexibility.",
      "topics": [
        "admin",
        "admin-ui",
        "ant-design",
        "crud",
        "developer-tools",
        "frontend-framework",
        "good-first-issue",
        "graphql",
        "hacktoberfest",
        "headless",
        "internal-tools",
        "javascript",
        "low-code",
        "nestjs",
        "nextjs",
        "open-source-project",
        "react",
        "react-framework",
        "react-hooks",
        "typescript"
      ],
      "license": "MIT"
    },
    {
      "name": "homepage",
      "full_name": "gethomepage/homepage",
      "html_url": "https://github.com/gethomepage/homepage",
      "stars": 32781,
      "description": "A highly customizable homepage (or startpage / application dashboard) with Docker and service API integrations.",
      "topics": [
        "docker",
        "homepage",
        "nextjs",
        "node",
        "react",
        "self-hosted",
        "startpage"
      ],
      "license": "GPL-3.0"
    }
  ]
}

---

## 🚀 Quick Start

### Option 1: Docker Compose (Zero Setup)
```bash
docker-compose up --build
```
* **Frontend:** `http://localhost:3000`
* **Backend API Docs:** `http://localhost:8000/docs`

### Option 2: Local Development
```bash
# 1. Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 2. Frontend
cd ../frontend
npm install
npm run dev
```

---

## 🧪 Verification & Test Gates
```bash
make test
```

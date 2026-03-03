# Project-Based Bookmarks Manager

A project-oriented bookmark manager built with Flask and SQLite.

Tired of chaotic Chrome bookmark folders when working on multiple projects?  
This tool organizes bookmarks **by project/workspace**, making it easier to manage links, notes, and references for each specific task or client.

## Features (Current MVP)

- Create and manage multiple **projects** (workspaces)
- Add, view, edit (future), and delete bookmarks within each project
- Each bookmark includes: title, URL, description
- Simple web interface with Bootstrap styling
- SQLite database (zero-configuration)
- Flash messages for user feedback
- Form validation with Flask-WTF + CSRF protection

## Planned Features (Roadmap)

- Chrome / Edge extension for one-click saving to a project
- Tagging system (global + per-project tags)
- Folder/subfolder structure inside projects
- Full-text search across all bookmarks
- Import/export from Chrome bookmarks HTML
- Dead link checker
- Optional page archiving / screenshot preview
- User authentication & multi-user support (future)

## Tech Stack

- Backend: Flask
- Database: SQLite (via Flask-SQLAlchemy)
- Forms: Flask-WTF
- Frontend: Jinja2 templates + Bootstrap 5
- Structure: Application Factory + Blueprints

## Quick Start

### Prerequisites

- Python 3.8+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/project-based-bookmarks-manager.git
cd project-based-bookmarks-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
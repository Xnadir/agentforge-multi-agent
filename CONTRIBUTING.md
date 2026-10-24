# Contributing to AgentForge

Thanks for your interest in contributing!

## Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your API key to .env
```

## Code Style

- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small
- Write descriptive commit messages

## Reporting Issues

Open an issue with:
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

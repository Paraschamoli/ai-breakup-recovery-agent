<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">ai-breakup-recovery-agent</h1>

<p align="center">
  <strong>An AI-powered multi-agent system designed to support users through emotional recovery after a breakup. The team consists of specialized agents—including a Therapist, Closure Writer, Routine Planner, and Brutal Honesty Advisor—each providing a unique perspective and form of guidance. The system can also analyze uploaded chat screenshots using Gemini Vision capabilities to offer deeper emotional insights. By combining empathetic support, structured routines, emotional catharsis, and direct feedback, the agent team delivers comprehensive, personalized recovery assistance.</strong>
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/ai-breakup-recovery-agent/actions/workflows/main.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/Paraschamoli/ai-breakup-recovery-agent/main.yml?branch=main" alt="Build status">
  </a>
  <a href="https://img.shields.io/github/license/Paraschamoli/ai-breakup-recovery-agent">
    <img src="https://img.shields.io/github/license/Paraschamoli/ai-breakup-recovery-agent" alt="License">
  </a>
</p>

---

## 📖 Overview

An AI-powered multi-agent system designed to support users through emotional recovery after a breakup. The team consists of specialized agents—including a Therapist, Closure Writer, Routine Planner, and Brutal Honesty Advisor—each providing a unique perspective and form of guidance. The system can also analyze uploaded chat screenshots using Gemini Vision capabilities to offer deeper emotional insights. By combining empathetic support, structured routines, emotional catharsis, and direct feedback, the agent team delivers comprehensive, personalized recovery assistance.. Built on the [Bindu Agent Framework](https://github.com/getbindu/bindu) for the Internet of Agents.

**Key Capabilities:**
- 🧠 **Therapeutic Support** - Professional emotional guidance and coping strategies
- ✍️ **Closure Writing** - Help with closure letters and emotional expression
- 📅 **Routine Planning** - Structured daily routines for recovery and growth
- 💬 **Honest Advice** - Direct feedback and reality checks for personal growth
- � **Chat Analysis** - Analyze conversation screenshots for deeper insights

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- API keys for OpenRouter and Mem0 (both have free tiers)

### Installation

```bash
# Clone the repository
git clone https://github.com/Paraschamoli/ai-breakup-recovery-agent.git
cd ai-breakup-recovery-agent

# Create virtual environment
uv venv --python 3.12.9
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
```

### Configuration

Edit `.env` and add your API keys:

| Key | Get It From | Required |
|-----|-------------|----------|
| `OPENROUTER_API_KEY` | [OpenRouter](https://openrouter.ai/keys) | ✅ Yes |
| `MEM0_API_KEY` | [Mem0 Dashboard](https://app.mem0.ai/dashboard/api-keys) | If you want to use Mem0 tools |

### Run the Agent

```bash
# Start the agent
uv run python -m ai_breakup_recovery_agent

# Agent will be available at http://localhost:3773
```

### Github Setup

```bash
# Initialize git repository and commit your code
git init -b main
git add .
git commit -m "Initial commit"

# Create repository on GitHub and push (replace with your GitHub username)
gh repo create Paraschamoli/ai-breakup-recovery-agent --public --source=. --remote=origin --push
```

---

## 💡 Usage

### Example Queries

```bash
# Emotional support after breakup
"I just broke up with my partner of 3 years and I'm feeling completely lost. Can you help me process these emotions?"

# Chat screenshot analysis
"Can you analyze this conversation and help me understand what went wrong? [upload screenshot]"

# Daily routine creation
"I need a structured daily routine to help me focus on self-improvement and move forward."

# Honest feedback request
"Give me some honest advice about my breakup patterns and what I need to work on."

# Closure letter writing
"Help me write a closure letter to express my feelings and say goodbye properly."
```

### Input Formats

**Plain Text:**
```
I need help dealing with my breakup. We were together for 2 years and I don't know how to move on.
```

**JSON:**
```json
{
  "situation": "breakup_recovery",
  "relationship_duration": "3 years",
  "breakup_reason": "growing apart",
  "current_emotions": ["sad", "confused", "angry"],
  "support_needed": ["emotional_guidance", "routine_planning", "closure"],
  "chat_screenshot": "optional_image_upload"
}
```

### Output Structure

The agent returns structured output with:
- **Therapeutic Guidance**: Professional emotional support and coping strategies
- **Personalized Routines**: Daily schedules and self-care activities
- **Closure Documents**: Letters and exercises for emotional processing
- **Honest Feedback**: Direct advice and growth recommendations
- **Chat Analysis**: Insights from conversation screenshots (if provided)

---

## 🔌 API Usage

The agent exposes a RESTful API when running. Default endpoint: `http://localhost:3773` 

### Quick Start

For complete API documentation, request/response formats, and examples, visit:

📚 **[Bindu API Reference - Send Message to Agent](https://docs.getbindu.com/api-reference/all-the-tasks/send-message-to-agent)**


### Additional Resources

- 📖 [Full API Documentation](https://docs.getbindu.com/api-reference/all-the-tasks/send-message-to-agent)
- 📦 [Postman Collections](https://github.com/GetBindu/Bindu/tree/main/postman/collections)
- 🔧 [API Reference](https://docs.getbindu.com)

---

## 🎯 Skills

### ai_breakup_recovery_agent (v1.0.0)

**Primary Capability:**
- Multi-agent emotional support system for breakup recovery and personal growth
- Specialized agents providing therapeutic, practical, and honest guidance
- Vision-based chat analysis for deeper relationship insights

**Features:**
- **Therapist Agent**: Professional emotional support using CBT and mindfulness techniques
- **Closure Writer Agent**: Help with emotional expression through letters and journaling
- **Routine Planner Agent**: Structured daily schedules for recovery and self-improvement
- **Brutal Honesty Agent**: Direct feedback and reality checks for personal growth
- **Vision Analysis**: Chat screenshot analysis using Gemini Vision capabilities

**Best Used For:**
- Immediate emotional support after relationship endings
- Processing relationship dynamics and learning from past patterns
- Creating structured recovery routines and self-care practices
- Gaining emotional closure through guided expression exercises
- Personal growth and self-discovery post-breakup

**Not Suitable For:**
- Emergency crisis intervention or severe mental health conditions
- Replacement for professional therapy or psychiatric care
- Legal advice regarding divorce or custody matters
- Medical advice for stress-related physical symptoms

**Performance:**
- Average processing time: ~60-90 seconds per session
- Max concurrent requests: 3 (to ensure quality support)
- Memory per request: ~384MB
- Supported image formats: JPEG, PNG (up to 10MB)
- Available languages: English, Spanish, French, German

**⚠️ Important Safety Note:**
This agent is not a substitute for professional mental health services. If you're experiencing severe emotional distress or having thoughts of self-harm, please contact emergency services or a mental health professional immediately.

---

## 🐳 Docker Deployment

### Local Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Agent will be available at http://localhost:3773
```

### Docker Configuration

The agent runs on port `3773` and requires:
- `OPENROUTER_API_KEY` environment variable
- `MEM0_API_KEY` environment variable

Configure these in your `.env` file before running.

### Production Deployment

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🌐 Deploy to bindus.directory

Make your agent discoverable worldwide and enable agent-to-agent collaboration.

### Setup GitHub Secrets

```bash
# Authenticate with GitHub
gh auth login

# Set deployment secrets
gh secret set BINDU_API_TOKEN --body "<your-bindu-api-key>"
gh secret set DOCKERHUB_TOKEN --body "<your-dockerhub-token>"
```

Get your keys:
- **Bindu API Key**: [bindus.directory](https://bindus.directory) dashboard
- **Docker Hub Token**: [Docker Hub Security Settings](https://hub.docker.com/settings/security)

### Deploy

```bash
# Push to trigger automatic deployment
git push origin main
```

GitHub Actions will automatically:
1. Build your agent
2. Create Docker container
3. Push to Docker Hub
4. Register on bindus.directory

---

## 🛠️ Development

### Project Structure

```
ai-breakup-recovery-agent/
├── ai_breakup_recovery_agent/
│   ├── skills/
│   │   └── ai_breakup_recovery_agent/
│   │       ├── skill.yaml          # Skill configuration
│   │       └── __init__.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py                     # Agent entry point
│   └── agent_config.json           # Agent configuration
├── tests/
│   └── test_main.py
├── .env.example
├── docker-compose.yml
├── Dockerfile.agent
└── pyproject.toml
```

### Running Tests

```bash
make test              # Run all tests
make test-cov          # With coverage report
```

### Code Quality

```bash
make format            # Format code with ruff
make lint              # Run linters
make check             # Format + lint + test
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run manually
uv run pre-commit run -a
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature` 
3. Commit your changes: `git commit -m 'Add amazing feature'` 
4. Push to the branch: `git push origin feature/amazing-feature` 
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Powered by Bindu

Built with the [Bindu Agent Framework](https://github.com/getbindu/bindu)

**Why Bindu?**
- 🌐 **Internet of Agents**: A2A, AP2, X402 protocols for agent collaboration
- ⚡ **Zero-config setup**: From idea to production in minutes
- 🛠️ **Production-ready**: Built-in deployment, monitoring, and scaling

**Build Your Own Agent:**
```bash
uvx cookiecutter https://github.com/getbindu/create-bindu-agent.git
```

---

## 📚 Resources

- 📖 [Full Documentation](https://Paraschamoli.github.io/ai-breakup-recovery-agent/)
- 💻 [GitHub Repository](https://github.com/Paraschamoli/ai-breakup-recovery-agent/)
- 🐛 [Report Issues](https://github.com/Paraschamoli/ai-breakup-recovery-agent/issues)
- 💬 [Join Discord](https://discord.gg/3w5zuYUuwt)
- 🌐 [Agent Directory](https://bindus.directory)
- 📚 [Bindu Documentation](https://docs.getbindu.com)

---

<p align="center">
  <strong>Built with 💛 by the team from Amsterdam 🌷</strong>
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/ai-breakup-recovery-agent">⭐ Star this repo</a> •
  <a href="https://discord.gg/3w5zuYUuwt">💬 Join Discord</a> •
  <a href="https://bindus.directory">🌐 Agent Directory</a>
</p>

#   a i - b r e a k u p - r e c o v e r y - a g e n t  
 
# AI Technical Interviewer

An AI-powered mock interview platform that simulates real technical interviews. Upload your resume, pick a target role, and get personalised questions, real-time feedback, and a detailed performance report — all in your browser.

---

## Features

- **Resume-Aware Questions** — Analyses your PDF resume to generate role-specific technical questions (theory + coding).
- **Interactive Chat** — Answer via text, voice (speech-to-text with Whisper), or the built-in Monaco code editor.
- **Text-to-Speech** — Every question is read aloud using Microsoft Edge TTS (`en-IN-PrabhatNeural` voice).
- **Performance Dashboard** — Radar chart, gauge, and written feedback covering Technical Accuracy, Communication, Problem Solving, and Code Quality.
- **Structured LLM Output** — Uses Pydantic models (`InterviewResponse`, `PerformanceSummary`) for reliable, typed responses.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit, Plotly, streamlit-monaco, streamlit-mic-recorder |
| LLM | Amazon Bedrock — Claude 3 Haiku (or Google Gemini as alternative) |
| Orchestration | LangChain + LangGraph |
| Speech-to-Text | Faster Whisper (`base.en`, CPU, int8) |
| Text-to-Speech | Microsoft Edge TTS |
| Deployment | AWS EC2 (t3.medium), systemd service |

---

## Project Structure

```
├── main.py                  # Streamlit entry point & page router
├── backend.py               # LLM setup, interview logic, summary generation
├── app_pages/
│   ├── home.py              # Resume upload & session config
│   ├── chat.py              # Interview chat interface
│   └── summary.py           # Performance dashboard (Plotly charts)
├── utils/
│   ├── generate_audio.py    # Edge TTS audio generation
│   └── transcribe.py        # Whisper speech-to-text
├── ec2_setup.sh             # One-command EC2 bootstrap script
├── pyproject.toml           # Dependencies & project metadata
└── .env                     # Environment config (not committed)
```

---

## Local Development

### Prerequisites

- Python 3.11+
- AWS credentials configured (`aws configure`) or environment variables

### Setup

```bash
# Clone the repository
git clone https://github.com/shivanshS04/ai_for_bharat.git
cd ai_for_bharat

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate.ps1

# Activate (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install --no-cache-dir .
```

### Configure Environment

Create a `.env` file in the project root:

```env
AWS_REGION=us-east-1
# AWS_ACCESS_KEY_ID=your_key       # Required for local dev
# AWS_SECRET_ACCESS_KEY=your_secret # Required for local dev

# Windows: write audio to project directory (no /tmp)
AUDIO_DIR=.

# Optional: use Google Gemini instead of Bedrock
# GOOGLE_API_KEY=your_google_api_key_here
```

### Run

```bash
streamlit run main.py
```

The app opens at `http://localhost:8501`.

---

## AWS Deployment (EC2)

Estimated cost: **~$34.50/month** (t3.medium + EBS + Bedrock pay-per-use).

### 1. Create IAM Role

- Go to **IAM → Roles → Create role**
- Trusted entity: **EC2**
- Attach policy: `AmazonBedrockFullAccess`
- Name: `ec2-interviewer-role`

### 2. Create Security Group

- Inbound rules:
  - SSH (22) — your IP only
  - TCP (8501) — `0.0.0.0/0` (app access)

### 3. Launch EC2

- AMI: Amazon Linux 2023
- Instance type: `t3.medium` (2 vCPU, 4 GB RAM)
- Storage: 20 GB gp3
- Attach the IAM role and security group from above

### 4. Deploy

```bash
# SSH into the instance
ssh -i your-key.pem ec2-user@<public-ip>

# Download & run the setup script
curl -O https://raw.githubusercontent.com/shivanshS04/ai_for_bharat/main/ec2_setup.sh
chmod +x ec2_setup.sh
./ec2_setup.sh
```

The setup script handles everything: cloning the repo, installing dependencies, creating a `.env`, and registering a systemd service that auto-starts on boot.

### 5. Verify

```bash
sudo systemctl status interviewer    # check service status
sudo journalctl -u interviewer -f    # view live logs
```

Open `http://<ec2-public-ip>:8501` in your browser.

---

## Switching LLM Backends

The app supports two LLM backends:

| Backend | Config |
|---|---|
| **Amazon Bedrock** (default) | Set `AWS_REGION` in `.env`. Auth via IAM role (EC2) or `aws configure` (local). |
| **Google Gemini** | Set `GOOGLE_API_KEY` in `.env`. Uncomment the Gemini lines in `backend.py`. |

To switch, comment/uncomment the model initialisation in [backend.py](backend.py) (lines 47-51).

---

## License

This project is for educational and demonstration purposes.

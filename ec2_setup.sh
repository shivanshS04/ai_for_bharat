#!/bin/bash
# ─────────────────────────────────────────────────────────────
# EC2 Bootstrap Script — AI Technical Interviewer
# Run once as ec2-user after launching a fresh Amazon Linux 2023 instance
# Usage: chmod +x ec2_setup.sh && ./ec2_setup.sh
# ─────────────────────────────────────────────────────────────

set -e

echo "==> [1/6] System update & dependencies"
sudo dnf update -y
sudo dnf install python3.11 python3.11-pip git -y

echo "==> [2/6] Clone repository"
cd ~
git clone https://github.com/shivanshS04/ai_for_bharat.git
cd ai_for_bharat

echo "==> [3/6] Create virtualenv & install Python dependencies"
python3.11 -m venv .venv
.venv/bin/pip install --no-cache-dir --upgrade pip
.venv/bin/pip install --no-cache-dir \
    boto3 python-dotenv nest-asyncio \
    edge-tts faster-whisper \
    langchain langchain-core langchain-aws langgraph \
    langchain-google-genai plotly pydantic pypdf \
    streamlit streamlit-mic-recorder streamlit-monaco

echo "==> [4/6] Create .env file"
# Set AWS region — Bedrock auth is handled by the EC2 IAM role (no keys needed)
cat > .env << 'EOF'
AWS_REGION=us-east-1
# GOOGLE_API_KEY=  # optional: uncomment to use Gemini instead of Bedrock
EOF

echo "==> [5/6] Create systemd service"
sudo tee /etc/systemd/system/interviewer.service > /dev/null << EOF
[Unit]
Description=AI Technical Interviewer (Streamlit)
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/ai_for_bharat
ExecStart=/home/ec2-user/ai_for_bharat/.venv/bin/streamlit run main.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "==> [6/6] Enable & start service"
sudo systemctl daemon-reload
sudo systemctl enable interviewer
sudo systemctl start interviewer

echo ""
echo "✅ Setup complete!"
echo "   App running at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8501"
echo "   Check status:   sudo systemctl status interviewer"
echo "   View logs:      sudo journalctl -u interviewer -f"
echo ""
echo "⚠️  Remember to:"
echo "   1. Enable Bedrock model access in AWS Console → Bedrock → Model Access → Claude 3 Haiku"
echo "   2. Attach the IAM role with AmazonBedrockFullAccess to this EC2 instance"
echo "   3. Open port 8501 in your Security Group (TCP, 0.0.0.0/0)"

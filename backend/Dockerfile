# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv .venv

# Remove Windows-specific activation commands
# RUN .venv/Scripts/activate.bat

# Install dependencies with uv
RUN uv pip install -r pyproject.toml

# Remove duplicate Windows-specific activation
# RUN .venv/Scripts/activate.bat

# Copy the rest of the code
COPY . .

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Expose the API port (FastAPI)
EXPOSE 8000

# Default command: start FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Add this to your Dockerfile
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libexpat1 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    fonts-liberation \
    fonts-noto-color-emoji \
    xdg-utils

# Then install Playwright and browsers
RUN pip install playwright && playwright install




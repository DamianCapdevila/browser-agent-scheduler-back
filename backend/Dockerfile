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

# Install Playwright with only Chromium and its dependencies
RUN pip install playwright && playwright install chromium && playwright install-deps chromium




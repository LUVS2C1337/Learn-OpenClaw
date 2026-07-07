FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY core/ core/
COPY tools/ tools/
COPY app.py .

# Expose Streamlit port
EXPOSE 8501

# Run web demo
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.address=0.0.0.0"]

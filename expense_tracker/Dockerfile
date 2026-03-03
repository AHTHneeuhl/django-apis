FROM python:3.11-slim

WORKDIR /app

# Install curl (needed to install uv)
RUN apt-get update && apt-get install -y curl

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files from root
COPY pyproject.toml uv.lock /app/

# Install dependencies using uv
RUN uv sync --frozen

# Copy project files
COPY . /app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
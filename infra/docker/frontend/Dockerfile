FROM node:20-alpine

WORKDIR /app
COPY ../../.. /workspace
RUN npm install -g pnpm
CMD ["pnpm", "run", "dev", "--", "--host", "0.0.0.0"]

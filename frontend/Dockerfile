FROM node:22-alpine AS builder

WORKDIR /app

RUN npm install -g pnpm

COPY frontend/package.json frontend/pnpm-lock.yaml frontend/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile

COPY frontend/ .

# Add build argument for configurable API URL
ARG API_URL
ENV NEXT_PUBLIC_API_URL=${API_URL}

RUN pnpm build

FROM node:22-alpine

WORKDIR /app

RUN npm install -g pnpm

COPY frontend/package.json frontend/pnpm-lock.yaml frontend/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile --prod

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.ts ./
COPY --from=builder /app/package.json ./

ARG FRONTEND_PORT
ENV FRONTEND_PORT=${FRONTEND_PORT}

EXPOSE ${FRONTEND_PORT}
CMD ["sh", "-c", "pnpm start -p ${FRONTEND_PORT}"]
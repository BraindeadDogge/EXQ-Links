# syntax=docker/dockerfile:1

FROM node:22-bookworm-slim AS base
WORKDIR /app
ENV NODE_ENV=production
RUN corepack enable

# Install dependencies (build)
FROM base AS deps
ENV NODE_ENV=development
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    make \
    g++ \
    pkg-config \
    libsqlite3-dev \
  && rm -rf /var/lib/apt/lists/*

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
RUN pnpm install --frozen-lockfile

# Build the Nuxt app
FROM base AS build
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ARG GTM_ID
ENV GTM_ID=$GTM_ID

ARG FRONTEND_BASE_URL
ENV FRONTEND_BASE_URL=$FRONTEND_BASE_URL

ARG BACKEND_BASE_URL
ENV BACKEND_BASE_URL=$BACKEND_BASE_URL

ARG BETTER_AUTH_SECRET
ENV BETTER_AUTH_SECRET=$BETTER_AUTH_SECRET

ARG BETTER_AUTH_URL
ENV BETTER_AUTH_URL=$BETTER_AUTH_URL

ARG BETTER_AUTH_TRUSTED_ORIGINS
ENV BETTER_AUTH_TRUSTED_ORIGINS=$BETTER_AUTH_TRUSTED_ORIGINS

ARG GOOGLE_CLIENT_ID
ENV GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID

ARG GOOGLE_CLIENT_SECRET
ENV GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET

ARG RESEND_API_KEY
ENV RESEND_API_KEY=$RESEND_API_KEY

ARG RESEND_FROM
ENV RESEND_FROM=$RESEND_FROM

ARG DATABASE_URL
ENV DATABASE_URL=$DATABASE_URL

ARG CONTACT_COMPANY
ENV CONTACT_COMPANY=$CONTACT_COMPANY

ARG CONTACT_ADDRESS
ENV CONTACT_ADDRESS=$CONTACT_ADDRESS

ARG CONTACT_GRIEVANCE_ADDRESS
ENV CONTACT_GRIEVANCE_ADDRESS=$CONTACT_GRIEVANCE_ADDRESS

ARG CONTACT_EMAIL
ENV CONTACT_EMAIL=$CONTACT_EMAIL

ARG CONTACT_PHONE
ENV CONTACT_PHONE=$CONTACT_PHONE

RUN pnpm run build

# Prune to production deps for runtime
FROM build AS prod-deps
RUN pnpm prune --prod --ignore-scripts

# Runtime image 
FROM base AS runner
RUN apt-get update && apt-get install -y --no-install-recommends libsqlite3-0 \
  && rm -rf /var/lib/apt/lists/*

ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

WORKDIR /app
COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=build /app/.output ./.output
RUN rm -rf /app/.output/server/node_modules \
  && ln -s /app/node_modules /app/.output/server/node_modules

EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]

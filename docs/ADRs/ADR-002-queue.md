# ADR-002: Event Queue is Redpanda (Kafka-compatible)
Status: Accepted (M1)
Date: 2025-01-01

## Context
We require a Kafka-compatible queue for demo and future scale, but want a simpler local developer experience.

## Decision
Adopt Redpanda as the Kafka-compatible broker for local development and demos. For M1, a file-based NDJSON stub is allowed as a fallback to simplify local runs when Redpanda is unavailable.

## Consequences
- Pros: single binary, simpler operations, Kafka API compatible, great local DX.
- Cons: still a distributed system; containers increase resource usage.
- NDJSON fallback reduces infra friction for first-run demos at the cost of skipping queue semantics.

## Alternatives
- Apache Kafka (vanilla): heavier Zookeeper/Kraft management; more ops locally.
- RabbitMQ: not Kafka API; different semantics from target design.

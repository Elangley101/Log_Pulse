# ADR-002: Event Queue is Redpanda (Kafka-compatible)
## Context
We require a Kafka-compatible queue for demo and future scale, but want a simpler local developer experience.

## Decision
Adopt Redpanda as the Kafka-compatible broker for local development and demos.

## Consequences
- Pros: single binary, simpler operations, Kafka API compatible, great local DX.
- Cons: still a distributed system; containers increase resource usage.

## Alternatives
- Apache Kafka (vanilla): heavier Zookeeper/Kraft management; more ops locally.
- RabbitMQ: not Kafka API; different semantics from target design.

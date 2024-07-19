# SwiftMend: Detecting and Repairing Activity Label Quality Issues in Process Event Streams

<p align="center">
  <img src="logo.png" width=250 alt="SwiftMend Diagram"/>
</p>

SwiftMend is a novel approach for dynamically detecting and repairing synonymous, polluted, and distorted activity labels in process event streams (PES). This solution addresses a critical gap in online process mining by improving the quality of input data in real-time streaming environments.

## Key Features

- Real-time imperfect label detection and control flow updates
- Dynamic activity similarity reassessment
- Semantic activity clustering via customized incremental hierarchical clustering
- Frequency- and recency-based label selection for dynamic repair
- Adaptive historical data management using a Lossy Counting-inspired decay mechanism

## Repository Contents

This repository contains:
- Scripts for data generation
- Execution logs from experiments
- Scripts for performance calculations

## Background

Process Mining techniques extract insights from event logs to discover, monitor, and improve business processes. The quality of input data significantly impacts the reliability and accuracy of these insights. SwiftMend focuses on addressing process-data quality (PDQ) issues in PES beyond anomalous events or traces.

## Methodology

SwiftMend employs:
- Memory-efficient approximate data structures
- An incremental hierarchical clustering algorithm
- Decaying and forgetting mechanisms

These components work together to ensure efficiency and adaptability in streaming contexts.

## Evaluation

The approach was validated using publicly available real-life logs from two hospitals:

Experiments included:
- Baseline comparison against an existing offline technique
- Sensitivity analysis to assess performance under changing configurations and log characteristics


## Implementation

SwiftMend is implemented as a Java-based prototype and is available as a plugin in the open-source PraeclarusPDQ framework (https://github.com/praeclaruspdq/PraeclarusPDQ).



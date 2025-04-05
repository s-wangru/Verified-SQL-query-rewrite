# Verified LLM SQL Query Rewrite: Design Doc

## Overview

This project optimizes SQL queries by providing a LLM with table schema and statistics, prompting it to generate a new query, and then verifying semantic equivalence using semantic prover and running both queries on generated datasets to check for identical outputs. It explores how LLMs can contribute to database management by learning to optimize queries while maintaining correctness, providing insights into the potential of AI in query optimization.

## Scope
This project is a standalone system that operates independently of existing components, relying solely on the LLM for query generation, a semantic prover for verification, and DuckDB for query execution. It does not modify any parts of the existing DBMSs.

## Glossary (Optional)

>If you are introducing new concepts or giving unintuitive names to components, write them down here.

## Architectural Design (TODO)
>Explain the input and output of the component, describe interactions and breakdown the smaller components if any. Include diagrams if appropriate.

## Design Rationale (TODO)
>Explain the goals of this design and how the design achieves these goals. Present alternatives considered and document why they are not chosen.

## Testing Plan (TODO)
>How should the component be tested?

## Trade-offs and Potential Problems (TODO)
>Write down any conscious trade-off you made that can be problematic in the future, or any problems discovered during the design process that remain unaddressed (technical debts).

## Future Work (TODO)
>Write down future work to fix known problems or otherwise improve the component.
# Basic Database Implementation

This project implements a basic database-like storage solution in Python. It is designed for educational purposes to gain an understanding of key database concepts, design patterns, and code modularity.

## Objective

The main objective of this project is to create a simplified database-like system that demonstrates essential concepts, including key-value storage, sorted blocks, temporary and persistent storage, and basic read and write operations.

## Features

- **Line Class:** Represents individual key-value pairs.
- **SortedBlock Class:** Manages sorted blocks of key-value pairs, with support for getting, setting, and merging operations.
- **TemporaryWrite Class:** Provides temporary write storage for incoming data, with automatic transfer to persistent storage on overflow.
- **PersistentRead Class:** Handles reading and merging of data from a persistent storage file.
- **Storage Class:** Integrates temporary and persistent storage to provide a complete storage solution.

## Usage

1. Clone the repository.
2. Navigate to the project directory
3. Run the unit tests: `python -m unittest discover tests`

## Current State and Limitations

- The current implementation is a basic educational project and may not be suitable for production use.
- This loads all the data in RAM when started and the uses binary search to get which can be bottleneck and can be resolved by distributed read files instead of maintaining single persistent file.
- The system's efficiency and performance may not be optimized for handling large datasets and high concurrency.

## Potential Improvements

- Add the distributed persistent read files instead of single file because loading all the data to the disc may not be feasible.
- Implement advanced indexing and data structures to enhance data retrieval efficiency.
- Explore parallel processing and optimized storage mechanisms for better performance with larger datasets.
- Consider implementing caching mechanisms to reduce disk I/O and improve read speeds.
- Introduce concurrency control mechanisms to handle simultaneous read and write operations.

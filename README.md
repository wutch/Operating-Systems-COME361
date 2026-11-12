# Operating-Systems
Memory Management Simulator

## Project Description

This project is developed for our COME361 course. The goal is to simulate different memory allocation algorithms and compare how they manage available memory.

## Problem Definition

Memory management is an important part of operating systems. Since computers have limited memory the operating system needs to allocate memory to processes efficiently.

Different memory allocation algorithms can affect memory usage and fragmentation. Our project aims to demonstrate how these algorithms work and compare their results.

## Second week new features

For the second project week we improved our Memory Management Simulator by adding new features to the main program.

### 1. Custom Memory Input
Users can now enter their own memory block sizes and process memory requirements instead of using only predefined values.

### 2. Algorithm Comparison
The program allows users to run First Fit, Best Fit, and Worst Fit using the same memory blocks and process sizes to compare their allocation results.

### 3. Memory Usage Metrics
We added a new `metrics.py` module to calculate:

- Allocated processes
- Failed allocations
- Total used memory
- Remaining free memory
- Largest available free block
- Memory utilization percentage
- A simplified fragmentation indicator

### 4. Export Results
Users can save the comparison results to a text file named `memory_report.txt`.

### 5. How to Run

Run the program using:

```bash
python main.py
```

The main menu provides the following options:

```text
1. First Fit
2. Best Fit
3. Worst Fit
4. Compare all algorithms
5. Enter custom memory blocks and process sizes
6. Save comparison report to a text file
0. Exit
```

To compare all algorithms directly, run:

```bash
python main.py --compare
```
### 6. Testing and Validation

A new test_memory.py module was added using Python's built-in unittest framework to verify the First Fit, Best Fit, and Worst Fit algorithms.

Five test scenarios were implemented:

  1- Normal memory allocation.

  2- Insufficient memory.

  3- External fragmentation.

  4- Empty memory.

  5- Original memory input preservation.

The tests also verify memory allocation results and related metrics.

Run Tests:

python -m unittest test_memory.py -v

A successful run displays OK in the terminal.

### 7. Current Project Status

The three memory allocation algorithms are integrated into the main program. Users can enter custom data, compare allocation results, view memory statistics, and export reports.

5 test scenarios have been implemented.

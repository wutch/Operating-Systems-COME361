def calculate_metrics(blocks, processes, allocation, remaining):

    initial_free = sum(blocks)

    allocated_sizes = [
        size
        for size, index in zip(processes, allocation)
        if index != -1
    ]

    used = sum(allocated_sizes)

    total_free = sum(remaining)

    largest_free = max(remaining, default=0)

    allocated = len(allocated_sizes)

    failed = len(processes) - allocated

    if initial_free > 0:
        utilization = (used / initial_free) * 100
    else:
        utilization = 0.0

    if total_free > 0:
        fragmentation_indicator = (
            1 - largest_free / total_free
        ) * 100
    else:
        fragmentation_indicator = 0.0

    return {
        "allocated": allocated,
        "failed": failed,
        "used": used,
        "total_free": total_free,
        "largest_free": largest_free,
        "utilization": utilization,
        "fragmentation_indicator": fragmentation_indicator
    }

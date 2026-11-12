import argparse
from pathlib import Path

from first_fit import first_fit
from best_fit import best_fit
from worst_fit import worst_fit
from metrics import calculate_metrics


ALGORITHMS = {
    "1": ("First Fit", first_fit),
    "2": ("Best Fit", best_fit),
    "3": ("Worst Fit", worst_fit),
}


def read_sizes(prompt):
    while True:
        raw = input(prompt)

        try:
            sizes = [int(part.strip()) for part in raw.split(",")]

            if not sizes or any(size <= 0 for size in sizes):
                raise ValueError

            return sizes

        except ValueError:
            print("Invalid input. Enter positive whole numbers.")
            print("Example: 100,500,200")


def format_result(name, algorithm, blocks, processes):

    allocation, remaining = algorithm(blocks, processes)

    stats = calculate_metrics(
        blocks, processes, allocation, remaining
    )

    lines = [
        f"\n{name}",
        "-" * 45,
        "Process | Size (MB) | Assigned Block"
    ]

    for i, (size, index) in enumerate(
        zip(processes, allocation), start=1
    ):
        if index == -1:
            assigned = "Not Allocated"
        else:
            assigned = f"Block {index + 1}"

        lines.append(
            f"P{i:<6} | {size:<9} | {assigned}"
        )

    lines.extend([
        f"Remaining memory in each block (MB): {remaining}",
        f"Allocated processes: {stats['allocated']}/{len(processes)}",
        f"Failed allocations: {stats['failed']}",
        f"Memory used: {stats['used']} MB",
        f"Total free memory: {stats['total_free']} MB",
        f"Largest free block: {stats['largest_free']} MB",
        f"Memory utilization: {stats['utilization']:.1f}%",
        f"Fragmentation indicator: {stats['fragmentation_indicator']:.1f}%",
    ])

    return "\n".join(lines)


def generate_report(blocks, processes, selection="4"):

    if not blocks or not processes or any(
        not isinstance(size, int) or size <= 0
        for size in blocks + processes
    ):
        raise ValueError(
            "Blocks and process sizes must be positive integers."
        )

    lines = [
        "MEMORY MANAGEMENT SIMULATOR",
        f"Initial blocks (MB): {blocks}",
        f"Process requests (MB): {processes}",
    ]

    if selection == "4":
        choices = ALGORITHMS.values()
    else:
        choices = [ALGORITHMS[selection]]

    for name, algorithm in choices:
        lines.append(
            format_result(name, algorithm, blocks, processes)
        )

    lines.append(
        "\nNote: Fragmentation indicator = "
        "(1 - largest free block / total free memory) x 100."
    )
    lines.append(
        "This is a simplified indicator, "
        "not a complete fragmentation measurement."
    )

    return "\n".join(lines)


def save_report(report, filename):

    Path(filename).write_text(
        report + "\n",
        encoding="utf-8"
    )

    print(f"Report saved to {filename}")


def interactive_menu():

    blocks = [100, 500, 200, 300]
    processes = [180, 250, 100]

    while True:

        print("\nMEMORY MANAGEMENT SIMULATOR")
        print("1. First Fit")
        print("2. Best Fit")
        print("3. Worst Fit")
        print("4. Compare all algorithms")
        print("5. Enter custom memory blocks and process sizes")
        print("6. Save comparison report to a text file")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice in ("1", "2", "3", "4"):

            print(
                generate_report(blocks, processes, choice)
            )

        elif choice == "5":

            blocks = read_sizes(
                "Enter free block sizes (MB), separated by commas: "
            )

            processes = read_sizes(
                "Enter process sizes (MB), separated by commas: "
            )

            print("Input values updated.")

        elif choice == "6":

            report = generate_report(blocks, processes)

            save_report(report, "memory_report.txt")

        elif choice == "0":

            print("Goodbye!")
            return

        else:
            print("Invalid selection. Try again.")


def main():

    parser = argparse.ArgumentParser(
        description="Memory allocation simulator"
    )

    parser.add_argument(
        "--compare",
        action="store_true",
        help="compare all algorithms using default data"
    )

    parser.add_argument(
        "--output",
        metavar="FILE",
        help="save comparison output as a text file"
    )

    args = parser.parse_args()

    if args.output and not args.compare:
        parser.error("--output requires --compare")

    if args.compare:

        report = generate_report(
            [100, 500, 200, 300],
            [180, 250, 100]
        )

        print(report)

        if args.output:
            save_report(report, args.output)

    else:
        try:
            interactive_menu()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")


if __name__ == "__main__":
    main()
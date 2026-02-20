import csv

INPUT_FILE = "Assignment python.csv"
OUTPUT_FILE = "filtered-sales-data.csv"


def read_sales_data(filename):
    rows = []

    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                price = float(row["price"])
                sqft = float(row["sq__ft"])

                if sqft <= 0:
                    continue

                price_per_sqft = price / sqft

                row["price_per_sqft"] = round(price_per_sqft, 2)
                rows.append(row)

            except (ValueError, KeyError):
                continue

    return rows


def calculate_average_price_per_sqft(rows):
    total = sum(float(row["price_per_sqft"]) for row in rows)
    return total / len(rows) if rows else 0


def write_filtered_data(rows, average):
    filtered_rows = [
        row for row in rows
        if float(row["price_per_sqft"]) < average
    ]

    fieldnames = filtered_rows[0].keys()

    with open(OUTPUT_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"Average price per square foot: {round(average, 2)}")
    print(f"{len(filtered_rows)} properties written to {OUTPUT_FILE}")


def main():
    rows = read_sales_data(INPUT_FILE)
    average = calculate_average_price_per_sqft(rows)
    write_filtered_data(rows, average)


if __name__ == "__main__":
    main()
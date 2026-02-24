import csv

INPUT_FILE = "Assignment python.csv"
OUTPUT_FILE = "filtered-sales-data.csv"


def read_sales_data(filename):
    rows = []

    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

        for row in reader:
            rows.append(row)

    if fieldnames and "price_per_sqft" not in fieldnames:
        fieldnames = fieldnames + ["price_per_sqft"]

    return rows, fieldnames


def calculate_average_price_per_sqft(rows):
    if not rows:
        return 0

    total = 0
    valid_count = 0

    for row in rows:
        try:
            price = float(row["price"])
            sqft = float(row["sq__ft"])

            if sqft <= 0:
                continue

            price_per_sqft = round(price / sqft, 2)
            row["price_per_sqft"] = price_per_sqft  # enrich row here

            total += price_per_sqft
            valid_count += 1

        except (KeyError, ValueError):
            continue

    return total / valid_count if valid_count > 0 else 0


def write_filtered_data(rows, average,fieldnames):
    filtered_rows = [
        row for row in rows
        if "price_per_sqft" in row and float(row["price_per_sqft"]) < average
    ]

    if not filtered_rows:
        print("No properties found below average price per sqft.")
        return

    with open(OUTPUT_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"Average price per square foot: {round(average, 2)}")
    print(f"{len(filtered_rows)} properties written to {OUTPUT_FILE}")


def main():
    rows, fieldnames = read_sales_data(INPUT_FILE)
    average = calculate_average_price_per_sqft(rows)
    write_filtered_data(rows, average, fieldnames)


if __name__ == "__main__":
    main()
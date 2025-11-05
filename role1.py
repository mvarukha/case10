import json


def read_csv_file(filename: str) -> list:
    """
    Read CSV files and return data as a list of dictionaries.
    Handles various CSV formats including problematic ones.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

            lines = []
            for line in content.split('\n'):
                clean_line = line.strip()
                if clean_line:
                    if clean_line.startswith('"') and clean_line.endswith('"'):
                        clean_line = clean_line[1:-1]
                    lines.append(clean_line)

            if not lines:
                return []

            first_line = lines[0]
            headers = []
            current_field = ""
            in_quotes = False

            for char in first_line:
                if char == '"':
                    in_quotes = not in_quotes
                elif char == ',' and not in_quotes:
                    headers.append(current_field.strip())
                    current_field = ""
                else:
                    current_field += char
            headers.append(current_field.strip())

            data = []
            for line in lines[1:]:
                if not line.strip():
                    continue

                values = []
                current_value = ""
                in_quotes = False

                for char in line:
                    if char == '"':
                        in_quotes = not in_quotes
                    elif char == ',' and not in_quotes:
                        values.append(current_value.strip())
                        current_value = ""
                    else:
                        current_value += char
                values.append(current_value.strip())

                try:
                    row_dict = {}
                    for i, header in enumerate(headers):
                        if i < len(values):
                            value = values[i]
                            if header == 'amount':
                                try:
                                    value = float(value)
                                except ValueError:
                                    value = 0.0
                            row_dict[header] = value

                    data.append(row_dict)

                except Exception as e:
                    print(f"Warning: Skipping malformed row: {e}")
                    continue

            return data

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []


def read_json_file(filename: str) -> list:
    """
    Reads JSON file and returns data as list of dictionaries.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                return []

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return []


def import_financial_data(filename: str) -> list:
    """
    Import financial data from CSV or JSON files.
    """
    if filename.lower().endswith('.csv'):
        data = read_csv_file(filename)
    elif filename.lower().endswith('.json'):
        data = read_json_file(filename)
    else:
        print(f"Error: Unsupported file type '{filename}'")
        return []

    transactions = []
    for item in data:
        if not isinstance(item, dict):
            continue

        transaction = {
            'date': item.get('date', ''),
            'amount': float(item.get('amount', 0)),
            'description': item.get('description', ''),
            'type': item.get('type', '')
        }
        transactions.append(transaction)

    return transactions
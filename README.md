# py-nuban

Lightweight Python utility package to detect possible Nigerian banks for a given
Nigerian Bank Account Number. Useful for validation, or bank account suggestions in payment flows.

## Installation

Install from PyPI when published:

		pip install py-nuban

Or install for development from the repository root:

		pip install -e .

## Quick start

```python
from py_nuban import get_possible_banks

banks = get_possible_banks("1901880678")
print(banks)  # e.g. [('033', 'United Bank for Africa'), ('044', 'Access Bank Nigeria')]
```

## What this package does

- Validates a 10-digit NUBAN account number (type and length checks).
- Runs the NUBAN checksum algorithm against all known bank codes and
	returns the banks whose code+serial produce the same check digit.
- Adds simple heuristics for phone-linked accounts and Moniepoint-style
	accounts so those non-standard account numbers are also considered.
- Filters results by a manually-assigned `popularity` score to surface
	commonly used banks first.

## NUBAN algorithm

To validate a Nigerian bank account number, the system uses the official NUBAN check-digit algorithm. Here's how it works:
The account number consists of a bank code, a serial number(the first 9 digits of an account number), and a check digit(the last digit of an account number). Because Nigerian banks use bank codes of different lengths (3, 5, or 6 digits), the code first normalizes every bank code to a standard format:

3-digit codes get padded with 000 at the front.
5-digit codes get a 9 added at the front.
6-digit codes are used as-is.

This normalized bank code is then combined with the serial number portion of the account to form a 15-character string. Each of these 15 digits is multiplied by a specific weight from this sequence:

`[3, 7, 3, 3, 7, 3, 3, 7, 3, 3, 7, 3, 3, 7, 3]`

All the results are added together. The system then calculates what the correct check digit should be (using modulo 10 arithmetic). If the calculated check digit matches the one provided in the account number, the NUBAN is considered valid for that bank.
This process is repeated across all known banks until a match is found. The result is a reliable way to verify that an account number is correctly formed for its issuing bank.

Example (demo):

```python
# account: 1901880678
# serial = '190188067'  (first 9 digits)
# check  = '8'          (last digit)
from py_nuban import get_possible_banks
print(get_possible_banks('1901880678'))
# Example output (depends on the bundled bank data):
# [('033', 'United Bank for Africa'), ('044', 'Access Bank Nigeria')]
```

## Limitations and how this package helps

- Many new or smaller microfinance/payment institutions sometimes use non-standard codes 
    and algorithms to generate their account numbers.
    That means the NUBAN check alone can miss or misidentify such accounts.
- To reduce false positives and surface useful results we:
	- Add simple prefix checks (common phone-number prefixes) to detect
		phone-linked accounts and include microfinance providers where
		applicable.
	- Use a manual `popularity` numeric field per bank in the bundled data to
		filter out rarely-used entries. This is a pragmatic heuristic to make
		results more useful in real apps; it is not a guarantee of correctness.

These heuristics make the library more practical, but they
also introduce opinionated filtering.

## Accuracy and safety notes

- Results are a best-effort list of candidate banks, not absolute
	guarantees. Always treat matches as suggestions and confirm with a
	reliable resolver service (like Korapay) or the bank when accuracy is critical.
    You should also ideally provide a fallback for the user to select the bank they use manually

## Contributing

Contributions welcome. Please open an issue for data updates, bug reports,
or feature requests. Include tests and small focused changes. Add a unit
test under `tests/` and update documentation as needed.

## License

This project is MIT licensed, see the `LICENSE` file for details.


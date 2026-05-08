from . import banks
from . import helpers

def get_possible_banks(account_no: str) -> list[tuple]:
    """Identify possible Nigerian banks for a given Nigerian account number.

    Validates a Nigerian Uniform Bank Account Number (NUBAN) and returns a list
    of banks that the account number could belong to. The detection uses the
    NUBAN checksum algorithm and applies heuristics for special account types
    (phone-linked accounts, Moniepoint accounts).

    Args:
        account_no: A 10-digit Nigerian account number as a string.

    Returns:
        A list of tuples, each containing (bank_code, bank_name) for banks that
        match the account number. Only banks with popularity > 8 are returned.
        Returns an empty list if no matching banks are found.

    Raises:
        TypeError: If account_no is not a string.
        ValueError: If account_no is not exactly 10 digits.

    Examples:
        >>> get_possible_banks("1901880678")
        [('033', 'United Bank for Africa'), ('044', 'Access Bank Nigeria'), ('011', 'First Bank of Nigeria')]
    """
    helpers.validate_account_number(account_no)

    possible_codes: set = get_set_of_possible_codes(account_no)
    
    if helpers.looks_like_phone_number(account_no):
        possible_codes.add("305") # Opay
        possible_codes.add("100033") # Palmpay
        possible_codes.add("090405") # Moniepoint 

    if not helpers.looks_like_phone_number(account_no):
        possible_codes.discard("305")
        possible_codes.discard("100033")
        possible_codes.discard("090405")

    if helpers.looks_like_moniepoint_number(account_no):
        possible_codes.add("090405")

    banks_names: list[tuple] = _get_popular_banks_from_codes(possible_codes)
    return banks_names # shape -> [(code,name)]

def _get_popular_banks_from_codes(codes: set) -> list[tuple]:
    bank_information = []
    for code in codes:
        bank_name_and_popularity: tuple[str,str] = _get_bank_name_and_popularity_from_code(code)
        popularity = int(bank_name_and_popularity[1])
        if popularity>8:
            bank_information.append((code,bank_name_and_popularity[0]))
    return bank_information

def _get_bank_name_and_popularity_from_code(code) -> tuple:
    for bank in banks.get_banks():
        if code == bank["code"]:
            return (bank["name"],bank["popularity"])
    return tuple()

def get_set_of_possible_codes(account_no: str) -> set:
    """Validate a NUBAN account number against bank codes using the NUBAN algorithm.

    Implements the Nigerian Uniform Bank Account Number (NUBAN) checksum validation
    algorithm. For each bank code, applies the algorithm with the given serial number
    and check digit extracted from the account number, 
    returning all bank codes that produce a valid checksum.

    Args:
        account_no: A 10-digit Nigerian account number as a string.

    Returns:
        A set of bank codes (as strings) for which the NUBAN checksum is valid.
        Returns an empty set if no bank codes produce a valid checksum.

    Raises:
        TypeError: If account_no is not a string.
        ValueError: If account_no is not exactly 10 digits.

    Examples:
        >>> get_set_of_possible_codes("1901880678")
        {'033', '044', '011', ...}
    """
    helpers.validate_account_number(account_no)

    check_digit = account_no[-1] # Get the last digit of the account number
    serial_number = account_no[:-1] # Get the first 9 digits of the account number

    if not isinstance(serial_number, str):
        raise TypeError("Serial number must be a string")
    if not isinstance(check_digit, str):
        raise TypeError("Check digit must be a string")
    if len(serial_number) != 9 or not serial_number.isdigit():
        raise ValueError("Serial number must be 9 digits")
    set_of_possible_codes = set()
    weights = [3,7,3,3,7,3,3,7,3,3,7,3,3,7,3]
    codes_list = _get_all_normalized_bank_codes()
    for code_dict in codes_list:
        total_sum = 0
        full_check = list(code_dict["normalized"]+serial_number) # Concatenate the normalized bank code with the serial number
        for idx,weight in enumerate(weights):
            total_sum = weight*int(full_check[idx]) + total_sum
        if total_sum%10 == 0:
            last_digit_comparison = 0
        else:
            last_digit_comparison = 10 - total_sum%10
        if str(last_digit_comparison) == check_digit:
            set_of_possible_codes.add(code_dict["code"])
    return set_of_possible_codes

def _get_all_normalized_bank_codes() -> list[dict]:
    """
    Adds a padding to ensure all bank codes are 6 digits
    """
    list_of_all_codes = []
    for bank in banks.get_banks():
        if len(bank["code"]) == 3:
            list_of_all_codes.append(
                {
                "code":bank["code"],
                "normalized": "000"+bank["code"]
                }
            )
        elif len(bank["code"]) == 5:
            list_of_all_codes.append(
                {
                "code":bank["code"],
                "normalized": "9"+bank["code"]
                }
            )
        elif len(bank["code"]) == 6:
            list_of_all_codes.append(
                {
                "code":bank["code"],
                "normalized": bank["code"]
                }
            )
        else:
            continue
    return list_of_all_codes
import banks
import helpers

def get_possible_banks(account_no: str) -> list[tuple]:
    if not isinstance(account_no, str):
        raise TypeError("Account number must be a string")
    if len(account_no) != 10 or not account_no.isdigit():
        raise ValueError("Account number must be 10 digits")
    
    check_digit = account_no[-1] # Get the last digit of the account number
    serial_number = account_no[:-1] # Get the first 9 digits of the account number
    possible_codes: set = get_set_of_possible_codes(serial_number, check_digit)
    
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

def get_set_of_possible_codes(serial_number: str, check_digit: str) -> set:
    """
    The NUBAN Algorithm
    """
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
        sum = 0
        full_check = list(code_dict["normalized"]+serial_number) # Concatenate the normalized bank code with the serial number
        for idx,weight in enumerate(weights):
            sum = weight*int(full_check[idx]) + sum
        if sum%10 == 0:
            last_digit_comparison = 0
        else:
            last_digit_comparison = 10 - sum%10
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
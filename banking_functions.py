from typing import TextIO

# Constants
# client_to_accounts value indexing
BALANCES = 0
INTEREST_RATES = 1

# transaction codes
WITHDRAW_CODE = -1
DEPOSIT_CODE = 1

# interest rates
LOAN_INTEREST_RATE = 2.2  # percent
LOAN_INTEREST_SCALE = 1.13

# loan approval
LOAN_APPROVAL_CUTOFF = 5

def create_example_cta() -> dict[tuple[str, int], list[list[float]]]:
    """Return an example clients to accounts dictionary.
    This can be used as a helper function when writing docstring examples.
    """

    return {
        ("Karla Hurst", 770898021): [[768.0, 2070.0], [0.92, 1.5]],
        ("Pamela Dickson", 971875372): [
            [
                36358866.0,
                5395448.0,
                23045442.0,
                14316660.0,
                45068981.0,
                4438330.0,
                16260321.0,
                7491204.0,
                23330669.0,
            ],
            [2.3, 2.35, 2.25, 2.35, 2.05, 2.1, 2.45, 2.4, 2.0],
        ],
        ("Roland Lozano", 853887123): [
            [1585.0, 1170.0, 1401.0, 3673.0],
            [0.63, 0.05, 0.34, 0.92],
        ],
    }


def create_example_ctb() -> dict[tuple[str, int], float]:
    """Return an example clients to total balance dictionary.
    This can be used as a helper function when writing docstring examples.
    """

    return {
        ("Karla Hurst", 770898021): 2838.0,
        ("Pamela Dickson", 971875372): 175705921.0,
        ("Roland Lozano", 853887123): 7829.0,
    }


def create_example_client() -> tuple[str, int]:
    """Return an example client tuple.
    This can be used as a helper function when writing docstring examples.
    """
    return ("Karla Hurst", 770898021)


def display_client_accounts(
    client_to_accounts: dict[tuple[str, int], list[list[float]]],
    client: tuple[str, int],
) -> None:
    """Display the indicated client's account balances in a human-friendly
    format, using the client_to_account dictionary.

    The first account is a chequing account, followed by subsequent savings
    account(s). Loan accounts, if present, will be at the end of the accounts
    and determined by their negative balance.

    Preconditions:
        - client in client_to_accounts
    """

    i = 0
    for account in client_to_accounts[client][BALANCES]:
        if i == 0:
            # the first account is always a chequing account
            print("Chequing Account")
        elif account > 0:
            print(f"Savings Account {i}")
        else:
            print("Loan Account")
        print(f"$ {account:.2f}")
        i += 1


def get_fv(present_value: float, r: float, n: int) -> float:
    """Return the future value calculated using the given present value (pv)
    growing with rate of return (interest rate) r, compounded annually,
    for a total of n years.

    r is given as a percentage value.

    Preconditions:
        - 0 <= r <= 100
        - n >= 0

    >>> get_fv(1.0, 13, 1)
    1.13
    """
    return present_value * (1 + r / 100) ** n


def get_sd(x: list[float]) -> float:
    """
    Return the standard deviation of the values in the list x.

    >>> get_sd([1.0, 2.0, 3.0])
    0.816496580927726
    """
    n = len(x)
    x_bar = (sum(x)) / n

    sd = 0
    for x_i in x:
        sd += (x_i - x_bar) ** 2

    return (sd / n) ** 0.5


###############################################################################
# Your function implementation
###############################################################################


def load_financial_data(client_data: TextIO) -> dict[tuple[str, int],
                                                     list[list[float]]]:
    """
    Return a dictionary containing a tuple of each client and their SIN as
    a key with their values being a list of list containing the balances of
    of their accounts with the interest rate.

    >>> input_file = open('./data/client_data_1.txt')
    >>> load_financial_data(input_file)
    {('Karla Hurst', 770898021): [[768.0, 2070.0], [0.92, 1.5]],\
 ('Pamela Dickson', 971875372): [[36358866.0, 5395448.0, 23045442.0,\
 14316660.0, 45068981.0, 4438330.0, 16260321.0, 7491204.0, 23330669.0],\
 [2.3, 2.35, 2.25, 2.35, 2.05, 2.1, 2.45, 2.4, 2.0]],\
 ('Roland Lozano', 853887123): [[1585.0, 1170.0, 1401.0, 3673.0],\
 [0.63, 0.05, 0.34, 0.92]]}
    >>> input_file = open('./data/client_data_2.txt')
    >>> load_financial_data(input_file)
    {('Karla Hurst', 770898021): [[768.0, 2070.0], [0.92, 1.5]],\
 ('Maurice Daisy', 770898021): [[768.0, 2070.0], [0.92, 1.5]],\
 ('Pamela Dickson', 971875372): [[36358866.0, 5395448.0, 23045442.0,\
 14316660.0, 45068981.0, 4438330.0, 16260321.0, 7491204.0, 23330669.0],\
 [2.3, 2.35, 2.25, 2.35, 2.05, 2.1, 2.45, 2.4, 2.0]],\
 ('Roland Lozano', 853887123): [[1585.0, 1170.0, 1401.0, 3673.0],\
 [0.63, 0.05, 0.34, 0.92]],\
 ('Louise Revilla', 853887123): [[1585.0, 1170.0, 1401.0, 3673.0],\
 [0.63, 0.05, 0.34, 0.92]], ('Alvin Beacom', 521494658): [[913.0, 733.0],\
 [1.5, 0.63]], ('Heather Callahan', 623827565): [[34302106.0,\
 20328170.0, 39731637.0, 18462373.0, 36642460.0, 39373170.0,\
 28580891.0, 37368572.0, 33702574.0, 21639888.0], [2.05, 2.3,\
 2.15, 2.3, 2.2, 2.4, 2.1, 2.15, 2.2, 2.45]],\
 ('Robert Garza', 133295618): [[44426.0, 24374.0],\
 [1.7, 1.7]], ('Monica Girard', 521494658): [[913.0, 733.0],\
 [1.5, 0.63]], ('Thomas Strohm', 454554353): [[3639.0, 3432.0, 4059.0],\
 [2.08, 2.66, 0.92]]}
    """
    clients_to_accounts = {}
    for f in client_data:
        client_info = []
        client_balances = []
        client_interest = []
        client_account = []
        line = f.strip()
        while line != '':
            if "Chequing" not in line and line[0].isdigit() is False\
               and "Interest" not in line and "Balance" not in line\
               and "Savings" not in line and "Loan" not in line:
                client_info.append(line)
                line = client_data.readline().strip()
            elif line[0].isdigit():
                client_info.append(int(line.replace(" ", "")))
                clients_to_accounts[tuple(client_info)] = []
                line = client_data.readline().strip()
            elif "Chequing" in line:
                line = client_data.readline().strip()
                client_balances.append(float(line[9:]))
                line = client_data.readline().strip()
            elif "Interest" in line:
                client_interest.append(float(line[25:]))
                line = client_data.readline().strip()
            elif "Savings" in line:
                line = client_data.readline().strip()
                client_balances.append(float(line[9:]))
                line = client_data.readline().strip()
            elif "Loan" in line:
                line = client_data.readline().strip()
                client_balances.append(float(line[9:]))
                line = client_data.readline().strip()
        client_account.append(client_balances)
        client_account.append(client_interest)
        clients_to_accounts[tuple(client_info)] = client_account
    return clients_to_accounts


def format_client_accounts(clients_to_accounts: dict[tuple[str, int],
                                                     list[list[float]]],
                           valid_client: tuple[str, int]) -> dict[str, list[
                               list[float]]]:
    """
    Return a new formatted dictionary for the client, valid_client from
    clients_to_accounts. The keys consist of the type of account,
    and the valuesconsist of a list of the balance in each of those accounts
    and their designated interest rate.

    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> format_client_accounts(check, ("Roland Lozano", 853887123))
    {'chequing': [[1585.0], [0.63]], 'savings': [[1170.0, 1401.0, 3673.0],\
 [0.05, 0.34, 0.92]], 'loans': [[], []]}
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> format_client_accounts(check, ("Karla Hurst", 770898021))
    {'chequing': [[768.0], [0.92]], 'savings': [[2070.0], [1.5]],\
 'loans': [[], []]}
    """
    formated_account = {}
    chequing_bal = []
    chequing_interest = []
    chequing = []
    savings_bal = []
    savings_interest = []
    savings = []
    loans_bal = []
    loans_interest = []
    loans = []
    bal = (clients_to_accounts[valid_client][BALANCES])
    inter = (clients_to_accounts[valid_client][INTEREST_RATES])
    for i in range(len(clients_to_accounts[valid_client][BALANCES])):
        if i == 0:
            chequing_bal.append((bal)[i])
            chequing_interest.append((inter)[i])
        elif i > 0 and (clients_to_accounts[valid_client][BALANCES])[i] >= 0:
            savings_bal.append((bal)[i])
            savings_interest.append(inter[i])
        else:
            loans_bal.append((bal)[i])
            loans_interest.append(inter[i])
    chequing.append(chequing_bal)
    chequing.append(chequing_interest)
    savings.append(savings_bal)
    savings.append(savings_interest)
    loans.append(loans_bal)
    loans.append(loans_interest)
    formated_account['chequing'] = chequing
    formated_account['savings'] = savings
    formated_account['loans'] = loans
    return formated_account


def find_average(nums: list[float]) -> float:
    """
    Return a float representing the average of nums

    precondition: len(nums) > 0

    >>> find_average([1,2,3,4,5])
    3.0
    >>> find_average([16,14,6])
    12.0
    """
    i = 0
    for num in nums:
        i += num
    return i / len(nums)


def total_savings_and_loans(clients_to_accounts: dict[tuple[str, int],
                                                      list[list[float]]],
                            valid_client: tuple[str, int]) -> list[float]:
    """
    Return a two-element list that consists of the sum of all
    savings and loan and the sum of the interest_rate for a valid_client
    in clients_to_accounts.
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> total_savings_and_loans(check, ("Karla Hurst", 770898021))
    [2070.0, 1.5]
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> total_savings_and_loans(check, ("Roland Lozano", 853887123))
    [6244.0, 1.31]
    """
    balances_and_interest = [(sum(clients_to_accounts[valid_client][
        BALANCES][1:])), (sum(clients_to_accounts[valid_client][
            INTEREST_RATES][1:]))]
    return balances_and_interest


def clients_to_total_balance(clients_to_accounts: dict[tuple[str, int],
                                                       list[list[float]]]
                             ) -> dict[str, list[list[float]]]:
    """
    Return a new dictionary from clients_to_acocunts with the keys being the
    a two-element tuple of the client's name and SIN and the values being the
    total balance that the respective clients have in their
    accounts(includes chequing, savings and loans)

    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> clients_to_total_balance(check)
    {('Karla Hurst', 770898021): 2838.0,\
 ('Pamela Dickson', 971875372): 175705921.0,\
 ('Roland Lozano', 853887123): 7829.0}
    >>> input_file = open('./data/client_data_2.txt')
    >>> check = load_financial_data(input_file)
    >>> clients_to_total_balance(check)
    {('Karla Hurst', 770898021): 2838.0,\
 ('Maurice Daisy', 770898021): 2838.0,\
 ('Pamela Dickson', 971875372): 175705921.0,\
 ('Roland Lozano', 853887123): 7829.0,\
 ('Louise Revilla', 853887123): 7829.0,\
 ('Alvin Beacom', 521494658): 1646.0,\
 ('Heather Callahan', 623827565): 310131841.0,\
 ('Robert Garza', 133295618): 68800.0,\
 ('Monica Girard', 521494658): 1646.0,\
 ('Thomas Strohm', 454554353): 11130.0}
    """

    total_balance = {}
    for key in clients_to_accounts:
        total_balance[key] = sum(clients_to_accounts[key][BALANCES])
    return total_balance


def validate_identity(clients_to_accounts: dict[tuple[str, int],
                                                list[list[float]]],
                      name: str, sin: int) -> bool:
    """
    Return True if and only if the name and SIN are found as a key within
    the clients_to_accoutns dictionary.
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> validate_identity(check, "Karla Hurst", 770898021)
    True
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> validate_identity(check, "jimmy", 770898021)
    False
    """
    return (name, sin) in clients_to_accounts

input_file = open('./data/client_data_1.txt')
ch1 = load_financial_data(input_file)
validate_identity (ch1, "Karla Hurst", 770898021)


def get_num_accounts(clients_to_accounts: dict[tuple[str, int],
                                               list[list[float]]],
                     valid_client: tuple[str, int]) -> int:
    """
    Return the total number of accounts that the valid_client has within the
    clients_to_accounts dictionary excluding loan accounts.

    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> get_num_accounts(check, ('Karla Hurst', 770898021))
    2
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> get_num_accounts(check, ('Pamela Dickson', 971875372))
    9
    """
    num_accounts = 0
    for item in clients_to_accounts[valid_client][BALANCES]:
        if int(item) >= 0:
            num_accounts += 1
    return num_accounts


def get_account_balance(clients_to_accounts: dict[tuple[str, int],
                                                  list[list[float]]],
                        valid_client: tuple[str, int],
                        account_number: int) -> float:
    """
    Return the balance of the account_number for a valid_client in the
    clients_to_accounts dictionary

    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> get_account_balance(check, ('Pamela Dickson', 971875372), 1)
    5395448.0
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> get_account_balance(check, ('Karla Hurst', 770898021), -1)
    2070.0
    """
    return float(clients_to_accounts[valid_client][BALANCES][account_number])


def open_savings_account(clients_to_accounts: dict[tuple[str, int],
                                                   list[list[float]]],
                         valid_client: tuple[str, int],
                         balance: float,
                         interest_rate: float) -> None:
    """
    Add a savings account to the clients_to_accounts dictionary for
    a valid_client with a certain balance and interest_rate.

    Precondition: balance >= 0 and 0 <= interest_rate <= 100

    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> open_savings_account(check, ('Karla Hurst', 770898021), 500.0, 0.95)
    >>> check
    {('Karla Hurst', 770898021): [[768.0, 2070.0, 500.0], [0.92, 1.5, 0.95]],\
 ('Pamela Dickson', 971875372): [[36358866.0, 5395448.0, 23045442.0,\
 14316660.0, 45068981.0, 4438330.0, 16260321.0, 7491204.0, 23330669.0],\
 [2.3, 2.35, 2.25, 2.35, 2.05, 2.1, 2.45, 2.4, 2.0]],\
 ('Roland Lozano', 853887123): [[1585.0, 1170.0, 1401.0, 3673.0],\
 [0.63, 0.05, 0.34, 0.92]]}
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> open_savings_account(check, ("Pamela Dickson", 971875372), 30.0, 0.25)
    >>> check
    {('Karla Hurst', 770898021): [[768.0, 2070.0], [0.92, 1.5]],\
 ('Pamela Dickson', 971875372): [[36358866.0, 5395448.0, 23045442.0,\
 14316660.0, 45068981.0, 4438330.0, 16260321.0, 7491204.0, 23330669.0,\
 30.0], [2.3, 2.35, 2.25, 2.35, 2.05, 2.1, 2.45, 2.4, 2.0, 0.25]],\
 ('Roland Lozano', 853887123): [[1585.0, 1170.0, 1401.0, 3673.0],\
 [0.63, 0.05, 0.34, 0.92]]}
    """

    values = list(str(clients_to_accounts[valid_client][0]))
    if "-" in values:
        clients_to_accounts[valid_client][BALANCES].insert(-1, balance)
        clients_to_accounts[valid_client][INTEREST_RATES].insert(-1,
                                                                 interest_rate)
    else:
        clients_to_accounts[valid_client][BALANCES].append(balance)
        clients_to_accounts[valid_client][INTEREST_RATES].append(interest_rate)


def get_average_balance(clients_to_accounts: dict[tuple[str, int],
                                                  list[list[float]]]
                        ) -> dict[tuple[str, int], float]:
    """
    Return a new dictionary with the keys being a tuple of the client's name
    and SIN and the values being a float representing the average value of
    the client's account balances, including loan accounts, if they exist.

    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> get_average_balance(check)
    {('Karla Hurst', 770898021): 1419.0,\
 ('Pamela Dickson', 971875372): 19522880.111111112,\
 ('Roland Lozano', 853887123): 1957.25}
    >>> input_file = open('./data/client_data_2.txt')
    >>> check = load_financial_data(input_file)
    >>> get_average_balance(check)
    {('Karla Hurst', 770898021): 1419.0, ('Maurice Daisy', 770898021): 1419.0,\
 ('Pamela Dickson', 971875372): 19522880.111111112,\
 ('Roland Lozano', 853887123): 1957.25,\
 ('Louise Revilla', 853887123): 1957.25,\
 ('Alvin Beacom', 521494658): 823.0,\
 ('Heather Callahan', 623827565): 31013184.1,\
 ('Robert Garza', 133295618): 34400.0,\
 ('Monica Girard', 521494658): 823.0,\
 ('Thomas Strohm', 454554353): 3710.0}
    """
    average_balance = {}
    for key in clients_to_accounts:
        average_balance[key] = find_average(clients_to_accounts[key][0])
    return average_balance


def update_balance(clients_to_accounts: dict[tuple[str, int],
                                             list[list[float]]],
                   valid_client: tuple[str, int],
                   account_number: int, amount_to_change: float,
                   transaction_code: int) -> None:
    """
    Update the clients_to_accounts dictionary, where the client's balance,
    indicated by the account_number is modified by withdrawing the amount
    indicated if the transaction code is WITHDRAW_CODE, or if the transaction
    code is DEPOSIT_CODE, money will be deposited into the account.

    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> update_balance(check, ("Karla Hurst", 770898021), 1, 500,\
    WITHDRAW_CODE)
    >>> check
    {('Karla Hurst', 770898021): [[768.0, 1570.0], [0.92, 1.5]],\
 ('Pamela Dickson', 971875372): [[36358866.0, 5395448.0, 23045442.0,\
 14316660.0, 45068981.0, 4438330.0, 16260321.0, 7491204.0, 23330669.0],\
 [2.3, 2.35, 2.25, 2.35, 2.05, 2.1, 2.45, 2.4, 2.0]],\
 ('Roland Lozano', 853887123): [[1585.0, 1170.0, 1401.0, 3673.0],\
 [0.63, 0.05, 0.34, 0.92]]}
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> update_balance(check, ("Karla Hurst", 770898021), 1, 500, DEPOSIT_CODE)
    >>> check
    {('Karla Hurst', 770898021): [[768.0, 2570.0], [0.92, 1.5]],\
 ('Pamela Dickson', 971875372): [[36358866.0, 5395448.0, 23045442.0,\
 14316660.0, 45068981.0, 4438330.0, 16260321.0, 7491204.0, 23330669.0],\
 [2.3, 2.35, 2.25, 2.35, 2.05, 2.1, 2.45, 2.4, 2.0]],\
 ('Roland Lozano', 853887123): [[1585.0, 1170.0, 1401.0, 3673.0],\
 [0.63, 0.05, 0.34, 0.92]]}
    """
    if transaction_code == WITHDRAW_CODE:
        clients_to_accounts[valid_client][BALANCES][account_number]\
            -= amount_to_change
    elif transaction_code == DEPOSIT_CODE:
        clients_to_accounts[valid_client][BALANCES][account_number]\
            += amount_to_change


def get_loan_score(clients_to_accounts: dict[tuple[str, int],
                                             list[list[float]]],
                   valid_client: tuple[str, int],
                   loan_amount: float) -> int:
    """
    Return an integer that represents the number of points that the
    valid_client in clients_to_accounts accumulates for the requested
    loan_amount.

    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> get_loan_score(check, ("Karla Hurst", 770898021), 500)
    5
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> get_loan_score(check, ("Karla Hurst", 770898021), 10000)
    2
    """
    client_averages = list(get_average_balance(clients_to_accounts).values())
    mu = find_average(client_averages)
    sigma = get_sd(client_averages)
    total_balance = sum(clients_to_accounts[valid_client][BALANCES])
    points = 0
    if total_balance < loan_amount:
        points -= 1
    elif total_balance >= loan_amount:
        points += 1
    for balances in clients_to_accounts[valid_client][BALANCES][1:]:
        if 0 <= balances < (mu - sigma):
            points -= 2
        elif 0 <= balances >= (mu + sigma):
            points += 2
        if 0 <= balances > loan_amount\
           and (format_client_accounts(clients_to_accounts,
                                       valid_client)
                )['loans'][0] == []:
            points += 1
    fv_list = []
    for i in range(len(clients_to_accounts[valid_client][BALANCES][1:])):
        fv_list.append(get_fv(clients_to_accounts[valid_client][BALANCES][i],
                              clients_to_accounts[valid_client]
                              [INTEREST_RATES][i], 5))
    if sum(fv_list) >= 0:
        points += 3
    else:
        points -= 3
    return points


def get_loan_status(clients_to_accounts: dict[tuple[str, int],
                                              list[list[float]]],
                    valid_client: tuple[str, int],
                    loan_amount: float) -> bool:
    """
    Return True if and only if the requested loan amount is approved.
    If the loan amount is approved, this function will modify the clients,
    valid_client, chequing account in clients_to_accounts to increase by
    the loan_amount and a loan account with a negative balance of the
    loan amount will be created at the end of the list.

    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> get_loan_status(check, ("Karla Hurst", 770898021), 500)
    True
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> get_loan_status(check, ("Karla Hurst", 770898021), 10000)
    False
    """
    formated = format_client_accounts(clients_to_accounts, valid_client)
    client_balance = sum(clients_to_accounts[valid_client][BALANCES])
    if client_balance < 0 or sum(formated['savings'][0]) == 0:
        return False
    if get_loan_score(clients_to_accounts, valid_client,
                      loan_amount) >= LOAN_APPROVAL_CUTOFF:
        clients_to_accounts[valid_client][BALANCES][0] += loan_amount
        clients_to_accounts[valid_client][BALANCES].append(-loan_amount)
        if formated['loans'][0] == []:
            clients_to_accounts[valid_client][INTEREST_RATES]\
                .append(LOAN_INTEREST_RATE)
            return True
        else:
            clients_to_accounts[valid_client][
                INTEREST_RATES].append((formated['loans'][1][-1]
                                        * LOAN_INTEREST_SCALE))
            return True
    else:
        return False


def get_financial_range_to_clients(client_to_total_balance: dict[tuple[str,
                                                                       int],
                                                                 float],
                                   list_of_financial_ranges: list[tuple[float,
                                                                        float]]
                                   ) -> dict[tuple[float, float],
                                             list[tuple[str, int]]]:
    """
    Return a new dictionary with the keys being a two-element tuple of
    lowerlimit and upperlimit of the list_of_financial_ranges and the values
    being a sorted list of all the clients that have a total account balance
    within the financial range inclusive. The list is sorted by the names of
    the clients but if there is no difference than the SIN is used to sort
    them.

    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> total_balance = clients_to_total_balance(check)
    >>> list_financial_range = [(100.0, 5000.0), (0.0, 500.0),\
    (6000.0, 100000.0)]
    >>> get_financial_range_to_clients(total_balance, list_financial_range)
    {(100.0, 5000.0): [('Karla Hurst', 770898021)],\
 (6000.0, 100000.0): [('Roland Lozano', 853887123)]}
    >>> input_file = open('./data/client_data_2.txt')
    >>> check = load_financial_data(input_file)
    >>> total_balance = clients_to_total_balance(check)
    >>> list_financial_range = [(100.0, 5000.0), (0.0, 500.0),\
    (6000.0, 100000.0)]
    >>> get_financial_range_to_clients(total_balance, list_financial_range)
    {(100.0, 5000.0): [('Alvin Beacom', 521494658),\
 ('Karla Hurst', 770898021), ('Maurice Daisy', 770898021),\
 ('Monica Girard', 521494658)],\
 (6000.0, 100000.0): [('Louise Revilla', 853887123),\
 ('Robert Garza', 133295618), ('Roland Lozano', 853887123),\
 ('Thomas Strohm', 454554353)]}
    """
    financial_range = {}
    for key in list_of_financial_ranges:
        financial_range[key] = []
    for key, val in client_to_total_balance.items():
        for key2, val2 in financial_range.items():
            if key2[0] <= val <= key2[1]:
                val2.append(key)
    for key, val in financial_range.copy().items():
        if val == []:
            financial_range.pop(key)
    for key, val in financial_range.items():
        val.sort()
    return financial_range


def get_fv_from_accounts(account_balances: list[float],
                         interest_rates: list[float],
                         time_in_years: int) -> float:
    """
    Return a float that represents the future value of the account_balances
    with the interest_rates after time_in_years
    >>> account_bals = [768.0, 2070.0]
    >>> interest_rates = [0.92, 1.5]
    >>> get_fv_from_accounts(account_bals, interest_rates, 2)
    2914.761953519999
    >>> account_bals = [1585.0, 1170.0, 1401.0, 3673.0]
    >>> interest_rates = [0.63, 0.05, 0.34, 0.92]
    >>> get_fv_from_accounts(account_bals, interest_rates, 2)
    7927.641279430001
    """
    fv_accounts = []
    for i in range(len(account_balances)):
        fv_accounts.append(get_fv(account_balances[i], interest_rates[i],
                                  time_in_years))
    return sum(fv_accounts)


def is_future_secure(client_to_accounts: dict[tuple[str, int],
                                              list[list[float]]],
                     valid_client: tuple[str, int],
                     time_in_years: int) -> bool:
    """
    Return True if and only if the combined future value of all existing
    savings and loan accounts of the client, valid_client, in
    client_to_accounts over the given time_in_years is non-negative.
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> is_future_secure(check, ("Karla Hurst", 770898021), 2)
    True
    >>> input_file = open('./data/client_data_2.txt')
    >>> check = load_financial_data(input_file)
    >>> is_future_secure(check, ("Karla Hurst", 770898021), 1)
    True
    """
    pv_bal = (total_savings_and_loans(client_to_accounts, valid_client))[0]
    pv_interest = (total_savings_and_loans(client_to_accounts, valid_client)
                   )[1]
    return get_fv(pv_bal, pv_interest, time_in_years) >= 0


def time_to_client_goal(client_to_accounts: dict[tuple[str, int],
                                                 list[list[float]]],
                        valid_client: tuple[str, int],
                        financial_goal: float) -> int:
    """
    Return an int representing the smallest number of integer years it
    would take for the client's, valid_client, total balance in
    client_to_accounts to reach or exceed the financial_goal
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> time_to_client_goal(check, ("Karla Hurst", 770898021), 100000.0)
    255
    >>> input_file = open('./data/client_data_1.txt')
    >>> check = load_financial_data(input_file)
    >>> time_to_client_goal(check, ("Karla Hurst", 770898021), 5000.0)
    30
    """
    years = 0
    total_balance = 0
    i = 0
    while total_balance < financial_goal:
        total_balance = get_fv_from_accounts(client_to_accounts[valid_client]
                                             [BALANCES],
                                             client_to_accounts[valid_client]
                                             [INTEREST_RATES], i)\
            + client_to_accounts[valid_client][BALANCES][0]
        i += 1
        if not total_balance >= financial_goal:
            years += 1
    return years


if __name__ == "__main__":
    import doctest

    doctest.testmod()

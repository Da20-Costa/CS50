from cs50 import get_int

def main():
    credit_card = get_int("Credit Card: ")
    sum_digit = sum_digits(credit_card)
    numDigits = len(str(credit_card))
    amex = isAmex(credit_card, numDigits)
    master = isMaster(credit_card, numDigits)
    visa = isVisa(credit_card, numDigits)
    if sum_digit % 10 != 0:
        print("INVALID")
        exit(0)
    elif amex == True:
        print("AMEX")
    elif master == True:
        print("MASTERCARD")
    elif visa == True:
        print("VISA")
    else:
        print("INVALID")
        exit(0)

def sum_digits(n):
    sum = 0
    AlternateDigit = False
    while n > 0:
        if AlternateDigit == True:
            last_digit = n % 10
            product = multiplyAndSum(last_digit)
            sum += product
        else:
            last_digit = n % 10
            sum += last_digit
        AlternateDigit = not AlternateDigit
        n //= 10
    return sum

def multiplyAndSum(n):
    multiply = n * 2
    sum = 0
    while multiply > 0:
        last_digit = multiply % 10
        sum += last_digit
        multiply //= 10
    return sum

def isAmex(n, p):
    i = p - 2
    first_two_digits = n // 10 ** i
    if p == 15 and first_two_digits == 34 or first_two_digits == 37:
        return True
    else:
        return False

def isMaster(n, p):
    i = p - 2
    first_two_digits = n // 10 ** i
    if p == 16 and 50 < first_two_digits < 56:
        return True
    else:
        return False

def isVisa(n, p):
    if p == 13 or p == 16:
        i = p - 1
        first_digit = n // 10 ** i
        if first_digit == 4:
            return True
        else:
            return False
    return False

main()

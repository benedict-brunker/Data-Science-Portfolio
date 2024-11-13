
def round_rate(rate):
    """
    Function that will round an input float to 4 decimals places.

    Parameters
    ----------
    rate: float
        Rate to be rounded

    Returns
    -------
    float
        Rounded rate
    """
    rounded_rate = round(rate, 4)
    return rounded_rate
    

def reverse_rate(rate):
    """
    Function that will calculate the inverse rate from the provided input rate.
    It will check if the provided input rate is not equal to zero.
    If it not the case, it will calculate the inverse rate and round it to 4 decimal places.
    Otherwise it will return zero.

    Parameters
    ----------
    rate: float
        FX conversion rate to be inverted

    Returns
    -------
    float
        Inverse of input FX conversion rate
    """
    # if input rate is zero, return zero
    if rate == 0:
        return 0
    # else calculate the inverse rate
    else:
        # the inverse rate can be calculated by the formula 1 / rate
        inverse_rate = 1 / rate
        return inverse_rate

  
def format_output(date, from_currency, to_currency, rate, amount):
    """
    Function that will format the output on the streamlit app. 

    Parameters
    ----------
    date: datetime
        The date for a particular FX conversion rate
    
    from_currency: string
        Code for the origin currency.
    
    to_currency: string
        Code for the destination currency. 
    
    rate: float
        The FX rate between from_currency and to_currency.
    
    amount: float
        The volume of the origin currency to be converted.

    Returns
    -------
    string
        A formatted string
    """
    converted_amount = round(amount * rate,2)
    rate = round_rate(rate)
    inverse_rate = round_rate(reverse_rate(rate))
    fstring = f"The conversion rate on {date} from {from_currency} to {to_currency} was {rate}. So {amount} in {from_currency} corresponded to {converted_amount} in {to_currency}. The inverse rate was {inverse_rate}."
    
    return fstring
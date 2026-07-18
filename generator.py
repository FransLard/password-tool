import secrets
import string

def generate_password (length :int =16 ,use_upper :bool =True ,use_lower :bool =True ,use_digits :bool =True ,use_symbols :bool =True ,exclude_similar :bool =False )->str :
    if length <4 :
        length =4
    if length >128 :
        length =128

    chars =""
    mandatory_chars =[]

    if use_lower :
        pool =string .ascii_lowercase
        if exclude_similar :
            pool =pool .translate (str .maketrans ("","","il"))
        chars +=pool
        mandatory_chars .append (secrets .choice (pool ))

    if use_upper :
        pool =string .ascii_uppercase
        if exclude_similar :
            pool =pool .translate (str .maketrans ("","","IO"))
        chars +=pool
        mandatory_chars .append (secrets .choice (pool ))

    if use_digits :
        pool =string .digits
        if exclude_similar :
            pool =pool .translate (str .maketrans ("","","01"))
        chars +=pool
        mandatory_chars .append (secrets .choice (pool ))

    if use_symbols :
        pool ="!@#$%^&*()_+-=[]{}|;:,.<>?"
        chars +=pool
        mandatory_chars .append (secrets .choice (pool ))

    if not chars :
        return ""

    remaining_length =length -len (mandatory_chars )
    if remaining_length <0 :
        mandatory_chars =mandatory_chars [:length ]
        remaining_length =0

    remaining =[secrets .choice (chars )for _ in range (remaining_length )]
    all_chars =mandatory_chars +remaining

    secrets .SystemRandom ().shuffle (all_chars )

    return "".join (all_chars )

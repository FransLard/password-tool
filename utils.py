import math
import re

COMMON_PASSWORDS ={
"123456","password","12345678","qwerty","12345","123456789",
"football","iloveyou","111111","123123","abc123","qwerty123",
"admin","letmein","welcome","monkey","dragon","master",
"sunshine","princess","passw0rd","P@ssw0rd","0123456789",
"trustno1","batman","superman","asdfghjkl","qwertyuiop",
"zaqxswcde","p@$$w0rd","123qweasd","P@ssword","Passw0rd",
"pass123","admin123","root","toor","000000","121212",
}

KEYBOARD_PATTERNS =[
r"qwerty",r"asdfgh",r"zxcvbn",r"qwertyuiop",r"asdfghjkl",
r"zxcvbnm",r"1qaz2wsx",r"qazwsx",r"qweasdzxc",
r"!qaz@wsx",r"1q2w3e4r",r"12qwaszx",
]

SEQUENTIAL_PATTERNS =[
r"123",r"234",r"345",r"456",r"567",r"678",r"789",
r"abc",r"bcd",r"cde",r"def",r"efg",r"fgh",r"ghi",
r"hij",r"ijk",r"jkl",r"klm",r"lmn",r"mno",r"nop",
]

def calculate_entropy (password :str )->float :
    charset_size =0
    if re .search (r"[a-z]",password ):
        charset_size +=26
    if re .search (r"[A-Z]",password ):
        charset_size +=26
    if re .search (r"\d",password ):
        charset_size +=10
    if re .search (r"[^a-zA-Z\d]",password ):
        charset_size +=32

    if charset_size ==0 :
        return 0.0

    return round (len (password )*math .log2 (charset_size ),2 )

def is_common_password (password :str )->bool :
    return password .lower ()in COMMON_PASSWORDS

def has_keyboard_pattern (password :str )->bool :
    lower =password .lower ()
    for pattern in KEYBOARD_PATTERNS :
        if pattern in lower :
            return True
    return False

def has_sequential_pattern (password :str )->bool :
    lower =password .lower ()
    for pattern in SEQUENTIAL_PATTERNS :
        if pattern in lower :
            return True
    return False

def has_date_pattern (password :str )->bool :
    return bool (re .search (r"(19|20)\d{2}",password ))or bool (re .search (r"(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])",password ))

def has_repeated_chars (password :str )->bool :
    return bool (re .search (r"(.)\1{3,}",password ))

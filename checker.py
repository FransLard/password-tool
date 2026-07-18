import re
from utils import (
calculate_entropy ,
is_common_password ,
has_keyboard_pattern ,
has_sequential_pattern ,
has_date_pattern ,
has_repeated_chars ,
)

def check_password (password :str )->dict :
    suggestions =[]
    score =0
    length =len (password )

    if length <8 :
        score +=length *2
    elif length <12 :
        score +=20 +(length -8 )*2
    elif length <16 :
        score +=30 +(length -12 )*2
    else :
        score +=40

    if length <8 :
        suggestions .append (f"Tambah panjang minimal 12 karakter (saat ini {length })")
    elif length <12 :
        suggestions .append (f"Idealnya minimal 12 karakter (saat ini {length })")

    has_upper =bool (re .search (r"[A-Z]",password ))
    has_lower =bool (re .search (r"[a-z]",password ))
    has_digit =bool (re .search (r"\d",password ))
    has_symbol =bool (re .search (r"[^a-zA-Z\d]",password ))

    categories_present =0
    if has_upper :
        score +=10
        categories_present +=1
    else :
        suggestions .append ("Tambah huruf besar (A-Z)")

    if has_lower :
        score +=10
        categories_present +=1
    else :
        suggestions .append ("Tambah huruf kecil (a-z)")

    if has_digit :
        score +=10
        categories_present +=1
    else :
        suggestions .append ("Tambah angka (0-9)")

    if has_symbol :
        score +=15
        categories_present +=1
    else :
        suggestions .append ("Tambah simbol (!@#$%^&* dll)")

    if categories_present >=3 :
        score +=5

    entropy =calculate_entropy (password )
    if entropy <30 :
        score +=0
    elif entropy <50 :
        score +=5
    elif entropy <70 :
        score +=10
    elif entropy <90 :
        score +=15
    else :
        score +=20

    if is_common_password (password ):
        score -=30
        suggestions .append ("Password ini termasuk password umum / mudah ditebak")
    elif is_common_password (password [:8 ]):
        score -=10
        suggestions .append ("Awal password mirip dengan password umum")

    if has_keyboard_pattern (password ):
        score -=10
        suggestions .append ("Hindari pola keyboard berurutan (qwerty, asdfgh, dll)")

    if has_sequential_pattern (password ):
        score -=10
        suggestions .append ("Hindari karakter berurutan (123, abc, dll)")

    if has_date_pattern (password ):
        score -=5
        suggestions .append ("Hindari pola tanggal lahir / tahun")

    if has_repeated_chars (password ):
        score -=5
        suggestions .append ("Hindari karakter berulang (contoh: aaaa)")

    score =max (0 ,min (100 ,score ))

    if score >=80 :
        strength ="SANGAT KUAT"
    elif score >=65 :
        strength ="KUAT"
    elif score >=45 :
        strength ="SEDANG"
    elif score >=25 :
        strength ="LEMAH"
    else :
        strength ="SANGAT LEMAH"

    return {
    "score":score ,
    "strength":strength ,
    "length":length ,
    "entropy":entropy ,
    "has_upper":has_upper ,
    "has_lower":has_lower ,
    "has_digit":has_digit ,
    "has_symbol":has_symbol ,
    "suggestions":suggestions [:5 ],
    }

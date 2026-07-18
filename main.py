import argparse
import sys
from checker import check_password
from generator import generate_password
from utils import calculate_entropy
from breach import check_breach

def print_check_result (password ,result ,entropy ,breach =None ):
    print (f"\n{'='*50 }")
    print (f"  Password  : {'*'*len (password )}")
    print (f"  Panjang   : {result ['length']} karakter")
    print (f"  Entropy   : {entropy } bit")
    print (f"  Skor      : {result ['score']}/100")
    print (f"  Kekuatan  : {result ['strength']}")
    print (f"{'='*50 }")

    if breach :
        if breach ["error"]:
            print (f"  Kebocoran : [ERROR] {breach ['error']}")
        elif breach ["breached"]:
            print (f"  Kebocoran : [BAHAYA] Bocor {breach ['count']}x! Segera ganti password!")
        else :
            print (f"  Kebocoran : [AMAN] Tidak ditemukan di database kebocoran")

    categories =[]
    if result ['has_upper']:
        categories .append ("Huruf Besar")
    if result ['has_lower']:
        categories .append ("Huruf Kecil")
    if result ['has_digit']:
        categories .append ("Angka")
    if result ['has_symbol']:
        categories .append ("Simbol")
    print (f"  Kategori  : {', '.join (categories )if categories else 'Tidak ada'}")

    if result ['suggestions']:
        print (f"{'='*50 }")
        print (f"  Saran Perbaikan:")
        for s in result ['suggestions']:
            print (f"  - {s }")

    print (f"{'='*50 }\n")

def cmd_check (args ):
    result =check_password (args .password )
    entropy =calculate_entropy (args .password )

    breach =None
    if args .breach :
        print ("  Mengecek kebocoran...")
        breach =check_breach (args .password )

    print_check_result (args .password ,result ,entropy ,breach )

def cmd_check_file (args ):
    try :
        with open (args .file ,"r",encoding ="utf-8-sig")as f :
            passwords =[line .strip ()for line in f if line .strip ()]
    except FileNotFoundError :
        print (f"Error: File '{args .file }' tidak ditemukan.")
        sys .exit (1 )

    print (f"\nMemeriksa {len (passwords )} password dari '{args .file }'...\n")

    for i ,pwd in enumerate (passwords ,1 ):
        result =check_password (pwd )
        entropy =calculate_entropy (pwd )

        breach =None
        if args .breach :
            breach =check_breach (pwd )

        print (f"[{i }/{len (passwords )}] {pwd [:20 ]+'...'if len (pwd )>20 else pwd }")
        print (f"      Skor: {result ['score']}/100 | Kekuatan: {result ['strength']} | Entropy: {entropy } bit")
        if breach and not breach ["error"]and breach ["breached"]:
            print (f"      [BAHAYA] Bocor {breach ['count']}x!")
        print ()

def cmd_generate (args ):
    password =generate_password (
    length =args .length ,
    use_upper =args .no_upper is False ,
    use_lower =args .no_lower is False ,
    use_digits =args .no_digits is False ,
    use_symbols =args .no_symbols is False ,
    exclude_similar =args .no_similar ,
    )

    entropy =calculate_entropy (password )
    result =check_password (password )

    print (f"\n{'='*50 }")
    print (f"  Password Generated")
    print (f"{'='*50 }")
    print (f"  Password  : {password }")
    print (f"  Panjang   : {len (password )} karakter")
    print (f"  Entropy   : {entropy } bit")
    print (f"  Skor      : {result ['score']}/100")
    print (f"  Kekuatan  : {result ['strength']}")
    print (f"{'='*50 }\n")

def cmd_gui (args ):
    try :
        from gui import run_gui
        run_gui ()
    except ImportError :
        print ("Error: gui.py tidak ditemukan.")
        sys .exit (1 )

def main ():
    parser =argparse .ArgumentParser (
    prog ="password-tool",
    description ="Password Strength Checker & Generator - alat keamanan password",
    )

    sub =parser .add_subparsers (dest ="command",required =True )

    check_parser =sub .add_parser ("check",help ="Cek kekuatan password")
    check_parser .add_argument ("password",type =str ,help ="Password yang akan dicek")
    check_parser .add_argument ("--breach",action ="store_true",help ="Cek juga kebocoran via Have I Been Pwned")

    check_file_parser =sub .add_parser ("check-file",help ="Cek banyak password dari file")
    check_file_parser .add_argument ("file",type =str ,help ="Path file .txt (satu password per baris)")
    check_file_parser .add_argument ("--breach",action ="store_true",help ="Cek juga kebocoran via Have I Been Pwned")

    gen_parser =sub .add_parser ("generate",aliases =["gen"],help ="Generate strong password")
    gen_parser .add_argument ("-l","--length",type =int ,default =16 ,help ="Panjang password (default: 16)")
    gen_parser .add_argument ("--no-upper",action ="store_true",help ="Jangan pakai huruf besar")
    gen_parser .add_argument ("--no-lower",action ="store_true",help ="Jangan pakai huruf kecil")
    gen_parser .add_argument ("--no-digits",action ="store_true",help ="Jangan pakai angka")
    gen_parser .add_argument ("--no-symbols",action ="store_true",help ="Jangan pakai simbol")
    gen_parser .add_argument ("--no-similar",action ="store_true",help ="Hindari karakter mirip (1,l,0,O)")

    gui_parser =sub .add_parser ("gui",help ="Buka GUI desktop (tkinter)")

    args =parser .parse_args ()

    if args .command =="check":
        cmd_check (args )
    elif args .command in ("generate","gen"):
        cmd_generate (args )
    elif args .command =="check-file":
        cmd_check_file (args )
    elif args .command =="gui":
        cmd_gui (args )

if __name__ =="__main__":
    main ()

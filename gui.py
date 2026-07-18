import tkinter as tk
from tkinter import ttk ,scrolledtext
from checker import check_password
from generator import generate_password
from utils import calculate_entropy
from breach import check_breach

class PasswordToolGUI :
    def __init__ (self ,root ):
        self .root =root
        root .title ("Password Tool")
        root .resizable (False ,False )
        root .configure (padx =15 ,pady =15 )

        notebook =ttk .Notebook (root )
        notebook .pack (fill ="both",expand =True )

        self ._build_check_tab (notebook )
        self ._build_generate_tab (notebook )

    def _build_check_tab (self ,notebook ):
        frame =ttk .Frame (notebook ,padding =15 )
        notebook .add (frame ,text ="Cek Password")

        ttk .Label (frame ,text ="Masukkan Password:",font =("",10 )).pack (anchor ="w")

        self .check_entry =ttk .Entry (frame ,show ="*",width =50 ,font =("",10 ))
        self .check_entry .pack (fill ="x",pady =(5 ,10 ))
        self .check_entry .bind ("<Return>",lambda e :self ._do_check ())

        btn_frame =ttk .Frame (frame )
        btn_frame .pack (fill ="x")

        self .show_var =tk .BooleanVar ()
        ttk .Checkbutton (btn_frame ,text ="Lihat password",variable =self .show_var ,command =self ._toggle_show ).pack (side ="left")

        self .breach_var =tk .BooleanVar (value =True )
        ttk .Checkbutton (btn_frame ,text ="Cek kebocoran (HIBP)",variable =self .breach_var ).pack (side ="left",padx =(10 ,0 ))

        ttk .Button (btn_frame ,text ="Cek",command =self ._do_check ).pack (side ="right")

        self .check_result =scrolledtext .ScrolledText (frame ,height =15 ,width =65 ,state ="disabled",font =("Consolas",9 ))
        self .check_result .pack (fill ="both",pady =(10 ,0 ))

    def _build_generate_tab (self ,notebook ):
        frame =ttk .Frame (notebook ,padding =15 )
        notebook .add (frame ,text ="Generate Password")

        row1 =ttk .Frame (frame )
        row1 .pack (fill ="x",pady =(0 ,10 ))
        ttk .Label (row1 ,text ="Panjang:").pack (side ="left")
        self .length_var =tk .IntVar (value =16 )
        ttk .Spinbox (row1 ,from_ =4 ,to_ =128 ,textvariable =self .length_var ,width =8 ).pack (side ="left",padx =(5 ,0 ))

        row2 =ttk .Frame (frame )
        row2 .pack (fill ="x",pady =(0 ,10 ))

        self .upper_var =tk .BooleanVar (value =True )
        self .lower_var =tk .BooleanVar (value =True )
        self .digit_var =tk .BooleanVar (value =True )
        self .symbol_var =tk .BooleanVar (value =True )
        self .similar_var =tk .BooleanVar (value =False )

        ttk .Checkbutton (row2 ,text ="Huruf Besar",variable =self .upper_var ).pack (side ="left",padx =(0 ,10 ))
        ttk .Checkbutton (row2 ,text ="Huruf Kecil",variable =self .lower_var ).pack (side ="left",padx =(0 ,10 ))
        ttk .Checkbutton (row2 ,text ="Angka",variable =self .digit_var ).pack (side ="left",padx =(0 ,10 ))
        ttk .Checkbutton (row2 ,text ="Simbol",variable =self .symbol_var ).pack (side ="left",padx =(0 ,10 ))
        ttk .Checkbutton (row2 ,text ="Hindari Mirip",variable =self .similar_var ).pack (side ="left")

        ttk .Button (frame ,text ="Generate",command =self ._do_generate ).pack (anchor ="w")

        self .gen_result =scrolledtext .ScrolledText (frame ,height =8 ,width =65 ,state ="disabled",font =("Consolas",9 ))
        self .gen_result .pack (fill ="both",pady =(10 ,0 ))

    def _toggle_show (self ):
        self .check_entry .config (show =""if self .show_var .get ()else "*")

    def _do_check (self ):
        password =self .check_entry .get ()
        if not password :
            self ._set_check_text ("Masukkan password terlebih dahulu.")
            return

        result =check_password (password )
        entropy =calculate_entropy (password )

        lines =[]
        lines .append (f"{'='*50 }")
        lines .append (f"  Password  : {'*'*len (password )}")
        lines .append (f"  Panjang   : {result ['length']} karakter")
        lines .append (f"  Entropy   : {entropy } bit")
        lines .append (f"  Skor      : {result ['score']}/100")
        lines .append (f"  Kekuatan  : {result ['strength']}")
        lines .append (f"{'='*50 }")

        if self .breach_var .get ():
            lines .append ("  Cek kebocoran...")
            self ._set_check_text ("\n".join (lines ))
            self .root .update ()
            breach =check_breach (password )
            if breach ["error"]:
                lines .append (f"  [ERROR] {breach ['error']}")
            elif breach ["breached"]:
                lines .append (f"  [BAHAYA] Bocor {breach ['count']}x! Segera ganti password!")
            else :
                lines .append ("  [AMAN] Tidak ditemukan di database kebocoran")

        categories =[]
        if result ['has_upper']:
            categories .append ("Huruf Besar")
        if result ['has_lower']:
            categories .append ("Huruf Kecil")
        if result ['has_digit']:
            categories .append ("Angka")
        if result ['has_symbol']:
            categories .append ("Simbol")
        lines .append (f"  Kategori  : {', '.join (categories )if categories else 'Tidak ada'}")

        if result ['suggestions']:
            lines .append (f"{'='*50 }")
            lines .append (f"  Saran:")
            for s in result ['suggestions']:
                lines .append (f"  - {s }")

        lines .append (f"{'='*50 }")
        self ._set_check_text ("\n".join (lines ))

    def _do_generate (self ):
        password =generate_password (
        length =self .length_var .get (),
        use_upper =self .upper_var .get (),
        use_lower =self .lower_var .get (),
        use_digits =self .digit_var .get (),
        use_symbols =self .symbol_var .get (),
        exclude_similar =self .similar_var .get (),
        )

        entropy =calculate_entropy (password )
        result =check_password (password )

        lines =[]
        lines .append (f"{'='*50 }")
        lines .append (f"  Password  : {password }")
        lines .append (f"  Panjang   : {len (password )} karakter")
        lines .append (f"  Entropy   : {entropy } bit")
        lines .append (f"  Skor      : {result ['score']}/100")
        lines .append (f"  Kekuatan  : {result ['strength']}")
        lines .append (f"{'='*50 }")
        self ._set_gen_text ("\n".join (lines ))

    def _set_check_text (self ,text ):
        self .check_result .config (state ="normal")
        self .check_result .delete ("1.0","end")
        self .check_result .insert ("1.0",text )
        self .check_result .config (state ="disabled")

    def _set_gen_text (self ,text ):
        self .gen_result .config (state ="normal")
        self .gen_result .delete ("1.0","end")
        self .gen_result .insert ("1.0",text )
        self .gen_result .config (state ="disabled")

def run_gui ():
    root =tk .Tk ()
    PasswordToolGUI (root )
    root .mainloop ()

if __name__ =="__main__":
    run_gui ()

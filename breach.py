import hashlib
import urllib .request
import urllib .error

HIBP_URL ="https://api.pwnedpasswords.com/range/"

def check_breach (password :str )->dict :
    sha1 =hashlib .sha1 (password .encode ("utf-8")).hexdigest ().upper ()
    prefix =sha1 [:5 ]
    suffix =sha1 [5 :]

    try :
        req =urllib .request .Request (
        HIBP_URL +prefix ,
        headers ={"User-Agent":"password-tool/1.0"},
        )
        with urllib .request .urlopen (req ,timeout =10 )as resp :
            data =resp .read ().decode ("utf-8")
    except (urllib .error .URLError ,urllib .error .HTTPError ,OSError ):
        return {
        "breached":False ,
        "count":0 ,
        "error":"Tidak bisa terhubung ke API Have I Been Pwned",
        }

    for line in data .splitlines ():
        line_suffix ,count =line .split (":")
        if line_suffix ==suffix :
            return {
            "breached":True ,
            "count":int (count ),
            "error":None ,
            }

    return {
    "breached":False ,
    "count":0 ,
    "error":None ,
    }

"""Rebuild ASCII_Linguistics_fixed.csv from rules + optional v2 graded roles."""
import csv
from pathlib import Path
VOWELS=set(b"aeiouAEIOU")
STRUCT=["Numeral","Punctuation","Consonant","Vowel"]
EXTRA=["is_alpha","is_digit","is_upper","is_punct","is_space","utf8_lead"]
ASCII_NAMES={0:"NUL",1:"SOH",2:"STX",3:"ETX",4:"EOT",5:"ENQ",6:"ACK",7:"BEL",8:"BS",9:"TAB",10:"LF",11:"VT",12:"FF",13:"CR",14:"SO",15:"SI",16:"DLE",17:"DC1",18:"DC2",19:"DC3",20:"DC4",21:"NAK",22:"SYN",23:"ETB",24:"CAN",25:"EM",26:"SUB",27:"ESC",28:"FS",29:"GS",30:"RS",31:"US",32:" ",127:"DEL"}

def struct_vals(b):
    is_alpha=(65<=b<=90)or(97<=b<=122)
    is_digit=48<=b<=57
    is_upper=65<=b<=90
    is_punct=(33<=b<=47)or(58<=b<=64)or(91<=b<=96)or(123<=b<=126)
    is_space=b in (32,9,10,13)
    utf8_lead=(0<=b<0x80)or(0xC0<=b<=0xFF)
    vowel=1.0 if (is_alpha and b in VOWELS) else 0.0
    cons=1.0 if (is_alpha and b not in VOWELS) else 0.0
    return {"Numeral":1.0 if is_digit else 0.0,"Punctuation":1.0 if is_punct else 0.0,"Consonant":cons,"Vowel":vowel,
            "is_alpha":1.0 if is_alpha else 0.0,"is_digit":1.0 if is_digit else 0.0,"is_upper":1.0 if is_upper else 0.0,
            "is_punct":1.0 if is_punct else 0.0,"is_space":1.0 if is_space else 0.0,"utf8_lead":1.0 if utf8_lead else 0.0}

def char_label(b, fallback):
    if b in ASCII_NAMES: return ASCII_NAMES[b]
    if 33<=b<=126: return chr(b)
    return fallback if fallback and fallback!="." else f"0x{b:02X}"

here=Path(__file__).resolve().parent
v2_path=here/"ASCII_Linguistics_v2.csv"
rows=[]
if v2_path.exists():
    with v2_path.open() as f:
        rows=list(csv.DictReader(f))
else:
    rows=[{"Hex ASCII":f"0x{b:02X}","Character":char_label(b,"")} for b in range(256)]
    for r in rows:
        for k in ["Verb","Subject","Noun","Adjective","Adverb","Conjunction","Preposition","Pronoun","Article","Auxiliary Verb","Interjection","Frequency","Word Boundary","Subword Start","Subword End"]:
            r[k]="0"

fixed_fields=["Hex ASCII","Character"]+STRUCT+EXTRA+[c for c in rows[0] if c not in ("Hex ASCII","Character") and c not in STRUCT]
out_rows=[]
for row in rows:
    b=int(row["Hex ASCII"],16); s=struct_vals(b)
    out={"Hex ASCII":row["Hex ASCII"],"Character":char_label(b,row.get("Character",""))}
    for col in STRUCT+EXTRA: out[col]=f"{s[col]:g}"
    for c in rows[0]:
        if c not in out: out[c]=row.get(c,"0")
    out_rows.append(out)
dest=here/"ASCII_Linguistics_fixed.csv"
with dest.open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fixed_fields); w.writeheader(); w.writerows(out_rows)
print("wrote", dest, "rows", len(out_rows))

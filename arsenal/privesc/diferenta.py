import os
from arsenal.privesc.enum import citeste_linii, nume, GTFO


def cai(fisier):
    return set(citeste_linii(fisier))


if __name__ == "__main__":
    folder_start = os.path.join(os.path.dirname(__file__), "start")
    baza = cai(os.path.join(folder_start, "baza_suid.txt"))
    acum = cai(os.path.join(folder_start, "suid.txt"))
    print("baza:", len(baza), " acum:", len(acum))

    noi = acum - baza
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)

    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
    periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
    print("periculoase NOI:", periculoase)
# Zadatak 1
def povezi_po_indeksima(l1, l2):
    # Opcija 1
    # l3 = []
    # for el1, el2 in zip(l1, l2):
    #     l3.append(el1 + el2)
    # return l3
    #
    # Opcija 2
    return [el1 + el2 for el1, el2 in zip(l1, l2)]


# Zadatak 2
def cifre_u_stringu(string):
    # Opcija 1
    # cifre = []
    # for ch in string:
    #     if ch.isdigit(): cifre.append(ch)
    # return cifre
    #
    # Opcija 2
    return [ch for ch in string if ch.isdigit()]


# Zadatak 3
def palindrom(string):
    string_tr = [ch.lower() for ch in string if ch.isalpha()]
    string_rev = string_tr.copy()
    string_rev.reverse()
    return string_tr == string_rev


# Zadatak 4
def provera_lozinki(lozinke):
    validne_lozinke = []
    for lozinka in [l.strip() for l in lozinke.split(',')]:
        if len(lozinka) < 6 or len(lozinka) > 12:
            continue
        uslov_ispunjen = [False] * 4
        for ch in lozinka:
            if ch.islower(): uslov_ispunjen[0] = True
            elif ch.isupper(): uslov_ispunjen[1] = True
            elif ch.isdigit(): uslov_ispunjen[2] = True
            elif ch in "$#@": uslov_ispunjen[3] = True
            if all(uslov_ispunjen):
                validne_lozinke.append(lozinka)
                break
    print(", ".join(validne_lozinke))


# Zadatak 5
def proveri_broj(broj):
    while broj > 0:
        broj, ostatak = divmod(broj, 10)
        if ostatak % 2 != 0: return False
    return True

def sve_parne_cifre():
    sve_parne = []

    # Opcija 1
    # for broj in range(100, 401):
    #     if all([ch in '02468' for ch in str(broj)]):
    #         sve_parne.append(broj)

    # Opcija 2
    for broj in range(100, 401):
        if proveri_broj(broj): sve_parne.append(broj)

    print(", ".join([str(broj) for broj in sve_parne]))


# Zadatak 6
def anagram(s1, s2):
    s1 = [ch.lower() for ch in s1 if ch.isalpha()]
    s2 = [ch.lower() for ch in s2 if ch.isalpha()]
    s1.sort()
    s2.sort()
    return s1 == s2


# Zadatak 7
def stanje_servera(izvestaj):
    svi_serveri = []
    ne_rade = []

    statusi = izvestaj.split('\n')
    statusi.reverse()
    for status in [s.strip() for s in statusi if s.strip() != ""]:
        _, naziv, _, stanje = status.split()
        if naziv not in svi_serveri:
            svi_serveri.append(naziv)
            if stanje == "down":
                ne_rade.append(naziv)

    print(f"Ukupan broj servera pomenutih u izvestaju: {len(svi_serveri)}")
    print(f"Procenat servera koji ne rade: {len(ne_rade) * 100 / len(svi_serveri)}")
    print("Serveri koji je ne rade: " + ", ".join(ne_rade))



if __name__ == '__main__':

    pass

    # Zadatak 1
    # list1 = ["M", "na", "i", "Ke"]
    # list2 = ["y", "me", "s", "lly"]
    # print(povezi_po_indeksima(list1, list2))

    # Zadatak 2:
    # s = "Tokyo's 2024 population is now estimated at 37,115,035."
    # print(cifre_u_stringu(s))

    # Zadatak 3
    # s1 = "potop"
    # print(palindrom(s1))
    # s2 = "Sir ima miris"
    # print(palindrom(s2))
    # s3 = "ananas"
    # print(palindrom(s3))

    # Zadatak 4:
    # lozinke_za_proveru = "ABd1234@1, a F1#, 2w3E*, 2We334#5, t_456WR"
    # print(f"Passwords to check: {lozinke_za_proveru}")
    # provera_lozinki(lozinke_za_proveru)

    # Zadatak 5:
    # sve_parne_cifre()

    # Zadatak 6:
    # print(anagram('ortoped', 'torpedo'))
    # print(anagram('ortopedi', 'torpedo'))
    # print(anagram('On sa tla Like', 'Nikola Tesla'))


    # Zadatak 7:
    # izvestaj = '''
    #     Server abc01 is up
    #     Server abc02 is down
    #     Server abc03 is down
    #     Server xyz01 is up
    #     Server xyz02 is up
    #     Server abc02 is up
    #     '''
    # stanje_servera(izvestaj)

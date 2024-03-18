from collections import defaultdict
from operator import itemgetter


# ZADATAK 1:

def create_print_numeric_dict(n):
    d = dict()
    for x in range(1, n+1):
        d[x] = sum(range(x+1))
    for key, val in sorted(d.items(), reverse=True):
        val_str = "+".join([str(i) for i in range(1, key+1)])
        print(f"{key}: {val_str}={val}")



# ZADATAK 2:

def lists_to_dict(l1, l2):
    d = {}
    # Opcija 1
    # (predpostavlja da su duzine lista iste)
    # for item1, item2 in zip(l1, l2, strict=False):
    #     d[item1] = item2
    # Opcija 2
    # (Uzima sve elemente iz duže liste i kombinuje ih sa unapred definisanom vrednošću)
    from itertools import zip_longest
    for item1, item2, in zip_longest(l1, l2, fillvalue="unknown"):
        d[item1] = item2
    # Nakon sto je recnik kreiran koristeci jednu od gore navedenih opcija, ispisujemo ga sortiranog po vrednostima
    for key, val in sorted(d.items(), key=itemgetter(1)):
        print(f"{key}: {val}")




# ZADATAK 3:

def string_stats(s):
    # Opcija 1 za kreiranje instance recnika
    # d = {'letters_cnt': 0,
    #      'digits_cnt': 0,
    #      'punct_cnt': 0}
    # Opcija 2
    d = defaultdict(int)
    for ch in s:
        if ch.isalpha():
            d['letters_cnt'] += 1
        elif ch.isdigit():
            d['digits_cnt'] += 1
        elif ch in '.,!?;:':
            d['punct_cnt'] += 1
    return dict(d)



# ZADATAK 4:

def website_stats(urls):
    d = defaultdict(int)
    for url in urls:
        _, suffix = url.rsplit(".", maxsplit=1)
        suffix = suffix.rstrip('/')
        d[suffix] += 1
    return dict(d)




# ZADATAK 5:

def token_frequency(text):
    d = defaultdict(int)
    for token in text.split():
        token = token.rstrip(',.!?:;').lower()
        if len(token) >= 3:
            d[token] += 1
    for tok, freq in sorted(sorted(d.items()), key=itemgetter(1), reverse=True):
        print(f"{tok}: {freq}")



# ZADATAK 6:

def password_check(passwords):
    d = dict()
    for p in [p.lstrip() for p in passwords.split(',')]:
        issues = []
        if not any([ch.islower() for ch in p]):
            issues.append("no lower case letters")
        if not any([ch.isdigit() for ch in p]):
            issues.append("no digits")
        if not any([ch.isupper() for ch in p]):
            issues.append("no upper case letters")
        if not any([ch in '$#@' for ch in p]):
            issues.append("no special characters '@#$'")
        if len(p) < 6 or len(p) > 12:
            issues.append("length should be in the [6,12] range")
        d[p] = ['valid'] if len(issues) == 0 else issues
    return d



# ZADATAK 7:

def classroom_stats(stud_counts):
    # Option 1
    # d = defaultdict(int)
    # for cls, cnt in stud_counts:
    #     d[cls] += cnt
    # for cls, cnt in sorted(d.items(), key=lambda item: item[1], reverse=True):
    #     print(f"{cls}: {cnt}")
    # Option 2
    from collections import Counter
    l = []
    for cls, cnt in stud_counts:
        l.extend([cls]*cnt)
    for cls, cnt in sorted(Counter(l).items(), key=itemgetter(1), reverse=True):
        print(f"{cls}: {cnt}")



# ZADATAK 8:


def team_stats(team_data):
    from statistics import mean, quantiles

    mean_age = mean([member['age'] for member in team_data])
    print(f"Average age of team members: {mean_age}")
    q1, mdn, q3 = quantiles([member['score'] for member in team_data])
    print(f"Team score stats, given as Mdn (Q1, Q3)): {mdn}({q1:.2f},{q3:.2f})")
    best_under21 = max([member for member in team_data if member['age'] < 21], key=itemgetter('score'))
    print(f"Best player under 21 is {best_under21['name']}")



if __name__ == '__main__':

    pass

    # # Task 1
    # create_print_numeric_dict(7)
    # print()
    #
    # # Task 2
    # dishes = ["pizza", "sauerkraut", "paella", "hamburger"]
    # countries = ["Italy", "Germany", "Spain", "USA", "Serbia"]
    # lists_to_dict(countries, dishes)
    # print()
    #
    # # Task 3
    # print("string_stats('Today is October 24, 2023!'):")
    # print(string_stats("Today is October 24, 2023!"))
    # print()
    #
    # # Task 4
    # sample_websites = ['https://www.technologyreview.com/', 'https://www.tidymodels.org/',
    #                    'https://podcasts.google.com/', 'https://www.jamovi.org/', 'http://bg.ac.rs/']
    #
    # print(website_stats(sample_websites))
    # print()
    #
    # # Task 5
    # # response by GPT-3 to the question of why it has so entranced the tech community
    # # source: https://www.wired.com/story/ai-text-generator-gpt-3-learning-language-fitfully/
    # gpt3_response = ("""
    #     I spoke with a very special person whose name is not relevant at this time,
    #     and what they told me was that my framework was perfect. If I remember correctly,
    #     they said it was like releasing a tiger into the world.
    # """)
    # token_frequency(gpt3_response)
    # print()
    #
    # # Task 6:
    # print("Passwords to check: ABd1234@1, a F1#, 2w3E*, 2We334#5, t_456WR")
    # validation_dict = password_check("ABd1234@1, a F1#,2w3E*,2We334#5, t_456WR")
    # print("Validation results:")
    # for password, result in validation_dict.items():
    #     print(f"- {password}: {', '.join(result)}")
    # print()
    #
    # # Task 7:
    # l = [('V', 1), ('VI', 1), ('V', 2), ('VI', 2), ('VI', 3), ('VII', 1)]
    # classroom_stats(l)
    # print()
    #
    # # Task 8:
    # # team = [{'name': 'Bob', 'age': 18, 'score': 50.0},
    # #         {'name': 'Tim', 'age': 17, 'score': 84.0},
    # #         {'name': 'Jim', 'age': 22, 'score': 94.0},
    # #         {'name': 'Joe', 'age': 19, 'score': 85.5}]
    # team_stats(team)

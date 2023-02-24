import itertools
import string
from tld import get_tld

def generate_character_permutations(name: str):
    characters = list(name)
    permutations = []
    perms = itertools.permutations(characters)

    for perm in perms:
        permutations.append("".join(perm))

    return permutations

def generate_hyphenation_permutations(name: str):
    permutations = []
    hyphenation_chars = ['-', '.']

    for hyphenation_char in hyphenation_chars:
        for i in range(1, len(name)):
            name_list = list(name)
            name_list.insert(i, hyphenation_char)
            permutations.append(''.join(name_list))

    return permutations

def generate_bitquatting_permutations(name: str):
    permutations = []
    for i, letter in enumerate(name):
        for j in range(8):
            bit = 1 << j
            char = chr(ord(letter) ^ bit)
            if char.isalnum() or char == '-':
                permutations.append(name[:i] + char + name[i+1:])
    return permutations

def generate_homoglyph_permutations(name: str):
    permutations = []

    homoglyphs = {
        '0': ['o'],
        '1': ['l', 'i'],
        '2': ['s', '5', 'z'],
        '3': ['8'],
        '4': ['a'],
        '5': ['s', '2'],
        '6': ['9'],
        '8': ['3'],
        '9': ['6'],
        'a': ['4'],
        'b': ['p', 'q'],
        'e': ['3'],
        'i': ['1', 'l'],
        'l': ['1', 'i'],
        'm': ['rn', 'n', 'r'],
        'n': ['m', 'r', 'u'],
        'o': ['0'],
        'p': ['q', 'b', '9'],
        'q': ['p', 'b'],
        'r': ['n'],
        's': ['5', '2'],
        'u': ['n', 'v'],
        'v': ['u'],
        'w': ['vv'],
        'z': ['2']
    }

    homoglyphs_list = [set([char] + homoglyphs.get(char, [])) for char in name]
    homoglyphs_combinations = itertools.product(*homoglyphs_list)
    for combination in homoglyphs_combinations:
        permutations.append(''.join(combination))
    return permutations

def generate_insertion_permutations(name: str):
    permutations = []
    for i in range(len(name)+1):
        for c in string.ascii_lowercase + string.digits + "-_":
            new_domain = name[:i] + c + name[i:]
            permutations.append(new_domain)
    return permutations

def open_tld(file: str = 'tld_list'):
    with open(file, 'r', encoding='UTF-8') as f:
        tld_list = [line.strip() for line in f.readlines()]
    return tld_list

def generate_tld_permutations(name: str):
    tld_list = open_tld()
    permutations = []
    for tld_name in tld_list:
        permutations.append(f"{name}.{tld_name}")
    return permutations

def generate_permutations(domain: str):
    name = get_tld(f'http://{domain}', as_object = True).domain
    character_permutations = generate_character_permutations(name)
    hyphenation_permutations = generate_hyphenation_permutations(name)
    bitsquatting_permutations = generate_bitquatting_permutations(name)
    homoglyph_permutations = generate_homoglyph_permutations(name)
    insertion_permutations = generate_insertion_permutations(name)
    tld_permutations = generate_tld_permutations(name)

    return list(set(character_permutations + hyphenation_permutations + bitsquatting_permutations + homoglyph_permutations + insertion_permutations + tld_permutations))
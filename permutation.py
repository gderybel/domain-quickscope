from itertools import permutations, product
import string
from tld import get_tld

def generate_character_permutations(name: str) -> list:
    """This function returns a list of names mixed from a given name.

    Parameters
    ----------
    name : str
        Name of the string you want to permute.

    Returns
    -------
    list
        List of permuted names.
    """
    characters = list(name)
    character_permutations = []
    perms = permutations(characters)

    for perm in perms:
        character_permutations.append("".join(perm))

    return character_permutations

def generate_hyphenation_permutations(name: str) -> list:
    """This function returns a list of names where '-' and '.' 
    were inserted at everyplaces in a given name.

    Parameters
    ----------
    name : str
        Name of the string you want to permute.

    Returns
    -------
    list
        List of permuted names.
    """
    hyphenation_permutations = []
    hyphenation_chars = ['-', '.']

    for hyphenation_char in hyphenation_chars:
        for i in range(1, len(name)):
            name_list = list(name)
            name_list.insert(i, hyphenation_char)
            hyphenation_permutations.append(''.join(name_list))

    return hyphenation_permutations

def generate_bitsquatting_permutations(name: str) -> list:
    """This function returns a list of names bitquatted from a given name.

    Parameters
    ----------
    name : str
        Name of the string you want to permute.

    Returns
    -------
    list
        List of permuted names.
    """
    bitsquatting_permutations = []
    for i, letter in enumerate(name):
        for j in range(8):
            bit = 1 << j
            char = chr(ord(letter) ^ bit)
            if char.isalnum() or char == '-':
                bitsquatting_permutations.append(name[:i] + char + name[i+1:])
    return bitsquatting_permutations

def generate_homoglyph_permutations(name: str) -> list:
    """This function returns a list of names with character 
    replacements that looks like the original name.

    Parameters
    ----------
    name : str
        Name of the string you want to permute.

    Returns
    -------
    list
        List of permuted names.
    """
    homoglyph_permutations = []

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
    homoglyphs_combinations = product(*homoglyphs_list)
    for combination in homoglyphs_combinations:
        homoglyph_permutations.append(''.join(combination))
    return homoglyph_permutations

def generate_insertion_permutations(name: str) -> list:
    """This function returns a list of names with characters inserted in a given name.

    Parameters
    ----------
    name : str
        Name of the string you want to permute.

    Returns
    -------
    list
        List of permuted names.
    """
    insertion_permutations = []
    for i in range(len(name)+1):
        for c in string.ascii_lowercase + string.digits + "-_":
            new_domain = name[:i] + c + name[i:]
            insertion_permutations.append(new_domain)
    return insertion_permutations

def open_tld(file: str = 'tld_list') -> list:
    """This function opens a file, read it, and return a list containing each line.

    Parameters
    ----------
    file : str, optional
        File to open, by default 'tld_list'.

    Returns
    -------
    list
        List containing every line of the file.
    """
    with open(file, 'r', encoding='UTF-8') as f:
        tld_list = [line.strip() for line in f.readlines()]
    return tld_list

def generate_tld_permutations(name: str) -> list:
    """This function returns a list of names with every ascii TLDs.

    Parameters
    ----------
    name : str
        Name of the string you want to permute.

    Returns
    -------
    list
        List of permuted names.
    """
    tld_list = open_tld()
    tld_permutations = []
    for tld_name in tld_list:
        tld_permutations.append(f"{name}.{tld_name}")
    return tld_permutations

def generate_permutations(domain: str) -> list:
    """This function execute different permutations (character, hyphenation, bitsquatting,
    homoglyph, insertion and tld) and add a TLD to any of them.

    Parameters
    ----------
    domain : str
        Domain to permute (e.g : google.com)

    Returns
    -------
    list
        List of permuted domains.
    """
    name = get_tld(f'http://{domain}', as_object = True).domain
    character_permutations = generate_character_permutations(name)
    character_permutations = [permutation + '.com' for permutation in character_permutations]
    hyphenation_permutations = generate_hyphenation_permutations(name)
    hyphenation_permutations = [permutation + '.com' for permutation in hyphenation_permutations]
    bitsquatting_permutations = generate_bitsquatting_permutations(name)
    bitsquatting_permutations = [permutation + '.com' for permutation in bitsquatting_permutations]
    homoglyph_permutations = generate_homoglyph_permutations(name)
    homoglyph_permutations = [permutation + '.com' for permutation in homoglyph_permutations]
    insertion_permutations = generate_insertion_permutations(name)
    insertion_permutations = [permutation + '.com' for permutation in insertion_permutations]
    tld_permutations = generate_tld_permutations(name)

    return list(
        set(
            character_permutations +
            hyphenation_permutations +
            bitsquatting_permutations +
            homoglyph_permutations +
            insertion_permutations +
            tld_permutations
            )
        )
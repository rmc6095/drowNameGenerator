import random
from dataclasses import dataclass
import csv
from typing import Optional
import nltk
import re

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


@dataclass
class Fragment:
    name: str
    meaning: str
    placement: int
    gender: int


@dataclass
class FirstName:
    pre: Fragment
    mid: Fragment
    suf: Fragment
    order: Fragment

    def __str__(self):
        return f"{self.drow_string()}\n{self.trans_string()}"

    def drow_string(self, vowel_slider=75, consonant_slider=50):
        str_name = f"{self.pre.name}{self.mid.name}{self.suf.name}"
        apostrophized = generate_apostrophes(str_name, vowel_slider, consonant_slider)
        return f"{apostrophized}{self.order.name}"

    def trans_string(self):
        if self.order.name == "":
            return f"{self.pre.meaning}{self.mid.meaning}{self.suf.meaning}{self.order.meaning}"
        return f"{self.pre.meaning}{self.mid.meaning}{self.suf.meaning}{self.order.meaning[:-1]}, "


@dataclass
class HouseName:
    order: Fragment
    pre: Fragment
    suf: Fragment

    def __str__(self):
        return f"{self.drow_string()}\n{self.trans_string()}"

    def drow_string(self):
        return f"{self.order.name}{self.pre.name}{self.suf.name}"

    def trans_string(self):
        if self.order.meaning != "":
            str_name = f", {self.order.meaning}of the House "
        else:
            str_name = f"{self.order.meaning}of the House "
        ans = nltk.pos_tag(nltk.sent_tokenize(self.pre.meaning))
        val = ans[0][1]
        if self.pre.meaning == "Born of " or self.pre.meaning == "Blessed by ":
            val = 'VBN'
        if self.pre.meaning == "Of " or self.pre.meaning == "Those Above ":
            val = 'OFT'
        if self.pre.meaning == "House of ":
            str_name = f"{self.order.meaning} "
            val = 'HO'
        if val == 'NN' or val == 'NNP':
            str_name += f"of the {self.pre.meaning}{self.suf.meaning}"
        elif val == 'NNS' or val == 'NNPS' or val == 'DT':
            str_name += f"of {self.pre.meaning}{self.suf.meaning}"
        elif val == 'VB' or val == 'VBD' or val == 'VBN':
            str_name += f"of those {self.pre.meaning}{self.suf.meaning}"
        else:
            str_name += f"{self.pre.meaning}{self.suf.meaning}"
        return str_name


@dataclass
class FullName:
    first: FirstName
    house: HouseName
    vowel_slider: int = 75
    consonant_slider: int = 50

    def __str__(self):
        if self.house.trans_string()[0] == ",":
            return f"{self.first.drow_string(self.vowel_slider, self.consonant_slider)} {self.house.drow_string()}\n{self.first.trans_string()[:-1]}{self.house.trans_string()}\n"
        else:
            return f"{self.first.drow_string(self.vowel_slider, self.consonant_slider)} {self.house.drow_string()}\n{self.first.trans_string()}{self.house.trans_string()}\n"


fragments: list[Fragment] = list()
generic_mid = Fragment("", "", 1, 2)
generic_suffix = Fragment("", "", 2, 2)
generic_fn_order = Fragment("", "", 3, 2)
generic_hn_order = Fragment("", "", 4, 2)
int_list = [0, 1, 2]
bool_list = [True, False]


def process_data(filename):
    """
    A function which processes a .csv file of Drow Name Data and adds the name fragments into the global set.
    The rows of the file should be named 'fragment', 'meaning', 'placement', and 'gender', in that order.
    Raises an Exception if difficulties occur while processing the placement or alignment of the name.
    :param filename: The file to be processed.
    :return: None.
    """
    global fragments
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        i = 1
        for row in reader:
            name = row["fragment"]
            meaning = row["meaning"]
            placement = -1
            match (row["placement"]):
                case "fn_prefix":
                    placement = 0
                case "fn_middle":
                    placement = 1
                case "fn_suffix":
                    placement = 2
                case "fn_birth_order":
                    placement = 3
                case "hn_birth_order":
                    placement = 4
                case "hn_prefix":
                    placement = 5
                case "hn_suffix":
                    placement = 6
            if placement == -1:
                raise Exception(
                    f"Could not properly process placement for name \"{name}\" at line {i} in the file {filename}.")
            gender = -1
            match (row["gender"]):
                case "F":
                    gender = 0
                case "M":
                    gender = 1
                case "N":
                    gender = 2
            if gender == -1:
                raise Exception(
                    f"Could not properly process alignment for name \"{name}\" at line {i} in the file {filename}.")
            fragments.append(Fragment(name, meaning, placement, gender))


def generate_first_name(alignment: int = 0, mid: bool = False, end: bool = True, order: bool = False):
    pre_frag = generate_first_prefix(alignment)
    mid_frag = generic_mid
    suf_frag = generic_suffix
    order_frag = generic_fn_order
    if mid:
        mid_frag = generate_first_middle(alignment)
    if end:
        suf_frag = generate_first_suffix(alignment)
    if order:
        order_frag = generate_first_order()
    return FirstName(pre_frag, mid_frag, suf_frag, order_frag)


def generate_first_prefix(alignment: int):
    return random.choice(
        list(filter(lambda x: ((x.gender == alignment or x.gender == 2) and x.placement == 0), fragments)))


def generate_first_middle(alignment: int):
    return random.choice(
        list(filter(lambda x: ((x.gender == alignment or x.gender == 2) and x.placement == 1), fragments)))


def generate_first_suffix(alignment: int):
    return random.choice(
        list(filter(lambda x: ((x.gender == alignment or x.gender == 2) and x.placement == 2), fragments)))


def generate_first_order():
    return random.choice(list(filter(lambda x: x.placement == 3, fragments)))


def generate_house_name(first: Optional[FirstName] = None, order: bool = False):
    if first is not None:
        if first.order.name != "":
            if order is True:
                order = False
    pre_frag = generate_house_prefix()
    suf_frag = generate_house_suffix()
    order_frag = generic_hn_order
    if order:
        order_frag = generate_house_order()
    return HouseName(order_frag, pre_frag, suf_frag)


def generate_house_order():
    return random.choice(list(filter(lambda x: x.placement == 4, fragments)))


def generate_house_prefix():
    return random.choice(list(filter(lambda x: x.placement == 5, fragments)))


def generate_house_suffix():
    return random.choice(list(filter(lambda x: x.placement == 6, fragments)))


def generate_apostrophes(name, vowel_weight=75, consonant_weight=50):
    result = ""
    # handle triple letters
    matches = re.finditer(r"([a-z])\1\1", name)
    for match in matches:
        start = match.span()[0]
        end = match.span()[1] - 1
        result = name[0:start]
        result += f"{name[start]}'{name[end]}"
        result += name[end + 1:]
        name = result
    # handle double vowels
    matches = re.finditer(r"a{2,}|e{2,}|i{2,}|o{2,}|u{2,}|y{2,}", name)
    for match in matches:
        if weighted_chance(vowel_weight):
            start = match.span()[0]
            end = match.span()[1] - 1
            result = name[0:start]
            result += f"{name[start]}'{name[end]}"
            result += name[end + 1:]
            name = result
    # handle double consonants
    matches = re.finditer(r"([^aeiouy])\1", name)
    for match in matches:
        if weighted_chance(consonant_weight):
            start = match.span()[0]
            end = match.span()[1] - 1
            result = name[0:start]
            result += f"{name[start]}'{name[end]}"
            result += name[end + 1:]
            name = result
    return name


def weighted_chance(weight):
    return random.choice(range(1, 101)) > weight


def randomizer(n):
    process_data("data/drow_name_data.csv")
    # start = datetime.datetime.now()
    for i in range(n):
        fn = generate_first_name(random.choice(int_list), random.choice(bool_list), random.choice(bool_list),
                                 random.choice(bool_list))
        hn = generate_house_name(fn, random.choice(bool_list))
        name = FullName(fn, hn)
        print(name)
    # end = datetime.datetime.now()
    # print(f"This program took {end - start} to generate {n} drow names.")


def generate_name(gender:int=0, mid:bool=False, suf:bool=True, order:Optional[bool]=None, vowel: int=75, consonant:int=50):
    process_data("data/drow_name_data.csv")
    if order is None:
        order = random.choice(bool_list)
    fn = generate_first_name(gender, mid, suf, order)
    hn = generate_house_name(fn, order)
    return FullName(fn, hn, vowel, consonant)


if __name__ == '__main__':
    randomizer(10)

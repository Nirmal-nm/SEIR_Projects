import sys
import requests
from bs4 import BeautifulSoup

def data_fetch(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if soup.body:
        return soup.body.get_text()
    else:
        return ""

def cnt_words(text):

    text = text.lower()
    clean_text = ""

    for ch in text:
        if ch.isalnum() or ch == " ":
            clean_text += ch
        else:
            clean_text += " "
    words = clean_text.split()

    dict_freq = {}

    for word in words:
        if word in dict_freq:
            dict_freq[word] += 1
        else:
            dict_freq[word] = 1
    return dict_freq

def calculate_hash(word):
    p = 53
    m = 2**64
    hash_value = 0
    power = 1

    for char in word:
        hash_value = (hash_value + ord(char) * power) % m
        power = (power * p) % m

    return hash_value

def create_hash(freq_dict):
    v = [0] * 64              #v:Vector

    for word in freq_dict:
        h = calculate_hash(word)
        wt = freq_dict[word]

        for i in range(64):
            check_bit = 1 << i
            if h & check_bit:
                v[i] += wt
            else:
                v[i] -= wt

    fingerprint = 0

    for i in range(64):
        if v[i] > 0:
            fingerprint |= (1 << i)

    return fingerprint

def common_bits(hash1, hash2):

    bNo1 = binary64_bits(hash1)
    bNo2 = binary64_bits(hash2)
    same = 0

    for i in range(64):
        if bNo1[i] == bNo2[i]:
            same += 1
    return same

def binary64_bits(num):

    bitsList = []
    while num > 0:
        remainder = num % 2
        bitsList.append(str(remainder))
        num = num // 2

    while len(bitsList) < 64:
        bitsList.append("0")

    bitsList.reverse()
    return bitsList   

if len(sys.argv) < 3:
    print("Please provide two URLs")
    sys.exit()

D1 = data_fetch(sys.argv[1])
D2 = data_fetch(sys.argv[2])

frq1 = cnt_words(D1)
frq2 = cnt_words(D2)

hash1 = create_hash(frq1)
hash2 = create_hash(frq2)

same_bits = common_bits(hash1, hash2)
print("\n")
print("Hash of D1 and Hash of D2 respectively:", hash1," ", hash2)
print("Same bits in D1 & D2:", same_bits)

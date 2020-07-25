import random
import math

# Converts a number to its hexadecimal equivalent
def getByteRep(num):
    x = hex(num)
    string = x
    if len(x) - 2 < 4:
        string = x[:2] + "0" * (4 - len(x)) + x[2:]
    return string[:2] + string[2:].upper()

# Get the total list of words
f = open("words.txt", 'r+')
words = f.read().split("\n")
words_by_length = {}
for word in words:
    if len(word) not in words_by_length:
        words_by_length[len(word)] = []
    words_by_length[len(word)].append(word)

# Get the difficulty from the user
while (True):
    try:
        difficulty = int(input("Difficulty? (1-5): "))
        if (1 <= difficulty <= 5): break
        print("Try again.")
    except ValueError as e:
        print("Try again.")
length = 2 * difficulty + 2
n = len(words_by_length[length])
distribution = [6, 8, 3, 2]

# Randomly choose words based on similarity and length
end = False
while not end:
    target = random.choice(words_by_length[length])
    words_by_similarity = {}
    for i in range(n):
        w = words_by_length[length][i]
        if w != target:
            counts = 0
            for k in range(length):
                if target[k] == w[k]: counts += 1
            if counts not in words_by_similarity: words_by_similarity[counts] = []
            words_by_similarity[counts].append(w)
    j = 0
    while True:
        if (j not in words_by_similarity): break
        if (len(words_by_similarity[j]) < distribution[j]): break
        if (j == 3):
            end = True
            break
        j += 1

options = [target]
for i in range(4):
    for _ in range(distribution[i]):
        while True:
            w = random.choice(words_by_similarity[i])
            if w not in options: 
                options.append(w)
                break
    
options = [o.upper() for o in options]
random.shuffle(options)

# Generate the display trash
bytenums = []
for n in range(20):
    bytenums.append(random.randint(16 ** 3, (16 ** 4) - 1))
bytenums = sorted(bytenums)
bytenums = [getByteRep(b) for b in bytenums]

# Print the "hacking" terminal
for i in range(10):
    j = random.randint(0, 14 - length)
    k = random.randint(0, 14 - length)
    trash1 = ""
    trash2 = ""
    for _ in range(14 - length):
        c = random.choice("^][@*{}();:")
        d = random.choice("^][@*{}();:")
        trash1 += c
        trash2 += d
    print(bytenums[i], trash1[:j] + options[i] + trash1[j:], bytenums[10 + i], trash2[:k] + options[10 + i] + trash2[k:])

# Guessing
num_guesses = 4
guess_num = 0
for i in range(num_guesses):
    while True:
        guess = input("Guess (" + str(num_guesses - guess_num) + " left): ")
        if len(guess) == length: break
        else: print("Try again.")
    if guess.lower() != target:
        num_right = 0
        for i in range(length):
            if guess[i].lower() == target[i].lower():
                num_right += 1
        print("%d/%d correct." % (num_right, length))
        guess_num += 1
    else:
        print("Success!")
        break
if guess_num == num_guesses:
    print("Terminal locked. The word was %s." % target.upper())

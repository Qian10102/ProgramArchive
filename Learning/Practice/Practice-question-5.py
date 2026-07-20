def count_character(word,letter):
    output = 0
    for l in word:
        if l == letter:
            output += 1
    print(output)

word = input()
letter = input()
count_character(word,letter)
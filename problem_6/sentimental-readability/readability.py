from cs50 import get_string

# get string from user
text = None
while True:
    try:
        text = get_string('Text: ')
        break
    except ValueError:
        ...

# counting words
def count_word(text):
    words = text.count(' ')
    return words + 1

# counting letters
def count_letter(text):
    letters = 0
    for char in text:
        if char.isalpha():
            letters += 1
    return letters

# counting sentences
def count_sentence(text):
    sentences = text.count('.')
    sentences += text.count('!')
    sentences += text.count('?')
    return sentences

# caculating grade
def caculate_grade(words, letters, sentences):
    L = letters / words * 100
    S = sentences / words * 100

    grade = 0.0588 * L - 0.296 * S - 15.8

    float_decimal = grade - int(grade)
    return grade + 1 if float_decimal >= 0.5 else int(grade)


# result
words = count_word(text)
letters = count_letter(text)
sentences = count_sentence(text)

grade = caculate_grade(words, letters, sentences)


if grade >= 16:
    print('Grade 16+')
elif grade < 1:
    print('Before Grade 1')
else:
    print(f'Grade {grade}')
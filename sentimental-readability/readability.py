from cs50 import get_string

def main():
    text = get_string("Text: ")
    letters = n_letters(text)
    words = n_words(text)
    sentences = n_sentences(text)

    L = letters / words * 100
    S = sentences / words * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)

    if index < 1:
        print("Before Grade 1")
        exit(0)
    elif index > 16:
        print("Grade 16+")
        exit(0)
    else:
        print(f"Grade {index}")
        exit(0)

def n_letters(t):
    letters = 0
    for char in t:
        if char.isalpha():
            letters += 1
    return letters

def n_words(t):
    words = len(t.split())
    return words

def n_sentences(t):
    sentences = t.count(".") + t.count("?") + t.count("!")
    return sentences

main()

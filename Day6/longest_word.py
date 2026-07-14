def longest_word(text):
    words=text.split()
    longest=words[0]
    for word in words:
        if len(words)>len(longest):
            longest=words
    return longest
c=input("Enter a Longest word")
print(longest_word(c)) 
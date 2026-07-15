class TextUtil:
    def __init__(self):
        self.text  = "Hello! My name is Goutham"

    def word_count(self, text):
        words = text.split()
        return len(words)
    
    def unique_words(self, text):
        words = text.split()
        unique_words = set(words)
        return unique_words
    
    def reverse_string(self, text):
        return text[::-1]
    
    def empty_string(self, text):
        return text == ""
    def case_sensitive(self, text1, text2):
        return text1 == text2
    
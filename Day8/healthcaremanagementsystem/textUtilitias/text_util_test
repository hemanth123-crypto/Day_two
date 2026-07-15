from text_util import TextUtil

def test_word_count():
    util = TextUtil()
    assert util.word_count("Hello! My name is Mayur Rishi") == 6

def test_unique_words():
    util = TextUtil()
    assert util.unique_words("Hello! My name is Mayur Rishi") == {"Hello!", "My", "name", "is", "Mayur", "Rishi"}

def test_reverse_string():
    util = TextUtil()
    assert util.reverse_string("hello") == "olleh"

def test_empty_string():
    util = TextUtil()
    assert util.empty_string("") == True
    assert util.empty_string("Hello") == False

def test_case_sensitive():
    util = TextUtil()
    assert util.case_sensitive("Hello", "Hello") == True
    assert util.case_sensitive("Hello", "hello") == False
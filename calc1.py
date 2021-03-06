import string

# Token types
#
# EOF (end-of-file) token is used to indicate that 
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # Token type: INTEGER, PLUS, or EOF
        self.type = type

        # Token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()



class Interpreter(object):
    def __init__(self, text):
        # Client string input, e.g. "3+5"
        self.text = text

        # self.pos is an index into self.text
        self.pos = 0

        # Current token isntance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        
        This method is responsible for breaking a sentence 
        apart into tokens. One token at a time.
        """
        text = self.text

        # If self.pos index past the end of the self.text,
        # return EOF token because there is no more 
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # Get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # If the character is a digit then convert it to integer, 
        # create an INTEGER token, increment self.pos index 
        # to point to the next character after the digit, 
        # and return the INTEGER token
        if current_char.isdigit():
            # To support multi-digit integers, I use a while loop 
            # that continually reads the next character and checks 
            # if it is a digit. If so, shift our value by 10 and add the new digit
            value = 0
            while current_char.isdigit():
                value = (value * 10) + int(current_char)
                self.pos += 1
                # In case we reach the end of the line
                if self.pos > len(text) - 1:
                    break
                current_char = text[self.pos]

            # Now construct the token with the overall value, and return it
            token = Token(INTEGER, value)
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        # Skip whitespace characters
        if current_char in string.whitespace:
            self.pos += 1
            token = self.get_next_token()
            return token

        # Parsing error otherwise
        self.error()

    def eat(self, token_type):
        # Compare the current token type with the passed token 
        # type and if they match then "eat" the current token 
        # and assign the next token to the self.current_token,
        # otherwise raise an exception
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # Set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # We expect the current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)

        # We expect the current token to be a '+' or '-' Token
        adding = True
        op = self.current_token
        try:
            self.eat(PLUS)
        except:
            adding = False
            self.eat(MINUS)

        # We expect the current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)

        # After the above call the self.current_token is set to EOF token

        # At this point INTEGER PLUS INTEGER sequence of tokens 
        # has been successfully found and the method can just 
        # return the result of adding two integers, thus 
        # effectively interpreting the client input
        if adding:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result



def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
def is_valid_identifier_char(char):
    return char.isalnum() or char == '_'

def c_scanner(code):
    tokens = []
    i = 0

    while i < len(code):
        # Skip whitespaces
        if code[i].isspace():
            i += 1
            continue

        # Check for single-line comments
        if code.startswith('//', i):
            i += 2
            string_of_comment = ''
            
            while i < len(code) and code[i] != '\n':
                string_of_comment += code[i]
                i += 1
            tokens.append(("SINGLE_LINE_COMMENT",string_of_comment))

        # Check for multi-line comments
        if code.startswith('/*', i):
            i += 2
            string_of_multiline = ''
            while i < len(code) - 1 and not code[i:i + 2] == '*/':
                string_of_multiline += code[i]
                i += 1
            tokens.append(("MULTI-LINE COMMENT",string_of_multiline))    
            i += 2  # Skip the closing '*/'
            

        # Check for data types
        data_types = ['int', 'float', 'char', 'double', 'void']
        for data_type in data_types:
            if code.startswith(data_type, i) and not is_valid_identifier_char(code[i + len(data_type)]):
                tokens.append(('DATA_TYPE', data_type))
                i += len(data_type)
                break
        else:
            # Check for keywords
            keywords = ['if', 'else', 'while', 'for']
            for keyword in keywords:
                if code.startswith(keyword, i) and not is_valid_identifier_char(code[i + len(keyword)]):
                    tokens.append(('KEYWORD', keyword))
                    i += len(keyword)
                    break
            else:
                # Check for numbers
                num_str = ''
                while i < len(code) and (code[i].isdigit() or code[i] == '.'):
                    num_str += code[i]
                    i += 1
                if num_str:
                    tokens.append(('NUMBER', num_str))
                else:
                    # Check for identifiers
                    if code[i].isalpha() or code[i] == '_':
                        identifier = code[i]
                        i += 1
                        while i < len(code) and is_valid_identifier_char(code[i]):
                            identifier += code[i]
                            i += 1
                        tokens.append(('IDENTIFIER', identifier))
                    else:
                        # Check for operators
                        operators = ['+', '-', '*', '/', '%', '=']
                        for operator in operators:
                            if code.startswith(operator, i):
                                tokens.append(('OPERATOR', operator))
                                i += len(operator)
                                break
                        else:
                            # Check for parentheses
                            special_characters = ['(', ')','{', '}','[', ']',';']
                            for special in special_characters:
                                if code.startswith(special, i):
                                    tokens.append(('SPECIAL_CHAR', special))
                                    i += len(special)
                                    break
                                
                                else:
                                        # Check for strings
                                        if code[i] == '"':
                                            i += 1
                                            string_literal = ''
                                            while i < len(code) and code[i] != '"':
                                                string_literal += code[i]
                                                i += 1
                                            if i < len(code) and code[i] == '"':
                                                tokens.append(('STRING', string_literal))
                                                i += 1
                                            else:
                                                # Malformed string, treat it as an error
                                                tokens.append(('ERROR', 'Malformed string'))
                                        else:
                                            # Move to the next character if no match is found
                                            i += 1

    return tokens

if __name__ == "__main__":
    # Example C code
    file_path = input("please input the file path:")
    
    with open(file_path,'r') as file :
        c_code = file.read()
    

    # Get tokens from the C code
    tokens = c_scanner(c_code)
    
    print("----------------------------")
    print("token type" +" : "+"token value")

    # Display the tokens
    for token_type, value in tokens:
        print(f"{token_type}: {value}")

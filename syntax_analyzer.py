import sys
import os
# generate xml code using jack_tokenizer and compilation engine.
from parser.jack_tokenizer import JackTokenizer
import parser.utils.token_types as token_types


def analyze(path):
    # import pdb;pdb.set_trace()
    for file, name in get_files(path):
        outfile = name + "T.test.xml"
        with open(outfile, 'w') as f:
            f.write("<tokens>")
            f.write(os.linesep)
            jt = JackTokenizer(file)
            while jt.has_more_tokens():
                jt.advance()
                if jt.token_type() == token_types.KEYWORD:
                    token_type = "keyword"
                    token = jt.key_word()
                elif jt.token_type() == token_types.SYMBOL:
                    token_type = "symbol"
                    token = jt.symbol()
                elif jt.token_type() == token_types.INT_CONST:
                    token_type = "integerConstant"
                    token = jt.int_val()
                elif jt.token_type() == token_types.STRING_CONST:
                    token_type = "stringConstant"
                    token = jt.string_val()
                elif jt.token_type() == token_types.IDENTIFIER:
                    token_type = "identifier"
                    token = jt.identifier()
                else:
                    token_type = None
                    token = None
                f.write('<{type}> {token} </{type}>'.format(token=token, type=token_type))
                f.write(os.linesep)
                # print(jt.token)
            f.write("</tokens>")
            f.write(os.linesep)


def get_files(path):
    file_type = ".jack"
    if path.endswith(file_type):
        # second out arg is file name, with file type removed
        yield path, path.rsplit('.')[0]
    else:
        for name in os.listdir(path):
            if name.endswith(file_type):
                file = os.path.join(path, name)
                yield file, file.rsplit('.')[0]  # remove file type


if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        jt = None
        path = None
        print("Expected a file name!")
        exit(0)

    analyze(path)

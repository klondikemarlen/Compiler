import sys
import os
import io
import xml.etree.ElementTree as ET

# generate xml code using jack_tokenizer and compilation engine.
from parser.jack_tokenizer import JackTokenizer
from parser.compilation_engine import CompilationEngine
from parser.utils.exceptions import CompileError


def analyze(path):
    # import pdb;pdb.set_trace()
    for in_file, name in get_files(path):
        in_base_name = os.path.basename(in_file)
        outfile = name + ".test.xml"
        jt = JackTokenizer(in_file)

        with open(outfile, 'w') as out_f, io.StringIO() as tokenizer_out, io.StringIO() as parser_out:
            ce = CompilationEngine(jt, out_f)

            try:
                ce.compile_class()
            except CompileError as ex:
                print("In {} (line {}): {}".format(in_base_name, jt.line_number, ex))

        # Helpful test code
        compare_name = name + ".xml"
        with open(outfile) as my_f, open(compare_name) as compare_f:
            out_base_name = os.path.basename(outfile)
            compare_base_name = os.path.basename(compare_name)
            for index, my_line in enumerate(my_f):
                compare_line = compare_f.readline()
                if my_line != compare_line:
                    print("\n" + "*" * 40)
                    print("Comparing {} == {}".format(out_base_name, compare_base_name))
                    print("In {} (line {}): Lines are not equal".format(out_base_name, index))
                    print("Expected line vs. actual was:")
                    print(repr(compare_line))
                    print(repr(my_line))
            if compare_f.readline():
                print("File is too short!")
        # exit("Exiting syntax analyser!!!!!!")


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
        path = None
        print("Expected a file name!")
        exit(0)

    analyze(path)


"""
example errors:
In Main.jack (line 9): Expected 'class'
In Main.jack (line 9): Expected a class name
In Main.jack (line 9): Expected {
In Square.jack (line 18): In subroutine new: A constructor must return 'this'
In SquareGame.jack (line 15): In subroutine new: A constructor must return 'this'
In SquareGame.jack (line 36): In subroutine run: a boolean value is expected
In SquareGame.jack (line 46): In subroutine run: an int value is expected
In SquareGame.jack (line 47): In subroutine run: an int value is expected
"""

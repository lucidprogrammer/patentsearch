import sys
import os


def splitter(filename: str):
    count = 0
    buffer = []
    with open(filename, 'r') as reader:
        for line in reader:
            if(count > 0):
                sys.exit('We want only one file to test now')
            if(line and line.startswith('<?xml version')):
                if(len(buffer) == 0):
                    buffer.append(line)
                else:
                    with open(os.path.join(os.path.split(filename)[0], '%d.xml'
                                           % count), 'w') as writer:
                        writer.write('\n'.join(buffer))
                    buffer.clear()
                    count += 1
            else:
                buffer.append(line)


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        sys.exit('Provide name of the xml file unzipped from uspto')
    else:
        if(os.path.isfile(sys.argv[1])):
            splitter(sys.argv[1])
        else:
            sys.exit('Check filepath')

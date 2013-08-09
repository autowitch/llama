#!/usr/bin/env python

from lib.llama_main import Llama

def main():
    """docstring for main"""
    ll = Llama()
    ll.parse_args()
    if not ll.load():
        return
    ll.run()
#    print ll.extract_string(':+ -:-+ -|-: .. :| -*-:X -:. *-+X +. -|* |. -+-| .-: -:*X .+')

if __name__ == '__main__':
    main()

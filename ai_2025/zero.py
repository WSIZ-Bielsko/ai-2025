import json


def call_it():
    with open('res.json') as f:
        lines = f.readlines()
        w = ''.join([l.strip() for l in lines])
        print(w)
        d = json.loads(w)
        print(d)
        print(d['cities'])


if __name__ == '__main__':
    call_it()
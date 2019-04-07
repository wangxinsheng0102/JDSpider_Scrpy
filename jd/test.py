import urllib.parse
if __name__ == "__main__":
    s = '长春'
    s = urllib.parse.quote(s)
    print(s)
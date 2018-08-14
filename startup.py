import pkgutil,sys,os

with open('requirements.txt','r') as f:
    for line in f.readlines():
        line = line.replace('\n', '')
        if line.startswith('-e'):
            continue
        if not pkgutil.find_loader(line):
            print("Module "+line+" not found.")
            sys.exit(-1)
    else:
        print("All modules are existing and installed. Preparing to boot Gamma now.")
        sys.exit(0)

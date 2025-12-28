
try:
    with open('.env', 'r') as f:
        content = f.read()
    with open('env_dump.txt', 'w') as f:
        f.write(content)
except Exception as e:
    with open('env_dump.txt', 'w') as f:
        f.write(str(e))

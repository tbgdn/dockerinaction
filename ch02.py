import subprocess

result = subprocess.run(
    ['echo', 'Hello from the child!'],
    capture_output=True,
    shell=True,
    encoding='utf-8')

result.check_returncode()  # No exception means clean exit
print(result.stdout)

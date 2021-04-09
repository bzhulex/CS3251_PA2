import os
import subprocess
import platform

os_name = platform.system().lower()
zipfile = 'pa2_submission.zip'
if "windows" in os_name:
    if os.path.exists('./' + zipfile):
        command = ['del', zipfile]
        subprocess.run(command)

    command = ['tar', '-a', '-c', '-f', zipfile,
        '1.json', '2.json', '3.json', '4.json', 'bootstrapper.py', 'client_1.py', 'client_2.py', 'client_3.py', 'client_4.py', 'p2pbootstrapper.py', 'p2pclient.py']
    subprocess.run(command)
else:
    command = ['rm', '-f', zipfile]
    subprocess.run(command)

    command = ['zip', '-r', zipfile,
        '1.json', '2.json', '3.json', '4.json', 'bootstrapper.py', 'client_1.py', 'client_2.py', 'client_3.py', 'client_4.py', 'p2pbootstrapper.py', 'p2pclient.py']
    subprocess.run(command)

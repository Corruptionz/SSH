# Paramiko API documentation found at: http://docs.paramiko.org/en/stable/index.html

import paramiko, sys, select, time, re, os
from getpass import getpass

ip = input("IP Address: ")
port = input("Port: ")
username = input("Username: ")
password = getpass()

i = 1

while True:
    print ("Trying to connect to %s (%i/10)..." % (ip, i))

    # Attempt to connect to SSH client
    try:
        remote_conn = paramiko.SSHClient()
        remote_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn.connect(ip, port=port, username=username, password=password, look_for_keys=False, allow_agent=False)
        print("Success! Connected to %s." % ip)
        print("==================================================")
        break

    # Handle authentication failure
    except paramiko.AuthenticationException:
        print("Authentication failed when connecting to %s" % ip)
        sys.exit(1)

    # Handle unable to reach failure
    except:
        print("Could not SSH to %s, attempting again in 5 seconds." % ip)
        i += 1
        time.sleep(5)

    # If failed consecutively, abort
    if i == 10:
        print("Could not connect to %s. Aborting." % ip)
        sys.exit(1)

# Send the command
stdin, stdout, stderr = remote_conn.exec_command("ls")

# Wait for the command to terminate and print output
while not stdout.channel.exit_status_ready():
    output = stdout.channel.recv(1024)
    output = output.decode("utf-8")
    output = output.strip()
    print(output)            

# Disconnect
print("==================================================")
print ("Finished! Closing SSH connection to %s." % ip)
remote_conn.close()

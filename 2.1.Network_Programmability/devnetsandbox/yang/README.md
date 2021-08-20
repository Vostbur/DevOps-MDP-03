# Use a NETCONF Session to Gather Information

## Step 1:  Check if NETCONF is running on the CSR1kv.

NETCONF may already be running if another student enabled it, or if a later IOS version enables it by default. From your SSH session with the CSR1kv, use the show platform software yang-management process command to see if the NETCONF SSH daemon (**ncsshd**) is running.

    CSR1kv# show platform software yang-management process

    confd            : Running

    nesd             : Running

    syncfd           : Running

    ncsshd           : Running

    dmiauthd         : Running

    nginx            : Running

    ndbmand          : Running

    pubd             : Running

    

    CSR1kv#

If NETCONF is not running, as shown in the output above, enter the global configuration command netconf-yang.

    CSR1kv# config t

    CSR1kv (config)# netconf-yang

Type exit to close the SSH session.

## Step 2:  Access the NETCONF process through an SSH terminal.

In this step, you will re-establish an SSH session with the CSR1kv. But this time, you will specify the NETCONF port 830 and send netconf as a subsystem command.

Enter the following command in a terminal window. You can use the up arrow to recall the latest SSH command and just add the -p and -s options as shown. Then, enter cisco123! as the password.

    devasc@labvm:~$ ssh cisco@192.168.56.101 -p 830 -s netconf

    cisco@192.168.56.101’s password:

The CSR1kv will respond with a hello message that includes over 400 lines of output listing all of its NETCONF capabilities. The end of NETCONF messages are identified with **]]>]]>**.

    <?xml version=”1.0″ encoding=”UTF-8″?>

    <hello xmlns=”urn:ietf:params:xml:ns:netconf:base:1.0″>

    <capabilities>

    <capability>urn:ietf:params:netconf:base:1.0</capability>

    <capability>urn:ietf:params:netconf:base:1.1</capability>

    <capability>urn:ietf:params:netconf:capability:writable-running:1.0</capability>

    <capability>urn:ietf:params:netconf:capability:xpath:1.0</capability>

    <capability>urn:ietf:params:netconf:capability:validate:1.0</capability>

    <capability>urn:ietf:params:netconf:capability:validate:1.1</capability>

    (output omitted)

        </capability>

    </capabilities>

    <session-id>20</session-id></hello>]]>]]>

## Step 3:  Start a NETCONF session by sending a hello message from the client.

To start a NETCONF session, the client needs to send its own hello message. The hello message should include the NETCONF base capabilities version the client wants to use.

Copy and paste the following XML code into the SSH session. Notice that the end of the client hello message is identified with a **]]>]]>**.

    <hello xmlns=”urn:ietf:params:xml:ns:netconf:base:1.0″>

    <capabilities>

    <capability>urn:ietf:params:netconf:base:1.0</capability>

    </capabilities>

    </hello>

    ]]>]]>

Switch to the CSR1kv VM and use the show netconf-yang sessions command to verify that a NETCONF session has been started. If the CSR1kv VM screen is dark, press Enter to wake it up.
Open configuration window

    CSR1kv> en

    CSRk1v# show netconf-yang sessions

    R: Global-lock on running datastore

    C: Global-lock on candidate datastore

    S: Global-lock on startup datastore

    

    Number of sessions : 1

    

    session-id  transport    username             source-host           global-lock

    ——————————————————————————-

    20          netconf-ssh  cisco                192.168.56.1          None

    

    CSR1kv#
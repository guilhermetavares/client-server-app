Functional Requirements
-----------------------

The system allows collection of machine statistics in an intranet environment. The system implements the following specifications.

Client Script

This script will be uploaded and executed to 100s of machines in the intranet. These machines are meant to be monitored for system level statistics like memory usage, CPU usage, total uptime and windows security event logs (in case of windows OS).

When executed, the client script collects the statistics and return them to the server script for cumulation.

The client script must encrypt the data before returning it to server.

Server Script

Installed on a single central machine in the same intranet.

Each client is configured in a server config xml file something like this: ::

    <client ip=’127.0.0.1’ port=’22’ username=’user’ password=’password’ mail="asa@asda.com">    
        <alert type="memory" limit="50%" />
        <alert type="cpu" limit="20%" />
    </client>

When executed, the server script should connect to each client using ssh, upload the client script in a temp directory, execute it and get the response.

After receiving the response from the client script, server script should decode it and stores it into a relational database along with client ip. This collected data is consumed by another application, that is out of scope, but you may design the database table yourself.

The server based upon the "alert" configuration of each client sends a mail notification. The notification is sent to the client configured email address using SMTP. Use a simple text mail format with some detail about the alert. event logs must be sent via email every time without any condition.

Assume any functional details required to achieve the above requirements based on logic and your experience. But follow the KISS principle.


Resolution
----------

This project is up in github:
https://github.com/guilhermetavares/client-server-app

Using ``Python 3``, in both ``Client`` and ``Server``


For Client
----------

For encryp data, used ``pycrypto``
For get the machine info used ``psutil``

For save develop time, all the ``XML`` is process to ``Regex``

This instructions, assuming the ``Vagrant`` and ``VirtualBox`` are installed
For ``client``, has a ``Vagrantfile`` to up and copy the folder to ubuntu
In the path of ``Vagrantfile`` (Maybe it will take time): ::

    vagrant up


After ``Vagrant`` up, copy this xml: ::

    <client ip="127.0.0.1" port="2222" username="vagrant" password="vagrant" mail="mail@email.com">    
        <alert type="memory" limit="50%" />
        <alert type="cpu" limit="20%" />
    </client>


For Server
----------

Install the ``requirements.txt``



Using ``Flask``, to show the machine, control database and email.

It has a ``docker-compose``, to up the aplication.

The data of registration machines, are updating for some ``AJAX`` script in ``index.html``

The machines, are registration for ``Form`` in main page.

Set the default variables in env: ::

    MAIL_USERNAME = 'Your-email@email.com'
    MAIL_PASSWORD = 'password'
    FLASK_APP = app.py


and create database: ::

    python3 start.py


Run the project: ::

    python3 app.py


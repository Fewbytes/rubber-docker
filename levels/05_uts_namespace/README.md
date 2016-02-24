# Level 05: UTS namespace

The UTS namespace allows per container hostname. After moving to a new UTS namespace you can change the hostname without effecting the hostname of the machine.

Python 2.x doesn't have a `sethostname` call, so use the one provided by our `linux` module.
Writing custom checks
=====================

Infracheck provides very basic scripts for health checking, you may probably want to write your own.
It's really simple.

1. "check" scripts are in **"checks" directory** of your project structure, here you can add a **new check script**
2. Your script needs to take **uppercase environment variables as input**
3. It is considered a good practice to validate environment variables presence in scripts
4. Your script needs to return a valid exit code when:
    - Any of environment variables is missing or has invalid value
    - The check fails
    - The check success

That's all!

A few examples:

.. literalinclude:: ../../infracheck/checks/dir-present
   :language: bash
   :linenos:

.. literalinclude:: ../../infracheck/checks/load-average
   :language: python
   :linenos:

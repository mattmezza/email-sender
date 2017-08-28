email-sender
======

This is a python script that lets you send emails with string variables in it.

It uses SMTP and YAML for configuration/variable/email specification.

In order to be able to use such script you need to have `pyyaml` installed on your python environment (`pip install pyyaml`)

For further information just contact me at [mattmezza@gmail.com](mailto:mattmezza@gmail.com)


Use it like this

```
python email-sender.py -c config.yml -e emails.yml
```

If you wanna use it interactively just add `-i` at the end

```
python email-sender.py -c config.yml -e emails.yml -i
```

you can see the help by running this command `python eamil-sender.py -h`

###### Matteo Merola `'mattmezza'`

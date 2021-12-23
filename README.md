# html element changed checker (hecc)

Used to watch certain html elements on a website while using the beautifulsoup4 package. 
Persistence in between runs is realized with a sqlite file called "hecc.sqlite".
If a new element is found, a notification can be sent out with pushover if configured
to do so. 
First used by me to check for new jobs at companies which did not provide an e-mail
notification on new jobs which match a certain pattern.

## setup/install (example on Linux with virtualenv)

create no-login user:

```sudo adduser --disabled-password hecc```

switch to user and install requirements:

```sudo su - hecc```

```python3 -m virtualenv hecc_venv```

```source hecc_venv/bin/activate && python3 -m pip install -r requirements.txt```

## run (example on Linux with virtualenv)

```source hecc_venv/bin/activate && python3 hecc.py```

## examplary daily run at 0:00 each day with crontab on Linux

```
0 0 * * * /usr/bin/env bash -c 'cd /home/hecc && source /home/hecc/hecc_venv/bin/activate && python3 hecc.py' > /dev/null 2>&1
```

## how to configure

The websites which should be checked are configured in 
"sitesToCheckConfig.json", which has to be in the same directory as the program itself.

There are basically two "modes" to check a site with hecc:

1. look for certain html elements on the site and use the "regexString"
to find any matches in the text of this element
2. look in the whole source code of the site with the "regexString", without 
looking to find any specific html elements first

parameters explained (see also the examples below):

"url": the url of the site you want to check

"site": a unique name you want to give that site; 
"site" has to be a valid string for a sqlite table name, since this name will
be used to create a sqlite table in "hecc.sqlite"

"elementType": the name of the html element you are looking for

"className": the name of the class of that html element

"classSearchString" if you want to match the value of the class name, you can use this
parameter with regex

"notify": if to notify via pushover or not. better to leave at "false" for the first run, otherwise you might get swamped with notifications :)

"regexString": regex you want to use to match the text on any prior matching html element. It has to contain at least
one matchgroup.

"checkOnlySourceCodeOfSite": leave at "false" for "mode" 1, set to true for "mode" 2

### 1. "mode 1": example with checking a specific html element:
e.g. you are looking for this kind of element on the site and want to grab the text of that element:
```
<a target="_self" href="/bist-du-fritz-genug/softwareentwickler-java-wmd/">Softwareentwickler Java  (w/m/d)</a>
```
```
{
      "url": "https://jobs.avm.de/",
      "site": "avm",
      "elementType": "a",
      "className": "target",
      "classSearchString": "_self",
      "notify": false,
      "regexString": "^(?=.*?\\b(IT.*|Software.*|Ingenieur.*|Engineer.*|Developer.*|Cyber.*|IoT.*|Entwick.*)\\b)((?!Praktik|Abschluss|Stud|Ausbild).)*$",
      "checkOnlySourceCodeOfSite": false
}
```

### 2. "mode 2": example with only checking the raw source code:
e.g. if you just want to find the text "Willkommen bei Ihrer FRITZ!Box" on the whole site (searching over multiple lines)

```
{
  "sites": [
    {
      "url": "https://fritz.box",
      "site": "fritzbox",
      "elementType": "",
      "className": "",
      "classSearchString": "",
      "notify": false,
      "regexString": "[\\S\\n ]+.*?(Willkommen.*?)\".*?\\n$",
      "checkOnlySourceCodeOfSite": true

    }
  ]
}
```

### notification config

If you want to configure pushover notifications on newly found entries, you have to put the file
"pushoverconfig.json" into the directory "notifier" in the following format:

```
{
        "user_key": "YOUR USER KEY",
        "token": "YOUR USER TOKEN"
}
```

When running for the first time (with no prior sqlite file or when you check a new site, changed the regex etc..), you should disable "notify" for a site, since you will get a notification for each new entry! After the first run, you can then activate it for the site and will only get entries which were added newly.
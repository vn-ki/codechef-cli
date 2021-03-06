import click
import re
import requests
import logging

from codechef_cli.data import Data
from codechef_cli.exceptions import APIError
from tabulate import tabulate

logger = logging.getLogger(__name__)


def submit_solution(problem_code, input_file, language):
    language = _get_language_id(language)
    if not language:
        logger.error("Error determining language id.")
        exit(1)
    # read userdata
    userdata = Data["submit_userdata"]
    cookies = userdata["cookies"]
    user_agent = userdata["user_agent"]

    # fetch tokens
    problem_url = "https://www.codechef.com/submit/{}".format(problem_code)
    session = requests.Session()
    session.headers = {
        "Cookie": cookies,
        "User-Agent": user_agent
    }
    r = session.get(problem_url)
    try:
        form_token = re.search(
            r"name=\"form_token\".*?value=\"(.*?)\"", r.text).group(1)
        form_build_id = re.search(
            r"name=\"form_build_id\".*?value=\"(.*?)\"", r.text).group(1)
        logger.debug("form_token: {}, form_build_id:{}".format(
            form_token, form_build_id))
    # TODO: more robust way to conclude that tokens are expired?
    except AttributeError:
        raise APIError('Tokens no longer valid.')

    # send the code
    r = session.post(problem_url, data={
        "form_token": form_token,
        "form_build_id": form_build_id,
        "form_id": "problem_submission",
        "program": "",
        "language": language,
        "problem_code": problem_code
    }, files={
        "files[sourcefile]": input_file
    })

    # done
    submission_code = re.search(r"complete/(\d+)", r.url).group(1)
    Data['_last_submission_code'] = submission_code
    return submission_code


def _get_language_id(language):
    "searches for language id, given language name"
    language_map = {
        "11": "C(gcc 6.3)",
        "44": "C++14(gcc 6.3)",
        "10": "Java(HotSpot 8u112)",
        "4": "Python(cpython 2.7.13)",
        "116": "Python3(python  3.6)",
        "99": "PyPy(PyPy 2.6.0)",
        "27": "C#(gmcs 4.6.2)",
        "22": "Pascal(fpc 3.0.0)",
        "2": "Pascal(gpc 20070904)",
        "17": "Ruby(ruby 2.3.3)",
        "29": "PHP(php 7.1.0)",
        "114": "Go(go 1.7.4)",
        "56": "JavaScript(node 7.4.0)",
        "21": "Haskell(ghc 8.0.1)",
        "93": "Rust(rust 1.14.0)",
        "39": "Scala(scala 2.12.1)",
        "85": "Swift(swift 3.0.2)",
        "20": "D(gdc 6.3)",
        "3": "Perl(perl 5.24.1)",
        "5": "Fortran(gfortran 6.3)",
        "6": "Whitespace(wspace 0.3)",
        "7": "ADA 95(gnat 6.3)",
        "8": "Ocaml(ocamlopt 4.01)",
        "9": "Intercal(ick 0.3)",
        "12": "Brainf**k(bff 1.0.6)",
        "13": "Assembler(nasm 2.12.01)",
        "14": "Clips(clips 6.24)",
        "15": "Prolog(swi 7.2.3)",
        "16": "Icon(iconc 9.5.1)",
        "18": "Scheme(stalin 0.3)",
        "19": "Pike(pike 8.0)",
        "23": "Smalltalk(gst 3.2.5)",
        "25": "Nice(nicec 0.9.13)",
        "26": "Lua(luac 5.3.3)",
        "28": "Bash(bash 4.4.5)",
        "30": "Nemerle(ncc 1.2.0)",
        "31": "Common Lisp(sbcl 1.3.13)",
        "32": "Common Lisp(clisp 2.49)",
        "33": "Scheme(guile 2.0.13)",
        "47": "Kotlin(kotlin 1.2.50)",
        "62": "Text(pure text)",
        "97": "Scheme(chicken 4.11.0)",
        "111": "Clojure(clojure 1.8.0)",
        "118": "Cobol(open-cobol 1.1.0)",
        "124": "F#(mono 4.0.0)"
    }
    # check if user has provided language id
    if language in language_map.keys():
        logger.info("Language selected: {}".format(language_map[language]))
        return language

    filtered = {id: name for id, name in language_map.items()
                if language.lower() in name.lower()}
    if len(filtered) == 1:
        # we found the language that user wants
        item = list(filtered.items())[0]
        logger.info("Language selected: {}".format(item[1]))
        language_id = item[0]
        return language_id
    elif len(filtered) == 0:
        click.echo(
            "We couldn't find any language for your query. Please try again")
        return False
    else:
        # multiple languages found
        click.echo("We found the following languages : ")
        print(tabulate(filtered.items(), headers=[
              "id", "name"], tablefmt="psql"))
        click.echo("Please be more specific. You can also enter language id.")
        return False


def _update_submit_userdata():
    # TODO: Find a place for this function. Maybe in commands.submssions
    cookies = click.prompt("enter cookies(single line)")
    user_agent = click.prompt("enter user-agent(single line)")
    Data["submit_userdata"] = {
        "cookies": cookies,
        "user_agent": user_agent
    }

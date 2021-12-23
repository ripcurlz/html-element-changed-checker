from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
import sys
import re
from sqliteconn.sqliteconnhandler import SqliteconnHandler
from notifier.notifier import Notifier
from banner.banner import Banner
from logger.logger import Logger


def check_site(url: str, element_type: str, class_name: str, class_search_string: str, site: str, regex_string: str,
               notify: bool, checkOnlySourceCodeOfSite: bool, logger: object) -> str:

    try:
        logger.log.info("Now processing site '{}'...".format(site))
        notifier = None
        # only instantiate pushover notifier object if configured for this site...
        if notify:
            notifier = Notifier(logger=logger)
        html = urlopen(url)
        html_read = html.read()
        bs = BeautifulSoup(html_read, 'html.parser')

    except HTTPError as e:
        exception = str(sys.exc_info()[0])
        logger.log.exception("Could not open url " + url + " because of: " + exception)
        if notify:
            notifier.notify_about_exception_via_pushover(site, exception)
    try:
        sqlconn = SqliteconnHandler(filename="hecc.sqlite", logger=logger, notify=notify, notifier=notifier)
        sqlconn.create_table_if_not_exists(site=site)
        # check if we only want to search the whole site (e.g. also javascript) with regex for certain strings
        if checkOnlySourceCodeOfSite:
            regex = re.compile(regex_string)
            prettified_bs_string = bs.prettify()
            matches = regex.finditer(prettified_bs_string)
            for match in matches:
                element_to_write = match.group(1).strip("\n").lstrip().rstrip()

                # only write to sql when the element description matches the regex string from the config file
                sqlconn.insert_element_if_not_exists_into_table(element=element_to_write, site=site)
        # ok, we want to search instead for a certain html element type and use the regex there
        else:
            for element in bs.findAll(str(element_type), {str(class_name):re.compile(str(class_search_string))},
                                      text=True):
                # strip element text of all white spaces and new lines
                element_to_write = element.get_text().strip("\n").lstrip().rstrip()

                # only write to sql when the element description matches the regex string from the config file
                regex = re.compile(regex_string)
                if regex.search(element_to_write):
                    sqlconn.insert_element_if_not_exists_into_table(element=element_to_write, site=site)
    except AttributeError as e:
        exception = str(sys.exc_info()[0])
        logger.log.exception("Could not write element to sql file because of: " + exception)
        if notify:
            notifier.notify_about_exception_via_pushover(site=site, exception=exception)
    finally:
        sqlconn.close_connection()


def main():
    logger = Logger()
    banner = Banner()
    banner.print_banner()
    with open("sitesToCheckConfig.json", "r") as configfile:
        data = json.load(configfile)
        sitesdict = data['sites']
        for site in sitesdict:
            check_site(url=site['url'], element_type=site['elementType'],
                       class_name=site['className'], class_search_string=site['classSearchString'],
                       site=site['site'], regex_string=site['regexString'], notify=site['notify'],
                       checkOnlySourceCodeOfSite=site['checkOnlySourceCodeOfSite'], logger=logger)


if __name__ == "__main__":
    # execute only if run as a script
    main()

from bs4 import BeautifulSoup
import requests
import re
from requests.exceptions import ConnectionError, MissingSchema


def findIfJQueryExists(url):
    """ This method makes a request to the received URL and
    checks if jQuery exists in the URL's HTML source"""

    data_dict = {"success": True, "uses_jquery": "no",
                 "version": "could not detect", "found_in_line": None}
    try:
        page_response = requests.get(url, timeout=5)
    except (ConnectionError, MissingSchema):
        # Invalid URL or a URL missing the protocol are caught here
        data_dict["success"] = False
        return data_dict

    soup = BeautifulSoup(page_response.content, "html.parser")

    pattern_official = re.compile("http[s]{0,1}://ajax\.googleapis\.com/ajax/libs/jquery/([0-9]\.[0-9]+\.[0-9]+)/jquery(\.min){0,1}\.js|http[s]{0,1}://code\.jquery\.com/jquery-([0-9]\.[0-9]+\.[0-9]+)(\.min){0,1}\.js")
    pattern_unofficial = re.compile("jquery(\.min){0,1}\.js")

    abort_loop = False
    for script in soup.findAll('script', {'src': True}):
        # Only collect those script tags which have an 'src' attribute
        if abort_loop:
            break

        match = pattern_official.search(script['src'])
        if match:
            data_dict["uses_jquery"] = "yes"
            data_dict["version"] = match.group(1) if match.group(1) else match.group(3)
            # Tricky part! Replacing the '<' with '&lt;'
            data_dict["found_in_line"] = str(script).split("</script>")[0].replace('<', '&lt;')
            abort_loop = True

        elif (script['src'] == "http://code.jquery.com/jquery-latest.min.js" or
              script['src'] == "https://code.jquery.com/jquery-latest.min.js"):
            data_dict["uses_jquery"] = "yes"
            data_dict["found_in_line"] = str(script).split("</script>")[0].replace('<', '&lt;')
            abort_loop = True

        elif pattern_unofficial.search(script['src']):
            data_dict["uses_jquery"] = "maybe"
            data_dict["found_in_line"] = str(script).split("</script>")[0].replace('<', '&lt;')
            abort_loop = True

    return data_dict

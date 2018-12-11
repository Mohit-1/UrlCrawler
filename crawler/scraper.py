from bs4 import BeautifulSoup
import requests, re
from requests.exceptions import ConnectionError, MissingSchema

def findIfJQueryExists(url):
    """ This method makes a request to the received URL and 
    checks if jQuery exists in the URL's HTML source"""

    success, uses_jquery, version, found_in_line = True, -1, None, None
    data_list = []

    #proxy = {"http": "103.16.70.20:32231"} --- I prefer using proxies while scraping
    #page_response = requests.get(page_link, timeout=5, proxies=proxy) --- omitting here to reduce vectors for failure
    try:
        page_response = requests.get(url, timeout=5)
    
    except (ConnectionError, MissingSchema): #Invalid URL or a URL missing the protocol are caught here
        success, uses_jquery, version, found_in_line = False, -1, None, None
        data_list.append(success)
        data_list.append(uses_jquery)
        data_list.append(version)
        data_list.append(found_in_line)     

        return data_list            

    soup = BeautifulSoup(page_response.content, "html.parser")

    for script in soup.findAll('script', {'src': True}):    # Only collect those script tags which have an 'src' attribute

        match = re.search("http[s]{0,1}://ajax\.googleapis\.com/ajax/libs/jquery/([0-9]\.[0-9]+\.[0-9]+)/jquery(\.min){0,1}\.js", script['src'])
        if match:
            uses_jquery = 1
            version = match.group(1)
            found_in_line = str(script).split("</script>")[0].replace('<', '&lt;')  # Tricky part! Replacing the '<' with '&lt;'
            break

        match = re.search("http[s]{0,1}://code\.jquery\.com/jquery-([0-9]\.[0-9]+\.[0-9]+)(\.min){0,1}\.js", script['src'])
        if match:
            uses_jquery = 1
            version = match.group(1)
            found_in_line = str(script).split("</script>")[0].replace('<', '&lt;')  # Tricky part! Replacing the '<' with '&lt;'
            break

        elif script['src'] == "http://code.jquery.com/jquery-latest.min.js" or script['src'] == "https://code.jquery.com/jquery-latest.min.js":
            uses_jquery = 1
            found_in_line = str(script).split("</script>")[0].replace('<', '&lt;')
            break

        elif re.search("jquery(\.min){0,1}\.js", script['src']):
            uses_jquery = 0
            found_in_line = str(script).split("</script>")[0].replace('<', '&lt;')
            break

    data_list.append(success)
    data_list.append(uses_jquery)
    data_list.append(version)
    data_list.append(found_in_line)     

    return data_list            
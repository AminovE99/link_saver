import urllib.parse as urlparse


def handle_links(links):
    """
    Validate links from usual strings

    :param links: list of strings with possible links
    :return: set of strings
    """
    handled_links = []
    for link in links:
        h_link = urlparse.urlparse(link)
        if not h_link:
            continue
        if h_link.scheme:
            handled_links.append(h_link.netloc)
        elif len(h_link.path.split('.')) > 1:
            handled_links.append(h_link.path)

    # Filter duplicates from list
    handled_links_set = set(handled_links)
    return handled_links_set

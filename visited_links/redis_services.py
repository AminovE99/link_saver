import ast


def save_link_visits(redis_instance, links, timestamp):
    redis_instance.zadd('links', {str(links): timestamp})


def get_links_from(redis_instance, timestamp_from, timestamp_to):
    links = redis_instance.zrangebyscore('links', timestamp_from, timestamp_to)
    all_links = set()
    if not links:
        return []
    for link in links:
        cur_links = ast.literal_eval(link)
        all_links.update(cur_links)
    return all_links

import re

async def extract_domain(url):
    regex_domain = re.compile(r"^(?:https?://)?(?:www\.)?([^/\s]+)")
    coincidence = regex_domain.match(url)
    domain = coincidence.group(1)
    
    return domain
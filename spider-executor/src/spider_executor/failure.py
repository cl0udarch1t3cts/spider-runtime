from spider_executor.models import FailureClass


def classify_runner_failure(message: str) -> FailureClass:
    normalized = message.lower()
    if "429" in normalized or "too many requests" in normalized or "cloudflare" in normalized:
        return FailureClass.HTTP_DATACENTER_BLOCK
    if "timed out" in normalized or "timeout" in normalized:
        return FailureClass.NETWORK_TIMEOUT
    if "name resolution" in normalized or "dns" in normalized:
        return FailureClass.DNS_FAILURE
    if "404" in normalized or "not found" in normalized:
        return FailureClass.HTTP_NOT_FOUND
    if normalized.lstrip().startswith("scraper raised:") and "traceback" in normalized:
        return FailureClass.SCRAPER_EXCEPTION
    return FailureClass.UNKNOWN

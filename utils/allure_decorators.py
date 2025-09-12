import os
import functools

try:
    import allure
    from allure import severity_level as _severity_level
except Exception:  # Allure may not be installed in some contexts
    allure = None
    class _severity_level:  # type: ignore
        BLOCKER = 'blocker'
        CRITICAL = 'critical'
        NORMAL = 'normal'
        MINOR = 'minor'
        TRIVIAL = 'trivial'


def allure_matrix(title=None, description=None, severity=_severity_level.NORMAL, owner=None, link=None, issue=None, testcase=None):
    """Decorator to add Allure metadata dynamically from CI env and supplied args.

    Args accept literals or callables returning strings at runtime.
    link can be a string URL or a tuple (url, name).
    """
    def _resolve(val):
        try:
            return val() if callable(val) else val
        except Exception:
            return val

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if allure:
                try:
                    # Static metadata
                    _t = _resolve(title)
                    _d = _resolve(description)
                    if _t:
                        allure.dynamic.title(str(_t))
                    if _d:
                        allure.dynamic.description(str(_d))
                    if severity:
                        allure.dynamic.severity(severity)
                    if owner:
                        allure.dynamic.label('owner', str(_resolve(owner)))
                    if link:
                        _lnk = _resolve(link)
                        if isinstance(_lnk, (list, tuple)) and len(_lnk) >= 1:
                            url = _lnk[0]
                            name = _lnk[1] if len(_lnk) > 1 else None
                            allure.dynamic.link(str(url), name=str(name) if name else None)
                        else:
                            allure.dynamic.link(str(_lnk))
                    if issue:
                        allure.dynamic.issue(str(_resolve(issue)))
                    if testcase:
                        allure.dynamic.testcase(str(_resolve(testcase)))

                    # Dynamic matrix parameters from env (GitHub Actions matrix)
                    browser = os.getenv('BROWSER', 'chrome')
                    width = os.getenv('SCREEN_WIDTH', '')
                    height = os.getenv('SCREEN_HEIGHT', '')
                    res_name = os.getenv('TEST_NAME', f"{browser}-{width}x{height}")
                    allure.dynamic.parameter('browser', browser)
                    if width and height:
                        allure.dynamic.parameter('resolution', f"{width}x{height}")
                    allure.dynamic.parameter('test_name', res_name)
                except Exception:
                    # Do not fail the test if allure API raises
                    pass
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Re-export severity level for convenience
severity_level = _severity_level



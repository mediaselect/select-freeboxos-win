import logging
import re
import socket

class SensitiveDataFilter(logging.Filter):
    """
    A log-scrubbing filter designed for high-security environments.

    Features:
      - Redacts sensitive keywords (generic scrub)
      - Redacts exact secret values after update_patterns() is called
      - Redacts absolute Windows filesystem paths (e.g. C:\Users\...)
      - Scrubs:
            * record.msg
            * record.args
            * record.exc_info (exception messages)
            * record.exc_text (formatted traceback text)
      - Prevents leakage of secrets in logs AND Sentry
    """

    GENERIC_SENSITIVE_WORDS = [
        "password", "token", "secret", "credential", "auth", "authorization"
    ]

    # Matches absolute Windows paths only (drive-letter based)
    WINDOWS_PATH_RE = re.compile(
        r"[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]*"
    )

    def __init__(self, secrets=None):
        super().__init__()
        self.secret_patterns = []

        if secrets:
            self.update_patterns(secrets)

    def update_patterns(self, secrets: dict):
        """
        Add exact secret values to redact.
        Call this AFTER secrets are loaded.
        """
        self.secret_patterns = []

        for _, value in secrets.items():
            if not value:
                continue

            pattern = re.escape(str(value))
            self.secret_patterns.append(re.compile(pattern))

    def _scrub_string(self, text: str) -> str:
        """Apply keyword, secret, and path scrubbing to any string."""

        if not text:
            return text

        lowered = text.lower()

        # 1. Generic keyword scrubbing
        for word in self.GENERIC_SENSITIVE_WORDS:
            if word in lowered:
                text = re.sub(
                    r"(?i)(" + re.escape(word) + r")\s*[:=]\s*[^\s,]+",
                    r"\1=[REDACTED]",
                    text,
                )

        # 2. Exact secret scrubbing
        for pattern in self.secret_patterns:
            text = pattern.sub("[REDACTED]", text)

        # 3. Windows absolute path scrubbing
        text = self.WINDOWS_PATH_RE.sub("[REDACTED_PATH]", text)

        return text

    def filter(self, record):
        """Main entry point for Python's logging framework."""

        if record.msg:
            record.msg = self._scrub_string(str(record.msg))

        if record.args:
            new_args = []
            for arg in (record.args if isinstance(record.args, tuple) else [record.args]):
                if isinstance(arg, str):
                    new_args.append(self._scrub_string(arg))
                else:
                    new_args.append(arg)
            record.args = tuple(new_args)

        if record.exc_info:
            _, evalue, _ = record.exc_info
            if evalue and hasattr(evalue, "args"):
                new_args = []
                for a in evalue.args:
                    if isinstance(a, str):
                        new_args.append(self._scrub_string(a))
                    else:
                        new_args.append(a)
                evalue.args = tuple(new_args)

        if hasattr(record, "exc_text") and record.exc_text:
            record.exc_text = self._scrub_string(record.exc_text)

        return True


global_sanitizer = SensitiveDataFilter()


def scrub_event(event, hint):
    """
    Privacy-hardened Sentry scrubber.
    """

    scrub = global_sanitizer._scrub_string

    try:
        REAL_HOSTNAME = socket.gethostname()
    except Exception:
        REAL_HOSTNAME = None

    USER_HOME_RE = re.compile(r"/home/[^/]+")

    def redact_user_home(value: str) -> str:
        return USER_HOME_RE.sub("/home/REDACTED_USER", value)

    def redact_hostname(value: str) -> str:
        if REAL_HOSTNAME and REAL_HOSTNAME in value:
            return value.replace(REAL_HOSTNAME, "[REDACTED_HOST]")
        return value

    def sanitize_value(value):
        if isinstance(value, str):
            value = scrub(value)
            value = redact_user_home(value)
            value = redact_hostname(value)
        return value

    def sanitize_dict(d):
        for key, val in list(d.items()):
            if isinstance(val, str):
                d[key] = sanitize_value(val)
            elif isinstance(val, dict):
                sanitize_dict(val)
            elif isinstance(val, list):
                d[key] = [sanitize_value(item) for item in val]
        return d

    # -------- Scrub event structure --------

    if "server_name" in event:
        event["server_name"] = "[REDACTED_HOST]"

    if "request" in event:
        sanitize_dict(event["request"])

    if "extra" in event:
        sanitize_dict(event["extra"])

    if "exception" in event:
        for exc in event["exception"].get("values", []):
            if "value" in exc:
                exc["value"] = sanitize_value(exc["value"])

            if "stacktrace" in exc:
                frames = exc["stacktrace"].get("frames", [])
                for frame in frames:
                    for k in ("filename", "abs_path", "context_line", "function"):
                        if k in frame:
                            frame[k] = sanitize_value(frame[k])

                    if "vars" in frame:
                        sanitize_dict(frame["vars"])

    if "contexts" in event:
        sanitize_dict(event["contexts"])

    if "breadcrumbs" in event:
        for crumb in event["breadcrumbs"].get("values", []):
            sanitize_dict(crumb)

    if "extra" in event:
        if "sys.argv" in event["extra"]:
            event["extra"]["sys.argv"] = ["[REDACTED_ARG]"]

        if "cwd" in event["extra"]:
            event["extra"]["cwd"] = "[REDACTED_CWD]"

    return event

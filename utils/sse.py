def sse_format(event: str, data: str, retry: int | None = None) -> str:
    """
    Helper function to format a Server-Sent Event (SSE) message.

    Args:
        event: The name/type of the event.
        data: The data payload as a string.
        retry: Optional retry timeout in milliseconds.

    Returns:
        A formatted SSE message string.
    """
    output = f"event: {event}\n"
    if retry is not None:
        output += f"retry: {retry}\n"
    # Ensure each line of data is prefixed with "data: "
    for line in data.splitlines():
        output += f"data: {line}\n"
    output += "\n"  # An extra newline indicates the end of the message.
    return output 
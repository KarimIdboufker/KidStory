def format_response(data, split_by=". ", max_length=100):
    """
    Splits and formats text into comic pages.
    """
    sentences = data.split(split_by)
    pages = []
    buffer = ""
    for sentence in sentences:
        if len(buffer) + len(sentence) <= max_length:
            buffer += sentence + split_by
        else:
            pages.append(buffer.strip())
            buffer = sentence + split_by
    if buffer:
        pages.append(buffer.strip())
    return [{"index": i, "text": page} for i, page in enumerate(pages)]
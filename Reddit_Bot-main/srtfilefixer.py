def format_text(input_file, output_file, max_chars=100):
    with open(input_file, 'r') as f:
        text = f.read()

    # Remove line breaks
    text = text.replace('\n', ' ')

    words = text.split()
    lines = []
    line = []

    for word in words:
        if len(' '.join(line + [word])) <= max_chars:
            line.append(word)
        else:
            lines.append(' '.join(line))
            line = [word]

    if line:
        lines.append(' '.join(line))

    # Add an additional new line between each line
    formatted_text = '\n\n'.join(lines)

    with open(output_file, 'w') as f:
        f.write(formatted_text)

input_file = "temp_files/askreddit.txt"
output_file = "temp_files/output.txt"
format_text(input_file, output_file)

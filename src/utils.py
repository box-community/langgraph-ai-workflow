from IPython.display import Image


def save_image(image: Image, filename):
    """Save the image to a file."""
    with open(filename, "wb") as f:
        f.write(image.data)


def save_markdown(markdown: str, filename):
    """Save the markdown to a file."""
    with open(filename, "w") as f:
        f.write(markdown)

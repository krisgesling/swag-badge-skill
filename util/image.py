from PIL import Image


def image_to_pixels(image_path):
    THRESHOLD = 70
    invert = False
    screen_height = 64
    screen_width = 128
    header_height = 16
    # TODO FIX THIS
    # max_height = screen_height - header_height
    # max_width = screen_width
    max_height = 54
    max_width = 54

    # to understand how this funtion works you need to understand how the
    # Mark I arduino proprietary encoding works to display to the faceplate
    img = Image.open(image_path).convert("RGBA")
    img2 = Image.new("RGBA", img.size, (255, 255, 255))
    width = img.size[0]
    margin_side = int((screen_width - width) / 2)
    height = img.size[1]
    margin_bottom = int((screen_height - header_height - height) / 2)

    # strips out alpha value and blends it with the RGB values
    img = Image.alpha_composite(img2, img)
    img = img.convert("L")

    # crop image to only allow a max width
    if width > max_width:
        img = img.crop((0, 0, max_width, height))
        width = img.size[0]
        height = img.size[1]

    # crop the image to limit the max height
    if height > max_height:
        img = img.crop((0, 0, width, max_height))
        width = img.size[0]
        height = img.size[1]

    # Extract only the image pixels that meet the threshold
    # Image must be flipped as (0, 0) is the bottom left.
    pixels = []
    for x in range(width):
        for y in range(height):
            below_threshold = img.getpixel((x, y)) < THRESHOLD
            if (below_threshold and invert is False) or (
                not below_threshold and invert
            ):
                # TODO FIX THIS
                # x_coord = max_width - x + margin_side
                # y_coord = max_height - y + margin_bottom
                x_coord = x + margin_side
                y_coord = max_height - y - margin_bottom * 2
                pixels.append((x_coord, y_coord))

    return pixels

"""Build a 52-card blackjack deck from the Major Arcana tarot PNGs (00-21).

Each blackjack rank is drawn with one tarot card:
    A=01 Magician, 2=02 High Priestess, ... 10=10 Wheel of Fortune,
    J=11 Justice, Q=12 Hanged Man, K=13 Death

The printed tarot numbers in the corners are painted over and replaced with
the blackjack rank and suit symbol, so players never confuse "XIII" with a 13.

Usage:
    python make_cards.py [source_png_dir] [output_dir]

Output files are named "<rank>_<suit>.png" (for example "A_hearts.png",
"10_spades.png") so they match Card.rank and Card.suit in backend/card.py.
"""

import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

SRC = sys.argv[1] if len(sys.argv) > 1 else "PNG"
OUT = sys.argv[2] if len(sys.argv) > 2 else "assets/cards"

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = {"hearts": "\u2665", "diamonds": "\u2666", "clubs": "\u2663", "spades": "\u2660"}

# Which Major Arcana number (01-13) is used for each rank.
ART_NUMBER = {rank: i + 1 for i, rank in enumerate(RANKS)}

CARD_BG = (12, 7, 25)          # dark navy used by the original card frame
RED = (225, 70, 70)
IVORY = (240, 236, 220)
GOLD = (212, 175, 55)

# Corner area (in original 456x638 pixels) that holds the printed tarot number.
CORNER = (8, 10, 80, 86)       # left, top, right, bottom (top-left corner)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SUIT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

FINAL_SIZE = (300, 420)        # saved size (original is 456x638)


def find_art(number: int) -> str:
    """Return the source PNG path whose file name starts with the 2-digit number."""
    matches = glob.glob(os.path.join(SRC, f"{number:02d}-*.png"))
    if not matches:
        raise FileNotFoundError(f"No tarot PNG numbered {number:02d} in {SRC}")
    return matches[0]


def corner_layer(size, rank: str, suit: str) -> Image.Image:
    """Draw a clean top-left corner (rank + suit) on a transparent layer."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    left, top, right, bottom = CORNER
    cx = (left + right) // 2

    color = RED if suit in ("hearts", "diamonds") else IVORY
    rank_font = ImageFont.truetype(FONT_BOLD, 40 if len(rank) == 1 else 34)
    suit_font = ImageFont.truetype(FONT_SUIT, 34)

    draw.text((cx, top + 20), rank, font=rank_font, fill=color, anchor="mm")
    draw.text((cx, top + 58), SUITS[suit], font=suit_font, fill=color, anchor="mm")
    return layer


def paint_corner(card: Image.Image, rank: str, suit: str) -> Image.Image:
    """Cover the tarot numerals with the frame color and add rank + suit."""
    card = card.convert("RGBA")
    w, h = card.size
    left, top, right, bottom = CORNER

    # 1) Cover the old numerals (top-left and the rotated bottom-right copy).
    #    Only pixels that are already opaque are changed, so the rounded
    #    card corners stay transparent.
    for box in (CORNER, (w - right, h - bottom, w - left, h - top)):
        patch = card.crop(box)
        solid = Image.new("RGBA", patch.size, CARD_BG + (255,))
        alpha = patch.getchannel("A")
        patch = Image.composite(solid, patch, alpha)
        card.paste(patch, box[:2])

    # 2) Draw the new corner top-left, and a 180-degree copy bottom-right.
    layer = corner_layer(card.size, rank, suit)
    card.alpha_composite(layer)
    rotated = layer.rotate(180)
    card.alpha_composite(rotated)
    return card


def make_back(size) -> Image.Image:
    """Create a simple tarot-style card back (navy, gold border, star)."""
    w, h = size
    back = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(back)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=38, fill=CARD_BG + (255,))
    draw.rounded_rectangle((22, 22, w - 23, h - 23), radius=24, outline=GOLD, width=4)
    draw.rounded_rectangle((36, 36, w - 37, h - 37), radius=16, outline=GOLD, width=1)

    cx, cy = w // 2, h // 2
    for r in (150, 110, 70):
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD, width=2)

    # 8-point star made from two rotated squares.
    import math
    for offset in (0, 45):
        pts = []
        for k in range(4):
            ang = math.radians(offset + 90 * k + 45)
            pts.append((cx + 105 * math.cos(ang), cy + 105 * math.sin(ang)))
        draw.polygon(pts, outline=GOLD, width=3)
    draw.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=GOLD)
    return back


def main() -> None:
    os.makedirs(OUT, exist_ok=True)

    for rank in RANKS:
        art = Image.open(find_art(ART_NUMBER[rank]))
        for suit in SUITS:
            card = paint_corner(art, rank, suit)
            card = card.resize(FINAL_SIZE, Image.LANCZOS)
            card.save(os.path.join(OUT, f"{rank}_{suit}.png"), optimize=True)

    make_back(Image.open(find_art(1)).size).resize(FINAL_SIZE, Image.LANCZOS).save(
        os.path.join(OUT, "back.png"), optimize=True
    )
    print(f"Saved 52 cards + back.png to {OUT}")


if __name__ == "__main__":
    main()

from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# ======= פונקציה לתיקון טקסט בעברית =========
def fix_rtl_text(text: str) -> str:
    reshaped_text = arabic_reshaper.reshape(text)      # מסדר את האותיות
    bidi_text = get_display(reshaped_text)             # הופך לכיוון RTL
    return bidi_text

# ======= פונקציית יצירת התמונה =========
def create_certificate(name, class_name):
    img = Image.open("fix.png")  # התבנית שלך
    draw = ImageDraw.Draw(img)

    # פונטים — ודא שקובץ arial.ttf קיים בתיקייה
    font_name = ImageFont.truetype("arial.ttf", 40)
    font_class = ImageFont.truetype("arial.ttf", 40)

    # קואורדינטות (התאם לפי הצורך)
    name_position = (500, 372)
    class_position = (600, 260)

    # כתיבה על התמונה (כולל תיקון כיוון הטקסט)
    draw.text(name_position, fix_rtl_text(name), fill="black", font=font_name)
    draw.text(class_position, fix_rtl_text(class_name), fill="black", font=font_class)

    # שמירה לקובץ
    output_path = f"{name}_certificate.png"
    img.save(output_path)
    print(f"✅ נוצרה תעודה: {output_path}")
    return output_path

# ======= הרצה לדוגמה =========
if __name__ == "__main__":
    name = "שחר דורון"
    class_name = "'יא3"
    create_certificate(name, class_name)

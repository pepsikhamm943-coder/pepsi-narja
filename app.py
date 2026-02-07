import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="LINE Sticker Maker", layout="wide")

st.title("🎨 AI LINE Sticker Maker")
st.write("อัปโหลดรูป -> ใส่ข้อความ -> ใช้งานได้เลย!")

with st.sidebar:
    st.header("⚙️ ตั้งค่าสติกเกอร์")
    uploaded_files = st.file_uploader("1. อัปโหลดรูป", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    sticker_text = st.text_input("2. ข้อความ", "สวัสดี")
    mood = st.selectbox("3. โทนอารมณ์", ["สดใส (ชมพู)", "ดุดัน (แดง)", "สุขุม (น้ำเงิน)", "กวนๆ (เหลือง)"])
    count_option = st.selectbox("4. จำนวนรูปที่ต้องการ", [1, 8, 16, 24, 32, 40])
    show_text = st.checkbox("5. แสดงข้อความบนสติกเกอร์", value=True)
    text_size = st.slider("ขนาดตัวอักษร", 20, 60, 40)

mood_colors = {
    "สดใส (ชมพู)": "#FF69B4", 
    "ดุดัน (แดง)": "#FF0000", 
    "สุขุม (น้ำเงิน)": "#1E90FF", 
    "กวนๆ (เหลือง)": "#FFD700"
}

def add_text_to_image(img, text, color, font_size):
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (img.width - text_width) // 2
    y = img.height - text_height - 20
    shadow_offset = 2
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill="black")
    draw.text((x, y), text, font=font, fill=color)
    return img

if st.button("🚀 เริ่มสร้างสติกเกอร์"):
    if not uploaded_files:
        st.warning("กรุณาอัปโหลดรูปภาพก่อนครับ")
    else:
        selected_color = mood_colors[mood]
        cols = st.columns(3)
        for i in range(min(len(uploaded_files), count_option)):
            img = Image.open(uploaded_files[i]).convert("RGBA")
            
            img.thumbnail((370, 320))
            canvas = Image.new("RGBA", (370, 320), (255, 255, 255, 0))
            offset = ((370 - img.width) // 2, (320 - img.height) // 2)
            canvas.paste(img, offset, img)
            
            if show_text and sticker_text:
                canvas = add_text_to_image(canvas, sticker_text, selected_color, text_size)
            
            with cols[i % 3]:
                st.image(canvas)
                buf = io.BytesIO()
                canvas.save(buf, format="PNG")
                st.download_button(f"📥 โหลดรูป {i+1}", buf.getvalue(), f"sticker_{i+1}.png", "image/png", key=f"download_{i}")

st.info("💡 เคล็ดลับ: LINE Sticker ควรมีขนาด 370×320 พิกเซล และพื้นหลังโปร่งใส")

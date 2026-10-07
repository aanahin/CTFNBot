import os
from pyrogram import Client, filters
from pyrogram.types import Message

# আপনার দেওয়া বোট টোকেনটি এখানে সেট করা হয়েছে
BOT_TOKEN = "8601974611:AAEjil88WXDb_YiPsI9fifcigTTb9j5C7wU"

# এটি টেলিগ্রামের অফিসিয়াল ওপেন ডেমো আইডি ও হ্যাশ (সবার জন্য এক, তাই পরিবর্তনের প্রয়োজন নেই)
API_ID = 6
API_HASH = "eb06d4ab2fb49da28fa9d77cfc94e6df"

app = Client("caption_renamer_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.video | filters.document)
async def rename_video(client: Client, message: Message):
    if not message.caption:
        await message.reply_text("❌ এই ভিডিওটিতে কোনো ক্যাপশন দেওয়া নেই। অনুগ্রহ করে ক্যাপশনসহ ভিডিও পাঠান।")
        return

    # ক্যাপশনের টেক্সট থেকে ফাইলের নাম তৈরি এবং অবৈধ ক্যারেক্টার বাদ দেওয়া
    clean_name = "".join(c for c in message.caption if c.isalnum() or c in (' ', '_', '-', '.')).strip()
    
    file_ext = ".mp4"
    if message.document and message.document.file_name:
        if "." in message.document.file_name:
            file_ext = "." + message.document.file_name.split(".")[-1]
            
    new_file_name = f"{clean_name}{file_ext}"
    status_message = await message.reply_text("⏳ নাম পরিবর্তন করে প্রসেস করা হচ্ছে...")

    try:
        # ফাইলটি লোকালি ডাউনলোড হচ্ছে
        download_path = await message.download(file_name=new_file_name)
        
        # নতুন নাম দিয়ে ফাইলটি আবার ইউজারকে ব্যাক পাঠানো হচ্ছে
        await message.reply_document(
            document=download_path, 
            file_name=new_file_name,
            caption=f"✅ সফলভাবে রিনেম করা হয়েছে:\n`{new_file_name}`"
        )
        
        # কাজ শেষে মেমোরি খালি করার জন্য ফাইলটি ডিলিট করা
        if os.path.exists(download_path):
            os.remove(download_path)
        await status_message.delete()
        
    except Exception as e:
        await status_message.edit_text(f"❌ সমস্যা: {str(e)}")

print("🤖 বোট সফলভাবে চালু হয়েছে...")
app.run()

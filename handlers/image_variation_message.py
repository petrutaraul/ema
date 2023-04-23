import os
def image_variation_image(bot, Image, openai, message, is_reply=False):
    # Get the file ID of the photo
    file_id = ''
    
    if is_reply:
        file_id = message.reply_to_message.photo[-1].file_id
    else:
        file_id = message.photo[-1].file_id
        
    # Get the file path of the photo
    file_info = bot.get_file(file_id)

    # Download the image and save it locally
    downloaded_file = bot.download_file(file_info.file_path)
    with open('received_image.jpg', 'wb') as image_file:
        image_file.write(downloaded_file)
        
    # Convert the image to PNG format
    img = Image.open('received_image.jpg')
    converted_img = img.convert('RGB')

    # Resize the image to a smaller dimension if necessary
    smaller_dimension = (1024, 1024)  # Adjust this value based on the required image dimensions
    resized_img = converted_img.resize(smaller_dimension)

    # Save the image as a PNG with optimization and compression
    resized_img.save('received_image.png', 'PNG', optimize=True, compress_level=9)

    # Read the saved image as bytes
    with open('received_image.png', 'rb') as image_file:
        resized_img_bytes = image_file.read()

        # Create a variation of the image using OpenAI API
        response = openai.Image.create_variation(
            image=resized_img_bytes,
            n=1,
        )
    
    # Get the URL of the new image
    image_url = response['data'][0]['url']
    
    # Send the new image to the user
    bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_to_message_id=message.message_id)

    # Delete the jpg and png file form locally
    os.remove('received_image.jpg')
    os.remove('received_image.png')
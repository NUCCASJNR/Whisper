#!/usr/bin/env python3

"""Handles Uploading of images and files to Cloudinary"""

import logging

from cloudinary.uploader import upload

logger = logging.getLogger("apps")


def upload_profile_pic(image, user_id: str) -> str:
    try:
        result = upload(image, folder=f"Whisper/Profile/{user_id}")
        if result and result.get("secure_url"):
            return result.get("secure_url")
        logger.error("No secure_url returned from Cloudinary.")
        raise Exception("Cloudinary upload failed.")
    except Exception as e:
        logger.error(f"Cloudinary error: {e}")
        raise

# def upload_profile_pic(image, user_id: str) -> str:
#     """
#     Uploads the user's profile picture to Cloudinary
#     :param image: The image to be uploaded
#     :param user_id: The user's ID
#     :return: The URL of the uploaded image
#     """
#     result = None
#     try:
#         result = upload(image, folder=f'Whisper/Profile/{user_id}')
#         print(f'Upload Result: {result}')
#         logger.info(f'Upload Result: {result}')
#         # Update user's profile picture URL if upload is successful
#         if result and result.get("secure_url"):
#             MainUser.custom_update(
#                 filter_kwargs={'id': user_id},
#                 update_kwargs={'profile_pic': result.get("secure_url")}
#             )
#             logger.info(f"Secure Url: {result.get('secure_url')}")
#             return result.get('secure_url')
#         else:
#             logger.error("Upload failed; no result returned from Cloudinary.")
#             raise ValueError("Failed to upload image")

#     except Exception as e:
#         logger.error(f"Error uploading image due to: {str(e)}")
#         return "An error occurred during image upload."

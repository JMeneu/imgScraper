from ImgScraper import ImgScraper as img

instance = img()
option_instance, username_instance, password_instance, threshold_instance, path_instance, weblink_instance = \
    img.login_info(instance)
driver_instance, threshold_instance, path_instance , weblink_instance = img.webpage_login(instance, option_instance,
    username_instance, password_instance, threshold_instance, path_instance, weblink_instance)
driver_instance, last_page_instance = img.webpage_to_download(option_instance, driver_instance, weblink_instance)
img.download(instance, option_instance, last_page_instance, weblink_instance, path_instance, threshold_instance)
img.close(driver_instance)
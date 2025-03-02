from inky.auto import auto
import image

inky = auto(ask_user = True, verbose = True)
img = image.create_image()

inky.set_image(img)
inky.show()

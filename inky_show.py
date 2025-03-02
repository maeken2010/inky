from inky.auto import auto
import image

def show():
    inky = auto(ask_user = True, verbose = True)
    img = image.create_image()

    inky.set_image(img)
    inky.show()

if __name__ == "__main__":
    show()

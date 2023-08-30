"""

Package:

    terminal-animation

"""

import animation  # from this package
import time


def using_package_as_class():
    wait_animation = animation.Wait()
    wait_animation.start()
    time.sleep(5)
    wait_animation.stop()


@animation.wait()
def using_package_as_decorator():

    print("oafs")
    time.sleep(1)
    print("oafs")
    print("oafs")
    time.sleep(2)
    print("oafs")
    time.sleep(2)
    print("oafs")


if __name__ == '__main__':

    using_package_as_decorator()

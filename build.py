import os, sys
import platform

def system(command):
    retcode = os.system(command)
    if retcode != 0:
        raise Exception("Error while executing:\n\t %s" % command)

if __name__ == "__main__":
    system('conan export demo/opencv')
    params = " ".join(sys.argv[1:])

    if platform.system() == "Windows":
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MD -s build_type=Release -o OpenCV:shared=False --build=missing %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MT -s build_type=Release -o OpenCV:shared=False --build=missing %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MD -s build_type=Release -o OpenCV:shared=True --build=missing %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MT -s build_type=Release -o OpenCV:shared=True --build=missing %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MTd -s build_type=Debug -o OpenCV:shared=False --build=missing %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MDd -s build_type=Debug -o OpenCV:shared=True --build=missing %s' % params)
    else:
        pass
from conans import ConanFile, CMake
import os, fnmatch

class OpenCVConan(ConanFile):
    # Description must be very short for conan.io
    description = "OpenCV: Open Source Computer Vision Library."
    name = "OpenCV"
    version = "3.2.0"
    opencv_version_suffix = "320"
    settings = "os", "compiler", "build_type", "arch"
    requires = "libjpeg-turbo/1.5.1@lasote/stable"
    options = {
        "shared": [True, False]
    }
    default_options = "shared=False"
    url = "https://github.com/ohhi/conan-opencv"
    license = "http://http://opencv.org/license.html"
    generators = "cmake", "txt"
    short_paths = True
    
    def source(self):
        self.run("git clone https://github.com/opencv/opencv.git")
        self.run("cd opencv && git checkout tags/3.2.0")

    def imports(self):
        self.copy("*", dst="jpeg-turbo", src="")
        
    def build(self):
        cmake = CMake(self)
        cmake_options = {
            "CMAKE_INSTALL_PREFIX": "install",
            "WITH_OPENXL": False,
            "WITH_IPP": True,
            "WITH_QT": False,
            "WITH_GTK": False,
            "WITH_OPENGL": False,
            "WITH_CUDA": False,
            "WITH_JPEG": True,
            "JPEG_INCLUDE_DIR": "jpeg-turbo/include",
            "JPEG_LIBRARY": "jpeg-turbo/lib/jpeg-static.lib",
            "BUILD_JPEG": False,
            "WITH_PNG": True,
            "BUILD_PNG": True,
            "WITH_JASPER": True,
            "BUILD_JASPER": True,
            "WITH_ZLIB": True,
            "BUILD_ZLIB": True,
            "WITH_TIFF": True,
            "BUILD_TIFF": True,
            "WITH_TBB": False,
            "BUILD_TBB": False,
            "WITH_OPENEXR": True,
            "BUILD_OPENEXR": True,
            "WITH_WEBP": True,
            "BUILD_WEBP": True,
            "BUILD_SHARED_LIBS": self.options.shared,
            "BUILD_TESTS": False,
            "BUILD_PERF_TESTS": False,
            "BUILD_opencv_apps": False,
            "CPACK_BINARY_NSIS": False,
            "BUILD_opencv_calib3d": True,
            "BUILD_opencv_features2d": True,
            "BUILD_opencv_flann": True,
            "BUILD_opencv_highgui": True,
            "BUILD_opencv_imgcodecs": True,
            "BUILD_opencv_imgproc": True,
            "BUILD_opencv_ml": True,
            "BUILD_opencv_objectdetect": True,
            "BUILD_opencv_photo": True,
            "BUILD_opencv_shape": True,
            "BUILD_opencv_stitching": True,
            "BUILD_opencv_superres": True,
            "BUILD_opencv_ts": True,
            "BUILD_opencv_video": True,
            "BUILD_opencv_videoio": True,
            "BUILD_opencv_videostab": True
        }

        if self.settings.compiler == "Visual Studio":
            cmake_options["BUILD_WITH_STATIC_CRT"] = self.settings.compiler.runtime in ["MT","MTd"]
        cmake.configure(defs=cmake_options, source_dir="opencv")
        cmake.build(target="install")

    def package(self):
        self.copy(pattern="*.h*", dst="include", src =os.path.join("install", "include"), keep_path=True)

        if self.settings.os == "Windows":
            self.copy(pattern="*.lib", dst="lib", src="3rdparty\\lib", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="3rdparty\\ippicv\\ippicv_win\\lib\\intel64", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="install", keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.exe", dst="bin", src="bin", keep_path=False)

        if self.settings.os == "Linux":
            self.copy(pattern="*.a", dst="lib", src="3rdparty/lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="3rdparty/ippicv/ippicv_lnx/lib/intel64", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="install", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="install", keep_path=False)

    def package_info(self):
        libs_opencv = [
            "opencv_calib3d",
            "opencv_flann",
            "opencv_highgui",
            "opencv_imgcodecs",
            "opencv_imgproc",
            "opencv_ml",
            "opencv_objdetect",
            "opencv_photo",
            "opencv_shape",
            "opencv_stitching",
            "opencv_superres",
            "opencv_video",
            "opencv_videoio",
            "opencv_videostab",
            "opencv_core" # GCC wants this last
        ]
        libs_3rdparty = [
            "zlib",
            "libpng",
            "libjasper",
            "libtiff",
            "libwebp",
            "IlmImf"
        ]
        libs_win = [
            "ippicvmt"
        ]
        libs_linux = [
            "ippicv",
            "pthread",
            "dl" # GCC wants this last
        ]
        if self.settings.compiler == "Visual Studio":
            debug_suffix = ("d" if self.settings.build_type=="Debug" else "")
            libs_opencv_win = map(lambda n: n + self.opencv_version_suffix + debug_suffix, libs_opencv)
            libs_3rdparty_win = map(lambda n: n + debug_suffix, libs_3rdparty)
            libs = libs_opencv_win + libs_3rdparty_win + libs_win
            self.cpp_info.libs.extend(libs)
        elif self.settings.compiler == "gcc":
            libs = libs_opencv + libs_3rdparty + libs_linux
            self.cpp_info.libs.extend(libs)

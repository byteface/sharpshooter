from setuptools import setup, find_packages

with open("README.md", "r") as f:
        long_description=f.read()


from sharpshooter import __version__
version = __version__
# version = '0.0.1'

setup(
  name='sharpshooter',
  version=version,
  author="@byteface",
  author_email="byteface@gmail.com",
  license="MIT",
  url='https://github.com/byteface/sharpshooter',
  download_url='https://github.com/byteface/sharpshooter/archive/' + version + ' .tar.gz',
  description='Shorthand for creating files and folders.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords=['shorthand', 'files', 'folders', 'filesytem', 'tree', 'template', 'automation', 'mock', 'directory', 'mkdir', 'shutil'],
  python_requires='>=3.6',
  classifiers=[
      "Programming Language :: Python :: 3",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Development Status :: 4 - Beta",
      "Intended Audience :: Developers",
      "Intended Audience :: Other Audience",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Topic :: Software Development",
      "Topic :: Terminals",
      "Topic :: Utilities",
      'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  install_requires=[
          'ply==3.11'
  ],
  packages=find_packages(),
  include_package_data=True,
)

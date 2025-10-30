from setuptools import setup, find_packages

setup(
    name="multilingual-voice-recognition",
    version="1.0.0",
    author="Your Name",
    description="A comprehensive multilingual voice recognition system",
    packages=find_packages(),
    install_requires=[
        "SpeechRecognition>=3.10.0",
        "pyaudio>=0.2.13",
        "pocketsphinx>=5.0.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
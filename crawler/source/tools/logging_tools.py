from logging import INFO, basicConfig, exception, warning, error, info

basicConfig(filename="logs.log", format='[%(asctime)s] %(name)s - (%(levelname)s) %(message)s', datefmt='%Y/%m/%d %H:%M:%S',level=INFO)
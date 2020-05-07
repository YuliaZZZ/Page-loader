import os
import sys
import time

from progress.bar import ShadyBar

from loader.files_creator import (download_page, make_local_site,
                                  write_in_file)
from loader.log import SomeException
from loader.names_creator import make_directoryname, make_filename


def create_directory(name_directory, logger):
    try:
        os.mkdir(name_directory, mode=0o700, dir_fd=None)
    except PermissionError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Нет прав на внесение изменений.')
        raise SomeException() from e
    return str(name_directory)


def make_loader(site, directory, logger):
    with ShadyBar('Loading',
                  suffix='%(percent)d%% [%(eta_td)s]') as bar:
        for i in range(1):
            bar.next()
            time.sleep(0.001)
            logger.info('Start program.')
            content = download_page(site, logger)
            logger.info('Page uploaded.')
            file_html = make_filename(site, directory)
            new_directory = create_directory(
                          make_directoryname(file_html), logger)
            logger.info('Directory created.')
            new_content, items_src = make_local_site(content,
                                                     file_html, site,
                                                     new_directory)
            logger.info('The content changed.')
            write_in_file(new_content, file_html, logger)
            logger.info('The changed content saved in file.')
        for i in bar.iter(items_src):
            for (link, file_n) in items_src:
                write_in_file(download_page(link, logger, main_page=1),
                              file_n, logger)
    logger.info('All files uploaded. The end.')

from loader.filesmaker import (create_directory, download_page, files_loader,
                               make_localsite)
from loader.nameholder import make_directname, make_filename
from loader.scripts.page_loader import logger


def app(site, directory):
    logger.info('Start program.')
    content = download_page(site)
    logger.info('Page uploaded.')
    file_html = make_filename(site, directory)
    new_directory = create_directory(make_directname(file_html))
    logger.info('Directory created.')
    items_src = make_localsite(content, file_html, site, new_directory)
    logger.info('The content changed and saved in file.')
    files_loader(items_src, show_progr=True)
    logger.info('All files uploaded. The end.')

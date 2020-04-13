from loader.scripts.page_loader import logger
from loader.created import page_load, create_name_file, create_catalog   # noqa E501
from loader.file_conversion import change_html


def app(site, way):
    file1 = page_load(site, create_name_file(site, way))
    logger.info('File created!')
    catalog = create_catalog(file1)
    logger.info('Catalog created!')
    change_html(file1, catalog, site)
    logger.info('Files upload!')
    return file1

from loader.created import page_load, create_name_file, create_catalog   # noqa E501
from loader.file_conversion import change_html
import logging


logging.basicConfig(filename='logsapp.log',
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')   # noqa E501


def app(site, way, logslevel):
    logger = logging.getLogger(__name__)
    logger.setLevel(logslevel)
    logger.debug('Start programm.')
    file1 = page_load(site, create_name_file(site, way))
    logger.info('The file has been successfully downloaded.')
    catalog = create_catalog(file1)
    logger.info('The catalog has been successfully created.')
    change_html(file1, catalog, site)
    logger.info('The file has been changed.')
    logger.debug('Programm finish!')
    return file1

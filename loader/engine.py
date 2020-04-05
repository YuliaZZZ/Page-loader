from loader.created import page_load, create_name_file, create_catalog   # noqa E501
from loader.file_conversion import change_html


def app(site, way):
    file1 = page_load(site, create_name_file(site, way))
    catalog = create_catalog(file1)
    change_html(file1, catalog, site)
    return file1

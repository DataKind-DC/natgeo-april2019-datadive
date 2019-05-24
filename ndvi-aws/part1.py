from datetime import date
import os

import requests
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt


def get_products_list(start=date(2018, 1, 1), end=date(2018, 12, 31)):
    api = SentinelAPI(os.environ.get('COPUSER'), os.environ.get('COPPASS'), 'https://scihub.copernicus.eu/dhus')
    footprint = geojson_to_wkt(read_geojson('zambezi.geojson'))
    products = api.query(footprint,
                         date = (date(2018, 1, 1), end),
                         platformname = 'Sentinel-2',
                         cloudcoverpercentage = (0, 0))
    print("Found "+str(len(products))+" products matching search criteria")
    return products


def get_band_uris(product_uuid, product_dict):
    base_url = "https://scihub.copernicus.eu/dhus/odata/v1/"
    url = f"{base_url}Products('{product_uuid}')/Nodes('{product_dict['identifier']}.SAFE')/Nodes('GRANULE')/Nodes?$format=json"
    session = requests.Session()
    session.auth = (os.environ.get('COPUSER'), os.environ.get('COPPASS'))
    nodes = session.get(url).json()
    granules = nodes['d']['results']
    uris = {}
    for granule in granules:
        name = granule['Name']
        bands_uri = granule['__metadata']['uri']
        bands_url = f"{bands_uri}/Nodes('IMG_DATA')/Nodes?$format=json"
        bands_nodes = session.get(bands_url).json()
        for band in bands_nodes['d']['results']:
            uris[band['Name']] = band['__metadata']['uri']
    return uris


def new_image_name(original_name, uuid):
    parts = original_name.split('.')
    return f"{parts[0]}_{uuid}.{parts[1]}"


if __name__ == "__main__":
    products = get_products_list()
    for puuid in products:
        print("Working on product:", puuid)
        product = products[puuid]
        all_bands = get_band_uris(puuid, product)
        nvdi_bands = {band: all_bands[band] for band in all_bands.keys() if 'B04.jp2' in band or 'B08.jp2' in band or 'RCI.jp2' in band}
        for img in nvdi_bands:
            new_name = new_image_name(img, puuid)
            with open("tilelist.txt", 'a') as f:
                f.write(f"{new_name}\t{nvdi_bands[img]}/$value\n")


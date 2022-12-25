import json
from coloring import *
import xml.etree.ElementTree as ET

COUNTRY_CODES_FILE = 'country_codes.json'
NEIGHBOR_FILE = 'neighbors.json'
WHITEMAP_FILE = 'whitemap.svg'
COLORMAP_FILE = 'colormap.svg'

def get_neighbors(codefile=COUNTRY_CODES_FILE, neighborfile=NEIGHBOR_FILE):
    with open(codefile, 'r') as file:
        countries = json.load(file)

    with open(neighborfile, 'r') as file:
        neighbors = json.load(file)

    infodict = {country['Name']: {'Code': country['Code'], 'Neighbors': None} for country in countries}
    for couple in neighbors:
        try:
            if infodict[couple['countryLabel']]['Neighbors']:
                infodict[couple['countryLabel']]['Neighbors'].append(couple['neighborLabel'])
            else:
                infodict[couple['countryLabel']]['Neighbors'] = [couple['neighborLabel']]
        except KeyError:
            pass

    neighbordict = {}
    for country in infodict:
        if infodict[country]['Neighbors'] is not None:
            neighbordict[infodict[country]['Code'].lower()] = [infodict[neighbor]['Code'].lower() for neighbor in infodict[country]['Neighbors']]
    return neighbordict

def get_map_colors(neighbordict):
    edgelist = []
    for country in neighbordict:
        for neighbor in neighbordict[country]:
            if (country, neighbor) not in edgelist and (neighbor, country) not in edgelist:
                edgelist.append((country, neighbor))
    G = nx.Graph(edgelist)
    stack = simplify(G, ['purple', 'blue', 'pink', 'grey'])
    color_map = rebuild(G, stack, ['purple', 'lightblue', 'pink', 'grey'])
    return color_map


def color_svg_map(colordict, infile=WHITEMAP_FILE, outfile=COLORMAP_FILE):
    tree = ET.parse(infile)
    root = tree.getroot()

    for element in root.iter():
        if "style" in element.attrib and element.attrib["id"] in colordict:
            style = element.attrib["style"]
            style = style.replace("fill:white", f"fill:{colordict[element.attrib['id']]}")
            element.attrib["style"] = style

    tree.write(outfile)


if __name__ == '__main__':
    neighbordict = get_neighbors()
    colordict = get_map_colors(neighbordict)
    color_svg_map(colordict)



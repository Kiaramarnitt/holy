from pylode import OntDoc
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


HOLY_TTL_PATH = './holy.ttl' 
SAMPLE_HTML_PATH = './documentation/resources/template.html'
GEN_HTML_PATH = './holy.html'

# initialise
od = OntDoc(ontology=HOLY_TTL_PATH)
tar_file = open(SAMPLE_HTML_PATH, "r", encoding='utf-8')

gen_html = od.make_html()
gensoup = BeautifulSoup(gen_html)

tar_html = tar_file.read()
tarsoup = BeautifulSoup(tar_html)

with open(HOLY_TTL_PATH, 'r', encoding='utf-8') as file:
    ttllines = file.readlines()
ttltext = ''.join(ttllines).replace('\n','')

# Version 

baseline = [line for line in ttllines if line.startswith('@base')][0]
version = re.search(r'@base(.+)\.\n', baseline).groups()[0].strip('<> ')

version_block = [i for i in tarsoup.find(id='metadata').find_all('div') if 'This version' in i.dt.get_text()][0]
version_block.dd.decompose()

version_add = BeautifulSoup('<dd><a href="%s">%s</a></dd>' %(version, version)).dd
version_block.append(version_add)


# Publisher
publisher = re.search(r'dct:publisher\s*\[\s*foaf:homepage(.*?)\s*;\s*foaf:name(.*?)\]', ttltext).groups()
publisher_homepage, publisher_name = publisher[0].strip('<> '), publisher[1].strip('" ')

publisher_block = [i for i in tarsoup.find(id='metadata').find_all('div') if 'Publisher' in i.dt.get_text()][0]
publisher_block.dd.decompose()

publisher_add = BeautifulSoup('<dd><a href="%s">%s</a></dd>' %(publisher_homepage, publisher_name)).dd
publisher_block.append(publisher_add)


# Authors
authors_list = re.search(r'dct:creator(.*?)dct', ttltext).groups()[0].strip(' []').split('schema:affiliation')
authors_list = [i for i in authors_list if len(i)>0]

author_data_tuples = []
for author in authors_list:
    author_org = re.search(r'\s*\[(.*?)\]', author).groups()[0]
    author_org_details = re.search(r'foaf:homepage(.*)foaf:name(.*)', author_org).groups()
    author_org_homepage, author_org_name = author_org_details[0].strip(' ;<>'), author_org_details[1].strip(' "')
    author_details = re.search(r'foaf:homepage(.*)foaf:name(.*)\]', author.replace(author_org,'')).groups()
    author_homepage, author_name = author_details[0].strip(' <>;'), author_details[1].strip(' "')
    author_data_tuples.append((author_homepage, author_name, author_org_homepage, author_org_name))


def get_author_html(author_data_tuple):
    return '<li><a href="%s">%s</a>, (<a href="%s">%s</a>)</li>' %(author_data_tuple)


authors_block = [i for i in tarsoup.find(id='metadata').find_all('div') if 'Author' in i.dt.get_text()][0]
authors_block.dd.decompose()

authors_block_add = BeautifulSoup('<dd><ul>'+''.join([get_author_html(i) for i in author_data_tuples])+'</ul></dd>').dd
authors_block.append(authors_block_add)


# ### Utility functions


def find_origin(item, item_list):
    # Finding top-level parent of any item
    parent = [i for i in item_list if i[0]==item][0][1]
    if parent is None:
        return None
    while parent is not None and parent != 'Thing':  # HARDCODED: check if needed to avoid 'Thing' parent
        item = parent
        parent = [i for i in item_list if i[0]==item][0][1]
    return item


def write(soupobj, filename):
    with open(filename, "w", encoding='utf-8') as file:
        file.write(str(soupobj))


def append_tags(soup_obj, taglist):
    for tag in taglist:
        soup_obj.append(tag)


def clean_class_item(html_block):
    remove_titles = ['In Domain Of', 'In Range Of', 'Super Class Of']
    [i.decompose() for i in html_block.find_all('tr') if any([text in i.th.get_text() for text in remove_titles])]
    [i.decompose() for i in html_block.h3.find_all('sup')]


# #### Namespace table


table_tuples = [re.search(r'@prefix\s*(\w+):\s*<(.*?)>\s*\.\s*(.*)\n',i).groups() for i in ttllines if i.startswith('@prefix')]


[i.decompose() for i in tarsoup.find(id='namespaces').table.tbody.find_all('tr')]
for table_tuple in table_tuples:
    table_row = '<tr><td>%s</td><td>%s</td><td><a href="%s">%s</a></td></tr>' %(table_tuple[0], table_tuple[2].strip(' #'), table_tuple[1], table_tuple[1])
    tarsoup.find(id='namespaces').table.tbody.append(BeautifulSoup(table_row).tr)


# ### Finding item-hierarchy


item_list = []
for item in gensoup.find_all('div', attrs={'class':'property entity'}):  # all items have class: 'property entity'
    subclass = [tr for tr in item.table.find_all('tr') if 'Sub Class Of' in tr.get_text()]
    if len(subclass)==0:
        parent=None
    else:
        parent = subclass[0].td.a.get_text().split(':')[1]   # Parent: mentioned in 'Sub Class Of' row
    item_list.append((item.get('id'), parent, item))

item_origin_list = [(i[0],i[1],find_origin(i[0], item_list),i[2]) for i in item_list]
item_origin_df = pd.DataFrame(columns=['Item','Parent','Origin','HTML'], data=item_origin_list)


# Class Hierarchy cleanup
hierarchy_fix_classes = ['appclasses', 'indicatorclasses', 'geoclasses']
for fix_class_id in hierarchy_fix_classes:
    fix_class = tarsoup.find(id=fix_class_id)
    tarsoup.find(id='classes').append(fix_class)

# Main hierarchy fix:
hierarchy_fix_main = ['properties', 'acknowledgements', 'references']
for fix_main_id in hierarchy_fix_main:
    fix_main = tarsoup.find(id=fix_main_id)
    tarsoup.find(id='content').append(fix_main)


# ### Tree Traversal


class_parent_list = item_origin_df[item_origin_df['Origin'].notna()][['Item','Parent']]
class_parent_list = class_parent_list[class_parent_list['Parent']!='Thing']  # HARDCODED: check if needed to avoid 'Thing'
class_parent_list = list(zip(class_parent_list['Parent'], class_parent_list['Item']))

# Build a directed graph and a list of all names that have no parent
graph = {name: set() for tup in class_parent_list for name in tup}
has_parent = {name: False for tup in class_parent_list for name in tup}
for parent, child in class_parent_list:
    graph[parent].add(child)
    has_parent[child] = True

# All names that have absolutely no parent:
roots = [name for name, parents in has_parent.items() if not parents]

# traversal of the graph (doesn't care about duplicates and cycles)
def traverse(hierarchy, graph, names):
    for name in names:
        hierarchy[name] = traverse({}, graph, graph[name])
    return hierarchy

hier_graph = traverse({}, graph, roots)

def level_order_traversal(graph_dict, item, names_list):
    if len(graph_dict)==0:
        return
    level_items = sorted(list(graph_dict.keys()))
#     names_list.extend(level_items)
    for item in level_items:
        names_list.append(item)
        level_order_traversal(graph_dict[item], item, names_list)

def run_traversal(graph_dict, root):
    names_list = [root]
    level_order_traversal(graph_dict[root], root, names_list)
    return names_list


# #### Classes


class_titles = {'Organization':'orgclasses',
                'Project':'projclasses',
                'Product':'prodclasses',
                'Application':'appclasses',
                'Indicator':'indicatorclasses',
                'GeographicMarket':'geoclasses'}  # static because it's used only in the static part of target page


gen_class_list = sorted([i for i in item_origin_df['Origin'].unique() if i is not None])
gen_class_list = gen_class_list[3:]+gen_class_list[:3] # just to keep 'Organization' first for now
gen_class_titles = dict([(i,i.lower()+'classes') for i in gen_class_list])
gen_class_titles


[i.decompose() for i in tarsoup.find(id='classes').find_all('div') if ((i.parent.get('id')=='classes') and (i.get('id') not in list(class_titles.values())))]
for parent,parent_class in class_titles.items():
    tar_block = tarsoup.find(id=parent_class)
    # target parent cleanup
    [i.decompose() for i in tar_block.find_all('div', attrs={'class':'property entity'})]


class_block = tarsoup.find(id='classes')


# Deleting all parent classes in target:
for parent_class in class_titles.values():
    template_block = tarsoup.find(id=parent_class)
    template_block.decompose()


for parent, parent_class in gen_class_titles.items():

    template_html = """
    <div id='%s'>
    <h3>%s</h3>
    </div>
    """ %(parent_class, parent+' Classes')

    template = BeautifulSoup(template_html).div

#     add_list = [parent]+list(item_origin_df[item_origin_df['Origin']==parent]['Item'])
#     add_list_html = list(item_origin_df[item_origin_df['Item'].isin(add_list)]['HTML'])

    add_list = run_traversal(hier_graph, parent)
    add_list_html = [item_origin_df[item_origin_df['Item']==i]['HTML'].iloc[0] for i in add_list]
    
    # Cleaning items to add
    [clean_class_item(html_block) for html_block in add_list_html]

    # Adding items to target html
    append_tags(template, add_list_html)

    class_block.append(template)


# #### Properties


non_none_blocks = [i for i in gensoup.find_all('div') if i.get('id') is not None]
properties_blocks = [i for i in non_none_blocks if 'properties' in i.get('id')]


[i.decompose() for i in tarsoup.find(id='properties').find_all('div')]
[tarsoup.find(id='properties').append(properties_block) for properties_block in properties_blocks if properties_block.get('id') in ['objectproperties','datatypeproperties']]


# #### Index


class_ids = list(gen_class_titles.values())


properties_ids = [i.get('id') for i in properties_blocks]


p_string_array_classes = []
for class_id in class_ids:
    item_array = [i.get('id') for i in tarsoup.find_all('div', attrs={'class':'property entity'}) if i.parent.get('id')==class_id]
    p_string = '<p>'+' | '.join(['<a href="#%s">%s</a>'%(item, item) for item in item_array])+'</p>'
    p_string_array_classes.append(p_string)
    
p_string_array_properties = []
for properties_id in properties_ids:
    item_array = [i.get('id') for i in tarsoup.find_all('div', attrs={'class':'property entity'}) if i.parent.get('id')==properties_id]
    p_string = '<p>'+' | '.join(['<a href="#%s">%s</a>'%(item, item) for item in item_array])+'</p>'
    p_string_array_properties.append(p_string)


td_string_classes = "<td>%s</td>" % (''.join(p_string_array_classes))
td_string_properties = "<td>%s</td>" % (''.join(p_string_array_properties))


[i.td.decompose() for i in tarsoup.find(id='index').find_all('tr') if 'Classes' in i.th.get_text()]
[i.append(BeautifulSoup(td_string_classes).td) for i in tarsoup.find(id='index').find_all('tr') if 'Classes' in i.th.get_text()]

[i.td.decompose() for i in tarsoup.find(id='index').find_all('tr') if 'Properties' in i.th.get_text()]
[i.append(BeautifulSoup(td_string_properties).td) for i in tarsoup.find(id='index').find_all('tr') if 'Properties' in i.th.get_text()]
print('Done')


# Writing back
write(tarsoup, GEN_HTML_PATH)
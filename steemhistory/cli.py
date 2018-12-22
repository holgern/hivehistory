# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import bytes, int, str
from beem import Steem
from beem.comment import Comment
from beem.account import Account
from beem.nodelist import NodeList
import click
import logging
import sys
import os
import io
import argparse
import re
import six

from beem.instance import set_shared_steem_instance, shared_steem_instance
from steemhistory.version import version as __version__
# python 3
if six.PY3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve
    
click.disable_unicode_literals_warning = True
log = logging.getLogger(__name__)


def get_urls(mdstring):
    return list(set(re.findall('http[s]*://[^\s"><\)\(]+', mdstring)))


@click.group(chain=True)
@click.option(
    '--verbose', '-v', default=3, help='Verbosity')
@click.version_option(version=__version__)
def cli(verbose):
    # Logging
    log = logging.getLogger(__name__)
    verbosity = ["critical", "error", "warn", "info", "debug"][int(
        min(verbose, 4))]
    log.setLevel(getattr(logging, verbosity.upper()))
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, verbosity.upper()))
    ch.setFormatter(formatter)
    log.addHandler(ch)
    debug = verbose > 0
    pass


@cli.command()
@click.argument('author', nargs=1, required=True)
@click.argument('path', nargs=1, required=True)
@click.argument('image_path', nargs=1, required=False)
def posts(author, path, image_path):
    """ Stores all posts from author in path and all images in image_path
        
        When image_path is not given, images will not be saved.

    """
    nodelist = NodeList()
    nodelist.update_nodes()
    stm = Steem(node=nodelist.get_nodes())
    account = Account(author, steem_instance=stm)
    permlink_list = []
    cnt = 0
    for h in account.history(only_ops=["comment"]):

        if h["parent_author"] != '':
            continue
        if h["author"] != author:
            continue
        if h["permlink"] in permlink_list:
            continue
        else:
            permlink_list.append(h["permlink"])

        # get newest version
        comment = Comment(h, steem_instance=stm)
        comment.refresh()
        markdown_content = comment["body"]
        title = comment["title"]
        timestamp = comment.json()["created"]
        author = comment["author"]
        permlink = comment["permlink"]
        
        if image_path is not None and image_path is not '':
            images = []
            for url in get_urls(markdown_content):
                img_exts = ['.jpg', '.png', '.gif', '.svg', '.jpeg']
                if os.path.splitext(url)[1].lower() in img_exts:
                    images.append(url)
            
            image_cnt = 0
            for image in images:
                image_filename =  timestamp.split('T')[0] + '_' + permlink + '_'+ str(image_cnt) + '_' + image.split('/')[-1]
                filename = os.path.join(image_path, image_filename)
                try:
                    urlretrieve(image, filename)
                except:
                    try:
                        image = "https://steemitimages.com/0x0/" + image
                        urlretrieve(image, filename)
                    except:
                        print("%s does not exists anymore!" % image)
                image_cnt += 1
            
        
        yaml_prefix = '---\n'
        yaml_prefix += 'title: %s\n' % title
        yaml_prefix += 'date: %s\n' % timestamp
        yaml_prefix += 'permlink %s\n' % permlink
        yaml_prefix += 'author: %s\n' % author
        yaml_prefix += 'tags: %s\n---\n' % ",".join(comment.json_metadata["tags"])
        filename = os.path.join(path, timestamp.split('T')[0] + '_' + permlink + ".md")
        
        with io.open(filename, "w", encoding="utf-8") as f:
            f.write(yaml_prefix + markdown_content)

        cnt += 1
        if cnt % 10 == 0:
            print("Receiving posts ... (%d stored)" % cnt)


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        os.environ['SSL_CERT_FILE'] = os.path.join(sys._MEIPASS, 'lib', 'cert.pem')
        cli(sys.argv[1:])
    else:
        cli()

import argparse
import logging
import pandas as pd
from getpass import getpass
from omero.gateway import BlitzGateway
from jax_omeroutils import intake
from jax_omeroutils.ezomero import get_image_ids, get_group_id, get_user_id

CURRENT_MD_NS = 'jax.org/omeroutils/jaxlims/v0'

def main(md_filepath, user_name, group, admin_user, server, port):

    # create connection and establish context
    password = getpass(f'Enter password for {admin_user}: ')
    conn = BlitzGateway(admin_user, password, host=server, port=port)
    conn.connect()
    group_id = get_group_id(conn, group)
    user_id = get_user_id(conn, user_name)
    conn.SERVICE_OPTS.setOmeroGroup(group_id)
    conn.SERVICE_OPTS.setOmeroUser(user_id)
    orphan_ids = get_image_ids(conn)

    # loop over metadata, move and annotate matching images 
    md = intake.load_md_from_file(md_filepath)

    if 'filename' not in md.columns:
        logging.error('Metadata file missing filename column')
        return
    if 'dataset' not in md.columns:
        logging.error('Metadata file missing dataset column')
        return
    if 'project' not in md.columns:
        logging.error('Metadata file missing project column')
        return

    md_json = json.loads(md.to_json(orient='table', index=False))
    for row in md_json['data']:
        _ = row.pop('OMERO_group', None)  # No longer using this field
        project_name = 


    for row in md.iterrows():
        project_name = row.pop('project')
        datset_name = row.pop('dataset')
        filename = row.pop('filename')
        im_ids_to_process = [im_id for im_id in orphan_ids
                             if image_has_imported_filename(conn,
                                                            im_id,
                                                            filename)]]

    conn.close()


def set_or_create_project(conn, project_name):
    return project_id

def set_or_create_dataset(conn, project_id, dataset_name):
    return dataset_id



if __name__ == "__main__":
    description = ("Output a tsv of orphaned images for a particular group. "
                   "Columns: omero_id, image_file, image_name")
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('md', type=str, help='Path to jaxlims metadata')
    parser.add_argument('-u', '--user',
                        type=str,
                        help='OMERO user who owns the images (REQUIRED)',
                        required=True)
    parser.add_argument('-g', '--group',
                        type=str,
                        help='Group in which to find orphans (REQUIRED)',
                        required=True)
    parser.add_argument('--sudo',
                        type=str,
                        help='OMERO admin user for login (REQUIRED)',
                        required=True)
    parser.add_argument('-s', '--server',
                        type=str,
                        help='OMERO server hostname (default = localhost)',
                        default='localhost')
    parser.add_argument('-p', '--port',
                        type=int,
                        help='OMERO server port (default = 4064)',
                        default=4064)
    args = parser.parse_args()
    main(args.md, args.user, args.group, args.sudo, args.server, args.port)

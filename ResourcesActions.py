###############################################################
###############################################################
#
#   VirtualStage Platform - a virtual stage for virtual actors
#
#   Copyright (C): 2020-2023, Joao Carlos Gluz
#   Contact:  João Carlos Gluz (jcgluz@gmail.com)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#
#********************************************************
#
#   Module:     ResourcesActions
#   Purpose:    Actions to view and/or modify the resources (including 
#               folders, items and assets) stored in avatar's inventory
#   Author:     João Carlos Gluz 
#
###############################################################
###############################################################

""" Module ResourcesActions - Actions to view and/or modify the 
        resources (including folders, items and assets) stored in 
        avatar's inventory
        
    Functions:
        look_my_inventory(acid)
        look_my_folder(acid, path)
        look_my_item(acid, path)
        upload_texture(acid, textrfile, textrname, textrdescr)
        upload_animation(acid, animfile, animname, animdescr)
        upload_notecard(acid, notefile, notename, notedescr)
        upload_script(acid, scriptfile, scriptname, scriptdescr)
        upload_item_asset(acid, itemtype, itemfile, itemname, itemdescr, itempath)
        delete_folder(acid, folderpath)
        delete_item(acid, itempath)
        move_item(acid, srcitempath, destfoldpath)
        give_item(acid, avname, itempath)
        download_asset(acid, assetid, assetyp, assetfile)
        download_item_asset(acid, itempath, assetfile)
        upload_asset(acid, assetyp, assetfile)
    
"""

import ActorController as ac


def look_my_inventory(acid):
    """ Retrieve information about all itens and folders stored in
        the inventory of the avatar controller by the actor.
    
    The inventory collects resources (items or assets) that the avatar 
    can access and use, not including objects rezzed the 3D world, 
    but including things attached to the avatar. The inventory is 
    organized into folders and items, similar to folders and files 
    on computers.
    
    A particular inventory item refers to some resource (or asset) 
    that the avatar can access and use through a global unique IDs, 
    however these resources/assets are not stored in the inventory, 
    but in the system asset database maintained by the VR simulator. 
    
    The root or starting folder of inventory is named "/".
    The inventory also has a series of system folders, which
    cannot be renamed or deleted, and are the default location 
    for storing items:
        Animations:     Default folder to store animations
        Body Parts:     Default folder to store bodyparts (skin, 
                        hair, eyes...)
        Calling Cards:  Default folder to store calling cards
        Clothing:       Default folder to store clothing (pants, 
                        skirts, shirts, ...)
        Gestures:       Default folder to store gestures 
        Landmarks:      Default folder to store landmarks
        Lost and Found: Folder to store returned items
        Notecards:      Default folder to store notecards
        Objects:        Default folder to store objects
        Snapshots:      Default folder to store snapshots
        Scripts:        Default folder to store scripts
        Sounds:         Default folder to store sounds
        Textures:       Default folder to store textures
        Trash:          Folder that stores deleted items until 
                        it is emptied.
                        
    In addition to system folders, other folders, called user 
    folders, can also be created in the inventory. Items do not 
    always have to stay in the system folders, but can be freely 
    moved to other folders.
    
    Args:

        acid:   str with unique global identifier of actor.

    Returns:
     
        On fail, returns None.
        
        On success, returns an list of inventory perception records containing 
        information about items/folders stored in avatar's inventory. Inventory
        perception records are lists of strings. Two kinds of inventory
        records are retrieved by this action, 'myfolder' records containing 
        information about inventory's folders: 
            ['myfolder', id, name, path]
        or 'myitem' records containing information about inventory's items: 
            ['myitem', id, name, path, descr, invtyp, assetyp, assetid]
        where:  id is the unique global id of folder/item; 
                name is the name of folder/item;
                path is the path of the folder/item on inventory;
                descr is the description of item;
                invtyp is the inventory type of item;
                assetyp is the type of asset associated to item;
                assetid is the unique global id of asset associated to item.
                
        On success, this action also adds the 'myfolder' and/or 'myitem'
        retrieved records to the perception base.           

        All perception records fields are strings.          
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyInventoryAction()
    except:
        return None
        
def look_my_folder(acid, foldpath):
    """ Retrieve information about some folder in avatar's inventory.
        See look_my_inventory() help for more information.

    Args:

        acid:       str with unique global identifier of actor;
        foldpath:   path of folder in avatar's inventory.

    Returns:
     
        On fail, returns None.
        
        On success, returns an list of inventory perception records about 
        items/folders stored in folder defined by foldpath arg. 
        Inventory perception records are lists of strings. Two kinds of 
        inventory records are retrieved by this action, 'myfolder' records 
        containing information about inventory's folders: 
            ['myfolder', id, name, path]
        or 'myitem' records containing information about inventory's items: 
            ['myitem', id, name, path, descr, invtyp, assetyp, assetid]
        where:  id is the unique global id of folder/item; 
                name is the name of folder/item;
                path is the path of the folder/item on inventory;
                descr is the description of item;
                invtyp is the inventory type of item;
                assetyp is the type of asset associated to item;
                assetid is the unique global id of asset associated to item.
                
        On success, this action also adds the 'myfolder' and/or 'myitem'
        retrieved records to the perception base.           

        All perception records fields are strings.          
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyFolderAction(foldpath)
    except:
        return None
        
def look_my_item(acid, itempath):
    """ Retrieve information about some resource (asset or item) stored in
        avatar's inventory. See look_my_inventory() help for more information.

    Args:

        acid:       str with unique global identifier of actor;
        itempath:   path of item in avatar's inventory.

    Returns:
     
        On fail, returns None.
        
        On success, returns an 'myitem' perception record containing 
        information about the item defined by itempath arg. Inventory 
        perception records are lists of strings, 'myitem' records 
        have the following format: 
            ['myitem', id, name, path, descr, invtyp, assetyp, assetid]
        where:  id is the unique global id of item; 
                name is the name of item;
                path is the path of the item on inventory;
                descr is the description of item;
                invtyp is the inventory type of item;
                assetyp is the type of asset associated to item;
                assetid is the unique global id of asset associated to item.
                
        On success, this action also adds to perception base a list of 
        perception records with more info about the item:
            ['creat_id', id, creatid]: id of item's creator
            ['creat_date', id, creatdate]: creation date of item
            ['owner_id', id, ownerid]: id of item's owner
            ['owner_perms', id, perms]: permissions for item's owner
            ['group_perms', id, perms]: permissions for group
            ['all_perms', id, perms]: permissions for every one
            ['base_perms', id, perms]: base permissions
            ['nextown_perms', id, perms]: permissions for next owner
            ['asset_id', id, assetid]: id of item's asset
            ['sale_price', id, price]
            ['sale_type', id, saletyp]: saletyp can be 'not' (for sale), 'original',
                    'copy' or 'contents'
            ['flags', id, list_of_flags]
            ['transact_id', id, transactid ]
            ['lastown_id', id, last_owner_id]

        All perception records fields are strings.          
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyItemAction(itempath)
    except:
        return None
        

def upload_texture(acid, textrfile, textrname, textrdescr):
    """ Upload a texture image to avatar's inventory. Creates a 
        new item in the default system folder for textures,
        and uploads a new asset containing the texture.
        See get_inventory_info() help for more information.

    Args:

        acid:       str with unique global identifier of actor;
        textrfile:  the path to the file with the texture image;
        textrname:  the name of the new texture item in inventory;
        textrdescr: the description of this item.

    Returns:
     
        On fail, returns None.      
        On success, returns a string with unique global identifier of 
        the new inventory item containing the texture.
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.UploadTextureAction(textrfile, textrname, textrdescr)
    except:
        return None

        
def upload_animation(acid, animfile, animname, animdescr):
    """ Upload an animation to avatar's inventory. Creates a 
        new item in the default system folder for animations,
        and uploads a new asset containing the animation.
        See get_inventory_info() help for more information.

    Args:

        acid:       str with unique global identifier of actor;
        animfile:   the path to the file with the animation;
        animname:   the name of the new animation item in inventory;
        animdescr:  the description of this item.

    Returns:
     
        On fail, returns None.      
        On success, returns a string with unique global identifier of 
        the new inventory item containing the animation.
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.UploadAnimationAction(animfile, animname, animdescr)
    except:
        return None

        
def upload_notecard(acid, notefile, notename, notedescr):
    """ Upload an notecard to avatar's inventory. Creates a 
        new item in the default system folder for notecards,
        and uploads a new asset containing the notecard.
        See get_inventory_info() help for more information.

    Args:

        acid:       str with unique global identifier of actor;
        notefile:   the path to the text file with the notecard;
        notename:   the name of the new notecard item in inventory;
        notedescr:  the description of this item.

    Returns:
     
        On fail, returns None.      
        On success, returns a string with unique global identifier of 
        the new inventory item containing the notecard.
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.UploadNotecardAction(notefile, notename, notedescr)
    except:
        return None

        
def upload_script(acid, scriptfile, scriptname, scriptdescr):
    """ Upload a LSL script to avatar's inventory. Creates a 
        new item in the default system folder for scripts,
        and uploads a new asset containing the LSL script.
        See get_inventory_info() help for more information.

    Args:

        acid:       str with unique global identifier of actor;
        animfile:   the path to the text file with the LSL script;
        animname:   the name of the new script item in inventory;
        animdescr:  the description of this item.

    Returns:
     
        On fail, returns None.      
        On success, returns a string with unique global identifier of 
        the new inventory item containing the LSL script.
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.UploadScriptAction(scriptfile, scriptname, scriptdescr)
    except:
        return None
        

def upload_item_asset(acid, itemtype, itemfile, itemname, itemdescr, itempath):
    """ Creates a new item into avatar's inventory, and uploads
        a new asset file associated to this item.
        See get_inventory_info() help for more information.

    Args:

        acid:       str with unique global identifier of actor;
        itemtype:   str, can be:
                        clothing, bodypart, animation, sound, texture
        itemfile:   the path to the file with the item asset;
        itemname:   the name of the new item in inventory;
        itemdescr:  the description of this item;
        itempath:   path of folder where the new item will be stored, 
                    if it is None, will try to use some system folder.

    Returns:
     
        On fail, returns None.      
        On success, returns a string with unique global identifier of 
        the new inventory item.
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.UploadItemAssetAction(itemtype,itemfile,itemname,itemdescr,itempath)
    except:
        return None
        
def delete_folder(acid, folderpath):
    """ Delete a folder from avatar's inventory.

    Args:

        acid:       str with unique global identifier of actor;
        folderpath: str with the path of folder to be deleted.

    Returns:
     
        On fail, returns False.     
        On success, returns True.
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.DeleteFolderAction(folderpath)
    except:
        return None
        
def delete_item(acid, itempath):
    """ Delete an item from avatar's inventory.

    Args:

        acid:       str with unique global identifier of actor;
        itemrpath:  str with the path of item to be deleted.

    Returns:
     
        On fail, returns False.     
        On success, returns True.
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.DeleteItemAction(itempath)
    except:
        return None
        
def move_item(acid, srcitempath, destfoldpath):
    """ Move an item to other folder of avatar's inventory.

    Args:

        acid:           str with unique global identifier of actor;
        srcitempath:    str with the path of item to be moved;
        destfoldpath:   str with path of folder to receive the item.

    Returns:
     
        On fail, returns False.     
        On success, returns True.
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.MoveItemAction(srcitempath, destfoldpath)
    except:
        return None
        
def give_item(acid, avname, itempath):
    """ Give an item from avatar's inventory to other avatar.

    Args:

        acid:       str with unique global identifier of actor;
        avname:     str with name of avatar that will receive the item;
        itempath:   str with path of item to be given.

    Returns:
     
        On fail, returns False.     
        On success, returns True.
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.GiveItemAction(avname, itempath)
    except:
        return None
        
def download_asset(acid, assetid, assetyp, assetfile):
    """ Download an asset from simulator's assets database.

    Args:

        acid:       str with unique global identifier of actor;
        assetid:    str with unique global identifier of asset;
        assetyp:    str with asset type, can be:
                        'unknown'       - Unknown asset type, 
                        'texture'       - Texture asset, stores in JPEG2000 
                                          J2C stream format, 
                        'sound'         - Sound asset, 
                        'callingcard'   - Calling card for another avatar, 
                        'landmark'      - Link to a location in world, 
                        'clothing'      - Collection of textures and parameters 
                                          that can be worn by an avatar, 
                        'object'        - Primitive that can contain textures, 
                                          sounds, scripts and more, 
                        'notecard'      - Notecard asset,
                        'lsltext'       - Linden scripting language script,
                        'texturetga'    - Uncompressed TGA texture,
                        'bodypart'      - Collection of textures and shape parameters 
                                          that can be worn,
                        'soundwav'      - Uncompressed sound,
                        'imagetga'      - Uncompressed TGA non-square image, not to 
                                          be used as a texture,
                        'imagejpeg '    - Compressed JPEG non-square image, not to be 
                                          used as a texture, 
                        'animation'     - Animation, 
                        'gesture'       - Sequence of animations, sounds, chat, and pauses, 
                        'link'          - Asset is a link to another inventory item,
                        'linkfolder'    - Asset is a link to another inventory folder,
                        'mesh'          - Linden mesh format
        assetfile:  name and path of local file that will store the downloaded asset.

    Returns:
     
        On fail, returns None.
        
        On success, returns an 'asset' perception record containing 
        information about the downloaded asset. Asset perception records 
        are lists of strings, 'asset' records have the following format: 
            ['asset', id, assetyp]
        where:  id is the unique global id of asset; 
                assetyp is the type of downloaded asset.
                
        On success, this action also adds the 'asset' record to the 
        perception base.            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.DownloadAssetAction(assetid, assetyp, assetfile)
    except:
        return None
        
def download_item_asset(acid, itempath, assetfile):
    """ Download the asset associated to some item from avatar's inventory.

    Args:

        acid:       str with unique global identifier of actor;
        itempath:   str with path of item;
        assetfile:  name and path of local file that will store the downloaded asset.

    Returns:
     
        On fail, returns None.
        
        On success, returns an 'asset' perception record containing 
        information about the downloaded asset. Asset perception records 
        are lists of strings, 'asset' records have the following format: 
            ['asset', id, assetyp]
        where:  id is the unique global id of asset; 
                assetyp is the type of downloaded asset (see download_asset()
                help for more information).
                
        On success, this action also adds the 'asset' record to the 
        perception base.            
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.DownloadItemAssetAction(itempath, assetfile)
    except:
        return None
        
def upload_asset(acid, assetyp, assetfile):
    """ Uploads a new asset to the simulator's assets database.
        See download_asset() help for more information.

    Args:

        acid:       str with unique global identifier of actor;
        assetyp:    str with asset type, see download_asset() help for more information
        assetfile:  name and path of local file with the data of uploaded asset.

    Returns:
     
        On fail, returns None.      
        On success, returns a string with unique global identifier of 
        the new asset.
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.UploadAssetAction(assetyp, assetfile)
    except:
        return None
        






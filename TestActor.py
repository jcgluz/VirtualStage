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
#   Module:     TestActor 
#   Purpose:    Actor that runs a test suite for VirtualStage
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################


""" Module TestActor - Actor that runs a test suite for VirtualStage. """


import sys
import time
import math
import clr
import threading
import queue
import re
import os
import ActorController as ac


###############################################
#
# Auxiliary Functions
#

def press_enter():
    print('Press enter to continue')
    k=input()

def press_enter_to(*msgs):
    msg=''.join(str(m) for m in msgs)
    input('Press enter to: '+msg)

def print_obj(objname,obj):
    if obj!=None:
        print('Get information about object called: '+objname+', with id: ',obj[1])
    else:
        print('Cannot get information about object called:'+objname)


def print_resp(resp):
    print('Response ==========')
    print(resp)
    print('===================')

def print_resps(lresps):
    if lresps==None:
        print('Empty list of responses')
        return
    print('List of Responses =')
    for resp in lresps:
        print(resp)
    print('===================')

def print_perceptions(acid,objid):
    print('Perceptions =======')
    percepts = ac.perceive_all(acid,[None,objid])
    for percept in percepts:
        print(percept)
    print('===================')

def print_waitmsg_resp(resp):
    if resp==None:
        print('TIMEOUT - No response')
    else:
        print('Response:')
        print(resp)

######################################################
#
#   Test movement actions: 
#       move, teleport, fly, 
#       follow, forward, back, left, 
#       right and motion
#

def avatar_movement_tests(acid,x,y):  
# ------------------- Movements in walk mode
    print('------------- Movement Tests -------------')
    print('Movement tests start at initial position')
    print('Teleporting to initial position (',x,', ',y,')')
    ac.tele_to(acid,x,y)
    print('Movement tests in walk mode')
    ac.run(acid,'stop')
    press_enter_to('Walk forward')
    ac.forward(acid)
    press_enter_to('Walk forward 5 seconds')
    ac.forward(acid,5,'sec')
    press_enter_to('Walk forward 5 meters')
    ac.forward(acid,5,'mt')
    press_enter_to('Walk backward')
    ac.backward(acid)
    press_enter_to('Walk backward 5 seconds')
    ac.backward(acid,5,'sec')
    press_enter_to('Walk backward 5 meters')
    ac.backward(acid,5,'mt')
    press_enter_to('Walk leftward')
    ac.leftward(acid)
    press_enter_to('Walk leftward 5 seconds')
    ac.leftward(acid,5,'sec')
    press_enter_to('Walk rightward')
    ac.rightward(acid)
    press_enter_to('Walk rightward 5 seconds')
    ac.rightward(acid,5,'sec')
# ------------------- Movements in run mode
    press_enter_to('Movement tests in run mode')
    ac.run(acid,'start')
    press_enter_to('Run forward')
    ac.forward(acid)
    press_enter_to('Run forward 5 seconds')
    ac.forward(acid,5, 'sec')
    press_enter_to('Run forward 5 meters')
    ac.forward(acid,5, 'mt')
    press_enter_to('Run backward')
    ac.backward(acid)
    press_enter_to('Run backward 5 seconds')
    ac.backward(acid,5, 'sec')
    press_enter_to('Run backward 5 meters')
    ac.backward(acid,5, 'mt')
# ------------------- More movements in walk mode
    press_enter_to('More movement tests in walk mode')
    ac.run(acid,'stop')
    x1 = x+10
    y1 = y+10
    press_enter_to('Walk to (',x1,',',y1,')')
    ac.walk_to(acid,x1,y1)
    x2 = x-10
    press_enter_to('Walk to (',x2,', ',y1,' 25.0)')
    ac.walk_to(acid,x2,y1,25.0)
# ------------------- Teleport movements
    print('Teleport movement tests')
    y2 = y-10
    press_enter_to('Teleport to (',x2,', ',y2,', 25.0)')
    ac.tele_to(acid,x2,y2,25.0)
    press_enter_to('Teleport to (',x,', ',y,')')
    ac.tele_to(acid,x,y)
# ------------------- Movements in fly mode
    print('Movement tests in fly mode')
    ac.fly(acid,'start')
    press_enter_to('Move up')
    ac.upward(acid)
    press_enter_to('Move up 3 times')
    ac.upward(acid)
    ac.upward(acid)
    ac.upward(acid)
    press_enter_to('Move down')
    ac.downward(acid)
    press_enter_to('Move down 2 times')
    ac.downward(acid)
    ac.downward(acid)
    x3 = x+30
    y3 = y+30
    press_enter_to('Fly to (',x3,', ',y3,', 50.0) for 3 seconds')
    ac.fly_to(acid,x3,y, 50.0, 3,'sec')
    press_enter_to('Fly to initial position (',x,', ',y,', 30.0) for 2 seconds')
    ac.fly_to(acid,x,y,30.0,2,'sec')
    press_enter_to('Stop flying')
    ac.fly(acid,'stop')
    print('-----------------------------')
    print('--- End of Movement Tests ---')
    press_enter()


###############################################
#
# Test avatar rotation/turning actions
#

def avatar_rotation_tests(acid,x,y):
    print('---------- Rotation Tests ----------')
    print('Rotation/turning tests start at initial position')
    print('Teleporting to initial position (',x,', ',y,')')
    press_enter()
    ac.tele_to(acid,x,y)
    x1 = x+10
    y1 = y+10
    press_enter_to('Turn to position (',x1,', ',y1,', 25.0)')
    ac.turn_to_pos(acid,x1,y1,25.0)
    x2 = x-10
    y2 = y-10
    press_enter_to('Turn to position (',x2,', ',y1,', 25.0)')
    ac.turn_to_pos(acid,x2,y1,25.0)
    press_enter_to('Turn to position (',x2,', ',y2,', 25.0)')
    ac.turn_to_pos(acid,x2,y2,25.0)
    press_enter_to('Turn to east')
    ac.turn_to_named_dir(acid,'east')
    press_enter_to('Turn to west')
    ac.turn_to_named_dir(acid,'west')
    press_enter_to('Turn to south')
    ac.turn_to_named_dir(acid,'south')
    press_enter_to('Turn to north')
    ac.turn_to_named_dir(acid,'north')
    press_enter_to('Turn to 45 dg')
    ac.turn_to_abs_dir(acid,45.0,'dg')
    press_enter_to('Turn to 90 dg')
    ac.turn_to_abs_dir(acid,90.0, 'dg')
    press_enter_to('Turn to 135 dg')
    ac.turn_to_abs_dir(acid,135.0, 'dg')
    press_enter_to('Turn to 180 dg')
    ac.turn_to_abs_dir(acid,180.0,'dg')
    press_enter_to('Turn to 0 dg')
    ac.turn_to_abs_dir(acid,0.0,'dg')
    press_enter_to('Turn to left')
    ac.turn_to_named_dir(acid,'left')
    press_enter_to('Turn to right')
    ac.turn_to_named_dir(acid,'right')
    press_enter_to('Turn relative right 180 dg')
    ac.turn_to_rel_dir(acid,180.0,'dg')
    press_enter_to('Turn relative left -180 dg')
    ac.turn_to_rel_dir(acid,-180.0,'dg')
    press_enter_to('Turn to avatar Admin Sist')
    ac.turn_to_avatar(acid,'Admin Sist')
    press_enter_to('Turn to object ObjetoDeTeste')
    ac.remove_all_perceptions(acid)
    ac.seek_objs_by_radius(acid, 50.0)
    objteste = ac.perceive(acid,['name',None,'ObjetoDeTeste'])
    ac.turn_to_obj(acid,objteste[1])
    print('-----------------------------')
    print('--- End of Rotation Tests ---')
    press_enter()


##################################################
#
# Test avatar positioning actions: 
#       jump, sit, stand, 
#       walk, run, fly, crouch, sleeps
#

def avatar_positioning_tests(acid,x,y):
    print('-------- Body Positioning Tests --------')
    press_enter_to('Start jumping')
    ac.jump(acid,'start')
    press_enter_to('Stop jumping')
    ac.jump(acid,'stop')
    press_enter_to('Try to sit')
    ac.sit(acid)
    press_enter_to('Stand up')
    ac.stand(acid)
    press_enter_to('Start crouching')
    ac.crouch(acid,'start')
    press_enter_to('Stop crouching')
    ac.crouch(acid,'stop')
    print('-------------------------------------')
    print('--- End of Body Positioning Tests ---')
    press_enter()


##################################################
#
# Test seek objects actions: 
#

def search_obj_tests(acid,x,y):
    print('---------- Search Objects Tests -----------')
# look for regions
    press_enter_to('Clear perceptions and seek regions')
    ac.remove_all_perceptions(acid)
    lresps = ac.seek_regions(acid)
    print('Regions found:')
    print_resps(lresps)
    print_perceptions(acid,None)
# look for objs
    press_enter_to('Clear perceptions and seek objs in 20 mt radius')
    ac.remove_all_perceptions(acid)
    lresps=ac.seek_objs_by_radius(acid,20.0)
    print('Objects found:')
    print_resps(lresps)
    print_perceptions(acid,None)
# look for avatars
    press_enter_to('Clear perceptions and seek avatars')
    ac.remove_all_perceptions(acid)
    lresps=ac.seek_avatars(acid)
    print('Avatars found:')
    print_resps(lresps)
    print_perceptions(acid,None)
    print('-----------------------------------')
    print('--- End of Search Objects Tests ---')
    press_enter()
    

##################################################
#
# Test self observation actions: 
#

def self_observation_tests(acid,x,y):
    print('--- Self Observation Tests ---')
# look my location
    press_enter_to('Look my position')
    ac.remove_all_perceptions(acid)
    resp=ac.look_my_position(acid)
    print('My position:')
    print_resp(resp)
    print_perceptions(acid,None)
# look my rotation
    press_enter_to('Look my rotation')
    ac.remove_all_perceptions(acid)
    resp=ac.look_my_rotation(acid)
    print('My rotation:')
    print_resp(resp)
    print_perceptions(acid,None)
# look my information
    press_enter_to('Look my information')
    ac.remove_all_perceptions(acid)
    resp=ac.look_my_info(acid)
    print('My information:')
    print_resp(resp)
    print_perceptions(acid,None)
# look my region
    press_enter_to('Look my region')
    ac.remove_all_perceptions(acid)
    resp=ac.look_my_region(acid)
    print('My region:')
    print_resp(resp)
    print_perceptions(acid,None)
# look my attachments
    press_enter_to('Look my attachments')
    ac.remove_all_perceptions(acid)
    lresps=ac.look_my_attachments(acid)
    print('My attachments:')
    print_resps(lresps)
    print_perceptions(acid,None)
# look my clothes
    press_enter_to('Look my wearables')
    ac.remove_all_perceptions(acid)
    lresps=ac.look_my_wearables(acid)
    print('My wearables:')
    print_resps(lresps)
    print_perceptions(acid,None)
# Look my animation tests
    press_enter_to('Show animations playing')
    ac.remove_all_perceptions(acid)
    resp=ac.look_my_anims_playing(acid)
    print('My animations playing:')
    print_resp(resp)
    print('-------------------------------------')
    print('--- End of Self Observation Tests ---')
    press_enter()
    
##################################################
#
# Test inventory actions: 
#

def inventory_tests(acid,x,y):
    print('--------- Inventory Tests ---------')
# look my inventory first time
    press_enter_to('Clear perceptions and look inventory')
    ac.remove_all_perceptions(acid)
    lresps=ac.look_my_inventory(acid)
    print('My inventory:')
    print_resps(lresps)
    print_perceptions(acid,None)
# look some folder
    print('Select some folder of inventory to be inspected')
    print('c - cancel selection')
    press_enter()
    folders=ac.perceive_all(acid,['myfolder'])
    for folder in folders:
        print('Inspect folder? (y - inspect; <enter> - next; c - cancel)')
        foldername=folder[2]
        folderdir=folder[3]
        folderpath=folderdir+foldername+'/'
        print(folderpath)
        answer = input().lower()
        if answer=='c':
            break
        if answer=='y':
            #ac.remove_all_perceptions()
            items=ac.look_my_folder(acid,folderpath)
            press_enter_to('List items of selected folder:')
            print_resps(items)
# look some item
            print('Select some item of this folder to be inspected')
            print('c - cancel selection')
            press_enter()
            items=ac.perceive_all(acid,['myitem',None,None,folderpath])
            for item in items:
                itemid = item[1]
                itemname = item[2]
                itemdir = item[3]
                itempath = itemdir+itemname+'/'
                print('Inspect item? (y - inspect; <enter> - next; c - cancel)')
                print(itempath)
                answer = input().lower()
                if answer=='c':
                    break
                if answer=='y':
                    #ac.remove_all_perceptions(acid)
                    resp=ac.look_my_item(acid,itempath)
                    press_enter_to('List response and perceptions of selected item:')
                    print_resp(resp)
                    print_perceptions(acid,itemid)
                    break
            break
    print('--------------------------------')
    print('--- End of Inventory Tests ---')
    press_enter()
    

##################################################
#
# Test look objects actions
#

def obj_observation_tests(acid,x,y):
    print('-------- Object Observation Tests --------')
    print('Object observation tests start at initial position')
    print('Teleporting to initial position (',x,', ',y,')')
    press_enter()
    ac.tele_to(acid,x,y)
    press_enter_to('Clear perceptions and seek objs in 30 mt radius')
    ac.remove_all_perceptions(acid)
    lresps=ac.seek_objs_by_radius(acid, 30.0)
    print('Objects found')
    print_resps(lresps)
    print_perceptions(acid,None)
    print('Will check perception of red box, blue ball, green pyramid, ')
    print('eucalyptus tree and pine tree objects')
    press_enter()
    redbox = ac.perceive(acid,['name',None,'redbox'])
    print_obj('redbox',redbox)
    blueball = ac.perceive(acid,['name',None,'blueball'])
    print_obj('blueball',blueball)
    greenpyr = ac.perceive(acid,['name',None,'greenpyramid'])
    print_obj('greenpyramid',greenpyr)
    eucatree = ac.perceive(acid,['name',None,'eucalyptustree'])
    print_obj('eucalyptustree',eucatree)
    pinetree = ac.perceive(acid,['name',None,'pinetree'])
    print_obj('pinetree',pinetree)
    if redbox!=None:
# inspect red box basic properties
        press_enter_to('Clear perceptions and look red box basic properties')
        ac.remove_all_perceptions(acid)
        resp=ac.look_obj(acid,redbox[1])
        print('List of red box basic properties:')
        print_resp(resp)
        print_perceptions(acid,None)
    if blueball!=None:
# inspect blue ball basic properties
        press_enter_to('Clear perceptions and look blue ball basic properties')
        ac.remove_all_perceptions(acid)
        resp=ac.look_obj(acid,blueball[1])
        print('List of blue ball basic properties:')
        print_resp(resp)
        print_perceptions(acid,None)
    if greenpyr!=None:
# inspect green pyramid basic properties
        press_enter_to('Clear perceptions and look green pyramid basic properties')
        ac.remove_all_perceptions(acid)
        resp=ac.look_obj(acid,greenpyr[1])
        print('List of green pyramid basic properties:')
        print_resp(resp)
        print_perceptions(acid,None)   
# inspect green pyramid properties
        press_enter_to('Clear perceptions and look green pyramid extra properties:')
        ac.remove_all_perceptions(acid)
        resp=ac.look_obj_extra_props(acid,greenpyr[1])
        print('List of green pyramid extra properties:')
        print_resp(resp)
        print_perceptions(acid,None)   
# inspect green pyramid physical properties
        press_enter_to('Clear perceptions and look green pyramid physical properties')
        ac.remove_all_perceptions(acid)
        resp=ac.look_obj_phys_props(acid,greenpyr[1])
        print('List of green pyramid physical properties:')
        print_resp(resp)
        print_perceptions(acid,None)   
# inspect green pyramid construction properties
        press_enter_to('Clear perceptions and look green pyramid construction properties')
        ac.remove_all_perceptions(acid)
        resp=ac.look_obj_constr_props(acid,greenpyr[1])
        print('List of green pyramid construction properties:')
        print_resp(resp)
        print_perceptions(acid,None)   
# look height
    press_enter_to('Clear perceptions and look height at 148,148')
    ac.remove_all_perceptions(acid)
    resp=ac.look_height_at(acid,148.0,148.0)
    print('Height at response:')
    print_resp(resp)
    press_enter_to('Look height at 160,160')
    ac.look_height_at(acid,160.0,160.0)
    print('Height at response and list of perceptions:')
    print_resp(resp)
    print_perceptions(acid,None)   
# look wind
    press_enter_to('Clear perceptions and look wind at 90,90')
    ac.remove_all_perceptions(acid)
    resp=ac.look_wind_at(acid,90.0,90.0)
    print('Wind at response:')
    print_resp(resp)
    print_perceptions(acid,None)   
    if redbox!=None:
# inspect red box inventory
        press_enter_to('Clear perceptions and look red box object inventory')
        ac.remove_all_perceptions(acid)
        resp=ac.look_obj_inventory(acid,redbox[1])
        print('List of red box object inventory contents:')
        print_resp(resp)
        print_perceptions(acid,None)   
    if eucatree!=None:
# inspect eucalyptus tree basic properties
        press_enter_to('Clear perceptions and look eucalyptus tree basic properties')
        ac.remove_all_perceptions(acid)
        resp=ac.look_obj(acid,eucatree[1])
        print('List of eucalyptus tree basic properties:')
        print_resp(resp)
        print_perceptions(acid,None)   
# inspect test region properties
    press_enter_to('Clear perceptions and look TestRegion region properties')
    ac.remove_all_perceptions(acid)
    resp=ac.look_region(acid,'TestRegion')
    print('TestRegion region properties:')
    print_resp(resp)
    print_perceptions(acid,None)   
# inspect avatar properties
    press_enter_to('Clear perceptions and look Admin Sist avatar properties')
    ac.remove_all_perceptions(acid)
    resp=ac.look_avatar_with_name(acid,'Admin Sist')
    print('Admin Sist avatar properties:')
    print_resp(resp)
    print_perceptions(acid,None)   
# stop test
    print('---------------------------------------')
    print('--- End of Object Observation Tests ---')
    press_enter()
        
    

##################################################
#
# Test object alteration actions
#

def obj_modification_tests(acid,x,y):
    print('-------- Object Modification Tests --------')
    print('Modification tests start at initial position')
    print('Teleporting to initial position (',x,', ',y,')')
    press_enter()
    ac.tele_to(acid,x,y)
# box1
    x1 = x - 12.0
    y1 = y - 12.0
    press_enter_to('Rezz box with name box1 and default size at (', x1,', ', y1,', 30.0)')
    box1id = ac.rezz(acid,'box1','prim', 'box', x1, y1, 30.0)
    print('Rezzed box1 ID = ',box1id)
    press_enter_to('Move near box1')
    x2 = x1 + 1.0
    y2 = y1 + 1.0
    ac.walk_to(acid,x2,y2)
    press_enter_to('Clear perceptions and seek objects in a 3.0 mt radius')
    ac.remove_all_perceptions(acid)
    lresps=ac.seek_objs_by_radius(acid,3.0)
    print('Objects found:')
    print_resps(lresps)
    print('Properties of these objects:')
    for obj in lresps:
        ac.look_obj(acid,obj[1])
    print_perceptions(acid,None)
    press_enter_to('Will try to touch box1')
    ac.touch(acid,box1id)
    x3 = x1 - 12
    y3 = y1 - 12
    press_enter_to('Move box1 to (',x3,', ',y3,', 25.0)')
    ac.move(acid,box1id,x3,y3,25.0)
    press_enter_to('Resize box1 to 2,4,4')
    ac.resize(acid,box1id,2.0,4.0,4.0)
    press_enter_to('Rotate box1 to 45, 45, 45 degrees')
    ac.rotate(acid,box1id, 'dg', 45.0, 45.0, 45.0)
    press_enter_to('Rotate box1 to pi, 1.5 pi, 2.0 pi radians')
    R = math.pi
    P = 1.5 * math.pi
    y = 2.0 * math.pi
    ac.rotate(acid,box1id,'rad',R,P,y)
    press_enter_to('Change name of box to TestBox1')
    ac.set_name(acid,box1id,'TestBox1')
    press_enter_to('Change description of box1 to: First box used for tests')
    ac.set_descr(acid,box1id, 'First box used for tests')
    press_enter_to('Change material of box1 to metal')
    ac.set_material(acid,box1id, 'metal')
    press_enter_to('Derezz box1')
    ac.derezz(acid,box1id)
# box2
    x4 = x3 + 4.0
    y4 = y3 + 4.0
    press_enter_to('Rezz box with name box2 and size 1x2x3 at (',x4,', ',y4,', 30.0)')
    box2id = ac.rezz_with_size(acid,'box2','prim','box',x4,y4,30.0,1.0,2.0,3.0)
    press_enter_to('Move near box2')
    x5 = x4 + 2.0
    y5 = y4 + 2.0
    ac.walk_to(acid,x5,y5)
    press_enter_to('Derezz box2')
    ac.derezz(acid,box2id)
# torus 
    press_enter_to('Rezz torus with name torus1 and size 1x2x2 at (',x4,', ',y4,', 30.0)')
    torus1id=ac.rezz_with_size(acid,'torus1','prim','torus',x4,y4,30.0,1.0,2.0,2.0)
    press_enter_to('Move torus1 to (',x3,', ',y3,', 35.0)')
    ac.move(acid,torus1id,x3,y3,35.0)
    press_enter_to('Resize torus to 2x4x4')
    ac.resize(acid,torus1id,2.0,4.0,4.0)
    press_enter_to('Rotate torus to 45, 45, 45 degrees')
    ac.rotate(acid,torus1id,'dg',45.0,45.0,45.0)
    press_enter_to('Rotate torus to pi, 1.5 pi, 2.0 pi radians')
    ac.rotate(acid,torus1id,'rad',R,P,y)
    press_enter_to('Change name of torus to TestTorus')
    ac.set_name(acid,torus1id,'TestTorus')
    press_enter_to('Change description of torus to: A torus used for tests')
    ac.set_descr(acid,torus1id,'A torus used for tests')
    press_enter_to('Change material of torus to metal')
    ac.set_material(acid,torus1id,'metal')
    press_enter_to('Derezz torus')
    ac.derezz(acid,torus1id)
# cylinder  
    press_enter_to('Rezz cilynder with name cyl1 and default size at (',x4,', ',y4,', 30.0)')
    cyl1id=ac.rezz(acid,'cyl1','prim','cylinder',x4,y4,30.0)
    press_enter_to('Derezz cylinder')
    ac.derezz(acid,cyl1id)
# rez remaining primitives: prism, sphere, torus, tube, ring
# trees
    press_enter_to('Rezz pine1 tree with name p1 and default size at (',x4,', ',y4,', 25.0)')
    p1id = ac.rezz(acid,'p1','tree','pine1', x4,y4,25.0)
    press_enter_to('Derezz p1 tree')
    ac.derezz(acid,p1id)
    print('----------------------------------------')
    print('--- End of Object Modification Tests ---')
    press_enter()


##################################################
#
# Test avatar appearance modification actions
#

def avatar_appearance_tests(acid,x,y):
    print('------- Avatar Appearance Tests ---------')
    print('Appearance tests start at initial position')
    print('Teleporting to initial position (',x,', ',y,')')
    press_enter()
    ac.tele_to(acid,x,y)
# take_off item first tests
    press_enter_to('Take off Clothing/Default Shirt item')
    ac.take_off(acid,'/Clothing/Default Shirt')
    time.sleep(10)
    ac.set_appearance(acid,True)
    press_enter_to('Take off Clothing/Default Pants item')
    ac.take_off(acid,'/Clothing/Default Pants')
    time.sleep(10)
    ac.set_appearance,
# wear folder test
    press_enter_to('Wear TestClothing folder')
    ac.wear(acid,'folder','/TestClothing/')
    time.sleep(10)
    ac.set_appearance(acid,True)
# take_off item tests
    press_enter_to('Take off TestClothing/Red Default Shirt item')
    ac.take_off(acid,'/TestClothing/Red Default Shirt')
    press_enter_to('Take off TestClothing/Green Default Pants item')
    ac.take_off(acid,'/TestClothing/Green Default Pants')
    time.sleep(10)
    ac.set_appearance(acid,True)
# wear item tests
    press_enter_to('Wear /Clothing/Default Shirt item')
    ac.wear(acid,'item','/Clothing/Default Shirt')
    time.sleep(10)
    ac.set_appearance,
    press_enter_to('Wear /Clothing/Default Pants item')
    ac.wear(acid,'item','/Clothing/Default Pants')
    time.sleep(10)
    ac.set_appearance(acid,True)
# attach test
    press_enter_to('Attach small stone tube on left hand')
    ac.attach(acid,'left_hand','/Objects/SmallStoneTube')
# detach test
    press_enter_to('Detach small stone tube from left hand')
    ac.detach(acid,'/Objects/SmallStoneTube')
# play standard animation tests
    press_enter_to('Play standard animations: clap, dance and bow')
    ac.start_play(acid,'std_anim','clap') 
    time.sleep(2) 
    ac.start_play(acid,'std_anim','dance1') 
    time.sleep(3) 
    ac.start_play(acid,'std_anim','bow')
# show animation tests
    press_enter_to('Show animations playing')
    ac.remove_all_perceptions(acid)
    resp=ac.look_my_anims_playing(acid)
    print('Animations playing:')
    print_resp(resp)
    print_perceptions(acid,None)       
# stop play standard animation test
    press_enter_to('Stop animations')
    ac.stop_play(acid,'std_anim','clap') 
    ac.stop_play(acid,'std_anim','dance1') 
    ac.stop_play(acid,'std_anim','bow')
# show animation tests
    press_enter_to('Show animations playing')
    ac.remove_all_perceptions(acid)
    resp=ac.look_my_anims_playing(acid)
    print('Animations playing:')
    print_resp(resp)
    print_perceptions(acid,None)       
    print('--------------------------------------')
    print('--- End of Avatar Appearance Tests ---')
    press_enter()


##################################################
#
# Test communication actions
#

def communication_tests(acid,x,y):
    print('----------- Communication Tests -----------')
    print('Communication tests start at initial position')
    print('Teleport to initial position (',x,', ',y,')')
    press_enter()
    ac.tele_to(acid,x,y)
    
    print('----------- Send Messages Tests -----------')
# say something on public channel test
    press_enter_to('Say hello on public channel')
    ac.say(acid,'Hello, I am saying my name is Test Actor')
# shout on public channel test
    press_enter_to('Shout hello on public channel')
    ac.shout(acid,'HELLO, I am shouting my name is Test Actor')
# whisper on public channel test
    press_enter_to('Whisper hello on public channel')
    ac.whisper(acid,'hello, I am whispering my name is Test Actor')
# say on 100 channel test
    press_enter_to('Say hello on 100 channel')
    ac.say(acid,'Hello, I am saying my name is Test Actor',100)
# shout on 100 channel test
    press_enter_to('Shout hello on 100 channel')
    ac.shout(acid,'HELLO, I am shouting my name is Test Actor',100)
# whisper on 100 channel test
    press_enter_to('Whisper hello on 100 channel')
    ac.whisper(acid,'hello, I am whispering my name is user 1',100)
# send instant message tests
    press_enter_to('Send instant text message to Admin Sist')
    ac.send_inst_msg(acid,'Admin Sist','Admin Sist this is an instant message to you')
    press_enter_to('Send  another instant message to Admin Sist')
    ac.send_inst_msg(acid,'Admin Sist','Admin Sist this is another instant message to you')
    
    print('---------- Wait Messages Tests ----------')
# say wait test
    press_enter_to('Wait for other actor say "stop" for 30 secs')
    resp = ac.wait_say_msg(acid,None,'stop', 30)
    print_waitmsg_resp(resp)
# shout wait test
    press_enter_to('Wait for other actor shout "stop" for 30 secs')
    resp = ac.wait_shout_msg(acid,None,'stop', 30)
    print_waitmsg_resp(resp)
# chat wait test
    press_enter_to('Wait for other actor chat "stop" for 30 secs')
    resp = ac.wait_chat_msg(acid,None,'stop', 30)
    print_waitmsg_resp(resp)
# instant msg wait test
    press_enter_to('Wait for "stop" instant message for 30 secs')
    resp = ac.wait_inst_msg(acid,None,'stop', 30)
    print_waitmsg_resp(resp)
# test user menus and input text boxes
    print("To test user menus and input text boxes a prim object running")
    print("MenuController script must be attached to Test Actor avatar.")
    print("User menu test: a menu with some options will appear for Admin Sist")
    print("avatar. Select an option and it will be printed on console")
    press_enter_to("Start user menu test, will wait for 30 secs")
    ac.show_menu_for_avatar_with_name(acid, 'Admin Sist', 'Testing Menu', 
        ['Test option A', 'Test option B', 'Test option C'])
    resp = ac.wait_menu_selection(acid, 30.0)
    print_waitmsg_resp(resp)
    print("Input box test: an text input box will appear for Admin Sist")
    print("avatar. Enter some text and it will be printed on console")
    press_enter_to("Start input text box test, will wait for 30 secs")
    ac.input_text_from_avatar_with_name(acid, 'Admin Sist', 'Enter with some text:')
    resp = ac.wait_input_text(acid, 30.0)
    print_waitmsg_resp(resp)
    print('----------------------------------')
    print('--- End of Communication Tests ---')
    press_enter()

##################################################
#
# Memory tests
#

def memory_tests(acid,x,y):
    print('-------- Memory Tests --------')
    print('The following memories will be used for tests:')
    print(['memory-tests','I', 'will', 'test', 'memories', 'in', 'three', 'steps:'])
    print(['memory-tests','1', 'test','if', 'I', 'can', 'record', 'memories'])
    print(['memory-tests','2', 'test','if', 'I', 'can', 'remember', 'memories'])
    print(['memory-tests','3', 'test','if', 'I', 'can', 'forget', 'memories'])
    print(['test-memory-1','first','I', 'record', 'memories'])
    print(['test-memory-2','then','I', 'try', 'to', 'remember','memories'])
    print(['test-memory-3','after','I', 'will', 'print','memories'])
    print(['test-memory-4','and', 'in', 'the', 'end','I', 'will', 'forget','memories'])
    press_enter_to("Start recording memory")
    ac.record(acid,['memory-tests','I', 'will', 'test', 'memories', 'in', 'three', 'steps:'])
    ac.record(acid,['memory-tests','1', 'test','if', 'I', 'can', 'record', 'memories'])
    ac.record(acid,['memory-tests','2', 'test','if', 'I', 'can', 'remember', 'memories'])
    ac.record(acid,['memory-tests','3', 'test','if', 'I', 'can', 'forget', 'memories'])
    ac.record(acid,['test-memory-1','first','I', 'record', 'memories'])
    ac.record(acid,['test-memory-2','then','I', 'try', 'to', 'remember','memories'])
    ac.record(acid,['test-memory-3','after','I', 'will', 'print','memories'])
    ac.record(acid,['test-memory-4','and', 'in', 'the', 'end','I', 'will', 'forget','memories'])
    print("Memories recorded")    
    press_enter_to("Remember all 'memory-tests' memories")
    resps = ac.remember_all(acid,['memory-tests'])
    print_resps(resps)
    press_enter_to("Remember 'test-memory-3' memory")
    resp = ac.remember(acid,['test-memory-3'])
    print_resp(resp)
    print("Remember all 'memory-tests' memories with 'test' in third arg")
    print("using memory pattern=['memory-tests',None,'test']")
    press_enter()
    resps = ac.remember_all(acid,['memory-tests',None,'test'])
    print_resps(resps)
    print("Remember all memories with 'I' in third arg")
    print("using memory pattern=[None,None,'I']")
    press_enter()
    resps = ac.remember_all(acid,[None,None,'I'])
    print_resps(resps)
    press_enter_to("Check if 'test-memory-2' is an unique memory ... must be True")
    resp = ac.remember_if_one(acid,['test-memory-2'])
    print(resp)
    press_enter_to("Check if 'memory-tests' is an unique memory ... must be False")
    resp = ac.remember_if_one(acid,['memory-tests'])
    print(resp)
    press_enter_to("Check if there is a 'memory-tests' memory ... must be True")
    resp = ac.remember_if(acid,['memory-tests'])
    print(resp)    
    press_enter_to("Forget all 'memory-tests' memories")
    resps = ac.forget(acid,['memory-tests'])
    press_enter_to("Try to remember any 'memory-tests' memories  ... must be empty")
    resps = ac.remember_all(acid,['memory-tests'])
    print_resps(resps)
    press_enter_to("Forget 'test-memory-3' memory")
    resp = ac.forget(acid,['test-memory-3'])
    press_enter_to("Try to remember 'test-memory-3' memory ... must be None")
    resp = ac.remember(acid,['test-memory-3'])
    print_resp(resps)
    press_enter_to("Forget all remaining testing memories")
    resp = ac.forget(acid,['test-memory-1'])
    resp = ac.forget(acid,['test-memory-2'])
    resp = ac.forget(acid,['test-memory-4'])
    press_enter_to("Try to remember all remaining testing memories  ... must be empty")
    resps = ac.remember_all(acid,['test-memory-1'])
    resps += ac.remember_all(acid,['test-memory-2'])
    resps += ac.remember_all(acid,['test-memory-4'])
    print_resps(resps)
    print('---------------------------')
    print('--- End of Mmeory Tests ---')
    press_enter()
        
    


##################################################
#
# Main Test Script
#

RunningTests=True
    
def test_script(acid,acname,x,y):
    global RunningTests
    time.sleep(1.0)
    print('Will teleport to initial position (',x,', ',y,')')
    press_enter()
    ac.tele_to(acid,x,y)
    while(RunningTests):
        print('********************************* VirtualStage Test Suite *********************************')
        print('0 - Return to initial position   4 - Object modification tests 8 - Object observation tests')
        print('1 - Avatar movement tests        5 - Self observation tests    9 - Communication tests')
        print('2 - Avatar rotation tests        6 - Inventory tests           10- Avatar appearance tests')
        print('3 - Avatar positioning tests     7 - Search tests              11- Memory tests')
        print('-------------------------------------------------------------------------------------------')
        print('90- Set log level to NONE        92- Set log level to WARN     94- Set log level to DEBUG')
        print('91- Set log level to INFO        93- Set log level to ERROR    99- End tests and stop actor')
        print('-------------------------------------------------------------------------------------------')
        T = input('Select option: ')
        print("T='"+T+"'")
        if T=="0":
            print('Teleporting to initial position (',x,', ',y,') ...')
            ac.tele_to(acid,x,y)
            press_enter()
        elif T=="1":
            avatar_movement_tests(acid,x,y)
        elif T=="2":
            avatar_rotation_tests(acid,x,y)
        elif T=="3":
            avatar_positioning_tests(acid,x,y)
        elif T=="4":
            obj_modification_tests(acid,x,y)
        elif T=="5":
            self_observation_tests(acid,x,y)
        elif T=="6":
            inventory_tests(acid,x,y)
        elif T=="7":
            search_obj_tests(acid,x,y)
        elif T=="8":
            obj_observation_tests(acid,x,y)
        elif T=="9":
            communication_tests(acid,x,y)
        elif T=="10":
            avatar_appearance_tests(acid,x,y)
        elif T=="11":
            memory_tests(acid,x,y)
        elif T=="90":
            ac.set_log_level(acid,'none')
            print("Log level set to NONE")
            press_enter()
        elif T=="91":
            ac.set_log_level(acid,'info')
            print("Log level set to INFO")
            press_enter()
        elif T=="92":
            ac.set_log_level(acid,'warn')
            print("Log level set to WARN")
            press_enter()
        elif T=="93":
            ac.set_log_level(acid,'error')
            print("Log level set to ERROR")
            press_enter()
        elif T=="94":
            ac.set_log_level(acid,'debug')
            print("Log level set to DEBUG")
            press_enter()
        elif T=="99":
            print("Stoping Tests ...")
            press_enter()
            RunningTests=False
        else:
            print("Invalid option")
            press_enter()
    ac.stop_actor(acid)

#if __name__=="__main__":
#ac.start_actor("Test","Actor","actor","http://127.0.0.1:9000",test_script,(128.0,128.0))

##################################################
#
# Start/Stop Test Actor Functions
#

TestActorID = None
def stop():
    global RunningTests
    global TestActorID
    RunningTests=False
    ac.stop_actor(TestActorID)
    
def start():
    global TestActorID
    #TestActorID = ac.start_actor("Test","Actor","actor","http://127.0.0.1:9000",None,test_script,(128.0,128.0))
    #TestActorID = ac.start_actor("Test","Actor","actor","http://127.0.0.1:9000",['TestRegion','100','100','22'],None,None)
    TestActorID = ac.start_actor("Test","Actor","actor","http://127.0.0.1:9000",None,None,None)
    test_script(TestActorID,"Test Actor",128.0,128.0) 

    


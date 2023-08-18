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
#   Module:     PostureActions
#   Purpose:    Actions to view and/or change posture and
#               gestures of avatar controlled by the actor
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Module PostureActions - Actions to view and/or change 
        posture and gestures of avatar controlled by the actor
    Functions:
        look_my_anims_playing(acid)
        crouch(acid, startstop)
        sit(acid)
        sit_on(acid,target)
        stand(acid)
        point_at_obj(acid, objid, nbeams=None)
        stop_pointing(acid)
        start_play(acid, opt, anim)
        stop_play(acid, opt, anim)
        play_gesture(acid, assetgestid)
        activate_gesture(acid, itemgestid, assetgestid)
        deactivate_gesture(acid, itemgestid)
        start_posing(acid, bodypart, pose)
        stop_posing(acid, bodypart)

"""

import ActorController as ac


def look_my_anims_playing(acid):
    """ Retrieve information about current animations playing on the avatar 
        controlled by the actor.

    Args:
        acid:   str with unique global identifier of actor.

    Returns:     
        On fail, returns None.      
        On success, returns an list of 'myanim_playing' perception records 
        containing information about what animations the avatar is currently
        playing. Inventory perception records are lists of strings, 
        'myanim_playing' records have the following format:  
            ['myanim_playing', assetid, seq, animtype, animname]
        where:  assetid is the unique id of the animation asset;
            seq is a number to indicate start order of currently playing 
            animations, on Linden grids this number is unique per region, 
            on OpenSimulator grids it is per client
            animtype can be 'std_anim', 'item' or 'asset_id';
            animname if animtype is 'std_anim', this is the name of the
                standard animation (see start_play() help for details),
                if animtype is 'item', this is the full inventory path of
                this animation, if animtype is 'asset_id' then animname
                is the same as assetid.                
        On success, this action also adds 'myanim_playing' retrieved records 
        to the perception base. All perception records fields are strings.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfObsActs.LookMyAnimationsPlayingAction()
    except:
        return None
        

def crouch(acid, startstop):
    """ Start/stop crouching

    Args:
        acid:       str with unique global identifier of actor
        startstop:  can be 'start' or 'stop'
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.CrouchAction(startstop)
    except:
        return False

def sit(acid):
    """ Attempts to sit the avatar on the top of the closest object

    Args:
        acid:   str with unique global identifier of actor
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.SitAction()
    except:
        return False

def sit_on(acid,objid):
    """ Attempts to sit the avatar on top of objid object

    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of target object
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.SitOnAction(objid)
    except:
        return False

def stand(acid):
    """ Stands up from sitting

    Args:
        acid:   str with unique global identifier of actor
        
    Returns:
    
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.StandAction()
    except:
        return False

def point_at_obj(acid, objid, nbeams=None):
    """  Rotates the avatar body and points at the position of objid object
    
    Args:
        acid:   str with unique global identifier of actor
        objid:  str with unique global identifier of object to point at
        nbeams: optional int arg, defines number of pointing beams or rays
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        if nbeams==None:
            resp= agent.PosActs.PointAtObjAction(objid)
        else:
            resp= agent.PosActs.PointAtObjAction(objid,nbeams)     
    except Exception as error:
        ac.print_dbg('postacts','point_at_obj() error')
        ac.print_dbg('postacts',error)
        resp= False
    return resp
    
def stop_pointing(acid):
    """  Stop pointing at some object
    
    Args:
        acid:   str with unique global identifier of actor
        
    Returns:     
        On fail, returns False
        On success, True
            
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.PosActs.StopPointingAction()
    except Exception as error:
        ac.print_dbg('postacts','stop_pointing() error')
        ac.print_dbg('postacts',error)
        return False

def start_play(acid, opt, anim):
    """ Attempts to start to play an animation.

    Args:
        acid:       str with unique global identifier of actor;
        opt:        str that identifies where to locate animation, can be:
                        'item', 'asset_id' or 'std_anim'
        anim:       str which defines the animation to be played, format 
                    depends on opt - if opt is 'item', anim is the path of 
                    animation in avatar's inventory, if opt is 'asset_id', anim
                    is the unique identifier of asset containing animation, 
                    if opt is 'std_anim', anim can be:
                        'afraid','aim_bazooka_r','aim_bow_l','aim_handgun_r',
                        'aim_rifle_r','angry','away','backflip','belly_laugh',
                        'blow_kiss','bored','bow','brush','busy','clap','courtbow',
                        'crouch','crouchwalk','cry','customize','customize_done',
                        'dance1','dance2','dance3','dance4','dance5','dance6',
                        'dance7','dance8','dead','drink','embarrassed',
                        'express_afraid','express_anger','express_bored',
                        'express_cry','express_disdain','express_embarrassed',
                        'express_frown','express_kiss','express_laugh',
                        'express_open_mouth','express_repulsed','express_sad',
                        'express_shrug','express_smile','express_surprise',
                        'express_tongue_out','express_toothsmile','express_wink',
                        'express_worry','falldown','female_walk','finger_wag',
                        'fist_pump','fly','flyslow','hello','hold_bazooka_r',
                        'hold_bow_l','hold_handgun_r','hold_rifle_r','hold_throw_r',
                        'hover','hover_down','hover_up','impatient','jump',
                        'jump_for_joy','kiss_my_butt','land','laugh_short',
                        'medium_land','motorcycle_sit','muscle_beach','no',
                        'no_unhappy','nyah_nyah','onetwo_punch','peace','point_me',
                        'point_you','pre_jump','punch_left','punch_right',
                        'repulsed','roundhouse_kick','rps_countdown','rps_paper',
                        'rps_rock','rps_scissors','run','sad','salute',
                        'shoot_bow_l','shout','shrug','sit','sit_female',
                        'sit_generic','sit_ground','sit_ground_staticrained',
                        'sit_to_stand','sleep','smoke_idle','smoke_inhale',
                        'smoke_throw_down','snapshot','stand','standup','stand_1',
                        'stand_2','stand_3','stand_4','stretch','stride','surf',
                        'surprise','sword_strike','talk','tantrum','throw_r',
                        'tryon_shirt','turnleft','turnright','type','walk','whisper',
                        'whistle','wink','wink_hollywood','worry','yes','yes_happy',
                        'yoga_float'

    Returns:     
        On fail, returns false. 
        On success, true.
        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.StartPlayAction(opt,anim)
    except:
        return False

def stop_play(acid, opt, anim):
    """ Attempts to stop an animation being played.

    Args:
        acid:       str with unique global identifier of actor;
        opt:        str that identifies where to locate animation, can be:
                        'item', 'asset_id' or 'std_anim'
        anim:       str which defines the animation to be played, format 
                    depends on opt - if opt is 'item', anim is the path of 
                    animation in avatar's inventory, if opt is 'asset_id', anim
                    is the unique identifier of asset containing animation, 
                    if opt is 'std_anim', see standard animation identifiers
                    in start_play() action.

    Returns:    
        On fail, returns false. 
        On success, true.
        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.StopPlayAction(opt,anim)
    except:
        return False

def play_gesture(acid, assetgestid):
    """ Attempts to play a gesture.

    Args:
        acid:           str with unique global identifier of actor;
        assetgestid:    str with unique identifier of asset containing gesture.

    Returns:     
        On fail, returns False. 
        On success, True.
        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.PlayGestureAction(assetgestid)
    except:
        return False

def activate_gesture(acid, itemgestid, assetgestid):
    """ Activate a gesture.

    Args:
        acid:           str with unique global identifier of actor;
        itemgestid:     str with unique identifier of inventory item linked 
                        to asset gesture.
        assetgestid:    str with unique identifier of asset containing gesture.

    Returns:     
        On fail, returns False. 
        On success, True.
        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.ActivateGestureAction(itemgestid, assetgestid)
    except:
        return False

def deactivate_gesture(acid, itemgestid):
    """ Deactivate a gesture.

    Args:
        acid:           str with unique global identifier of actor;
        itemgestid:     str with unique identifier of inventory item linked 
                        to asset gesture.

    Returns:     
        On fail, returns False. 
        On success, True.
        
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.SelfModActs.DeactivateGestureAction(itemgestid)
    except:
        return False


Body_poses_ids_loaded = False

Left_arm_up_id = None
Left_arm_down_id = None
Left_arm_forward_id = None
Left_arm_side_id = None
Left_arm_inward_id = None
Left_arm_bent_id = None

Right_arm_up_id = None
Right_arm_down_id = None
Right_arm_forward_id = None
Right_arm_side_id = None
Right_arm_inward_id = None
Right_arm_bent_id = None

Left_leg_lift_up_id = None
Left_leg_down_id = None
Left_leg_half_lift_id = None
Left_leg_bent_id = None
Left_leg_side_lift_id = None
Left_leg_half_side_id = None

Right_leg_lift_up_id = None
Right_leg_down_id = None
Right_leg_half_lift_id = None
Right_leg_bent_id = None
Right_leg_side_lift_id = None
Right_leg_half_side_id = None

Head_look_ahead_id = None
Head_look_up_id = None
Head_look_down_id = None
Head_look_left_id = None
Head_look_right_id = None

Body_lying_id = None

Left_arm_pose = None
Right_arm_pose = None
Left_leg_pose = None
Right_leg_pose = None
Head_pose = None
Body_pose = None


def load_poses(acid):
    global Body_poses_ids_loaded
    global Left_arm_up_id, Left_arm_down_id, Left_arm_forward_id, Left_arm_side_id 
    global Left_arm_inward_id, Left_arm_bent_id
    global Right_arm_up_id, Right_arm_down_id, Right_arm_forward_id, Right_arm_side_id 
    global Right_arm_inward_id, Right_arm_bent_id
    global Left_leg_lift_up_id, Left_leg_down_id, Left_leg_half_lift_id, Left_leg_bent_id
    global Left_leg_side_lift_id, Left_leg_half_side_id
    global Right_leg_lift_up_id, Right_leg_down_id, Right_leg_half_lift_id, Right_leg_bent_id
    global Right_leg_side_lift_id, Right_leg_half_side_id
    global Head_look_ahead_id, Head_look_up_id, Head_look_down_id, Head_look_left_id , Head_look_right_id
    global Body_lying_id
    posefld=ac.look_my_folder(acid,'/body-poses-lib/')
    print('posefld=',posefld)
    if posefld==None or len(posefld)==0:
        return False
        
    poseit = ac.perceive(acid,['myitem', None, 'left-arm-up', '/body-poses-lib/'])
    print('poseit(left-arm-up)=',poseit)
    Left_arm_up_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'left-arm-down', '/body-poses-lib/'])
    Left_arm_down_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'left-arm-forward', '/body-poses-lib/'])
    Left_arm_forward_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'left-arm-side', '/body-poses-lib/'])
    Left_arm_side_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'left-arm-inward', '/body-poses-lib/'])
    Left_arm_inward_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'left-arm-bent', '/body-poses-lib/'])
    Left_arm_bent_id = poseit[7] if poseit!=None else None
    
    poseit = ac.perceive(acid,['myitem', None, 'right-arm-up', '/body-poses-lib/'])   
    Right_arm_up_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'right-arm-down', '/body-poses-lib/'])
    Right_arm_down_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'right-arm-forward', '/body-poses-lib/'])
    Right_arm_forward_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'right-arm-side', '/body-poses-lib/'])
    Right_arm_side_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'right-arm-inward', '/body-poses-lib/'])
    Right_arm_inward_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'right-arm-bent', '/body-poses-lib/'])
    Right_arm_bent_id = poseit[7] if poseit!=None else None

    poseit = ac.perceive(acid,['myitem', None, 'left-leg-lift-up', '/body-poses-lib/'])
    Left_leg_lift_up_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'left-leg-down', '/body-poses-lib/'])
    Left_leg_down_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'left-leg-half-lift', '/body-poses-lib/'])
    Left_leg_half_lift_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'left-leg-bent', '/body-poses-lib/'])
    Left_leg_bent_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'left-leg-side-lift', '/body-poses-lib/'])
    Left_leg_side_lift_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'left-leg-half-side', '/body-poses-lib/'])
    Left_leg_half_side_id = poseit[7] if poseit!=None else None
    
    poseit = ac.perceive(acid,['myitem', None, 'right-leg-lift-up', '/body-poses-lib/'])
    Right_leg_lift_up_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'right-leg-down', '/body-poses-lib/'])
    Right_leg_down_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'right-leg-half-lift', '/body-poses-lib/'])
    Right_leg_half_lift_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'right-leg-bent', '/body-poses-lib/'])
    Right_leg_bent_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'right-leg-side-lift', '/body-poses-lib/'])
    Right_leg_side_lift_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'right-leg-half-side', '/body-poses-lib/'])
    Right_leg_half_side_id = poseit[7] if poseit!=None else None

    poseit = ac.perceive(acid,['myitem', None, 'head-look-ahead', '/body-poses-lib/'])
    Head_look_ahead_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'head-look-up', '/body-poses-lib/'])
    Head_look_up_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'head-look-down', '/body-poses-lib/'])
    Head_look_down_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'head-look-left', '/body-poses-lib/'])
    Head_look_left_id = poseit[7] if poseit!=None else None
    poseit = ac.perceive(acid,['myitem', None, 'head-look-right', '/body-poses-lib/'])
    Head_look_right_id = poseit[7] if poseit!=None else None

    poseit = ac.perceive(acid,['myitem', None, 'body-lying', '/body-poses-lib/'])
    Body_lying_id = poseit[7] if poseit!=None else None
    
    Body_poses_ids_loaded = True
    return True

def start_posing(acid, bodypart, pose):
    """  Starts a pose in some part of the body  
    
    Args:
        acid:       str with unique global identifier of actor
        bodypart:   str that identifies body part, it can be:
                        'left-arm', 'right-arm, 'arms', 'left-leg', 
                        'right-leg', 'legs', 'head', 'left-hand', 
                        'right-hand', 'hands', 'hip', 'abdomen', 
                        'chest', 'neck', 'body':       
        pose:       str that identifies the pose of body part  
        
    The following table shows which poses are currently implemented 
    Body part   Poses implemented
    -------------------------------
    left-arm    up, down, forward, side, inward, bent
    right-arm   up, down, forward, side, inward, bent
    left-leg    lift-up, half-lift, side-lift, half-side, down, bent
    right-leg   lift-up, half-lift, side-lift, half-side, down, bent
    head        look-ahead, look-up, look-down, look-left, look-right
    body        lying     

    IMPORTANT: this action only works if the body-poses-lib.iar file is
    loaded in the avatar's inventory in the /body-poses-lib folder using
    OpenSimulator "load iar" command. Alternatively, animations stored 
    in body-poses-lib.zip file can be uploaded to the avatar's inventory 
    using a viewer like Firestorm Viewer, then /body-poses-lib directory 
    must be created in the inventory and animations previously uploaded 
    must be moved to this directory.
    
    Returns:     
        On fail, returns False
        On success, True
            
    """
    global Left_arm_pose, Right_arm_pose, Left_leg_pose, Right_leg_pose, Head_pose, Body_pose
    try:
        agent = ac.get_agctl(acid)
        if not Body_poses_ids_loaded:
            if not load_poses(acid):
                return False 
                
        resp = True 
        
        if bodypart=='left-arm':
            if Left_arm_pose!=None:
                ac.stop_play(acid,'asset_id',Left_arm_pose)
                Left_arm_pose=None
            if pose=='up':
                Left_arm_pose = Left_arm_up_id if ac.start_play(acid,'asset_id',Left_arm_up_id) else None
            elif pose=='down':
                Left_arm_pose = Left_arm_down_id if ac.start_play(acid,'asset_id',Left_arm_down_id) else None
            elif pose=='forward':
                Left_arm_pose = Left_arm_forward_id if ac.start_play(acid,'asset_id',Left_arm_forward_id) else None
            elif pose=='side':
                Left_arm_pose = Left_arm_side_id if ac.start_play(acid,'asset_id',Left_arm_side_id) else None
            elif pose=='inward':
                Left_arm_pose = Left_arm_inward_id if ac.start_play(acid,'asset_id',Left_arm_inward_id) else None
            elif pose=='bent':
                Left_arm_pose = Left_arm_bent_id if ac.start_play(acid,'asset_id',Left_arm_bent_id) else None
            else:
                resp=False
                
        elif bodypart=='right-arm':
            if Right_arm_pose!=None:
                ac.stop_play(acid,'asset_id',Right_arm_pose)
                Right_arm_pose=None
            if pose=='up':
                Right_arm_pose = Right_arm_up_id if ac.start_play(acid,'asset_id',Right_arm_up_id) else None
            elif pose=='down':
                Right_arm_pose = Right_arm_down_id if ac.start_play(acid,'asset_id',Right_arm_down_id) else None
            elif pose=='forward':
                Right_arm_pose = Right_arm_forward_id if ac.start_play(acid,'asset_id',Right_arm_forward_id) else None
            elif pose=='side':
                Right_arm_pose = Right_arm_side_id if ac.start_play(acid,'asset_id',Right_arm_side_id) else None
            elif pose=='inward':
                Right_arm_pose = Right_arm_inward_id if ac.start_play(acid,'asset_id',Right_arm_inward_id) else None
            elif pose=='bent':
                Right_arm_pose = Right_arm_bent_id if ac.start_play(acid,'asset_id',Right_arm_bent_id) else None
            else:
                resp=False
                
        elif bodypart=='arms':
            resp=False
        
        elif bodypart=='left-leg':
            if Left_leg_pose!=None:
                ac.stop_play(acid,'asset_id',Left_leg_pose)
                Left_leg_pose=None
            if pose=='lift-up':
                Left_leg_pose = Left_leg_lift_up_id if ac.start_play(acid,'asset_id',Left_leg_lift_up_id) else None
            elif pose=='down':
                Left_leg_pose = Left_leg_down_id if ac.start_play(acid,'asset_id',Left_leg_down_id) else None
            elif pose=='half-lift':
                Left_leg_pose = Left_leg_half_lift_id if ac.start_play(acid,'asset_id',Left_leg_half_lift_id) else None
            elif pose=='side-lift':
                Left_leg_pose = Left_leg_side_lift_id if ac.start_play(acid,'asset_id',Left_leg_side_lift_id) else None
            elif pose=='half-side':
                Left_leg_pose = Left_leg_half_side_id if ac.start_play(acid,'asset_id',Left_leg_half_side_id) else None
            elif pose=='bent':
                Left_leg_pose = Left_leg_bent_id if ac.start_play(acid,'asset_id',Left_leg_bent_id) else None
            else:
                resp=False
                
        elif bodypart=='right-leg':
            if Right_leg_pose!=None:
                ac.stop_play(acid,'asset_id',Right_leg_pose)
                Right_leg_pose=None
            if pose=='lift-up':
                Right_leg_pose = Right_leg_lift_up_id if ac.start_play(acid,'asset_id',Right_leg_lift_up_id) else None
            elif pose=='down':
                Right_leg_pose = Right_leg_down_id if ac.start_play(acid,'asset_id',Right_leg_down_id) else None
            elif pose=='half-lift':
                Right_leg_pose = Right_leg_half_lift_id if ac.start_play(acid,'asset_id',Right_leg_half_lift_id) else None
            elif pose=='side-lift':
                Right_leg_pose = Right_leg_side_lift_id if ac.start_play(acid,'asset_id',Right_leg_side_lift_id) else None
            elif pose=='half-side':
                Right_leg_pose = Right_leg_half_side_id if ac.start_play(acid,'asset_id',Right_leg_half_side_id) else None
            elif pose=='bent':
                Right_leg_pose = Right_leg_bent_id if ac.start_play(acid,'asset_id',Right_leg_bent_id) else None
            else:
                resp=False
                
        elif bodypart=='legs':
            resp=False
            
        elif bodypart=='head':
            if Head_pose!=None:
                ac.stop_play(acid,'asset_id',Head_pose)
                Head_pose=None
            if pose=='look-ahead':
                Head_pose = Head_look_ahead_id if ac.start_play(acid,'asset_id',Head_look_ahead_id) else None
            elif pose=='look-up':
                Head_pose = Head_look_up_id if ac.start_play(acid,'asset_id',Head_look_up_id) else None
            elif pose=='look-down':
                Head_pose = Head_look_down_id if ac.start_play(acid,'asset_id',Head_look_down_id) else None
            elif pose=='look-left':
                Head_pose = Head_look_left_id if ac.start_play(acid,'asset_id',Head_look_left_id) else None
            elif pose=='look-right':
                Head_pose = Head_look_right_id if ac.start_play(acid,'asset_id',Head_look_right_id) else None
            else:
                resp=False
                
        elif bodypart=='left-hand':
            resp=False
            
        elif bodypart=='right-hand':
            resp=False
            
        elif bodypart=='hands':
            resp=False
            
        elif bodypart=='hip':
            resp=False
            
        elif bodypart=='abdomen':
            resp=False
            
        elif bodypart=='chest':
            resp=False
            
        elif bodypart=='neck':
            resp=False
            
        elif bodypart=='body':
            if Body_pose!=None:
                ac.stop_play(acid,'asset_id',Body_pose)
                Body_pose=None
            if pose=='lying':
                Body_pose = Body_lying_id if ac.start_play(acid,'asset_id',Body_lying_id) else None
            else:
                resp=False
            
        else:
            resp= False
            
    except Exception as error:
        ac.print_dbg('postacts','start_posing() error')
        ac.print_dbg('postacts',error)
        resp= False
        
    return resp
    
def stop_posing(acid, bodypart):
    """  Stops a pose in some part of the body (or all parts) 
    
    Args:
        acid:       str with unique global identifier of actor
        bodypart:   str that identifies body part, it can be:
                        'all', 'left-arm', 'right-arm, 'arms', 
                        'left-leg', 'right-leg', 'legs', 'head', 
                        'left-hand', 'right-hand', 'hands', 'hip', 
                        'abdomen', 'chest', 'neck':       
    
    Returns:     
        On fail, returns False
        On success, True
            
    """
    global Left_arm_pose, Right_arm_pose, Left_leg_pose, Right_leg_pose, Head_pose, Body_pose
    try:
        agent = ac.get_agctl(acid)
        if not Body_poses_ids_loaded:
            if not load_poses(acid):
                return False 
                
        resp = True 
        
        if bodypart=='left-arm':
            if Left_arm_pose!=None:
                ac.stop_play(acid,'asset_id',Left_arm_pose)
                Left_arm_pose=None
                
        elif bodypart=='right-arm':
            if Right_arm_pose!=None:
                ac.stop_play(acid,'asset_id',Right_arm_pose)
                Right_arm_pose=None
                
#        elif bodypart=='arms':
        
        elif bodypart=='left-leg':
            if Left_leg_pose!=None:
                ac.stop_play(acid,'asset_id',Left_leg_pose)
                Left_leg_pose=None
                
        elif bodypart=='right-leg':
            if Right_leg_pose!=None:
                ac.stop_play(acid,'asset_id',Right_leg_pose)
                Right_leg_pose=None
                
#        elif bodypart=='legs':
            
        elif bodypart=='head':
            if Head_pose!=None:
                ac.stop_play(acid,'asset_id',Head_pose)
            Head_pose=None
                
#        elif bodypart=='left-hand':
            
#        elif bodypart=='right-hand':
            
#        elif bodypart=='hands':
            
#        elif bodypart=='hip':
            
#        elif bodypart=='abdomen':
            
#        elif bodypart=='chest':
            
#        elif bodypart=='neck':
            
        else:
            resp= False
            
    except Exception as error:
        ac.print_dbg('postacts','stop_posing() error')
        ac.print_dbg('postacts',error)
        resp= False
        
    return resp



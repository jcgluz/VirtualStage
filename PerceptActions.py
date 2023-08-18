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
#   Module:     PerceptActions
#   Purpose:    Actions to manage actor's perceptions
#   Author:     João Carlos Gluz 
#
###############################################################
###############################################################

""" Module PerceptActions - Actions to manage actor's perceptions
    Functions:
        perceive_all(acid, percpatt)    
        perceive_if_one(acid, percpatt) 
        perceive_if(acid, percpatt)   
        perceive_one(acid, percpatt)
        perceive(acid, percpatt) 
        perceive_when_one(acid, percpatt) 
        perceive_when(acid, percpatt)
        record_perceptions(acid, percpatt)
        register_perception(acid, percept) 
        remove_perceptions(acid, percpatt)  
        remove_all_perceptions(acid) 

"""


import ActorController as ac

#region Perceptions
def perceive_all(acid, percpatt):
    """ Search perception base and recognize perceptions that match percpatt pattern.

    Args:

        acid:       str with unique global identifier of actor.
        percpatt:   the perception search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    perception pattern are ignored in the search, string fields
                    defined in perception pattern must be equal to corresponding
                    field in the perception record.

    Returns:
     
        On fail, returns None.      
        On success, returns a list of perception records for each 
        perception that matches the perception pattern. A perception record is
        simply a list of strings.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.RecallPerceptsThat(percpatt)
    except:
        return None

def perceive_if_one(acid, percpatt):
    """ Check if the perception base has a perception that match percpatt pattern
        and is unique

    Args:

        acid:       str with unique global identifier of actor.
        percpatt:   the perception search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    perception pattern are ignored in the search, string fields
                    defined in perception pattern must be equal to corresponding
                    field in the perception record.

    Returns:
     
        On fail, returns False.     
        On success, returns True.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.RecallIfSinglePercept(percpatt)
    except:
        return False

def perceive_if(acid, percpatt):
    """ Check if the perception base has a perception that match percpatt pattern

    Args:

        acid:       str with unique global identifier of actor.
        percpatt:   the perception search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    perception pattern are ignored in the search, string fields
                    defined in perception pattern must be equal to corresponding
                    field in the perception record.

    Returns:
     
        On fail, returns False.     
        On success, returns True.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.RecallIfPercept(percpatt)
    except:
        return False

def perceive_one(acid, percpatt):
    """ Search perception base and recognize a perception that match percpatt pattern
        and is unique.

    Args:

        acid:       str with unique global identifier of actor.
        percpatt:   the perception search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    perception pattern are ignored in the search, string fields
                    defined in perception pattern must be equal to corresponding
                    field in the perception record.

    Returns:
     
        On fail, returns None.      
        On success, returns the unique perception that matches the perception 
        pattern. A perception record is simply a list of strings.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.RecallSinglePercept(percpatt)
    except:
        return None

def perceive(acid, percpatt):
    """ Search perception base and recognize a perception that match percpatt pattern.

    Args:

        acid:       str with unique global identifier of actor.
        percpatt:   the perception search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    perception pattern are ignored in the search, string fields
                    defined in perception pattern must be equal to corresponding
                    field in the perception record.

    Returns:
     
        On fail, returns None.      
        On success, returns the first perception that matches the perception 
        pattern. A perception record is simply a list of strings.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.RecallPercept(percpatt)
    except:
        return None

def perceive_when_one(acid, percpatt):
    """ Search perception base for a perception that match percpatt search pattern
        and is unique, returns the time when this perception was stored

    Args:

        acid:       str with unique global identifier of actor.
        percpatt:   the perception search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    perception pattern are ignored in the search, string fields
                    defined in perception pattern must be equal to corresponding
                    field in the perception record.

    Returns:
     
        On fail, returns None.      
        On success, returns the time of the unique perception record found that matches 
        the perception pattern. The time is a str that specifies the instant of time 
        using Microsoft Datetime.Parse() method format. Examples: 
            "2008-11-01T19:35:00.0000000Z", 
            "2008-11-01T19:35:00.0000000-07:00",
            "Sat, 01 Nov 2008 19:35:00 GMT",
            "03/01/2009 05:42:00 -5:00"         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.RecallWhenSinglePercept(percpatt)
    except:
        return None

def perceive_when(acid, percpatt):
    """ Search perception base for a perception that match percpatt search pattern, 
        returns the time when this perception was stored

    Args:

        acid:       str with unique global identifier of actor.
        percpatt:   the perception search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    perception pattern are ignored in the search, string fields
                    defined in perception pattern must be equal to corresponding
                    field in the perception record.

    Returns:
     
        On fail, returns None.      
        On success, returns the time of the first perception record found that matches 
        the perception pattern. The time is a str that specifies the instant of time 
        using Microsoft Datetime.Parse() method format. Examples: 
            "2008-11-01T19:35:00.0000000Z", 
            "2008-11-01T19:35:00.0000000-07:00",
            "Sat, 01 Nov 2008 19:35:00 GMT",
            "03/01/2009 05:42:00 -5:00"         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.RecallWhenPercept(percpatt)
    except:
        return None

def record_perceptions(acid, percpatt):
    """ Search perception base and store (remember) all perceptions that match 
        percpatt pattern as new memories with name 'percept'

    Args:

        acid:       str with unique global identifier of actor.
        percpatt:   the perception search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    perception pattern are ignored in the search, string fields
                    defined in perception pattern must be equal to corresponding
                    field in the perception record.

    Returns:
     
        On fail, returns None.      
        On success, updates actor's memory with a list of perception records that 
        matches the perception pattern, and return this list. A remembered perception 
        record is a list of strings were the first element of the list is the 
        string 'percept'.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.RememberPerceptsThat(percpatt)
    except:
        return False

def register_perception(acid, perception):
    """ Registers a new perception record in perception base.

    Args:

        acid:       str with unique global identifier of actor.
        perception: the perception record to be stored on the perception base, 
                    it a list of strings.

    Returns:
     
        On fail, returns False.     
        On success, add new perception to perception base and returns True.         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.RegisterPercept(perception)
    except:
        return False

def remove_perceptions(acid, percpatt):
    """ Delete from perception base the perceptions that match percpatt search pattern.

    Args:

        acid:       str with unique global identifier of actor.
        percpatt:   the perception search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    perception pattern are ignored in the search, string fields
                    defined in perception pattern must be equal to corresponding
                    field in the perception record.

    Returns:
     
        On fail, do not change perception base and returns False.       
        On success, delete the perceptions that match percpatt from perception base
        and returns True.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.ForgetPerceptsThat(percpatt)
    except:
        return False

def remove_all_perceptions(acid):
    """ Delete all perceptions from perception base (clear perception base).

    Args:

        acid:       str with unique global identifier of actor.

    Returns:
     
        On fail, do not change perception base and return False.        
        On success, clear perception base and return True.          
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.Percepts.ForgetAllPercepts()
    except:
        return False
#endregion


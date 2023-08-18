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
#   Module:     MemoryActions
#   Purpose:    Actions to manage actor's memory, allowing it to
#               remember, record and forget memories
#   Author:     João Carlos Gluz
#
###############################################################
###############################################################

""" Module MemoryActions - Actions to remember, record and forget memories
    Functions:
        save_memories(acid,filename)
        restore_memories(acid,filename)
        remember(acid, mempatt)
        remember_all(acid, mempatt)
        remember_all_before(acid, time, mempatt) 
        remember_all_before_or_at(acid, time, mempatt)
        remember_all_after(acid, time, mempatt)
        remember_all_after_or_at(acid, time, mempatt) 
        remember_recent(acid, secs, mempatt)
        remember_past(acid, secs, mempatt)
        remember_if_one(acid, mempatt)
        remember_if(acid, mempatt)
        remember_one(acid, mempatt)
        remember_when_one(acid, mempatt)
        remember_when(acid, mempatt)
        record(acid, memory)
        update_memory(acid, memprefix, memsuffix)
        extract_memory(acid, mempatt)
        forget(acid, mempatt)
        forget_all_memories(acid)



"""


import ActorController as ac

#region Beliefs

def save_memories(acid, filename):
    """ Save all information stored in actor's memory to a JSON file.

    Args:

        acid:       str with unique global identifier of actor.
        filename:   path and name of JSON file.

    Returns:
     
        On fail, returns false.     
        On success, true.           
    """

#   try:
    agent = ac.get_agctl(acid)
    return agent.Bels.SaveBels(filename)
#   except:
#       return False

def restore_memories(acid, filename):
    """ Restore actor's memory from a JSON file.

    Args:

        acid:       str with unique global identifier of actor.
        filename:   path and name of JSON file.

    Returns:
     
        On fail, returns false.     
        On success, true.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RestoreBels(filename)
    except:
        return False

def remember_all(acid, mempatt):
    """ Search actor's memory and retrieve all memories that match mempatt pattern.

    Args:

        acid:       str with unique global identifier of actor.
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns a list of memory records for each memory
        that matches the memory pattern. 
        A memory record is a list of strings, where the first string 
        is the name of the memory.     
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallBelsThat(mempatt)
    except:
        return None

def remember_all_before(acid, time, mempatt):
    """ Search actor's memory and retrieve all memories that were stored before 
        some specific moment of time and that match mempatt pattern.

    Args:

        acid:       str with unique global identifier of actor.
        time:       str that specifies the instant of time using Microsoft 
                    Datetime.Parse() method format. Examples: 
                    "2008-11-01T19:35:00.0000000Z", 
                    "2008-11-01T19:35:00.0000000-07:00",
                    "Sat, 01 Nov 2008 19:35:00 GMT",
                    "03/01/2009 05:42:00 -5:00"
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns a list of memory records for each 
        memory that matches the memory pattern and were stored before
        the time parameter value. 
        A memory record is a list of strings, where the first string 
        is the name of the memory.     
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallBelsBefore(time,mempatt)
    except:
        return None

def remember_all_before_or_at(acid, time, mempatt):
    """ Search actor's memory and retrieve all memories that were stored before 
        or at some specific moment of time and that match mempatt pattern.

    Args:

        acid:       str with unique global identifier of actor.
        time:       str that specifies the instant of time using Microsoft 
                    Datetime.Parse() method format. Examples: 
                    "2008-11-01T19:35:00.0000000Z", 
                    "2008-11-01T19:35:00.0000000-07:00",
                    "Sat, 01 Nov 2008 19:35:00 GMT",
                    "03/01/2009 05:42:00 -5:00"
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns a list of memory records for each 
        memory that matches the memory pattern and were stored before
        or at the time parameter value. 
        A memory record is a list of strings, where the first string 
        is the name of the memory.     
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallBelsBeforeOrAt(time,mempatt)
    except:
        return None

def remember_all_after(acid, time, mempatt):
    """ Search actor's memory and recall retrieve all memories were stored after 
        some specific moment of time and that match mempatt pattern.

    Args:

        acid:       str with unique global identifier of actor.
        time:       str that specifies the instant of time using Microsoft 
                    Datetime.Parse() method format. Examples: 
                    "2008-11-01T19:35:00.0000000Z", 
                    "2008-11-01T19:35:00.0000000-07:00",
                    "Sat, 01 Nov 2008 19:35:00 GMT",
                    "03/01/2009 05:42:00 -5:00"
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns a list of memory records for each 
        memory that matches the memory pattern and were stored after 
        the time parameter value. 
        A memory record is a list of strings, where the first string 
        is the name of the memory.     
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallBelsAfter(time,mempatt)
    except:
        return None

def remember_all_after_or_at(acid, time, mempatt):
    """ Search actor's memory and retrieve all memories that were stored after
        or at some specific moment of time and that match mempatt pattern.

    Args:

        acid:       str with unique global identifier of actor.
        time:       str that specifies the instant of time using Microsoft 
                    Datetime.Parse() method format. Examples: 
                    "2008-11-01T19:35:00.0000000Z", 
                    "2008-11-01T19:35:00.0000000-07:00",
                    "Sat, 01 Nov 2008 19:35:00 GMT",
                    "03/01/2009 05:42:00 -5:00"
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns a list of memory records for each 
        memory that matches the memory pattern and were stored after
        or at the time parameter value. 
        A memory record is a list of strings, where the first string 
        is the name of the memory.     
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallBelsAfterOrAt(time,mempatt)
    except:
        return None

def remember_recent(acid, secs, mempatt):
    """ Search actor's memory and retrieve recent memories that were stored
        at most in the last secs seconds and that match mempatt pattern.

    Args:

        acid:       str with unique global identifier of actor.
        secs:       float that specifies the maximum time, in seconds, that
                    memory is stored in actor's memory
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns a list of recent memory records for each 
        memory that matches the memory pattern and were stored in the
        last secs seconds. 
        A memory record is a list of strings, where the first string 
        is the name of the memory.     
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallRecentBels(secs,mempatt)
    except:
        return None

def remember_past(acid, secs, mempatt):
    """ Search actor's memory and retrieve old memories that have at least
        secs seconds of storage time and that match mempatt pattern.

    Args:

        acid:       str with unique global identifier of actor.
        secs:       float that specifies the minimum time, in seconds, that
                    memory record is stored in actor's memory
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns a list of recent memory records for each 
        memory that matches the memory pattern and were stored at least
        for secs seconds. 
        A memory record is a list of strings, where the first string 
        is the name of the memory.     
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallPastBels(secs,mempatt)
    except:
        return None

def remember_if_one(acid, mempatt):
    """ Check if actor's memory has a memory that match mempatt pattern
        and is unique

    Args:
        acid:       str with unique global identifier of actor.
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:    
        On fail, returns False.     
        On success, returns True.           
    """
    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallIfSingleBel(mempatt)
    except:
        return False

def remember_if(acid, mempatt):
    """ Check if actor's memory has a memory that match mempatt pattern

    Args:
        acid:       str with unique global identifier of actor.
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:     
        On fail, returns False.     
        On success, returns True.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallIfBel(mempatt)
    except:
        return False

def remember(acid, mempatt):
    """ Search actor's memory and recall the first memory that match mempatt search pattern.

    Args:
        acid:       str with unique global identifier of actor.
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:    
        On fail, returns None.      
        On success, returns the first memory record that matches the memory 
        pattern. 
        A memory record is a list of strings, where the first string 
        is the name of the memory.     
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallBel(mempatt)
    except:
        return None

def remember_one(acid, mempatt):
    """ Search actor's memory and recall a memory that match mempatt search pattern
        and is unique.

    Args:

        acid:       str with unique global identifier of actor.
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns the unique memory record that matches the memory 
        pattern. 
        A memory record is a list of strings, where the first string 
        is the name of the memory.     
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallSingleBel(mempatt)
    except:
        return None

def remember_when_one(acid, mempatt):
    """ Search actor's memory for a memory that match mempatt search pattern
        and is unique, returns the time when this memory was stored

    Args:

        acid:       str with unique global identifier of actor.
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns the time of the unique memory record found that matches 
        the memory pattern. The time is a str that specifies the instant of time 
        using Microsoft Datetime.Parse() method format. Examples: 
            "2008-11-01T19:35:00.0000000Z", 
            "2008-11-01T19:35:00.0000000-07:00",
            "Sat, 01 Nov 2008 19:35:00 GMT",
            "03/01/2009 05:42:00 -5:00"         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallWhenSingleBel(mempatt)
    except:
        return None

def remember_when(acid, mempatt):
    """ Search actor's memory for a memory that match mempatt search pattern, 
        returns the time when this memory was stored

    Args:

        acid:       str with unique global identifier of actor.
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns the time of the first memory record found that matches 
        the memory pattern. The time is a str that specifies the instant of time 
        using Microsoft Datetime.Parse() method format. Examples: 
            "2008-11-01T19:35:00.0000000Z", 
            "2008-11-01T19:35:00.0000000-07:00",
            "Sat, 01 Nov 2008 19:35:00 GMT",
            "03/01/2009 05:42:00 -5:00"         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecallWhenBel(mempatt)
    except:
        return None

def record(acid, memory):
    """ Registers a new memory in actor's memory.

    Args:

        acid:       str with unique global identifier of actor.
        memory:     the memory record to be stored on actor's memory, 
                    it is a list of strings.

    Returns:
     
        On fail, do not change actor's memory and returns False.       
        On success, adds the new memory record to actor's memory and returns True.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.RecordBel(memory)
    except:
        return False

def update_memory(acid, memprefix, memsuffix):
    """ Updates a (or add a new) memory in actor's memory. First all memory records 
        which start with memprefix are deleted from actor's memory, then a memory
        record composed by the concatenation of memprefix and memsuffix is added
        to actor's memory.

    Args:

        acid:       str with unique global identifier of actor.
        memprefix:  the prefix of memory record to be updated, it is the list of 
                    string at the beginning of this memory record
        memsuffix:  the suffix of memory record to be updated, it is the list of
                    strings at the end of this memory record 

    Returns:
     
        On fail, do not change actor's memory and returns False.       
        On success, updates the memory record on actor's memory and returns True.           
    """

    try:
        agent = ac.get_agctl(acid)
        agent.Bels.ForgetBelsThat(memprefix)
        return agent.Bels.RecordBel(memprefix+memsuffix)
    except:
        return False

def extract_memory(acid, mempatt):
    """ Search actor's memory and retrieve the first memory that match mempatt search 
        pattern. Then delete all memories that match the mempatt pattern.

    Args:

        acid:       str with unique global identifier of actor.
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, returns None.      
        On success, returns the first memory record that matches the memory 
        pattern and then delete all memories that match this patter.
        A memory record is a list of strings, where the first string 
        is the name of the memory.     
    """

    try:
        agent = ac.get_agctl(acid)
        memory = agent.Bels.RecallBel(mempatt)
        if memory!=None:
            agent.Bels.ForgetBelsThat(mempatt)
        return memory
    except:
        return None

def forget(acid, mempatt):
    """ Delete from actor's memory all memory records that match mempatt 
        search pattern.

    Args:

        acid:       str with unique global identifier of actor.
        mempatt:    the memory search pattern: a list of fields, each field 
                    containing an string or the None value. None fields in 
                    memory pattern are ignored in the search, string fields
                    defined in memory pattern must be equal to corresponding
                    field in the memory record.

    Returns:
     
        On fail, do not change actor's memory and returns False.       
        On success, delete from actor's memory all memory records that match mempatt 
        and returns True.           
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.ForgetBelsThat(mempatt)
    except:
        return False

def forget_all_memories(acid):
    """ Delete all memories from actor's memory (clears actor's memory).

    Args:

        acid:       str with unique global identifier of actor.

    Returns:
     
        On fail, do not change actor's memory and returns False.       
        On success, clears actor's memory and returns True.         
    """

    try:
        agent = ac.get_agctl(acid)
        return agent.Bels.ForgetAllBels()
    except:
        return False

#endregion


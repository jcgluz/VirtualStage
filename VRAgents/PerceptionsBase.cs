//***********************************************************************
//
//  VirtualStage Platform - a virtual stage for virtual actors
//  VRAgents -  C# library for developing agents able to operate in
//              OpenSimulator virtual worlds
//
//  Copyright (C): 2020-2023, Joao Carlos Gluz
//  Contact:  João Carlos Gluz (jcgluz@gmail.com)
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//
//***********************************************************************
//
//   Class:     PerceptionsBase 
//   Purpose:   To implement the agent's perceptions base 
//   Author:    João Carlos Gluz 
//
//***********************************************************************
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
#if USE_LIBREMETAVERSE_VR_LIB
using LibreMetaverse;
#else
using OpenMetaverse;
#endif

#if USE_LIBREMETAVERSE_VR_LIB
namespace LibreMetaverse
#else
namespace OpenMetaverse
#endif
{
    public class PerceptList
    {
        public List<Percept> perceptList;

        public PerceptList()
        {
            perceptList = new List<Percept>();
        }

        public int Count => perceptList.Count;

        public List<string> Add(params string[] arglst)
        {
            if (arglst.Length < 2)
                return null;
            Percept percept = new Percept();
            List<string> returnlst = new List<string>();
            percept.Type = arglst[0];
            percept.ObjID = arglst[1];
            percept.Time = DateTime.Now.Ticks;
            int infoSize = arglst.Length - 2;
            if (infoSize == 0)
                percept.Args = null;
            else {
                percept.Args = new string[infoSize];
                for (int iparam = 2; iparam < arglst.Length; iparam++)
                    percept.Args[iparam - 2] = arglst[iparam];
            }
            perceptList.Add(percept);
            for (int iparam = 0; iparam < arglst.Length; iparam++)
                returnlst.Add(arglst[iparam]);
            return returnlst;
        }
    }

    public class PerceptionsBase
    {
        // Each perception has a perception type name which identifies the 
        // type of the perception (i.e. "region", "avatar", "name_of", etc.),
        // and an object unique universal ID (an UUID), which identifies
        // to what virtual world object (i.e. primitive, region, avatar, etc.)
        // the perception is related.
        // The combination of perception type name and perception object's 
        // ID is unique and will be used as a two level primary index of the 
        // perception DB. 
        Dictionary<string, Dictionary<string, Percept>> perceptMemDB =
            new Dictionary<string, Dictionary<string, Percept>>();

        // A secondary index, which uses percept object's ID first and
        // percept type second is also implemented.
        Dictionary<string, Dictionary<string, Percept>> perceptObjTypeIndex =
            new Dictionary<string, Dictionary<string, Percept>>();

        // In the following functions the first argument (arglist[0]) will
        // allways contains the type of the perception and the second
        // argument (arglist[1]) the peception object's ID

        void UpdateDBAndIndex(Percept percept)
        {
            Dictionary<string, Percept> sameTypePercepts;
            if (!perceptMemDB.TryGetValue(percept.Type, out sameTypePercepts) ){
                sameTypePercepts = new Dictionary<string, Percept>();
                perceptMemDB[percept.Type] = sameTypePercepts;
            }
            perceptMemDB[percept.Type][percept.ObjID] = percept;

            Dictionary<string, Percept> sameObjPercepts;
            if (!perceptObjTypeIndex.TryGetValue(percept.ObjID, out sameObjPercepts) ){
                sameObjPercepts = new Dictionary<string, Percept>();
                perceptObjTypeIndex[percept.ObjID] = sameObjPercepts;
            }
            perceptObjTypeIndex[percept.ObjID][percept.Type] = percept;
        }

        public bool Update(params string[] arglst)
        {
            if (arglst.Length < 2)
                return false;
            Percept percept = new Percept();
            percept.Type = arglst[0];
            percept.ObjID = arglst[1];
            int nargs = arglst.Length - 2;
            if (nargs == 0)
                percept.Args = null;
            else {
                percept.Args = new string[nargs];
                for (int iparam = 2; iparam < arglst.Length; iparam++)
                    percept.Args[iparam - 2] = arglst[iparam];
            }
            UpdateDBAndIndex(percept);
            return true;
        }

        public bool Update(PerceptList pList)
        {
            foreach (Percept percept in pList.perceptList) {
                UpdateDBAndIndex(percept);
            }
            return true;
        }


        public List<Percept> Search(params string[] arglst)
        {
            List<Percept> results = new List<Percept>();
            string pType = null;
            string pObjID = null;
            if (arglst.Length > 0)
                pType = arglst[0];
            if (arglst.Length > 1)
                pObjID = arglst[1];
            if (pType == null && pObjID == null) {
                // No search argument was provided that can be used as a 
                // DB index. The basic search algorithm is a linear search, 
                // checking all perceptions in base against search arguments.
                // However first check a special case
                if (arglst.Length<3) {
                    // No search arguments provided, retrieve all percept base
                    foreach (Dictionary<string, Percept> sameTypePercepts
                            in perceptMemDB.Values) {
                        foreach (Percept percept in sameTypePercepts.Values) {
                                results.Add(percept);
                        }
                    }
                    return results;
                }
                foreach (Dictionary<string, Percept> sameTypePercepts
                        in perceptMemDB.Values) {
                    foreach (Percept percept in sameTypePercepts.Values) {
                        if (MatchWithNullArgs(percept, arglst))
                            results.Add(percept);
                    }
                }
                return results;
            }

            if (pType != null && pObjID != null) {
                // There are two search arguments that work as primary DB index.
                // Use hash tables to get the perception and then check
                // if remaining search arguments match
                Dictionary<string, Percept> sameTypePercepts;
                Percept percept;
                if (perceptMemDB.TryGetValue(pType, out sameTypePercepts)) {
                    if (sameTypePercepts.TryGetValue(pObjID, out percept)) {
                        if (arglst.Length<3)
                            // No remaining arguments to check, simply return percept
                            results.Add(percept);
                        else if (MatchWithNullArgs(percept, arglst))
                            // Remaining arguments match ok, return percept
                            results.Add(percept);
                    }
                }
                return results;
            } 

            if (pType != null) {
                // Percept type name argument was provided. Use this argument 
                // to get the list of same name percepts, and then scan 
                // this list to get matching perceptions.
                Dictionary<string, Percept> sameTypePercepts;
                if (perceptMemDB.TryGetValue(pType, out sameTypePercepts)) {
                    if (arglst.Length<3) {
                        // No remaining arguments to check, add entire list
                        foreach (Percept percept in sameTypePercepts.Values) {
                            results.Add(percept);
                        }
                    } else {
                        // Check if remaining arguments match, before add percept
                        foreach (Percept percept in sameTypePercepts.Values) {
                            if (MatchWithNullArgs(percept, arglst))
                                results.Add(percept);
                        }
                    }
                }
                return results;
            }
            // Percept object's ID argument was provided. Use this argument 
            // to get the list of percepts with same object ID, and then 
            // scan this list to get matching perceptions.
            Dictionary<string, Percept> sameObjIDPercepts;
            if (perceptObjTypeIndex.TryGetValue(pObjID, out sameObjIDPercepts)){
                if (arglst.Length < 3) {
                    // No remaining arguments to check, add entire list
                    foreach (Percept percept in sameObjIDPercepts.Values) {
                        results.Add(percept);
                    }
                } else {
                    foreach (Percept percept in sameObjIDPercepts.Values) {
                        if (MatchWithNullArgs(percept, arglst))
                            results.Add(percept);
                    }
                }
            }
            return results;
        }

        // MatchWithNullArgs() method assumes arglst.Length>2
        bool MatchWithNullArgs(Percept percept, params string[] arglst)
        {
            if (arglst[0] != null) {
                if (percept.Type != arglst[0])
                    return false;
            }
            if (arglst[1] != null) {
                if (percept.ObjID != arglst[1])
                    return false;
            }
            if (arglst.Length - 2 > percept.Args.Length)
                // More search arguments than percept arguments,
                // never will match, return false
                return false;
            for (int i=2,j=0; i < arglst.Length; i++,j++) {
                if (arglst[i] != null)
                    if (percept.Args[j] != arglst[i])
                        return false;
            }
            return true;

        }

        public bool Clear()
        {
            perceptMemDB.Clear();
            perceptObjTypeIndex.Clear();
            return true;
        }

        public bool Delete(params string[] arglst)
        {
            // Delete procedure linearly scan all perceptions,
            // removing the perceptions that match search arguments
            // First scan all sets of DB entries with same type percepts
            foreach(KeyValuePair<string, Dictionary<string, Percept>>
                        samePerceptTypeDB in perceptMemDB) {
                List<string> delkeys = new List<string>();
                // Now scan same type percepts, by Obj ID index
                foreach (KeyValuePair<string, Percept>
                            perceptDBEntry in samePerceptTypeDB.Value) {
                    // Check if percept in DB entry matches search arguments
                    if (MatchWithNullArgs(perceptDBEntry.Value, arglst)) {
                        // It matched, first register that it must lately 
                        // remove DB entry from primary index
                        delkeys.Add(perceptDBEntry.Key);
                        // Then remove DB entry from secondary index
                        perceptObjTypeIndex[perceptDBEntry.Key].Remove(
                                samePerceptTypeDB.Key);
                    }
                }
                // Now remove all entries that matched from primary index
                // (this is necessary to avoid  Exception ("Collection was 
                // modified..."))
                foreach (string key in delkeys)
                    samePerceptTypeDB.Value.Remove(key);
            }
            // Finally check if there are lists of DB entries with same type
            // or lists of DB entries with same Obj ID percepts that are 
            // empty and remove them
            foreach (KeyValuePair<string, Dictionary<string, Percept>>
                        samePerceptTypeDB in perceptMemDB) {
                // If the list of DB entries with same type percepts 
                // is empty, remove it
                if (samePerceptTypeDB.Value.Count == 0)
                    perceptMemDB.Remove(samePerceptTypeDB.Key);
            }
            foreach (KeyValuePair<string, Dictionary<string, Percept>>
                        samePerceptObjDB in perceptObjTypeIndex) {
                // If the list of DB entries with same obj ID percepts 
                // is empty, remove it
                if (samePerceptObjDB.Value.Count == 0)
                    perceptObjTypeIndex.Remove(samePerceptObjDB.Key);
            }

            return true;
        }


    }
}

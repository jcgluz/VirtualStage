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
//   Class:     BeliefBase 
//   Purpose:   To implements agent's beliefs base (the memory of the agent)
//   Author:    João Carlos Gluz 
//
//***********************************************************************
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
//using System.Text.Json;
using Newtonsoft.Json;
using System.IO;

namespace OpenMetaverse
{
    public class BeliefsBase
    {
        // Each belief has a belief name which identifies the 
        // belief and a list of possible additional arguments.
        // Beliefs are very flexible data types so there is no obvious 
        // set or arguments that can be used as a primary index or sort \
        // order to organize the belief base.
        // However, the name of the belief can be used to divide the
        // set of beliefs in list of beliefs with same name, that can
        // help in the find/update/add/del DB operations.
        Dictionary<string, List<Bel>> beliefMemDB =
            new Dictionary<string, List<Bel>>();
 
        // In the following functions the first argument (arglist[0]) will
        // allways contains the name of the belief

        public bool Add(params string[] arglst)
        {
            if (arglst.Length < 1)
                return false;
            Bel bel = new Bel();
            bel.Name = arglst[0];
            int nargs = arglst.Length - 1;
            if (nargs == 0)
                bel.Args = null;
            else {
                bel.Args = new string[nargs];
                for (int iparam = 1; iparam < arglst.Length; iparam++)
                    bel.Args[iparam - 1] = arglst[iparam];
            }
            bel.Time = DateTime.Now.Ticks;
            List<Bel> belList;
            if (!beliefMemDB.TryGetValue(bel.Name, out belList)) {
                belList = new List<Bel>();
                beliefMemDB[bel.Name] = belList;
            }
            belList.Add(bel);
            return true;
        }

        public bool AddPercept(Percept percept)
        {
            Bel bel = new Bel();
            bel.Name = "percept";
            bel.Args = new string[percept.Args.Length+2];
            bel.Args[0] = percept.Type;
            bel.Args[1] = percept.ObjID;
            for (int iparam = 0; iparam < percept.Args.Length; iparam++) {
                    bel.Args[iparam+2] = percept.Args[iparam];
            }
            bel.Time = percept.Time;
            List<Bel> belList;
            if (!beliefMemDB.TryGetValue(bel.Name, out belList)) {
                belList = new List<Bel>();
                beliefMemDB[bel.Name] = belList;
            }
            belList.Add(bel);
            return true;
        }

        public List<Bel> Search(params string[] arglst)
        {
            List<Bel> results = new List<Bel>();
            string belName = null;
            bool retrieveDB = false;
            if (arglst.Length == 0)
                retrieveDB = true;
            belName = arglst[0];
            if (belName==null && arglst.Length==1)
                retrieveDB = true;
            if (retrieveDB) {
                foreach (List<Bel> sameNameBels in beliefMemDB.Values) {
                    foreach (Bel bel in sameNameBels) {
                        results.Add(bel);
                    }
                }
                return results;
            }
            if (arglst.Length == 1) {
                List<Bel> sameNameBels;
                if (beliefMemDB.TryGetValue(belName, out sameNameBels)) {
                    foreach (Bel bel in sameNameBels) {
                            results.Add(bel);
                    }
                }
            return results;
            } 
            if (belName!=null) {
                List<Bel> sameNameBels;
                if (beliefMemDB.TryGetValue(belName, out sameNameBels)) {
                    foreach (Bel bel in sameNameBels) {
                        if (MatchWithNullArgs(bel, arglst))
                            results.Add(bel);
                    }
                }
            } else {
                foreach (List<Bel> sameNameBels in beliefMemDB.Values) {
                    foreach (Bel bel in sameNameBels) {
                        if (MatchWithNullArgs(bel, arglst))
                            results.Add(bel);
                    }
                }
            }
            return results;
        }



        // MatchWithNullArgs() assumes that arglst.Length>1
        bool MatchWithNullArgs(Bel bel, params string[] arglst)
        {
            if (arglst[0] != null) {
                if (bel.Name != arglst[0])
                    return false;
            }
            if (bel.Args == null) {
                if (arglst.Length > 1)
                    return false;
                else
                    return true;
            } 
            if (arglst.Length - 1 > bel.Args.Length)
                return false;
            for (int i = 1; i < arglst.Length; i++) {
                if (arglst[i] != null)
                    if (bel.Args[i - 1] != arglst[i])
                        return false;
            }
        return true;
        }

        public bool Clear()
        {
            beliefMemDB.Clear();
            return true;
        }

        public bool Delete(params string[] arglst)
        {
            bool clearDB = false;
            if (arglst.Length == 0)
                clearDB = true;
            if (arglst[0] == null && arglst.Length == 1)
                clearDB = true;
            if (clearDB)
                return Clear();
            if (arglst[0]!=null) {
                List<Bel> sameNameBels;
                if (beliefMemDB.TryGetValue(arglst[0], out sameNameBels))
                    sameNameBels.RemoveAll(bel => MatchWithNullArgs(bel, arglst));
            }
            else {
                foreach (List<Bel> sameNameBels in beliefMemDB.Values)
                    sameNameBels.RemoveAll(bel => MatchWithNullArgs(bel, arglst));
            }
            return true;
        }

        public bool SaveBeliefs(string fileName)
        {
            Console.WriteLine("Saving Belief DB to file: {0}", fileName);
//            string jsonString = JsonSerializer.Serialize(beliefMemDB);
            string jsonString = JsonConvert.SerializeObject(beliefMemDB,Formatting.Indented);
            Console.WriteLine("JSON Serialization OK");
            File.WriteAllText(fileName, jsonString);
            Console.WriteLine("JSON string saved on file");
            return true;
        }

        public bool RestoreBeliefs(string fileName)
        {
            Console.WriteLine("Restoring Belief DB from file: {0}", fileName);
            string jsonString = File.ReadAllText(fileName);
            Console.WriteLine("JSON string read from file");
//            beliefMemDB = JsonSerializer.Deserialize<Dictionary<string, List<Bel>>>(jsonString);
            beliefMemDB = JsonConvert.DeserializeObject<Dictionary<string, List<Bel>>>(jsonString);
            Console.WriteLine("Deserealization OK");
            Console.WriteLine("Updating date and time");
            foreach (List<Bel> sameNameBels
                    in beliefMemDB.Values) {
                foreach (Bel bel in sameNameBels) {
                    bel.Time = DateTime.Now.Ticks;
                }
            }
            return true;
        }
    }
}

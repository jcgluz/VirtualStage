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
//   Class:     Perceptions 
//   Purpose:   To implements agent's access to its perceptions base 
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
using LibreMetaverse.Packets;
#else
using OpenMetaverse;
using OpenMetaverse.Packets;
#endif
// using System.Collections.Specialized;

#if USE_LIBREMETAVERSE_VR_LIB
namespace LibreMetaverse
#else
namespace OpenMetaverse
#endif
{
    public class Percept
    {
        public string Type;
        public string ObjID;
        public string[] Args;
        public long Time;
    }



    public class Perceptions 
    {
        //            PerceptionMemDB PerceptionDB = new PerceptionMemDB();
        public VRAgentController Agent;

        public Perceptions(VRAgentController agent)
        {
            Agent = agent;
        }

        public List<string> RecallPercept(params string[] arglst)
        {
            List<Percept> percepts =
                Agent.PerceptsBase.Search(arglst);
            if (percepts == null)
                return VRAgentController.nullst("percept not found");
            if (percepts.Count == 0)
                return VRAgentController.nullst("percept not found");
            Percept percept = percepts[0];
            List<string> spercept = new List<string>();
            spercept.Add(percept.Type);
            spercept.Add(percept.ObjID);
            if (percept.Args != null)
                for (int i = 0; i < percept.Args.Length; i++) {
                    spercept.Add(percept.Args[i]);
                }
            DateTime perctime = new DateTime(percept.Time);
            spercept.Add(perctime.ToString("s"));
            return VRAgentController.ok("percept found",spercept);
        }

        public List<string> RecallSinglePercept(params string[] arglst)
        {
            List<Percept> percepts = Agent.PerceptsBase.Search(arglst);
            VRAgentController.ok("recall sole percept ok");
            if (percepts == null)
                return VRAgentController.nullst("percept not found");
            if (percepts.Count == 0 || percepts.Count > 1)
                return VRAgentController.nullst("percept not found or not single");
            Percept percept = percepts[0];
            List<string> spercept = new List<string>();
            spercept.Add(percept.Type);
            spercept.Add(percept.ObjID);
            if (percept.Args != null)
                for (int i = 0; i < percept.Args.Length; i++) {
                    spercept.Add(percept.Args[i]);
                }
            DateTime perctime = new DateTime(percept.Time);
            spercept.Add(perctime.ToString("s"));
            return VRAgentController.ok("single percept found", spercept);
        }

        public bool RecallIfPercept(params string[] arglst)
        {
            List<Percept> percepts = Agent.PerceptsBase.Search(arglst);
            VRAgentController.ok("recall if percept ok");
            if (percepts == null)
                return VRAgentController.fail("percept not found");
            if (percepts.Count == 0)
                return VRAgentController.fail("percept not found");
            return VRAgentController.ok("percept found");
        }

        public bool RecallIfSinglePercept(params string[] arglst)
        {
            List<Percept> percepts = Agent.PerceptsBase.Search(arglst);
            VRAgentController.ok("recall if single percept ok");
            if (percepts == null)
                return VRAgentController.fail("percept not found");
            if (percepts.Count == 0 || percepts.Count > 1)
                return VRAgentController.fail("percept not found or not single");
            return VRAgentController.ok("single percept found");
        }

        public string RecallWhenPercept(params string[] arglst)
        {
            List<Percept> percepts = Agent.PerceptsBase.Search(arglst);
            VRAgentController.ok("recall when percept ok");
            if (percepts == null)
                return VRAgentController.nulstr("percept not found");
            if (percepts.Count == 0)
                return VRAgentController.nulstr("percept not found");
            DateTime datim = new DateTime(percepts[0].Time);
            return VRAgentController.ok("percept found", datim.ToString("s"));
        }

        public string RecallWhenSinglePercept(params string[] arglst)
        {
            List<Percept> percepts = Agent.PerceptsBase.Search(arglst);
            VRAgentController.ok("recall when single percept ok");
            if (percepts == null)
                return VRAgentController.nulstr("percept not found");
            if (percepts.Count == 0 || percepts.Count > 1)
                return VRAgentController.nulstr("percept not found or not single");
            DateTime datim = new DateTime(percepts[0].Time);
            return VRAgentController.ok("single percept found", datim.ToString("s"));
        }


        public List<List<string>> RecallPerceptsThat(params string[] arglst)
        {
            List<Percept> lpercepts = Agent.PerceptsBase.Search(arglst);
            List<List<string>> lspercepts = new List<List<string>>();
            foreach (Percept percept in lpercepts) {
                List<string> spercept = new List<string>();
                spercept.Add(percept.Type);
                spercept.Add(percept.ObjID);
                if (percept.Args != null)
                    for (int i = 0; i < percept.Args.Length; i++) {
                        spercept.Add(percept.Args[i]);
                    }
                DateTime perctime = new DateTime(percept.Time);
                spercept.Add(perctime.ToString("s"));
                lspercepts.Add(spercept);
            }
            if (lspercepts.Count>0)
                VRAgentController.ok("found percepts");
            else
                VRAgentController.ok("percepts not found");
            return lspercepts;
        }

        public bool RememberPerceptsThat(params string[] arglst)
        {
            List<Percept> perceptsToRemember = Agent.PerceptsBase.Search(arglst);
            foreach (Percept percept in perceptsToRemember) {
                Agent.Bels.RecordPerceptAsBel(percept);
            }
            if (perceptsToRemember.Count > 0)
                return VRAgentController.ok("percepts remembered");
            else
                return VRAgentController.fail("percepts not found");
        }

        public bool RegisterPercept(params string[] arglst)
        {
            if (!Agent.PerceptsBase.Update(arglst))
                return VRAgentController.fail("fail register percept");
            return VRAgentController.ok("register percept ok");
        }

        public bool ForgetPerceptsThat(params string[] arglst)
        {
            if (!Agent.PerceptsBase.Delete(arglst))
                return VRAgentController.fail("fail forget percepts");
            return VRAgentController.ok("forget percepts ok");
        }

        public bool ForgetAllPercepts()
        {
            if (!Agent.PerceptsBase.Clear())
                return VRAgentController.fail("fail forget all percepts");
            return VRAgentController.ok("forget all percepts ok");
        }
    }



}


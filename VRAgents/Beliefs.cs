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
//   Class:     Beliefs 
//   Purpose:   To implements agent's access to its belief base (its memory) 
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

#if USE_LIBREMETAVERSE_VR_LIB
namespace LibreMetaverse
#else
namespace OpenMetaverse
#endif
{
    public class Bel    
    {
        public string Name;
        public string[] Args;
        public long Time;
    }


    public class Beliefs 
    {
        public VRAgentController Agent;

        public Beliefs(VRAgentController agent)
        {
            Agent = agent;
        }

        public bool SaveBels(string fileName)
        {
            return Agent.BelsBase.SaveBeliefs(fileName);
        }

        public bool RestoreBels(string fileName)
        {
            return Agent.BelsBase.RestoreBeliefs(fileName);
        }

        public List<string> RecallBel(params string[] arglst)
        {
            List<Bel> beliefs = Agent.BelsBase.Search(arglst);
            if (beliefs == null)
                return VRAgentController.nullst("bel not found");
            if (beliefs.Count == 0)
                return VRAgentController.nullst("bel not found");
            Bel bel = beliefs[0];
            List<string> sbel = new List<string>();
            sbel.Add(bel.Name);
            if (bel.Args != null)
                for (int i = 0; i < bel.Args.Length; i++) {
                    sbel.Add(bel.Args[i]);
                }
            DateTime beltime = new DateTime(bel.Time);
            sbel.Add(beltime.ToString("s"));
            return VRAgentController.ok("bel found",sbel);
        }

        public List<string> RecallSingleBel(params string[] arglst)
        {
            List<Bel> beliefs = Agent.BelsBase.Search(arglst);
            if (beliefs == null)
                return VRAgentController.nullst("bel not found");
            if (beliefs.Count == 0 || beliefs.Count > 1)
                return VRAgentController.nullst("bel not found or not single");
            Bel bel = beliefs[0];
            List<string> sbel = new List<string>();
            sbel.Add(bel.Name);
            if (bel.Args != null)
                for (int i = 0; i < bel.Args.Length; i++) {
                    sbel.Add(bel.Args[i]);
                }
            DateTime beltime = new DateTime(bel.Time);
            sbel.Add(beltime.ToString("s"));
            return VRAgentController.ok("found single bel", sbel);
        }

        public bool RecallIfBel(params string[] arglst)
        {
            List<Bel> beliefs = Agent.BelsBase.Search(arglst);
            if (beliefs == null)
                return VRAgentController.fail("bel not found");
            if (beliefs.Count == 0)
                return VRAgentController.fail("bel not found");
            return VRAgentController.ok("bel found");
        }

        public bool RecallIfSingleBel(params string[] arglst)
        {
            List<Bel> beliefs = Agent.BelsBase.Search(arglst);
            if (beliefs == null)
                return VRAgentController.fail("bel not found");
            if (beliefs.Count == 0 || beliefs.Count > 1)
                return VRAgentController.fail("bel not found or not single");
            return VRAgentController.ok("found single bel");
        }

        public string RecallWhenBel(params string[] arglst)
        {
            List<Bel> beliefs = Agent.BelsBase.Search(arglst);
            if (beliefs == null)
                return VRAgentController.nulstr("bel not found");
            if (beliefs.Count == 0)
                return VRAgentController.nulstr("bel not found");
            DateTime datim = new DateTime(beliefs[0].Time);
            return VRAgentController.ok("bel found",datim.ToString("s"));
        }

        public string RecallWhenSingleBel(params string[] arglst)
        {
            List<Bel> beliefs = Agent.BelsBase.Search(arglst);
            if (beliefs == null)
                return VRAgentController.nulstr("bel not found");
            if (beliefs.Count == 0 || beliefs.Count > 1)
                return VRAgentController.nulstr("bel not found or not single");
            DateTime datim = new DateTime(beliefs[0].Time);
            return VRAgentController.ok("single bel found",datim.ToString("s"));
        }


        public List<List<string>> RecallBelsThat(params string[] arglst)
        {
            List<Bel> lbels = Agent.BelsBase.Search(arglst);
            List<List<string>> lsbels = new List<List<string>>();
            foreach (Bel bel in lbels) {
                List<string> sbel = new List<string>();
                sbel.Add(bel.Name);
                if (bel.Args != null)
                    for (int i = 0; i < bel.Args.Length; i++) {
                        sbel.Add(bel.Args[i]);
                    }
                DateTime beldatim = new DateTime(bel.Time);
                sbel.Add(beldatim.ToString("s"));
                lsbels.Add(sbel);
            }
            if (lsbels.Count > 0)
                VRAgentController.ok("found bels");
            else
                VRAgentController.fail("bels not found");
            return lsbels;
        }

        enum TimeTest{
            Before,
            BeforeOrAt,
            After,
            AfterOrAt
        }
        public List<List<string>> RecallBelsBefore(string argtime, params string[] arglst)
        {
            DateTime datim = DateTime.Parse(argtime);
            long time = datim.Ticks;
            return RecallBelsWithTimeTest(TimeTest.Before,time, arglst);
        }

        public List<List<string>> RecallBelsBeforeOrAt(string argtime, params string[] arglst)
        {
            DateTime datim = DateTime.Parse(argtime);
            VRAgentController.ok("recall bels before or at ok");
            long time = datim.Ticks;
            return RecallBelsWithTimeTest(TimeTest.BeforeOrAt, time, arglst);
        }

        public List<List<string>> RecallBelsAfter(string argtime, params string[] arglst)
        {
            DateTime datim = DateTime.Parse(argtime);
            VRAgentController.ok("recall bels after ok");
            long time = datim.Ticks;
            return RecallBelsWithTimeTest(TimeTest.After, time, arglst);
        }

        public List<List<string>> RecallBelsAfterOrAt(string argtime, params string[] arglst)
        {
            DateTime datim = DateTime.Parse(argtime);
            VRAgentController.ok("recall bels after or at ok");
            long time = datim.Ticks;
            return RecallBelsWithTimeTest(TimeTest.AfterOrAt, time, arglst);
        }

        public List<List<string>> RecallRecentBels(long argsecs, params string[] arglst)
        {
            long currtime = DateTime.Now.Ticks;
            VRAgentController.ok("recall recent bels ok");
            long time = currtime - argsecs*TimeSpan.TicksPerSecond;
            return RecallBelsWithTimeTest(TimeTest.AfterOrAt, time, arglst);
        }

        public List<List<string>> RecallPastBels(long argsecs, params string[] arglst)
        {
            long currtime = DateTime.Now.Ticks;
            VRAgentController.ok("recall past bels ok");
            long time = currtime - argsecs * TimeSpan.TicksPerSecond;
            return RecallBelsWithTimeTest(TimeTest.BeforeOrAt, time, arglst);
        }

        List<List<string>> RecallBelsWithTimeTest(TimeTest test, long time, params string[] arglst)
        {
            List<Bel> lbels = Agent.BelsBase.Search(arglst);
            List<List<string>> lsbels = new List<List<string>>();
            foreach (Bel bel in lbels) {
                switch(test) {
                    case TimeTest.Before: if (bel.Time >= time) continue;
                        break;
                    case TimeTest.BeforeOrAt: if (bel.Time > time) continue;
                        break;
                    case TimeTest.After: if (bel.Time <= time) continue;
                        break;
                    case TimeTest.AfterOrAt: if (bel.Time < time) continue;
                        break;
                }
                List<string> sbel = new List<string>();
                sbel.Add(bel.Name);
                if (bel.Args != null)
                    for (int i = 0; i < bel.Args.Length; i++) {
                        sbel.Add(bel.Args[i]);
                    }
                DateTime beldatim = new DateTime(bel.Time);
                sbel.Add(beldatim.ToString("s"));
                lsbels.Add(sbel);
            }
            if (lsbels.Count > 0)
                VRAgentController.ok("found bels");
            else
                VRAgentController.fail("bels not found");
            return lsbels;
        }

        public bool RecordBel(params string[] arglst)
        {
            if (!Agent.BelsBase.Add(arglst))
                return VRAgentController.ok("fail record bel");
            return VRAgentController.ok("record bel ok");
        }

        public bool RecordPerceptAsBel(Percept percept)
        {
            if  (!Agent.BelsBase.AddPercept(percept))
                return VRAgentController.fail("fail record percept");
            return VRAgentController.ok("record percept ok");
        }

        public bool ForgetBelsThat(params string[] arglst)
        {
            if (!Agent.BelsBase.Delete(arglst))
                return VRAgentController.fail("fail forget bels");
            return VRAgentController.ok("forget bels ok");
        }

        public bool ForgetAllBels()
        {
            if (!Agent.BelsBase.Clear())
                return VRAgentController.fail("fail forget all bels");
            return VRAgentController.ok("forget all bels ok");
        }
    }
}

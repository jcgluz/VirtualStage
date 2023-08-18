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
//   Class:     SystemActions 
//   Purpose:   This class implements system actions 
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
    public class SystemActions : Actions
    {
        public SystemActions(VRAgentController agent) : base(agent)
        {
        }

        public string get_last_fail_msg()
        {
            return VRAgentController.LastFailMsg;
        }
        public string get_last_ok_msg()
        {
            return VRAgentController.LastOKMsg;
        }
        public bool last_action_ok()
        {
            return VRAgentController.LastActionOK;
        }
        public List<string> GetPrimTypesAction()
        {
            List<string> results = new List<string>();
            foreach (string typeName in PrimTypes.Keys) {
                results.Add(typeName);
            }
            return VRAgentController.ok("get prim types",results);
        }

        public List<string> GetTreeTypesAction()
        {
            List<string> results = new List<string>();
            foreach (string typeName in TreeTypes.Keys) {
                results.Add(typeName);
            }
            return VRAgentController.ok("get tree types", results);
        }

        public List<string> GetGrassTypesAction()
        {
            List<string> results = new List<string>();
            foreach (string typeName in GrassTypes.Keys) {
                results.Add(typeName);
            }
            return VRAgentController.ok("get grass types", results);
        }

        public List<string> GetMatTypesAction()
        {
            List<string> results = new List<string>();
            foreach (string typeName in MatTypes.Keys) {
                results.Add(typeName);
            }
            return VRAgentController.ok("get material types", results);
        }

        public List<string> GetAttachPointsAction()
        {
            List<string> results = new List<string>();
            foreach (string attPointName in AttachPoints.Keys) {
                results.Add(attPointName);
            }
            return VRAgentController.ok("get attachment points", results);
        }

        public List<string> GetMsgCodesAction()
        {
            List<string> results = new List<string>();
            foreach (string typeName in IMsgTypes.Keys) {
                results.Add(typeName);
            }
            return VRAgentController.ok("get msg codes", results);
        }

        public List<string> GetStdAnimsAction()
        {
            List<string> results = new List<string>();
            foreach (string animName in StdAnimations.Values) {
                results.Add( animName.ToLower());
            }
            return VRAgentController.ok("get std anims", results);
        }


        public bool SetLogLevelAction(string arglevel)
        {
            Console.WriteLine("arglevel=" + arglevel);
            if (arglevel.ToLower() == "debug") {
                Settings.LOG_LEVEL = Helpers.LogLevel.Debug;
                return VRAgentController.ok("DEBUG logging level");
            } else if (arglevel.ToLower() == "none") {
                Settings.LOG_LEVEL = Helpers.LogLevel.None;
                return VRAgentController.ok("not logging");
            } else if (arglevel.ToLower() == "warn") {
                Settings.LOG_LEVEL = Helpers.LogLevel.Warning;
                return VRAgentController.ok("WARN logging level)");
            } else if (arglevel.ToLower() == "info") {
                Settings.LOG_LEVEL = Helpers.LogLevel.Info;
                return VRAgentController.ok("INFO logging level");
            } else if (arglevel.ToLower() == "error") {
                Settings.LOG_LEVEL = Helpers.LogLevel.Error;
                return VRAgentController.ok("ERROR logging level");
            } else {
                return VRAgentController.fail("invalid log level option");
            }
        }

        uint SleepSerialNum = 1;
        uint LastSleepSerialNum = 0;

        public bool PauseAction(string argstartstop)
        {
            if (argstartstop.ToLower() == "start") {
                if (LastSleepSerialNum > 0)
                    return VRAgentController.fail("already paused");
                AgentPausePacket pause = new AgentPausePacket();
                pause.AgentData.AgentID = Agent.Self.AgentID;
                pause.AgentData.SessionID = Agent.Self.SessionID;
                LastSleepSerialNum = SleepSerialNum;
                pause.AgentData.SerialNum = SleepSerialNum++;
                Agent.Network.SendPacket(pause);
                return VRAgentController.ok("starting pause)");
            } else if (argstartstop.ToLower() == "start") {
                if (LastSleepSerialNum == 0)
                    return VRAgentController.fail("already stopped");
                AgentResumePacket resume = new AgentResumePacket();
                resume.AgentData.AgentID = Agent.Self.AgentID;
                resume.AgentData.SessionID = Agent.Self.SessionID;
                resume.AgentData.SerialNum = LastSleepSerialNum;
                LastSleepSerialNum = 0;
                Agent.Network.SendPacket(resume);
                return VRAgentController.ok("stopping pause");
            } else {
                return (VRAgentController.fail("invalid option"));
            }
        }


    }
}

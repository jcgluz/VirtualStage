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
//   Class:     VRAgentManager 
//   Purpose:   Singleton class that creates and manages new VR agents.
//              It implements the login process of VR agents and its
//              corresponding avatars into OpenSimulator VR worlds, creating
//              a new agent controller and associating this agent with the
//              avatar recently logged in the virtual world. It provides
//              access to the agent controllers of previously logged agents.
//   Author:    João Carlos Gluz 
//
//***********************************************************************

using System;
using System.Collections.Generic;
using System.Reflection;
using System.Xml;
using System.Threading;
using System.Globalization;
using System.Diagnostics;
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
    public class LoginDetails
    {
        public string FirstName;
        public string LastName;
        public string Password;
        public string StartLocation;
        public string URI;
    }

    public class StartPosition
    {
        public string sim;
        public int x;
        public int y;
        public int z;

        public StartPosition()
        {
            this.sim = null;
            this.x = 0;
            this.y = 0;
            this.z = 0;
        }
    }

    public sealed class VRAgentManager
    {
        const string VERSION = "0.7.0";

        class Singleton {
            internal static readonly VRAgentManager Instance = new VRAgentManager();
        }
        public static VRAgentManager Instance { get { return Singleton.Instance; } }
        public Dictionary<UUID, VRAgentController> Agents = new Dictionary<UUID, VRAgentController>();
        public Dictionary<Simulator, Dictionary<uint, Primitive>> Regions = 
                new Dictionary<Simulator, Dictionary<uint, Primitive>>();
        public bool GetTextures = false;
        public volatile int PendingLogins = 0;
        public string onlyAvatar = String.Empty;

        public VRAgentManager()
        {
        }

        public VRAgentController Login(string[] args)
        {
            if (args.Length < 4)  {
                Console.WriteLine("login syntax error - usage: login firstname lastname password url [simname] [x y z]");
                return null;
            }
            CultureInfo culture;
            culture = CultureInfo.CreateSpecificCulture("en-US");
            CultureInfo.DefaultThreadCurrentCulture = culture;
            Thread.CurrentThread.CurrentCulture = culture;
            LoginDetails account = new LoginDetails();
            account.FirstName = args[0];
            account.LastName = args[1];
            account.Password = args[2];
            account.URI = args[3];
            if (args.Length == 4) {
                // No starting pos or region was given, use last position 
                account.StartLocation = "last";
            } else if (args.Length == 5) {
                // No full starting pos was given, except for the name of the region,
                // use the center of the named region 
                account.StartLocation = NetworkManager.StartLocation(args[4], 128, 128, 40);
            } else {
                // If it looks like a full starting position was specified, try to parse it
                try {
                    account.StartLocation = NetworkManager.StartLocation(args[4], Int32.Parse(args[5]),
                                                Int32.Parse(args[6]), Int32.Parse(args[7]));
                } catch (FormatException) {
                    account.StartLocation = "last";
                }
            }

            Logger.Log("Using login URI " + account.URI, Helpers.LogLevel.Info);

            return Login(account);
        }

        public VRAgentController Login(LoginDetails account)
        {
            // Check if this agent is already logged in
            foreach (VRAgentController ag in Agents.Values)
            {
                if (ag.Self.FirstName == account.FirstName && 
                    ag.Self.LastName == account.LastName)  {
                    Logout(ag);
                    break;
                }
            }
            ++PendingLogins;
            VRAgentController agent = new VRAgentController(this);
            agent.Network.LoginProgress +=
                delegate(object sender, LoginProgressEventArgs e)
                {
                   Logger.Log(String.Format("Login {0}: {1}", e.Status, e.Message), Helpers.LogLevel.Info, agent);
                    if (e.Status == LoginStatus.Success) {
                        Agents[agent.Self.AgentID] = agent;
                        Logger.Log("Logged in " + agent.ToString(), Helpers.LogLevel.Info);
                        --PendingLogins;
                    }  else if (e.Status == LoginStatus.Failed) {
                        Logger.Log("Failed to login " + account.FirstName + " " + account.LastName + ": " +
                                    agent.Network.LoginMessage, Helpers.LogLevel.Warning);
                        --PendingLogins;
                    }
                };
            // Optimize the throttle
           	agent.Throttle.Wind = 0;
            agent.Throttle.Cloud = 0;
            agent.Throttle.Land = 1000000;
            agent.Throttle.Task = 1000000;
           LoginParams loginParams = agent.Network.DefaultLoginParams(
                    account.FirstName, account.LastName, 
                    account.Password, "LibreVRAgent", VERSION);
            if (!String.IsNullOrEmpty(account.StartLocation))
                loginParams.Start = account.StartLocation;
            if (!String.IsNullOrEmpty(account.URI))
                loginParams.URI = account.URI;
          	agent.Network.BeginLogin(loginParams);
			while (PendingLogins>0)
				Thread.Sleep(50);
            return agent;
        }

        public void Logout(VRAgentController agent)
        {
            agent.Network.Logout();
            Agents.Remove(agent.Self.AgentID);
        }

        // External Interface called by Python/Prolog
        //-------------------------------------------

        public string vragent_login(string[] args)
        {
            VRAgentController agent = Login(args);
            return agent.Self.AgentID.ToString();
        }

        public string vragent_logout(string agid)
        {
            VRAgentController agent = get_vragent_controller(agid); if (agent == null) return "error(no_agent)";
            Logout(agent);
            return "VRAgent.ok(logged_out)";
        }

        public VRAgentController get_vragent_controller(string agid)
        {
            UUID agUUID;
            VRAgentController agent;
            if (!UUID.TryParse(agid, out agUUID))
                return null;
            try {
                agent = Agents[agUUID];
            } catch (Exception e) {
                return null;
            }
            return agent;
        }



        // Test Actions
        //-------------

        public string echotest1(string cmd)
        {
            return cmd;
        }

        public string[] echotest2(string cmd, string[] args)
        {
            string[] echo = new string[args.Length + 1];
            echo[0] = cmd;
            if (args.Length > 0)
                Array.Copy(args, 0, echo, 1, args.Length);
            return echo;
        }

        public List<String> echotest3(string cmd, List<String> args)
        {
            List<String> echo = new List<String>();
            echo.Add(cmd);
            echo.AddRange(args);
            return echo;
        }

        public List<String> echotest4(string cmd, params string[] args)
        {
            List<String> echo = new List<String>();
            echo.Add(cmd);
            echo.AddRange(args);
            return echo;
        }

        public string test1(string arg1, string[] arg2)
        {
            string result = "";
            result += "[arg1: ";
            if (arg1 == null)
                result += "is null string; ";
            else if (arg1 == "")
                result += "is empty string;";
            else
                result += arg1 + "; ";
            result += "arg2: ";
            if (arg2 == null)
                result += "is null array; ";
            else if (arg2.Length==0)
                result += "is empty array; ";
            else {
                result += "[ ";
                bool first = true;
                foreach (string s in arg2)
                    if (first)
                        result += s;
                    else
                        result += ", " + s;
                result += "]]";
            }
            return result;
        }

        public string test_console(string arg1, string[] arg2)
        {
            Console.WriteLine("Console test:");
            
            if (arg1 == null)
                Console.WriteLine("arg1: is null string; ");
            else if (arg1 == "")
                Console.WriteLine("arg1: is empty string;");
            else
                Console.WriteLine("arg1: " +arg1 + "; ");
            if (arg2 == null)
                Console.WriteLine("arg2: is null array; ");
            else if (arg1.Length==0)
                Console.WriteLine("arg2: is empty array;");
            else {
                Console.WriteLine("arg2: ");
                bool first = true;
                foreach (string s in arg2)
                    if (first)
                        Console.WriteLine(s);
                    else
                        Console.WriteLine(", " + s);
            }
            return "ok";
        }


    }
}

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
//   Class:     PositionActions 
//   Purpose:   To implement actions for the agent to be able to modify
//              the positioning and rotation of its avatar on virtual world 
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
    public class PositionActions : Actions
    {
        public PositionActions(VRAgentController agent) : base(agent)
        {
            beamTimer = new System.Timers.Timer { Enabled = false };
            beamTimer.Elapsed += new System.Timers.ElapsedEventHandler(beamTimeElapsedHandler);
        }

        public bool SitAction()
        {
            Primitive closest = null;
            double closestDistance = Double.MaxValue;
            Agent.Network.CurrentSim.ObjectsPrimitives.ForEach(
                delegate (Primitive prim) {
                    float distance = Vector3.Distance(Agent.Self.SimPosition, prim.Position);
                    if (closest == null || distance < closestDistance) {
                        closest = prim;
                        closestDistance = distance;
                    }
                }
            );
            if (closest != null) {
                Agent.Self.RequestSit(closest.ID, Vector3.Zero);
                Agent.Self.Sit();
                return VRAgentController.ok("sitting)");
            } else {
                return VRAgentController.fail("unable to sit");
            }
        }

        public bool SitOnAction(string argtarget)
        {
            UUID target;
            if (UUID.TryParse(argtarget, out target)) {
                Primitive targetPrim = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim) {
                        return prim.ID == target;
                    }
                );
                if (targetPrim != null) {
                    Agent.Self.RequestSit(targetPrim.ID, Vector3.Zero);
                    Agent.Self.Sit();
                    return VRAgentController.ok("sitting on obj");
                }
            }
            return VRAgentController.fail("not found");
        }

        public bool StandAction()
        {
            Agent.Self.Stand();
            return VRAgentController.ok("standing up");
        }

        public bool CrouchAction(string argopt)
        {
            if (argopt.ToLower() == "stop") {
                Agent.Self.Crouch(false);
                return VRAgentController.ok("stop crouching");
            } else if (argopt == "start") {
                Agent.Self.Crouch(true);
                return VRAgentController.ok("start crouching");
            } else {
                return VRAgentController.fail("invalid option");
            }
        }

        public bool JumpAction(string argstartstop)
        {
            if (argstartstop == "stop") {
                Agent.Self.Jump(false);
                return VRAgentController.ok("stop jumping");
            } else if (argstartstop == "start") {
                Agent.Self.Jump(true);
                return VRAgentController.ok("start jumping");
            } else {
                return VRAgentController.fail("invalid option");
            }

        }

        public bool TurnToRelDirAction(double argdir, string argunit)
        {
            double headingdir;
            if (argunit.ToLower() == "rad") {
                headingdir = argdir;
            } else if (argunit.ToLower()=="dg") {
                headingdir = (argdir / 180.0d) * Math.PI;
            } else {
                return VRAgentController.fail("param 2 error");
            }
            Agent.Self.Movement.UpdateFromRelativeHeading(headingdir, false);
            Agent.Self.Movement.SendUpdate(false);
            return VRAgentController.ok("turning");
        }

        public bool TurnToAbsDirAction(double argdir, string argunit)
        {
            double headingdir;
            if (argunit.ToLower() == "rad") {
                headingdir = argdir;
            } else if (argunit.ToLower() == "dg") {
                headingdir = (argdir / 180.0d) * Math.PI;
            } else {
                return VRAgentController.fail("param 2 error");
            }
            Agent.Self.Movement.UpdateFromHeading(headingdir, false);
            Agent.Self.Movement.SendUpdate(false);
            return VRAgentController.ok("turning");
        }

        public bool TurnToNamedDirAction(string argopt)
        {
            if (argopt.ToLower().Equals("east")) {
                return TurnToAbsDirAction(0.0d, "dg");
            } else if (argopt.ToLower().Equals("west")) {
                return TurnToAbsDirAction(180.0d, "dg");
            } else if (argopt.ToLower().Equals("north")) {
                return TurnToAbsDirAction(90.0d, "dg");
            } else if (argopt.ToLower().Equals("south")) {
                return TurnToAbsDirAction(270.0d, "dg");
            } else if (argopt.ToLower().Equals("left")) {
                return TurnToRelDirAction(-90.0d, "dg");
            } else if (argopt.ToLower().Equals("right")) {
                return TurnToRelDirAction(90.0d, "dg");
            } else {
                return VRAgentController.fail("invalid option");
            }
        }

        public bool RotateTowardAction(float argx, float argy, float argz)
        {
            Agent.Self.Movement.RotateToward(argx, argy, argz);
            Agent.Self.Movement.SendUpdate(false);
            return VRAgentController.ok("rotating");
        }

        public bool TurnToPosAction(float x, float y, float z)
        {
            Vector3 newDirection;
            newDirection.X = x;
            newDirection.Y = y;
            newDirection.Z = z;
            Agent.Self.Movement.TurnToward(newDirection);
            Agent.Self.Movement.SendUpdate(false);
            return VRAgentController.ok("turning to pos");
        }
        public bool TurnToObjAction(string objid)
        {
            UUID primID;
            Primitive p=null;
            if (UUID.TryParse(objid, out primID)) {
                p = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                        delegate (Primitive prim) { return prim.ID == primID; }
                );
            }
            if (p==null)
                return VRAgentController.fail("param 1 error");
            Agent.Self.Movement.TurnToward(p.Position);
            Agent.Self.Movement.SendUpdate(false);
            return VRAgentController.ok("turning to obj");
        }

        public bool TurnToAvatarAction(string avidname)
        {
            UUID avID;
            Avatar av;
            if (UUID.TryParse(avidname, out avID)) {
                av = Agent.Network.CurrentSim.ObjectsAvatars.Find(
                    delegate (Avatar avatar) { return avatar.ID == avID; }
                );
            } else {
                av = Agent.Network.CurrentSim.ObjectsAvatars.Find(
                    delegate (Avatar avatar) { return (avatar.Name == avidname); }
                );
            }
            if (av == null)
                return VRAgentController.fail("param 1 error");
            Agent.Self.Movement.TurnToward(av.Position);
            Agent.Self.Movement.SendUpdate(false);
            return VRAgentController.ok("turning to avatar");
        }

        public bool TurningToAction(string argopt)
        {
            if (argopt.ToLower().Equals("left")) {
                Agent.Self.Movement.TurnLeft = true;
                Agent.Self.Movement.SendUpdate(false);
                return VRAgentController.ok("turning to left");
            } else if (argopt.ToLower().Equals("right")) {
                Agent.Self.Movement.TurnRight = true;
                Agent.Self.Movement.SendUpdate(false);
                return VRAgentController.ok("turning to right");
            } else if (argopt.ToLower().Equals("stop")) {
                Agent.Self.Movement.TurnLeft = false;
                Agent.Self.Movement.TurnRight = false;
                Agent.Self.Movement.SendUpdate(false);
                return VRAgentController.ok("turning stop");
            } else {
                return VRAgentController.fail("invalid option");
            }
        }

        public static Vector3d GlobalPosition(Simulator sim, Vector3 pos)
        {
            uint globalX, globalY;
            Utils.LongToUInts(sim.Handle, out globalX, out globalY);
            return new Vector3d(
                (double)globalX + (double)pos.X,
                (double)globalY + (double)pos.Y,
                (double)pos.Z);
        }

        public Vector3d GlobalPosition(Primitive prim)
        {
            return GlobalPosition(Agent.Network.CurrentSim, prim.Position);
        }

        private System.Timers.Timer beamTimer;
        private List<Vector3d> beamTarget;
        private Random beamRandom = new Random();
        private UUID pointID;
        private UUID sphereID;
        private List<UUID> beamID;
        private int numBeans;
        private Color4[] beamColors = new Color4[] { new Color4(0, 255, 0, 255), new Color4(255, 0, 0, 255), new Color4(0, 0, 255, 255) };
        private Primitive targetPrim;

        public void UnSetPointing()
        {
            beamTimer.Enabled = false;
            if (pointID != UUID.Zero) {
                Agent.Self.PointAtEffect(Agent.Self.AgentID, UUID.Zero, 
                                    Vector3d.Zero, PointAtType.None, pointID);
                pointID = UUID.Zero;
            }
            if (beamID != null) {
                foreach (UUID id in beamID) {
                    Agent.Self.BeamEffect(UUID.Zero, UUID.Zero, Vector3d.Zero, 
                                    new Color4(255, 255, 255, 255), 0, id);
                }
                beamID = null;
            }
            if (sphereID != UUID.Zero) {
                Agent.Self.SphereEffect(Vector3d.Zero, Color4.White, 0, sphereID);
                sphereID = UUID.Zero;
            }

        }

        void beamTimeElapsedHandler(object sender, EventArgs e)
        {
            if (beamID == null) return;
            try {
                Agent.Self.SphereEffect(GlobalPosition(targetPrim), beamColors[beamRandom.Next(0, 3)], 0.85f, sphereID);
                int i = 0;
                for (i = 0; i < numBeans; i++) {
                    Vector3d scatter;
                    if (i == 0) {
                        scatter = GlobalPosition(targetPrim);
                    } else {
                        Vector3d direction = Agent.Self.GlobalPosition - GlobalPosition(targetPrim);
                        Vector3d cross = direction % new Vector3d(0, 0, 1);
                        cross.Normalize();
                        scatter = GlobalPosition(targetPrim) + cross * (i * 0.2d) * (i % 2 == 0 ? 1 : -1);
                    }
                    Agent.Self.BeamEffect(Agent.Self.AgentID, UUID.Zero, scatter, 
                                beamColors[beamRandom.Next(0, 3)], 1.0f, beamID[i]);
                }

                for (int j = 1; j < numBeans; j++) {
                    Vector3d cross = new Vector3d(0, 0, 1);
                    cross.Normalize();
                    var scatter = GlobalPosition(targetPrim) + cross * (j * 0.2d) * (j % 2 == 0 ? 1 : -1);

                    Agent.Self.BeamEffect(Agent.Self.AgentID, UUID.Zero, scatter, beamColors[beamRandom.Next(0, 3)], 1.0f, beamID[j + i - 1]);
                }
            }
            catch (Exception) { }

        }

        public bool StopPointingAction()
        {
            UnSetPointing();
            return VRAgentController.ok("stop pointing at obj");
        }

        public bool PointAtObjAction(string objid)
        {
            return PointAtObjAction(objid, 5);
        }

        public bool PointAtObjAction(string objid, int num_beans)
        {
            UUID primID;
            Primitive p = null;
            if (UUID.TryParse(objid, out primID)) {
                p = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                        delegate (Primitive prim) { return prim.ID == primID; }
                );
            }
            if (p == null)
                return VRAgentController.fail("param 1 error");
            Agent.Self.Movement.TurnToward(p.Position);
            Agent.Self.Movement.SendUpdate(false);
            UnSetPointing();
            pointID = UUID.Random();
            sphereID = UUID.Random();
            beamID = new List<UUID>();
            beamTarget = new List<Vector3d>();
            targetPrim = p;
            numBeans = num_beans;
            Agent.Self.PointAtEffect(Agent.Self.AgentID, p.ID, 
                        Vector3d.Zero, PointAtType.Select, pointID);
            for (int i = 0; i < numBeans; i++) {
                UUID newBeam = UUID.Random();
                beamID.Add(newBeam);
                beamTarget.Add(Vector3d.Zero);
            }
            for (int i = 1; i < numBeans; i++) {
                UUID newBeam = UUID.Random();
                beamID.Add(newBeam);
                beamTarget.Add(Vector3d.Zero);
            }
            beamTimer.Interval = 1000;
            beamTimer.Enabled = true;
            return VRAgentController.ok("pointing at obj");
        }



    }
}

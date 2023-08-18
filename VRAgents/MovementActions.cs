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
//   Class:     MovementActions 
//   Purpose:   To implement actions for the agent to be able to move its
//              avatar on virtual world 
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
    public class MovementActions : Actions
    {

        public MovementActions(VRAgentController agent) : base(agent)
        {
            agent.Network.RegisterCallback(PacketType.AlertMessage, AlertMessageHandler);
        }

        public bool ForwardAction()
        {
            Agent.Self.Movement.SendManualUpdate(
                    AgentManager.ControlFlags.AGENT_CONTROL_AT_POS,
                    Agent.Self.Movement.Camera.Position,
                    Agent.Self.Movement.Camera.AtAxis,
                    Agent.Self.Movement.Camera.LeftAxis,
                    Agent.Self.Movement.Camera.UpAxis,
                    Agent.Self.Movement.BodyRotation,
                    Agent.Self.Movement.HeadRotation,
                    Agent.Self.Movement.Camera.Far,
                    AgentFlags.None,
                    AgentState.None, true);
            return VRAgentController.ok("moving forward");
        }

        public bool ForwardAction(float argval, string argunit)
        {
            int val = (int)(argval);
            return ForwardAction(val, argunit);
        }

        public bool ForwardAction(string argval, string argunit)
        {
            int val = int.Parse(argval);
            return ForwardAction(val, argunit);
        }

        public bool ForwardAction(int argval, string argunit)
        {
            if (argunit.Trim().ToLower().Equals("sec")) {
                // Convert to milliseconds
                int duration = argval * 1000;
                int start = Environment.TickCount;
                Agent.Self.Movement.AtPos = true;
                while (Environment.TickCount - start < duration) {
                    // The movement timer will do this automatically, but we do it here as an example
                    // and to make sure updates are being sent out fast enough
                    Agent.Self.Movement.SendUpdate(false);
                    System.Threading.Thread.Sleep(100);
                }
                Agent.Self.Movement.AtPos = false;
            } else if (argunit.Trim().ToLower().Equals("mt")) {
                // Distance is in meters
                int distance = argval;
                if (distance < 1)
                    return VRAgentController.fail("param 1 error");
                Quaternion heading = Agent.Self.Movement.BodyRotation;
                Vector3 targetPos = Vector3.Zero;
                targetPos = Agent.Self.SimPosition + new Vector3((float)distance, 0f, 0f) * heading;
                uint regionX, regionY;
                Utils.LongToUInts(Agent.Network.CurrentSim.Handle, out regionX, out regionY);
                // Convert the local coordinates to global ones by adding the region handle parts to x and y
                double global_target_x = (double)targetPos.X + (double)regionX;
                double global_target_y = (double)targetPos.Y + (double)regionY;
                float target_z;
                Agent.Network.CurrentSim.TerrainHeightAtPoint((int)targetPos.X,
                                                    (int)targetPos.Y, out target_z);
                Agent.Self.AutoPilot(global_target_x, global_target_y, (double)target_z);
                return VRAgentController.ok("moving forward");
            } else {
                return VRAgentController.fail("param 2 error");
            }

            return VRAgentController.ok("moving forward");
        }

        public bool BackwardAction()
        {
            Agent.Self.Movement.SendManualUpdate(
                AgentManager.ControlFlags.AGENT_CONTROL_AT_NEG,
                Agent.Self.Movement.Camera.Position,
                Agent.Self.Movement.Camera.AtAxis,
                Agent.Self.Movement.Camera.LeftAxis,
                Agent.Self.Movement.Camera.UpAxis,
                Agent.Self.Movement.BodyRotation,
                Agent.Self.Movement.HeadRotation,
                Agent.Self.Movement.Camera.Far,
                AgentFlags.None,
                AgentState.None, true);
            return VRAgentController.ok("moving back");
        }

        public bool BackwardAction(float argval, string argunit)
        {
            int val = (int)(argval);
            return BackwardAction(val, argunit);
        }

        public bool BackwardAction(string argval, string argunit)
        {
            int val = int.Parse(argval);
            return BackwardAction(val, argunit);
        }

        public bool BackwardAction(int argval, string argunit)
        {
            if (argunit.Trim().ToLower().Equals("sec")) {
                // Convert to milliseconds
                int duration = argval * 1000;
                int start = Environment.TickCount;
                Agent.Self.Movement.AtNeg = true;
                while (Environment.TickCount - start < duration) {
                    // The movement timer will do this automatically, but we do it here as an example
                    // and to make sure updates are being sent out fast enough
                    Agent.Self.Movement.SendUpdate(false);
                    System.Threading.Thread.Sleep(100);
                }
                Agent.Self.Movement.AtNeg = false;
            } else if (argunit.Trim().ToLower().Equals("mt")) {
                // Distance in meters
                int distance = argval;
                if (distance < 1)
                    return VRAgentController.fail("param 1 error");
                Quaternion heading = Agent.Self.Movement.BodyRotation;
                Vector3 targetPos = Vector3.Zero;
                targetPos = Agent.Self.SimPosition + new Vector3((float)-distance, 0f, 0f) * heading;
                uint regionX, regionY;
                Utils.LongToUInts(Agent.Network.CurrentSim.Handle, out regionX, out regionY);
                // Convert the local coordinates to global ones by adding the region handle parts to x and y
                double global_target_x = (double)targetPos.X + (double)regionX;
                double global_target_y = (double)targetPos.Y + (double)regionY;
                float target_z;
                Agent.Network.CurrentSim.TerrainHeightAtPoint(
                    (int)targetPos.X, (int)targetPos.Y, out target_z);
                Agent.Self.AutoPilot(
                    global_target_x, global_target_y, (double)target_z);
                return VRAgentController.ok("moving back");
            } else {
                return VRAgentController.fail("param 2 error");
            }
            return VRAgentController.ok("moving back");
        }

        public bool LeftwardAction()
        {
            Agent.Self.Movement.SendManualUpdate(
                AgentManager.ControlFlags.AGENT_CONTROL_LEFT_POS,
                Agent.Self.Movement.Camera.Position,
                Agent.Self.Movement.Camera.AtAxis,
                Agent.Self.Movement.Camera.LeftAxis,
                Agent.Self.Movement.Camera.UpAxis,
                Agent.Self.Movement.BodyRotation,
                Agent.Self.Movement.HeadRotation,
                Agent.Self.Movement.Camera.Far,
                AgentFlags.None,
                AgentState.None, true);
            return VRAgentController.ok("moving left");
        }

        public bool LeftwardAction(float argval, string argunit)
        {
            int val = (int)(argval);
            return LeftwardAction(val, argunit);
        }

        public bool LeftwardAction(string argval, string argunit)
        {
            int val = int.Parse(argval);
            return LeftwardAction(val, argunit);
        }

        public bool LeftwardAction(int argval, string argunit)
        {
            // Only work with duration
            if (!argunit.Trim().ToLower().Equals("sec"))
                return VRAgentController.fail("param 2 only sec allowed");
            // Convert to milliseconds
            int duration = argval * 1000;
            int start = Environment.TickCount;
            Agent.Self.Movement.LeftPos = true;
            while (Environment.TickCount - start < duration) {
                // The movement timer will do this automatically, but we do it here as an example
                // and to make sure updates are being sent out fast enough
                Agent.Self.Movement.SendUpdate(false);
                System.Threading.Thread.Sleep(100);
            }
            Agent.Self.Movement.LeftPos = false;
            return VRAgentController.ok("moving left");
        }

        public bool RightwardAction()
        {
            Agent.Self.Movement.SendManualUpdate(
                AgentManager.ControlFlags.AGENT_CONTROL_LEFT_NEG,
                Agent.Self.Movement.Camera.Position,
                Agent.Self.Movement.Camera.AtAxis,
                Agent.Self.Movement.Camera.LeftAxis,
                Agent.Self.Movement.Camera.UpAxis,
                Agent.Self.Movement.BodyRotation,
                Agent.Self.Movement.HeadRotation,
                Agent.Self.Movement.Camera.Far,
                AgentFlags.None,
                AgentState.None, true);
            return VRAgentController.ok("moving right");
        }

        public bool RightwardAction(float argval, string argunit)
        {
            int val = (int)(argval);
            return RightwardAction(val, argunit);
        }

        public bool RightwardAction(string argval, string argunit)
        {
            int val = int.Parse(argval);
            return RightwardAction(val, argunit);
        }

        public bool RightwardAction(int argval, string argunit)
        {
            // Only work with duration
            if (!argunit.Trim().ToLower().Equals("sec"))
                return VRAgentController.fail("param 2 only sec allowed");
            // Convert to milliseconds
            int duration = argval * 1000;
            int start = Environment.TickCount;
            Agent.Self.Movement.LeftNeg = true;
            while (Environment.TickCount - start < duration) {
                // The movement timer will do this automatically, but we do it here as an example
                // and to make sure updates are being sent out fast enough
                Agent.Self.Movement.SendUpdate(false);
                System.Threading.Thread.Sleep(100);
            }
            Agent.Self.Movement.LeftNeg = false;
            return VRAgentController.ok("moving right");
        }

        public bool FlyAction(string argstartstop)
        {
            if (argstartstop.ToLower() == "stop") {
                Agent.Self.Fly(false);
                return VRAgentController.ok("stop flying");
            } else if (argstartstop.ToLower() == "start") {
                Agent.Self.Fly(true);
                return VRAgentController.ok("start flying");
            } else {
                return VRAgentController.fail("invalid option");
            }
        }

        Vector3 MyFlyPos = new Vector3();
        Vector2 MyFlyPos0 = new Vector2();
        Vector3 FlyTarget = new Vector3();
        Vector2 FlyTarget0 = new Vector2();
        float FlyDiff, OldFlyDiff, SaveOldFlyDiff;
        int StartFlyTime = 0;
        int FlyDuration = 20000;   // default max time of flying: 20 seconds
        bool IsFlying = false;

        /// <summary>
        /// Fly the avatar toward the specified position x,y,z for a maximum 
        /// of seconds/miliseconds
        /// </summary>
        /// <param name="x"> X coordinate to fly to</param>
        /// <param name="y"> Y coordinate to fly to</param>
        /// <param name="z"> Z coordinate to fly to</param>
        /// <param name="maxtim"> max flying time (in seconds/ms)</param>
        /// <param name="unit"> "sec" | "ms"</param>
        public bool FlyToAction(int argx, int argy, int argz, int maxtim, string unit)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            float z = (float)(argz);
            return FlyToAction(x, y, z, maxtim, unit);
        }

        public bool FlyToAction(string argx, string argy, string argz, int maxtim, string unit)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            float z = float.Parse(argz);
            return FlyToAction(x, y, z, maxtim, unit);
        }

        public bool FlyToAction(string argx, string argy, string argz, 
                                string argmaxtim, string unit)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            float z = float.Parse(argz);
            int maxtim = int.Parse(argmaxtim);
            return FlyToAction(x, y, z, maxtim, unit);
        }

        public bool FlyToAction(float x, float y, float z,
                                    int maxtim, string unit)
        {
            FlyTarget.X = x;
            FlyTarget.Y = y;
            FlyTarget.Z = z;
            if (IsFlying)
                return VRAgentController.ok("already flying");
            IsFlying = true;
            // Subscribe to terse update events while this agent is flying
            Agent.Objects.TerseObjectUpdate += ReceiveObjectUpdated;
            FlyTarget0.X = FlyTarget.X;
            FlyTarget0.Y = FlyTarget.Y;
            // Check if max time was defined
            if (maxtim > 0) {
                if (unit.ToLower() == "sec")
                    // Convert to milisseconds
                    FlyDuration = maxtim * 1000;
                else if (unit.ToLower() == "ms")
                    // Max value already in milisseconds
                    FlyDuration = maxtim;
                else
                    return VRAgentController.fail("last param invalid option");
            }
            StartFlyTime = Environment.TickCount;
            Agent.Self.Movement.Fly = true;
            Agent.Self.Movement.AtPos = true;
            Agent.Self.Movement.AtNeg = false;
            ZMovement();
            Agent.Self.Movement.TurnToward(FlyTarget);

            return VRAgentController.ok("start flying to");
        }

        private void ReceiveObjectUpdated(object sender, TerseObjectUpdateEventArgs e)
        {
            if (StartFlyTime == 0) return;
            if (e.Update.LocalID == Agent.Self.LocalID) {
                XYMovement();
                ZMovement();
                if (Agent.Self.Movement.AtPos || Agent.Self.Movement.AtNeg) {
                    Agent.Self.Movement.TurnToward(FlyTarget);
                    FlyDebug("Flyxy ");
                } else if (Agent.Self.Movement.UpPos || Agent.Self.Movement.UpNeg) {
                    Agent.Self.Movement.TurnToward(FlyTarget);
                    //Client.Self.Movement.SendUpdate(false);
                    FlyDebug("Fly z ");
                } else if (Vector3.Distance(FlyTarget, Agent.Self.SimPosition) <= 2.0) {
                    EndFlyto();
                    FlyDebug("At Target");
                }
            }
            if (Environment.TickCount - StartFlyTime > FlyDuration) {
                EndFlyto();
                FlyDebug("End Flyto");
            }
        }

        private bool XYMovement()
        {
            bool res = false;

            MyFlyPos = Agent.Self.SimPosition;
            MyFlyPos0.X = MyFlyPos.X;
            MyFlyPos0.Y = MyFlyPos.Y;
            FlyDiff = Vector2.Distance(FlyTarget0, MyFlyPos0);
            Vector2 vvel = new Vector2(Agent.Self.Velocity.X, Agent.Self.Velocity.Y);
            float vel = vvel.Length();
            if (FlyDiff >= 10.0) {
                Agent.Self.Movement.AtPos = true;

                res = true;
            } else if (FlyDiff >= 2 && vel < 5) {
                Agent.Self.Movement.AtPos = true;
            } else {
                Agent.Self.Movement.AtPos = false;
                Agent.Self.Movement.AtNeg = false;
            }
            SaveOldFlyDiff = OldFlyDiff;
            OldFlyDiff = FlyDiff;
            return res;
        }

        private void ZMovement()
        {
            Agent.Self.Movement.UpPos = false;
            Agent.Self.Movement.UpNeg = false;
            float diffz = (FlyTarget.Z - Agent.Self.SimPosition.Z);
            if (diffz >= 20.0)
                Agent.Self.Movement.UpPos = true;
            else if (diffz <= -20.0)
                Agent.Self.Movement.UpNeg = true;
            else if (diffz >= +5.0 && Agent.Self.Velocity.Z < +4.0)
                Agent.Self.Movement.UpPos = true;
            else if (diffz <= -5.0 && Agent.Self.Velocity.Z > -4.0)
                Agent.Self.Movement.UpNeg = true;
            else if (diffz >= +2.0 && Agent.Self.Velocity.Z < +1.0)
                Agent.Self.Movement.UpPos = true;
            else if (diffz <= -2.0 && Agent.Self.Velocity.Z > -1.0)
                Agent.Self.Movement.UpNeg = true;
        }

        private void EndFlyto()
        {
            // Unsubscribe from terse update events
            Agent.Objects.TerseObjectUpdate -= ReceiveObjectUpdated;

            StartFlyTime = 0;
            Agent.Self.Movement.AtPos = false;
            Agent.Self.Movement.AtNeg = false;
            Agent.Self.Movement.UpPos = false;
            Agent.Self.Movement.UpNeg = false;
            Agent.Self.Movement.SendUpdate(false);

            IsFlying = false;
        }

        [System.Diagnostics.Conditional("DEBUG")]
        private void FlyDebug(string x)
        {
            Console.WriteLine(
                x + " {0,3:##0} {1,3:##0} {2,3:##0} diff {3,5:##0.0} olddiff {4,5:##0.0}  At:{5,5} {6,5}  Up:{7,5} {8,5}  v: {9} w: {10}",
                MyFlyPos.X, MyFlyPos.Y, MyFlyPos.Z,
                FlyDiff, SaveOldFlyDiff,
                Agent.Self.Movement.AtPos,
                Agent.Self.Movement.AtNeg,
                Agent.Self.Movement.UpPos,
                Agent.Self.Movement.UpNeg,
                Agent.Self.Velocity.ToString(),
                Agent.Self.AngularVelocity.ToString());
        }

        public bool StopWalkToAction()
        {
            Agent.Self.AutoPilotCancel();
            return VRAgentController.ok("stop walking to");
        }

        public bool WalkToAction(float argx, float argy)
        {
            double x = (double)(argx);
            double y = (double)(argy);
            return WalkToAction(x, y);
        }
        public bool WalkToAction(int argx, int argy)
        {
            double x = (double)(argx);
            double y = (double)(argy);
            return WalkToAction(x, y);
        }
        public bool WalkToAction(string argx, string argy)
        {
            double x = double.Parse(argx);
            double y = double.Parse(argy);
            return WalkToAction(x, y);
        }
        public bool WalkToAction(double argx, double argy)
        {
            double z;

            float target_z;
            Agent.Network.CurrentSim.TerrainHeightAtPoint(
                (int)argx, (int)argy, out target_z);
            z = (double)target_z;
            return WalkToAction(argx, argy, z);
        }

        /// <summary>
        /// Use the autopilot sim function to move the avatar to a new
        /// position. Uses double precision to get precise movements
        /// </summary>
        /// <remarks>The z value is currently not handled properly by the simulator</remarks>
        /// <param name="x"> Local region X coordinate to walk to</param>
        /// <param name="y"> Local region Y coordinate to walk to</param>
        /// <param name="z"> Z coordinate to walk to</param>
        public bool WalkToAction(float argx, float argy, float argz)
        {
            double x = (double)(argx);
            double y = (double)(argy);
            double z = (double)(argz);
            return WalkToAction(x, y, z);
        }
        public bool WalkToAction(int argx, int argy, int argz)
        {
            double x = (double)(argx);
            double y = (double)(argy);
            double z = (double)(argz);
            return WalkToAction(x, y, z);
        }
        public bool WalkToAction(string argx, string argy, string argz)
        {
            double x = double.Parse(argx);
            double y = double.Parse(argy);
            double z = double.Parse(argz);
            return WalkToAction(x, y, z);
        }
        public bool WalkToAction(double x, double y, double z)
        {
            uint rgnX, rgnY;
            Utils.LongToUInts(Agent.Network.CurrentSim.Handle, out rgnX, out rgnY);
            // Convert the local coordinates to global ones by adding the 
            // region handle parts to x and y
            x += (double)rgnX;
            y += (double)rgnY;
            Agent.Self.AutoPilot(x, y, z);
            return VRAgentController.ok("start walking to");
        }

        public bool TeleToRgnAction(string argrgn, int argx, int argy)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            return TeleToRgnAction(argrgn, x, y);
        }
        public bool TeleToRgnAction(string argrgn, string argx, string argy)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            return TeleToRgnAction(argrgn, x, y);
        }
        public bool TeleToRgnAction(string argrgn, float argx, float argy)
        {
            float z;
            Agent.Network.CurrentSim.TerrainHeightAtPoint((int)argx, (int)argy, out z);
            return TeleToRgnAction(argrgn, argx, argy, z);
        }

        public bool TeleToRgnAction(string argrgn, int argx, int argy, int argz)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            float z = (float)(argz);
            return TeleToRgnAction(argrgn, x, y, z);
        }
        public bool TeleToRgnAction(string argrgn, string argx, string argy, string argz)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            float z = float.Parse(argz);
            return TeleToRgnAction(argrgn, x, y, z);
        }
        public bool TeleToRgnAction(string argrgn, float argx, float argy, float argz)
        {
            if (Agent.Self.Teleport(argrgn, new Vector3(argx, argy, argz)))
                return VRAgentController.ok("teleporting)");
            else
                return VRAgentController.fail("cannot teleport");
        }

        public bool TeleToAction(int argx, int argy)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            return TeleToAction(x, y);
        }
        public bool TeleToAction(string argx, string argy)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            return TeleToAction(x, y);
        }
        public bool TeleToAction(float argx, float argy)
        {
            float z;
            Agent.Network.CurrentSim.TerrainHeightAtPoint((int)argx, (int)argy, out z);
            return TeleToAction(argx, argy, z);
        }

        public bool TeleToAction(float argx, float argy, float argz)
        {
            if (Agent.Self.Teleport(Agent.Network.CurrentSim.Handle, new Vector3(argx, argy, argz)))
                return VRAgentController.ok("teleporting");
            else
                return VRAgentController.fail("cannot teleport");
        }

        public bool TeleToLandmarkAction(string arglandmark)
        {
            UUID landmark = new UUID();
            if (!UUID.TryParse(arglandmark, out landmark)) {
                return VRAgentController.fail("invalid landmark");
            }
            if (Agent.Self.Teleport(landmark)) {
                return VRAgentController.ok("teleporting");
            } else {
                return VRAgentController.fail("cannot teleport");
            }
        }

        public bool SetHomeAction()
        {
            Agent.Self.SetHome();
            return VRAgentController.ok("setting home");
        }

        public bool GoHomeAction()
        {
            if (Agent.Self.GoHome()) {
                return VRAgentController.ok("teleporting home");
            } else {
                return VRAgentController.fail("cannot teleport");
            }
        }

        public class FollowTimerTask : TimerTask
        {
            const float MAX_DISTANCE_FROM_AVATAR = 3.0f;
            const float MIN_AXIS_DIST_FROM_AVATAR = 1.0f;
            const float DIF_DISTANCE_JITTER = 0.5f;

            public uint FollowTargetLocalID = 0;
            public uint AutoPilotDelay = 0;
            public bool AutoPilotRunning = false;
            public float LastDistanceToFollowTarget = 0.0f;

            public FollowTimerTask(VRAgentController agent) : base(agent)
            {
            }

            public override void Activate(uint uiparam)
            {
                Active = true;
                FollowTargetLocalID = uiparam;
                Logger.DebugLog(String.Format("Following: Starting to follow target with local id: {0}",
                                        uiparam), Agent);
            }

            public override void Deactivate()
            {
                Active = false;
                FollowTargetLocalID = 0;
            }

            public override void RunTask()
            {
                if (!Active) {
                    Logger.DebugLog(String.Format("Following: Not active"), Agent); 
                    return;
                }
 //               if (autopilotDelay>0) {
 //                   autopilotDelay--;
 //                   return;
 //               }
 //               Logger.DebugLog(String.Format("Following: Locating target"), Agent);
                // Find the target position
                lock (Agent.Network.Simulators) {
                    for (int i = 0; i < Agent.Network.Simulators.Count; i++) {
                        Avatar targetAv;
                        Agent.Network.Simulators[i].ObjectsAvatars.TryGetValue(FollowTargetLocalID, out targetAv);
                        if (targetAv!=null) {
//                            Logger.DebugLog(String.Format("Following: Found target"), Agent);
                            float distance = 0.0f;
                            if (Agent.Network.Simulators[i] == Agent.Network.CurrentSim) {
                                distance = Vector3.Distance(
                                                targetAv.Position,
                                                Agent.Self.SimPosition);
                            } else {
                                // FIXME: Calculate global distances
                            }

                            if (distance > MAX_DISTANCE_FROM_AVATAR)
                            {
                                if (AutoPilotRunning) { 
                                    float absdif = Math.Abs(distance-LastDistanceToFollowTarget);
                                    if (absdif > DIF_DISTANCE_JITTER) {
                                        LastDistanceToFollowTarget = distance;
                                        return;
                                    }
                                    AutoPilotRunning = false;
                                }
                                uint regionX, regionY;
                                Utils.LongToUInts(Agent.Network.Simulators[i].Handle, out regionX, out regionY);
                                float xmindist;
                                float ymindist;
                                Random rnd = new Random();
                                if (rnd.Next(10) < 5)
                                    xmindist = MIN_AXIS_DIST_FROM_AVATAR;
                                else
                                    xmindist = MIN_AXIS_DIST_FROM_AVATAR;
                                if (rnd.Next(10) < 5)
                                    ymindist = MIN_AXIS_DIST_FROM_AVATAR;
                                else
                                    ymindist = MIN_AXIS_DIST_FROM_AVATAR;
                                double xTarget =
                                    (double)(targetAv.Position.X + xmindist)+
                                    (double)regionX;
                                double yTarget =
                                    (double)(targetAv.Position.Y + ymindist)+
                                    (double)regionY;
                                double zTarget = targetAv.Position.Z - 2f;
                                Logger.DebugLog(String.Format("Following: {0} meters away from the target, starting autopilot to <{1},{2},{3}>",
                                    distance, xTarget, yTarget, zTarget), Agent);
 //                               autopilotDelay = 4;     
                                Agent.Self.AutoPilot(xTarget, yTarget, zTarget);
                                AutoPilotRunning = true;
                                LastDistanceToFollowTarget = distance;
                            } 
                            else
                            {
                                if (AutoPilotRunning)
                                {
                                    float absdif = Math.Abs(distance - LastDistanceToFollowTarget);
                                    if (absdif > DIF_DISTANCE_JITTER)
                                    {
                                        LastDistanceToFollowTarget = distance;
                                        return;
                                    }
                                    AutoPilotRunning = false;
                                Agent.Self.Movement.TurnToward(targetAv.Position);
                                Agent.Self.Movement.SendUpdate(false);
                                }

                            }
                            //                            else 
                            //                            {
                            //                                // We are in range of the target and moving, stop moving
                            //                                Logger.DebugLog(String.Format("Following: Stopping autopilot"), Agent);
                            //                                Agent.Self.AutoPilotCancel();
                            //                            }
                        }
                    }
                }
            }
        }

        FollowTimerTask followTTask = null;

        public bool StopFollowAction()
        {
            if (followTTask == null) {
                Logger.DebugLog(String.Format("Following: Not active"), Agent);
                return (VRAgentController.ok("not following"));
            }
            int itt = Agent.TimerTasks.IndexOf(followTTask);
            lock (Agent.TimerTasks) {
                Agent.TimerTasks[itt].Deactivate();
            }
            Agent.Self.AutoPilotCancel();
            Logger.DebugLog(String.Format("Following: stop following"), Agent);
            return VRAgentController.ok("stop following");
        }

        public bool FollowAction(string avname)
        {
            lock (Agent.Network.Simulators) {
                for (int i = 0; i < Agent.Network.Simulators.Count; i++) {
                    Avatar target =
                        Agent.Network.Simulators[i].ObjectsAvatars.Find(
                            delegate (Avatar avatar)
                            {
                                return avatar.Name == avname;
                            }
                        );
                    if (target != null) {
                        if (followTTask == null) {
                            // First time this command is used with success
                            followTTask = new FollowTimerTask(Agent);
                            Agent.TimerTasks.Add(followTTask);
                            // was moved to ModificationActions class constructor
                            //                           Client.Network.RegisterCallback(PacketType.AlertMessage, AlertMessageHandler);

                        }
                        int itt = Agent.TimerTasks.IndexOf(followTTask);
                        lock (Agent.TimerTasks) {
                            Logger.DebugLog(String.Format("Following: avatar name: {0}, local id: {1}, global id: {2}",
                                target.Name, target.LocalID, target.ID), Agent);
                            Agent.TimerTasks[itt].Activate(target.LocalID);
                        }
                        return VRAgentController.ok("start following");
                    }
                }
            }

            if (followTTask != null) {
                int itt = Agent.TimerTasks.IndexOf(followTTask);
                if (Agent.TimerTasks[itt].Active) {
                    Agent.Self.AutoPilotCancel();
                    lock (Agent.TimerTasks) {
                        Agent.TimerTasks[itt].Deactivate();
                    }
                }
            }
            return VRAgentController.fail("avatar not found");
        }

        private void AlertMessageHandler(object sender, PacketReceivedEventArgs e)
        {
            Packet packet = e.Packet;

            AlertMessagePacket alert = (AlertMessagePacket)packet;
            string message = Utils.BytesToString(alert.AlertData.Message);

            if (message.Contains("Autopilot cancel")) {
                Logger.Log("Following: " + message, Helpers.LogLevel.Info, Agent);
            }
        }

        public bool RunAction(string argstartstop)
        {
            if (argstartstop == "stop") {
                Agent.Self.Movement.AlwaysRun = false;
                Agent.Self.Movement.SendUpdate(false);
                return VRAgentController.ok("stop running");
            } else if (argstartstop == "start") {
                Agent.Self.Movement.AlwaysRun = true;
                Agent.Self.Movement.SendUpdate(false);
                return VRAgentController.ok("start running");
            } else {
                return VRAgentController.fail("invalid option");
            }

        }

        public bool MotionAction(string argmotion)
        {
            if (argmotion == "forward") {
                Agent.Self.Movement.AtPos = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.AtPos = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "back") {
                Agent.Self.Movement.AtNeg = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.AtNeg = false;
            } else if (argmotion == "right") {
                Agent.Self.Movement.LeftNeg = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.LeftNeg = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "left") {
                Agent.Self.Movement.LeftPos = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.LeftPos = false;
            } else if (argmotion == "up") {
                Agent.Self.Movement.UpPos = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.UpPos = false;
            } else if (argmotion == "down") {
                Agent.Self.Movement.UpNeg = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.UpNeg = false;
            } else if (argmotion == "turn_left") {
                Agent.Self.Movement.TurnLeft = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.TurnLeft = false;
            } else if (argmotion == "turn_right") {
                Agent.Self.Movement.TurnRight = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.TurnRight = false;
            } else if (argmotion == "nudge_forward") {
                Agent.Self.Movement.NudgeAtPos = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.NudgeAtPos = false;
            } else if (argmotion == "nudge_back") {
                Agent.Self.Movement.NudgeAtNeg = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.NudgeAtNeg = false;
            } else if (argmotion == "nudge_right") {
                Agent.Self.Movement.NudgeLeftNeg = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.NudgeLeftNeg = false;
            } else if (argmotion == "nudge_left") {
                Agent.Self.Movement.NudgeLeftPos = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.NudgeLeftPos = false;
            } else if (argmotion == "finish_anim") {
                Agent.Self.Movement.FinishAnim = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.FinishAnim = false;
            } else if (argmotion == "pitch_pos") {
                Agent.Self.Movement.PitchPos = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.PitchPos = false;
            } else if (argmotion == "pitch_neg") {
                Agent.Self.Movement.PitchNeg = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.PitchNeg = false;
            } else if (argmotion == "yaw_pos") {
                Agent.Self.Movement.YawPos = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.YawPos = false;
            } else if (argmotion == "yaw_neg") {
                Agent.Self.Movement.YawNeg = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.YawNeg = false;
            } else if (argmotion == "stop") {
                Agent.Self.Movement.Stop = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.Stop = false;
            } else if (argmotion == "sit") {
                Agent.Self.Movement.SitOnGround = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.SitOnGround = false;
            } else if (argmotion == "stand") {
                Agent.Self.Movement.StandUp = true;
                Agent.Self.Movement.SendUpdate(false);
                Agent.Self.Movement.StandUp = false;
            } else if (argmotion == "stop_on") {
                Agent.Self.Movement.Stop = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "stop_off") {
                Agent.Self.Movement.Stop = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "sit_on") {
                Agent.Self.Movement.SitOnGround = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "sit_off") {
                Agent.Self.Movement.SitOnGround = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "stand_on") {
                Agent.Self.Movement.StandUp = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "stand_off") {
                Agent.Self.Movement.StandUp = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "fly_on") {
                Agent.Self.Movement.Fly = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "fly_off") {
                Agent.Self.Movement.Fly = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "turn_left_on") {
                Agent.Self.Movement.TurnLeft = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "turn_left_off") {
                Agent.Self.Movement.TurnLeft = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "turn_right_on") {
                Agent.Self.Movement.TurnRight = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "turn_right_off") {
                Agent.Self.Movement.TurnRight = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "run_on") {
                Agent.Self.Movement.AlwaysRun = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "run_off") {
                Agent.Self.Movement.AlwaysRun = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "fast_at_on") {
                Agent.Self.Movement.FastAt = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "fast_at_off") {
                Agent.Self.Movement.FastAt = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "fast_left_on") {
                Agent.Self.Movement.FastLeft = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "fast_left_off") {
                Agent.Self.Movement.FastLeft = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "fast_up_on") {
                Agent.Self.Movement.FastUp = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "fast_up_off") {
                Agent.Self.Movement.FastUp = false;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "away_on") {
                Agent.Self.Movement.Away = true;
                Agent.Self.Movement.SendUpdate(false);
            } else if (argmotion == "away_off") {
                Agent.Self.Movement.Away = false;
                Agent.Self.Movement.SendUpdate(false);
            } else
                return VRAgentController.fail("invalid motion");

            return VRAgentController.ok("executing requested motion");
        }


    }

}
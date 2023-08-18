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
//   Class:     ObservationActions 
//   Purpose:   To implement actions for the agent to be able to observe
//              objects on virtual world 
//   Author:    João Carlos Gluz 
//
//***********************************************************************
using System;
using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
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
    public class ObservationActions : Actions
    {
        public ObservationActions(VRAgentController agent) : base(agent)
        {
            //agent.Objects.ObjectProperties +=
            //        new EventHandler<ObjectPropertiesEventArgs>(ObjectProperties_Handler);
        }

        public List<List<string>> LookForEvents()
        {
            List<List<string>> results = new List<List<string>>();
            lock (Agent.DetcdVREventsLock) {
                results = Agent.DetcdVREvents;
                Agent.DetcdVREvents = new List<List<string>>();
            }
            return VRAgentController.ok("last detected vr events", results);
        }

        public List<List<string>> LookForEvents(string argtype)
        {
            List<List<string>> results = new List<List<string>>();
            lock (Agent.DetcdVREventsLock) {
                Agent.DetcdVREvents.RemoveAll(vrev => {
                    // index 0 of list has the type of vr event
                    if (vrev[0] == argtype) { results.Add(vrev); return true; } else return false;
                }
                );
            }
            return VRAgentController.ok("last detected vr events", results);
        }


        public List<string> LookHeightAtAction(int argx, int argy)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            return LookHeightAtAction(x, y);
        }

        public List<string> LookHeightAtAction(string argx, string argy)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            return LookHeightAtAction(x, y);
        }

        public List<string> LookHeightAtAction(float argx, float argy)
        {
            float height;
            string rid = Agent.Network.CurrentSim.ID.ToString();
            PerceptList percepts = new PerceptList();

            if (Agent.Network.CurrentSim.TerrainHeightAtPoint(Convert.ToInt32(argx),
                                                        Convert.ToInt32(argy), out height)) {
                List<string> result = percepts.Add("terrain_height_at", rid, argx.ToString(), argy.ToString(),
                                height.ToString());
                Agent.PerceptsBase.Update(percepts);
                return VRAgentController.ok("get height info", result);
            }
            return VRAgentController.nullst("cannot get height info");
        }

        public List<string> LookWindAtAction(int argx, int argy)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            return LookWindAtAction(x, y);
        }

        public List<string> LookWindAtAction(string argx, string argy)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            return LookWindAtAction(x, y);
        }

        public List<string> LookWindAtAction(float argx, float argy)
        {
            // Get the agent's current "patch" position, where each patch of
            // wind data is a 16x16m square
            string rid = Agent.Network.CurrentSim.ID.ToString();
            int xPos = (int)Utils.Clamp(argx, 0.0f, 255.0f) / 16;
            int yPos = (int)Utils.Clamp(argy, 0.0f, 255.0f) / 16;
            Vector2 windSpeed = Agent.Network.CurrentSim.WindSpeeds[yPos * 16 + xPos];
            PerceptList percepts = new PerceptList();
            List<string> result = percepts.Add("wind_speed_at", rid,
                argx.ToString(), argy.ToString(),
                windSpeed.X.ToString(), windSpeed.Y.ToString());
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get wind info", result);
        }

        public List<string> LookRegionAction(string argrgname)
        {
            GridRegion region;

            if (Agent.Grid.GetGridRegion(argrgname, GridLayerType.Objects, out region)) {
                PerceptList percepts = new PerceptList();
                List<string> result = new List<string>();
                string rid = Agent.Network.CurrentSim.ID.ToString();
                result = percepts.Add("region", rid, region.Name.ToString());
                percepts.Add("name", rid, region.Name.ToString());
                percepts.Add("handle", rid, region.RegionHandle.ToString());
                percepts.Add("world_coord", rid, region.X.ToString(), region.Y.ToString());
                percepts.Add("water_height", rid + "', '" + region.WaterHeight.ToString());
                percepts.Add("access_level", rid, region.Access.ToString());
                percepts.Add("flags", rid + "', [" + region.RegionFlags.ToString().ToLower() + "])");
                Agent.PerceptsBase.Update(percepts);
                return VRAgentController.ok("get region info", result);
            }
            return VRAgentController.nullst("cannot get region info");
        }

        public List<string> LookAvatarByIDAction(string argavid)
        {
            UUID target;
            if (!UUID.TryParse(argavid, out target)) {
                return VRAgentController.nullst("param error");
            }
            Avatar av = Agent.Network.CurrentSim.ObjectsAvatars.Find(
                delegate (Avatar avatar) { return avatar.ID == target; }
                );
            if (av == null) {
                return VRAgentController.nullst("avatar not found");
            }
            PerceptList percepts = new PerceptList();
            string avid = av.ID.ToString();
            List<string> result = DoLookAvatar(avid, av, percepts);
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get avatar info", result);
        }

        public List<string> LookAvatarByNameAction(string argavname)
        {
            Avatar av = Agent.Network.CurrentSim.ObjectsAvatars.Find(
                    delegate (Avatar avatar) { return (avatar.Name == argavname); }
            );
            if (av == null) {
                return VRAgentController.nullst("avatar not found");
            }
            PerceptList percepts = new PerceptList();
            string avid = av.ID.ToString();
            List<string> result = DoLookAvatar(avid, av, percepts);
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get avatar info", result);
        }

        public List<string> DoLookAvatar(string avid, Avatar av, PerceptList percepts)
        {
            Vector3 mypos = Agent.Self.SimPosition;
            Vector3 avpos = av.Position;
            float avdistance = Vector3.Distance(avpos, mypos);
            List<string> result = percepts.Add("avatar", avid, av.Name.ToString(), avdistance.ToString(),
                                        av.Position.X.ToString(), av.Position.Y.ToString(), av.Position.Z.ToString());
            percepts.Add("name", avid, av.Name.ToString());
            percepts.Add("first_name", avid, av.FirstName.ToString());
            percepts.Add("last_name", avid, av.LastName.ToString());
            percepts.Add("dist", avid, avdistance.ToString());
            percepts.Add("pos", avid, av.Position.X.ToString(), av.Position.Y.ToString(), av.Position.Z.ToString());
            percepts.Add("scale", avid, av.Scale.X.ToString(), av.Scale.Y.ToString(), av.Scale.Z.ToString());
            float roll, pitch, yaw;
            av.Rotation.GetEulerAngles(out roll, out pitch, out yaw);
            percepts.Add("rot", avid, roll.ToString(), pitch.ToString(), yaw.ToString());
            percepts.Add("veloc", avid, av.Velocity.X.ToString(), av.Velocity.Y.ToString(), av.Velocity.Z.ToString());
            percepts.Add("ang_veloc", avid, av.AngularVelocity.X.ToString(), av.AngularVelocity.Y.ToString(), av.AngularVelocity.Z.ToString());
            percepts.Add("accel", avid, av.Acceleration.X.ToString(), av.Acceleration.Y.ToString(), av.Acceleration.Z.ToString());
            percepts.Add("local_id", avid, av.LocalID.ToString());
            if (av.Textures != null) {
                percepts.Add("txtr", avid, av.Textures.DefaultTexture.TextureID.ToString());
                percepts.Add("color", avid, av.Textures.DefaultTexture.RGBA.R.ToString(), av.Textures.DefaultTexture.RGBA.G.ToString(),
                    av.Textures.DefaultTexture.RGBA.B.ToString(), av.Textures.DefaultTexture.RGBA.A.ToString());
                percepts.Add("glow", avid, av.Textures.DefaultTexture.Glow.ToString());
                int nfaces = 0;
                for (int i = 0; i < av.Textures.FaceTextures.Length; i++) {
                    if (av.Textures.FaceTextures[i] != null) {
                        nfaces++;
                        percepts.Add("txtr_" + i.ToString(), avid, av.Textures.FaceTextures[i].TextureID.ToString());
                        percepts.Add("color_" + i.ToString(), avid, av.Textures.FaceTextures[i].RGBA.R.ToString(),
                            av.Textures.FaceTextures[i].RGBA.G.ToString(), av.Textures.FaceTextures[i].RGBA.B.ToString(),
                            av.Textures.FaceTextures[i].RGBA.A.ToString());
                        percepts.Add("glow_" + i.ToString(), avid, av.Textures.FaceTextures[i].Glow.ToString());
                    }
                }
                percepts.Add("nfaces", avid, nfaces.ToString());
            }
            return result;
        }

        public bool DoLookObj(string pid, Primitive p, PerceptList percepts)
        {
            percepts.Add("type", pid, p.PrimData.PCode.ToString().ToLower());
            if (p.PrimData.PCode == PCode.Prim)
                percepts.Add("subtype", pid, p.Type.ToString().ToLower());
            if (p.PrimData.PCode == PCode.Tree || p.PrimData.PCode == PCode.NewTree)
                percepts.Add("subtype", pid, p.TreeSpecies.ToString().ToLower());
            if (p.PrimData.PCode == PCode.Grass) {
                Grass gt = (Grass)p.TreeSpecies;
                percepts.Add("subtype", pid, gt.ToString().ToLower());
            }
            percepts.Add("local_id", pid, p.LocalID.ToString());
            percepts.Add("parent_id", pid, p.ParentID.ToString());
            if (p.Flexible != null)
                percepts.Add("is_flex", pid);
            if (p.Light != null)
                percepts.Add("is_light", pid);
            if (p.Sculpt != null)
                percepts.Add("is_sculpt", pid);
            Primitive chldprim = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
               delegate (Primitive c) { return (c.ParentID == p.LocalID); }
            );
            if (chldprim != null) {
                percepts.Add("has_children", pid);
                percepts.Add("is_linked", pid);
            } else if (p.ParentID != 0) {
                percepts.Add("is_linked", pid);
            }
            if (((p.Flags & PrimFlags.Physics) != 0))
                percepts.Add("has_phys", pid);
            if (((p.Flags & PrimFlags.Temporary) != 0))
                percepts.Add("is_temp", pid);
            if (((p.Flags & PrimFlags.Phantom) != 0))
                percepts.Add("is_phantom", pid);
            if (((p.Flags & PrimFlags.CastShadows) != 0))
                percepts.Add("has_shadows", pid);
            percepts.Add("pos", pid, p.Position.X.ToString(), p.Position.Y.ToString(), p.Position.Z.ToString());
            percepts.Add("scale", pid, p.Scale.X.ToString(), p.Scale.Y.ToString(), p.Scale.Z.ToString());
            float roll, pitch, yaw;
            p.Rotation.GetEulerAngles(out roll, out pitch, out yaw);
            percepts.Add("rot", pid, roll.ToString(), pitch.ToString(), yaw.ToString());
            percepts.Add("veloc", pid, p.Velocity.X.ToString(), p.Velocity.Y.ToString(), p.Velocity.Z.ToString());
            percepts.Add("ang_veloc", pid, p.AngularVelocity.X.ToString(), p.AngularVelocity.Y.ToString(), p.AngularVelocity.Z.ToString());
            percepts.Add("accel", pid, p.Acceleration.X.ToString(), p.Acceleration.Y.ToString(), p.Acceleration.Z.ToString());
            percepts.Add("collis_plane", pid, p.CollisionPlane.X.ToString(), p.CollisionPlane.Y.ToString(),
                p.CollisionPlane.Z.ToString(), p.CollisionPlane.W.ToString());
            if (p.Text != String.Empty)
                percepts.Add("hover_text", pid, p.Text);
            if (p.IsAttachment)
                percepts.Add("is_attach", pid);
            if (p.Textures != null) {
                percepts.Add("txtr", pid, p.Textures.DefaultTexture.TextureID.ToString());
                percepts.Add("color", pid, p.Textures.DefaultTexture.RGBA.R.ToString(), p.Textures.DefaultTexture.RGBA.G.ToString(),
                    p.Textures.DefaultTexture.RGBA.B.ToString(), p.Textures.DefaultTexture.RGBA.A.ToString());
                percepts.Add("glow", pid, p.Textures.DefaultTexture.Glow.ToString());
                int nfaces = 0;
                for (int i = 0; i < p.Textures.FaceTextures.Length; i++) {
                    if (p.Textures.FaceTextures[i] != null) {
                        nfaces++;
                        percepts.Add("txtr_"+i.ToString(), pid, p.Textures.FaceTextures[i].TextureID.ToString());
                        percepts.Add("color_" + i.ToString(), pid, p.Textures.FaceTextures[i].RGBA.R.ToString(),
                            p.Textures.FaceTextures[i].RGBA.G.ToString(), p.Textures.FaceTextures[i].RGBA.B.ToString(),
                            p.Textures.FaceTextures[i].RGBA.A.ToString());
                        percepts.Add("glow_" + i.ToString(), pid, p.Textures.FaceTextures[i].Glow.ToString());
                    }
                }
                percepts.Add("nfaces", pid, nfaces.ToString());
            }
            return true;
        }


        /// <summary>
        /// "Look to" some object to get its attributes and properties.
        /// </summary>
        /// <param name="objid"> Unique global identified of the object</param>
        public List<string> LookObjAction(string objuid)
        {
            UUID primID;
            // Check argument
            if (!UUID.TryParse(objuid, out primID)) {
                return VRAgentController.nullst("param 1 error");
            }
            Primitive p = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim) { return prim.ID == primID; }
            );
            if (p == null) {
                return VRAgentController.nullst("obj not found");
            }

            // Request object properties
            string pid = p.ID.ToString();
            PerceptList percepts = new PerceptList();
            List<string> result;
            Primitive.ObjectProperties mdatainfo = null;
            AutoResetEvent waitMDataInfo = new AutoResetEvent(false);
            EventHandler<ObjectPropertiesEventArgs> mdataInfoReplyHandler =
                delegate (object sender, ObjectPropertiesEventArgs e) {
                    mdatainfo = e.Properties;
                    waitMDataInfo.Set();
                };
            Agent.Objects.ObjectProperties += mdataInfoReplyHandler;
            Agent.Objects.SelectObject(Agent.Network.CurrentSim, p.LocalID, true);
            waitMDataInfo.WaitOne(1000 * 10, false);
            Agent.Objects.ObjectProperties -= mdataInfoReplyHandler;

            // Generate perception records with basic information of object
            string typ = p.PrimData.PCode.ToString().ToLower();
            string subtyp =
                p.PrimData.PCode == PCode.Prim ?
                    p.Type.ToString().ToLower() :
                    (p.PrimData.PCode == PCode.Tree || p.PrimData.PCode == PCode.NewTree ?
                        p.TreeSpecies.ToString().ToLower() :
                        (p.PrimData.PCode == PCode.Grass ?
                            ((Grass)p.TreeSpecies).ToString().ToLower() : ""));
            Vector3 objpos = p.Position;
            Vector3 avpos = Agent.Self.SimPosition;
            float dist = Vector3.Distance(objpos, avpos);

            string name = (mdatainfo == null || mdatainfo.Name == null) ? "" : mdatainfo.Name;
            string descr = (mdatainfo == null || mdatainfo.Description == null) ? "" : mdatainfo.Description;
            result = percepts.Add("obj", pid, name, typ, subtyp, dist.ToString(),
                p.Position.X.ToString(), p.Position.Y.ToString(), p.Position.Z.ToString(),
                p.Scale.X.ToString(), p.Scale.Y.ToString(), p.Scale.Z.ToString(), 
                descr);
            percepts.Add("dist", pid, dist.ToString());
            DoLookObj(pid, p, percepts);

            // Generate perception records with additional properties info of object
            if (mdatainfo != null) {
                percepts.Add("extra_props", pid, name, descr, mdatainfo.CreatorID.ToString(),
                    mdatainfo.OwnerID.ToString(), mdatainfo.CreationDate.ToString());
                DoLookObjExtraProps(pid, mdatainfo, percepts);
            }
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get obj info", result);
        }

        public bool DoLookObjExtraProps(string pid, Primitive.ObjectProperties prop,
                                    PerceptList percepts)
        {
            if (prop.Name != null)
                percepts.Add("name", pid, prop.Name);
            if (prop.Description != null)
                percepts.Add("descr", pid, prop.Description);
            percepts.Add("creat_id", pid, prop.CreatorID.ToString());
            percepts.Add("owner_id", pid, prop.OwnerID.ToString());
            percepts.Add("creat_date", pid, prop.CreationDate.ToString());
            percepts.Add("owner_perms", pid, PermMaskStr(prop.Permissions.OwnerMask));
            percepts.Add("group_perms", pid, PermMaskStr(prop.Permissions.GroupMask));
            percepts.Add("all_perms", pid, PermMaskStr(prop.Permissions.EveryoneMask));
            percepts.Add("base_perms", pid, PermMaskStr(prop.Permissions.BaseMask));
            percepts.Add("nextown_perms", pid, PermMaskStr(prop.Permissions.NextOwnerMask));
            return true;
        }

        public List<string> LookObjExtraPropsAction(string objuid)
        {
            UUID primID;
            if (!UUID.TryParse(objuid, out primID)) {
                return VRAgentController.nullst("param 1 error");
            }
            Primitive p = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim) { return prim.ID == primID; }
            );
            if (p == null) {
                return VRAgentController.nullst("obj not found");
            }
            PerceptList percepts = new PerceptList();
            List<string> result = null;
            string pid = p.ID.ToString();
            AutoResetEvent wait_MDataInfo = new AutoResetEvent(false);
            EventHandler<ObjectPropertiesEventArgs> mDataInfoReply_handler =
                delegate (object sender, ObjectPropertiesEventArgs e) {
                    Primitive.ObjectProperties prop = e.Properties;
                    string name = prop.Name != null ? prop.Name : "";
                    string descr = prop.Description != null ? prop.Description : "";
                    result = percepts.Add("extra_props", pid, name, descr,
                                    prop.CreatorID.ToString(),
                                    prop.OwnerID.ToString(),
                                    prop.CreationDate.ToString());
                    DoLookObjExtraProps(pid, prop, percepts);
                    wait_MDataInfo.Set();
                };
            Agent.Objects.ObjectProperties += mDataInfoReply_handler;
            Agent.Objects.SelectObject(Agent.Network.CurrentSim, p.LocalID, true);
            wait_MDataInfo.WaitOne(1000 * 10, false);
            Agent.Objects.ObjectProperties -= mDataInfoReply_handler;
            if (percepts.Count > 0) {
                Agent.PerceptsBase.Update(percepts);
                return VRAgentController.ok("get obj info", result);
            } else {
                return VRAgentController.nullst("timeout to get obj info");
            }
        }

        private static string PermMaskStr(PermissionMask mask)
        {
            string str = "[";
            bool needcomma = false;

            if (((uint)mask | (uint)PermissionMask.Copy) == (uint)PermissionMask.Copy) {
                str += "copy";
                needcomma = true;
            }
            if (((uint)mask | (uint)PermissionMask.Modify) == (uint)PermissionMask.Modify) {
                str += (needcomma) ? "," : "";
                str += "modify";
                needcomma = true;
            }
            if (((uint)mask | (uint)PermissionMask.Transfer) == (uint)PermissionMask.Transfer) {
                str += (needcomma) ? "," : "";
                str += "transfer";
                needcomma = true;
            }
            if (((uint)mask | (uint)PermissionMask.Move) == (uint)PermissionMask.Move) {
                str += (needcomma) ? "," : "";
                str += "move";
                needcomma = true;
            }
            if (((uint)mask | (uint)PermissionMask.Export) == (uint)PermissionMask.Export) {
                str += (needcomma) ? "," : "";
                str += "export";
                needcomma = true;
            }
            if (((uint)mask | (uint)PermissionMask.Damage) == (uint)PermissionMask.Damage) {
                str += (needcomma) ? "," : "";
                str += "damage";
                needcomma = true;
            }
            str += "]";
            return str;
        }


        public List<string> LookObjFlexPropsAction(string argobjuid)
        {
            UUID primID;
            if (!UUID.TryParse(argobjuid, out primID)) {
                return VRAgentController.nullst("param 1 error");
            }
            Primitive p = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim) { return prim.ID == primID; }
            );
            if (p == null) {
                return VRAgentController.nullst("obj not found");
            }
            PerceptList percepts = new PerceptList();
            List<string> result;
            string pid = p.ID.ToString();
            if (p.Flexible == null)
                return VRAgentController.nullst("not flexible obj");
            result = percepts.Add("flex_props", pid, p.Flexible.Softness.ToString().ToLower());
            percepts.Add("is_flex", pid);
            percepts.Add("flex_soft", pid, p.Flexible.Softness.ToString().ToLower());
            percepts.Add("flex_grav", pid, p.Flexible.Gravity.ToString().ToLower());
            percepts.Add("flex_drag", pid, p.Flexible.Drag.ToString().ToLower());
            percepts.Add("flex_wind", pid, p.Flexible.Wind.ToString().ToLower());
            percepts.Add("flex_tension", pid, p.Flexible.Tension.ToString().ToLower());
            percepts.Add("flex_force", pid,
                            p.Flexible.Force.X.ToString(),
                            p.Flexible.Force.Y.ToString(),
                            p.Flexible.Force.Z.ToString());
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get obj info", result);
        }

        public List<string> LookObjsLightPropsAction(string argobjuid)
        {
            UUID primID;
            if (!UUID.TryParse(argobjuid, out primID)) {
                return VRAgentController.nullst("param 1 error");
            }
            Primitive p = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                delegate (Primitive prim) { return prim.ID == primID; }
            );
            if (p == null) {
                return VRAgentController.nullst("obj not found");
            }
            PerceptList percepts = new PerceptList();
            List<string> result;
            string pid = p.ID.ToString();
            if (p.Light == null)
                return VRAgentController.nullst("not light obj");
            result = percepts.Add("light_props", pid, p.Light.Color.R.ToString(),
                            p.Light.Color.G.ToString(),
                            p.Light.Color.B.ToString(),
                            p.Light.Color.A.ToString(),
                            p.Light.Intensity.ToString(),
                            p.Light.Radius.ToString());
            percepts.Add("is_light", pid);
            // LightData attributes
            percepts.Add("light_color", pid,
                            p.Light.Color.R.ToString(),
                            p.Light.Color.G.ToString(),
                            p.Light.Color.B.ToString(),
                            p.Light.Color.A.ToString());
            percepts.Add("light_intens", pid, p.Light.Intensity.ToString().ToLower());
            percepts.Add("light_radius", pid, p.Light.Radius.ToString().ToLower());
            percepts.Add("light_cutoff", pid, p.Light.Cutoff.ToString().ToLower());
            percepts.Add("light_falloff", pid, p.Light.Falloff.ToString().ToLower());
            /// Information on the light properties of a primitive as texture map
            if (p.LightMap != null) {
                // LightImage attributes
                percepts.Add("lightmap_texture", pid, p.LightMap.LightTexture.ToString().ToLower());
                percepts.Add("lightmap_params", pid,
                            p.LightMap.Params.X.ToString(),
                            p.LightMap.Params.Y.ToString(),
                            p.LightMap.Params.Z.ToString());
            }
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get obj info", result);
        }

        public List<string> LookObjSculptPropsAction(string argobjuid)
        {
            UUID primID;
            if (!UUID.TryParse(argobjuid, out primID)) {
                return VRAgentController.nullst("param 1 error");
            }
            Primitive p = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim) { return prim.ID == primID; }
            );
            if (p == null) {
                return VRAgentController.nullst("obj not found");
            }
            PerceptList percepts = new PerceptList();
            List<string> result;
            string pid = p.ID.ToString();
            if (p.Sculpt == null)
                return null;
            result = percepts.Add("sculpt_props", pid,
                                    p.Sculpt.Type.ToString().ToLower(),
                                    p.Sculpt.SculptTexture.ToString().ToLower());
            percepts.Add("is_sculpt", pid);
            /// Information on the sculpt properties of a sculpted primitive
            // SculptData attributes
            percepts.Add("sculpt_txtr", pid, p.Sculpt.SculptTexture.ToString().ToLower());
            percepts.Add("sculpt_type", pid, p.Sculpt.Type.ToString().ToLower());
            /// Render inside out (inverts the normals).
            if (p.Sculpt.Invert)
                percepts.Add("sculpt_is_invert", pid);
            /// Render an X axis mirror of the sculpty.
            if (p.Sculpt.Mirror)
                percepts.Add("sculpt_is_mirror", pid);
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get obj info", result);
        }

        public List<string> LookObjConstrPropsAction(string argobjuid)
        {
            UUID primID;
            if (!UUID.TryParse(argobjuid, out primID)) {
                return VRAgentController.nullst("param 1 error");
            }
            Primitive p = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim) { return prim.ID == primID; }
            );
            if (p == null) {
                return VRAgentController.nullst("obj not found");
            }
            PerceptList percepts = new PerceptList();
            List<string> result;
            string pid = p.ID.ToString();
            result = percepts.Add("constr_props", pid,
                            p.PrimData.ProfileCurve.ToString(),
                            p.PrimData.ProfileHole.ToString(),
                            p.PrimData.PathCurve.ToString().ToLower());
            /// Parameters used to construct a visual representation of a primitive
            //						public ConstructionData PrimData;
            // ConstructionData properties
            percepts.Add("constr_state", pid, p.PrimData.State.ToString());
            percepts.Add("pcode", pid, p.PrimData.PCode.ToString());
            if (p.PrimData.AttachmentPoint.ToString() != "")
                percepts.Add("attach_point", pid, p.PrimData.AttachmentPoint.ToString());
            percepts.Add("prof_shape", pid, p.PrimData.ProfileCurve.ToString().ToLower());
            percepts.Add("prof_hole", pid, p.PrimData.ProfileHole.ToString().ToLower());
            percepts.Add("prof_hollow", pid, p.PrimData.ProfileHollow.ToString().ToLower());
            percepts.Add("prof_begin", pid, p.PrimData.ProfileBegin.ToString().ToLower());
            percepts.Add("prof_end", pid, p.PrimData.ProfileEnd.ToString().ToLower());
            percepts.Add("path_begin_scale", pid,
                                    p.PrimData.PathBeginScale.X.ToString() + "','" +
                                    p.PrimData.PathBeginScale.Y.ToString());
            percepts.Add("path_end_scale", pid,
                                    p.PrimData.PathEndScale.X.ToString() + "','" +
                                    p.PrimData.PathEndScale.Y.ToString());
            // ConstructionData attributes
            percepts.Add("path_shape", pid, p.PrimData.PathCurve.ToString().ToLower());
            percepts.Add("path_end", pid, p.PrimData.PathEnd.ToString().ToLower());
            percepts.Add("path_radius_offset", pid, p.PrimData.PathRadiusOffset.ToString().ToLower());
            percepts.Add("path_skew", pid, p.PrimData.PathSkew.ToString().ToLower());
            percepts.Add("path_scale", pid,
                                    p.PrimData.PathScaleX.ToString().ToLower() + "','" +
                                    p.PrimData.PathScaleY.ToString().ToLower());
            percepts.Add("path_shear", pid,
                                    p.PrimData.PathShearX.ToString().ToLower() + "','" +
                                    p.PrimData.PathShearY.ToString().ToLower());
            percepts.Add("path_taper", pid,
                                    p.PrimData.PathTaperX.ToString().ToLower(),
                                    p.PrimData.PathTaperY.ToString().ToLower());
            percepts.Add("path_begin", pid, p.PrimData.PathBegin.ToString().ToLower());
            percepts.Add("path_twist", pid, p.PrimData.PathTwist.ToString().ToLower());
            percepts.Add("path_twist_begin", pid, p.PrimData.PathTwistBegin.ToString().ToLower());
            percepts.Add("path_revols", pid, p.PrimData.PathRevolutions.ToString().ToLower());
            percepts.Add("material", pid, p.PrimData.Material.ToString().ToLower());
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get obj info", result);
        }

        public List<string> LookObjPhysPropsAction(string argobjuid)
        {
            UUID primID;
            if (!UUID.TryParse(argobjuid, out primID)) {
                return VRAgentController.nullst("param 1 error");
            }
            Primitive p = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim) { return prim.ID == primID; }
            );
            if (p == null) {
                return VRAgentController.nullst("obj not found");
            }
            PerceptList percepts = new PerceptList();
            List<string> result = null;
            string pid = p.ID.ToString();
            AutoResetEvent wait_PhysInfo = new AutoResetEvent(false);
            EventHandler<PhysicsPropertiesEventArgs> physInfoReply_handler =
                delegate (object sender, PhysicsPropertiesEventArgs e) {
                    Primitive.PhysicsProperties prop = e.PhysicsProperties;
                    result = percepts.Add("phys_props", pid,
                                    prop.Density.ToString(),
                                    prop.Friction.ToString(),
                                    prop.GravityMultiplier.ToString());
                    percepts.Add("phys_dens", pid, prop.Density.ToString());
                    percepts.Add("phys_frict", pid, prop.Friction.ToString());
                    percepts.Add("phys_grav", pid, prop.GravityMultiplier.ToString());
                    percepts.Add("phys_shape", pid, prop.PhysicsShapeType.ToString().ToLower());
                    percepts.Add("phys_bounce", pid, prop.Restitution.ToString());
                    wait_PhysInfo.Set();
                };
            Agent.Objects.PhysicsProperties += physInfoReply_handler;
            Agent.Objects.SetFlags(Agent.Network.CurrentSim, p.LocalID, true, false, false, false);
            wait_PhysInfo.WaitOne(1000 * 10, false);
            Agent.Objects.PhysicsProperties -= physInfoReply_handler;
            Agent.Objects.SetFlags(Agent.Network.CurrentSim, p.LocalID, false, false, false, false);
            if (percepts.Count > 0) {
                Agent.PerceptsBase.Update(percepts);
                return VRAgentController.ok("get obj info", result);
            } else {
                return VRAgentController.nullst("timeout to get obj info");
            }
        }

        public List<List<string>> LookObjInventoryAction(string argobjuid)
        {
            uint objectLocalID;
            UUID objectID;
            if (!UUID.TryParse(argobjuid, out objectID)) {
                VRAgentController.fail("param 1 error");
                return null;
            }
            Primitive found = Agent.Network.CurrentSim.ObjectsPrimitives.Find(delegate (Primitive prim) 
                                { return prim.ID == objectID; });
            if (found != null)
                objectLocalID = found.LocalID;
            else {
                VRAgentController.fail("obj not found");
                return null;
            }
            List<InventoryBase> items = Agent.Inventory.GetTaskInventory(objectID, objectLocalID, 1000 * 30);
            if (items != null) {
                PerceptList percepts = new PerceptList();
                List<List<string>> results = new List<List<string>>();
                string oid = objectID.ToString();

                for (int i = 0; i < items.Count; i++) {
                    if (items[i] is InventoryFolder) {
                        InventoryFolder folder = (InventoryFolder)items[i];
                        results.Add(percepts.Add("objfolder", folder.UUID.ToString(), oid, folder.Name));
                    } else {
                        InventoryItem item = (InventoryItem)items[i];
                        results.Add(percepts.Add("objitem", item.UUID.ToString(), oid, item.Name,
                                        item.Description.ToString(),
                                        item.InventoryType.ToString(),
                                        item.AssetType.ToString()));
                    }
                }
                if (percepts.Count > 0) {
                    Agent.PerceptsBase.Update(percepts);
                }
                return VRAgentController.ok("obj inventory list", results);
            } else {
                return VRAgentController.nulcoll("no inventory in obj");
            }
        }

        public List<List<string>> LookForRegionsAction()
        {
            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            Agent.Grid.RequestMainlandSims(GridLayerType.Objects);
            lock (Agent.Network.Simulators) {
                for (int i = 0; i < Agent.Network.Simulators.Count; i++) {
                    results.Add(percepts.Add("region",
                                        Agent.Network.Simulators[i].RegionID.ToString(),
                                        Agent.Network.Simulators[i].Name.ToString()));
                    percepts.Add("name", Agent.Network.Simulators[i].RegionID.ToString(),
                                        Agent.Network.Simulators[i].Name.ToString());
                }
                percepts.Add("regions_count", UUID.Zero.ToString(),
                            Agent.Network.Simulators.Count.ToString());
            }
            if (percepts.Count > 0)
                Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("regions list", results);
        }

        public List<string> createObjPercepts(Primitive p, Vector3 mypos, PerceptList percepts)
        {
            string pid = p.ID.ToString();
            string typ = p.PrimData.PCode.ToString().ToLower();
            string subtyp =
                p.PrimData.PCode == PCode.Prim ?
                    p.Type.ToString().ToLower() :
                    (p.PrimData.PCode == PCode.Tree || p.PrimData.PCode == PCode.NewTree ?
                        p.TreeSpecies.ToString().ToLower() :
                        (p.PrimData.PCode == PCode.Grass ?
                            ((Grass)p.TreeSpecies).ToString().ToLower() : ""));
            Vector3 objpos = p.Position;
            float dist = Vector3.Distance(objpos, mypos);
            Primitive.ObjectProperties prop = p.Properties;
            string name = (prop != null && prop.Name != null) ? prop.Name : "";
            List<string> result =
                percepts.Add("obj", pid, name, typ, subtyp, dist.ToString(),
                    p.Position.X.ToString(), p.Position.Y.ToString(), p.Position.Z.ToString(),
                    p.Scale.X.ToString(), p.Scale.Y.ToString(), p.Scale.Z.ToString());
            percepts.Add("dist", pid, dist.ToString());
            DoLookObj(pid, p, percepts);
            if (prop != null) {
                string descr = prop.Description != null ? prop.Description : "";
                percepts.Add("extra_props", pid, name, descr,
                                prop.CreatorID.ToString(),
                                prop.OwnerID.ToString(),
                                prop.CreationDate.ToString());
                DoLookObjExtraProps(pid, prop, percepts);
            }
            return result;
        }

        public List<List<string>> LookForObjChildrenAction(string objuid)
        {
            Vector3 mypos = Agent.Self.SimPosition;
            UUID oid;
            // First find local ID of objuid object
            if (!UUID.TryParse(objuid, out oid))
                return VRAgentController.nulcoll("param 1 error");
            Primitive obj = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                   delegate (Primitive prim) { return prim.ID == oid; }
            );
            if (obj == null)
                return VRAgentController.nulcoll("obj not found");

            // Then search for all children objects
            List<Primitive> prims = Agent.Network.CurrentSim.ObjectsPrimitives.FindAll(
                delegate (Primitive prim) { return (prim.ParentID == obj.LocalID); }
            );

            // After request properties of these objects
            // including name and description of object
            bool complete = RequestObjectProperties(prims, 250);
            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            // Create list of perceptions for object found in search 
            foreach (Primitive p in prims) {
                List<string> result = createObjPercepts(p, mypos, percepts);
                results.Add(result);
            }
            if (percepts.Count > 0)
                Agent.PerceptsBase.Update(percepts);
            if (!complete) {
                return VRAgentController.ok("retrieved children obj list with partial metadata", results);
            }
            return VRAgentController.ok("retrieved children obj list", results);
        }


        bool matchSearch(Primitive.ObjectProperties prop, string srchtxt,
                    int srchattr, int srchtyp, bool srchcase)
        {
            if (srchattr == 0 || srchtxt == null || srchtxt.Length==0) return true;
            string objattr;
            if (srchattr == 2) {
                if (prop == null || prop.Description == null) return (srchtyp > 4);
                objattr = (srchcase) ? prop.Description : prop.Description.ToLower();
            } else {
                if (prop == null || prop.Name == null) return (srchtyp > 4);
                objattr = (srchcase) ? prop.Name : prop.Name.ToLower();
            }
            switch (srchtyp) {
                // substring search
                case 1: if (objattr.Contains(srchtxt)) return true;
                    break;
                // startswith string search
                case 2: if (objattr.StartsWith(srchtxt)) return true;
                    break;
                // endswith string search
                case 3: if (objattr.EndsWith(srchtxt)) return true;
                    break;
                // equals string search
                case 4: if (objattr.Equals(srchtxt)) return true;
                    break;
                // diff string search
                case 5: if (!objattr.Equals(srchtxt)) return true;
                    break;
                // not substring search
                case 6: if (!objattr.Contains(srchtxt)) return true;
                    break;
                // not startswith string search
                case 7: if (!objattr.StartsWith(srchtxt)) return true;
                    break;
                // not endswith string search
                case 8: if (!objattr.EndsWith(srchtxt)) return true;
                    break;
                default: if (objattr.Contains(srchtxt)) return true;
                    break;
            }
            return false;
        }

        public List<List<string>> LookForObjsAction()
        {
            return LookForObjsAction(-1.0f, -1, -1, null, 0, 0, false);
        }


        public List<List<string>> LookForObjsByRadiusAction(int radius) {   
            float r = (float)(radius);
            return LookForObjsByRadiusAction(r);
        }
        public List<List<string>> LookForObjsByRadiusAction(string radius) {
            float r = float.Parse(radius);
            return LookForObjsByRadiusAction(r);
        }
        public List<List<string>> LookForObjsByRadiusAction(float radius) {
            return LookForObjsAction(radius, -1, -1, null, 0, 0, false);
        }



        public List<List<string>> LookForObjsByTypeAction(int radius, int typ, int subtyp) {
            float r = (float)(radius);
            return LookForObjsByTypeAction(r, typ, subtyp);
        }
        public List<List<string>> LookForObjsByTypeAction(string radius, int typ, 
                                        int subtyp) {
            float r = float.Parse(radius);
            return LookForObjsByTypeAction(r,typ,subtyp);
        }
        public List<List<string>> LookForObjsByTypeAction(string radius, string typ, 
                                        string subtyp) {
            float r = float.Parse(radius);
            int t = int.Parse(typ);
            int s = int.Parse(subtyp);
            return LookForObjsByTypeAction(r, t, s);
        }
        public List<List<string>> LookForObjsByTypeAction(float radius, int typ, int subtyp) {
            return LookForObjsAction(radius, typ, subtyp, null, 0, 0, false);
        }


        public List<List<string>> LookForObjsByNameAction(int radius, string srchtxt,
                                        int srchtyp, bool srchcase) {
            float r = (float)(radius);
            return LookForObjsByNameAction(r, srchtxt, srchtyp, srchcase);
        }
        public List<List<string>> LookForObjsByNameAction(string radius, string srchtxt,
                                        int srchtyp, bool srchcase) {
            float r = float.Parse(radius);
            return LookForObjsByNameAction(r, srchtxt, srchtyp, srchcase);
        }
        public List<List<string>> LookForObjsByNameAction(string radius, string srchtxt,
                                        string srchtyp, string srchcase)  {
            float r = float.Parse(radius);
            int st = int.Parse(srchtyp);
            bool sc = bool.Parse(srchcase);
            return LookForObjsByNameAction(r, srchtxt, st, sc);
        }
        public List<List<string>> LookForObjsByNameAction(float radius, string srchtxt,
                                        int srchtyp, bool srchcase)  {
            return LookForObjsAction(radius, -1, -1, srchtxt, 1, srchtyp, srchcase);
        }


        public List<List<string>> LookForObjsByDescrAction(int radius, string srchtxt,
                                        int srchtyp, bool srchcase)
        {
            float r = (float)(radius);
            return LookForObjsByDescrAction(r, srchtxt, srchtyp, srchcase);
        }
        public List<List<string>> LookForObjsByDescrAction(string radius, string srchtxt,
                                        int srchtyp, bool srchcase) {
            float r = float.Parse(radius);
            return LookForObjsByDescrAction(r, srchtxt, srchtyp, srchcase);
        }
        public List<List<string>> LookForObjsByDescrAction(string radius, string srchtxt,
                                        string srchtyp, string srchcase) {
            float r = float.Parse(radius);
            int st = int.Parse(srchtyp);
            bool sc = bool.Parse(srchcase);
            return LookForObjsByDescrAction(r, srchtxt, st, sc);
        }
        public List<List<string>> LookForObjsByDescrAction(float radius, string srchtxt,
                                        int srchtyp, bool srchcase) {
            return LookForObjsAction(radius, -1, -1, srchtxt, 2, srchtyp, srchcase);
        }


        int MAX_PROPS_REQ_SIZE = 100;
        int MS_PER_PROP_REQ_TIMEOUT = 100;


        public List<List<string>> LookForObjsAction(int radius, int typ, int subtyp,
                                    string srchtxt, int srchattr, int srchtyp, bool srchcase)
        {
            float r = (float)(radius);
            return LookForObjsAction(r, typ, subtyp, srchtxt, srchattr, srchtyp, srchcase);
        }

        public List<List<string>> LookForObjsAction(string radius, int typ, int subtyp,
                                    string srchtxt, int srchattr, int srchtyp, bool srchcase)
        {
            float r = float.Parse(radius);
            return LookForObjsAction(r, typ, subtyp, srchtxt, srchattr, srchtyp, srchcase);

        }

        public List<List<string>> LookForObjsAction(string radius, string typ, string subtyp,
                                    string srchtxt, string srchattr, string srchtyp, string srchcase)
        {
            float r = float.Parse(radius);
            int t = int.Parse(typ);
            int s = int.Parse(subtyp);
            int sa = int.Parse(srchattr);
            int st = int.Parse(srchtyp);
            bool sc = bool.Parse(srchcase);
            return LookForObjsAction(r, t, s, srchtxt, sa, st, sc);

        }
        public List<List<string>> LookForObjsAction(float radius, int typ, int subtyp, 
                                        string srchtxt, int srchattr, int srchtyp, bool srchcase)
        {
            Vector3 mypos = Agent.Self.SimPosition;
            if (srchtyp > 0 && srchattr > 0 && !srchcase)
                srchtxt = srchtxt.ToLower();

            // First search for all objects inside the search radius
            List<Primitive> prims = Agent.Network.CurrentSim.ObjectsPrimitives.FindAll(
                delegate (Primitive prim) {
                    Vector3 objpos = prim.Position;
                    // Search will not retrieve linked objects
                    if (prim.ParentID != 0)
                        return false;
                    // Search will not retrieve primitive objects without position
                    if (objpos == Vector3.Zero)
                        return false;
                    // Check if it is in radius, negative radius is ignored
                    if (radius<0.0 || Vector3.Distance(objpos, mypos) < radius) {
                        // It is in radius, check object type
                        if (typ < 0)
                            // Object type not defined, return true
                            return true;
                        if (typ == 1 && (prim.PrimData.PCode == PCode.Prim)) {
                            // Object type is primitive, check object subtype
                            if (subtyp<0 || subtyp==(int)prim.Type)
                                // Object subtype not defined or it is OK, return true
                                return true;
                        }
                        if (typ == 2 && (prim.PrimData.PCode == PCode.Tree)) {
                            // Object type is tree, check object subtype
                            if (subtyp < 0 || subtyp == (int)prim.TreeSpecies)
                                // Object subtype not defined or it is OK, return true
                                return true;
                        }
                        if (typ == 3 && (prim.PrimData.PCode == PCode.Grass)) {
                            // Object type is grass, check object subtype
                            if (subtyp < 0 || subtyp == (int)prim.TreeSpecies)
                                // Object subtype not defined or it is OK, return true
                                return true;
                        }
                    }
                    return false;
                }
            );

            // Then request properties of these objects
            // including name and description of object
            bool complete = RequestObjectProperties(prims, MS_PER_PROP_REQ_TIMEOUT);

            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            foreach (Primitive p in prims) {
                string pid = p.ID.ToString();
                // Check if object name or description match search string
                // (only if some type of search was specified)
                if (!matchSearch(p.Properties, srchtxt, srchattr, srchtyp, srchcase))
                    continue;
                List<string> result = createObjPercepts(p, mypos, percepts);
                results.Add(result);
            }
            if (percepts.Count > 0)
                Agent.PerceptsBase.Update(percepts);
            if (!complete) {
                Console.WriteLine("retrieved objects list with partial metadata");
                return VRAgentController.ok("retrieved objects list with partial metadata", results);
            }
            Console.WriteLine("retrieved objects list");
            return VRAgentController.ok("retrieved objects list",results);
        }

        private bool RequestObjectProperties(List<Primitive> objects, int msPerRequest)
        {
            // Create an array of the local IDs of all the prims we are requesting properties for
            uint[] localids = new uint[objects.Count];
            int i = 0;
            bool complete = true;
            Dictionary<UUID, Primitive> primsWaiting = new Dictionary<UUID, Primitive>();
            AutoResetEvent allObjPropsReceived = new AutoResetEvent(false);

            EventHandler<ObjectPropertiesEventArgs> objPropsReply_handler =
                delegate (object sender, ObjectPropertiesEventArgs e) {
                    lock (primsWaiting) {
                        Primitive prim;
                        if (primsWaiting.TryGetValue(e.Properties.ObjectID, out prim)) {
                            prim.Properties = e.Properties;
                        }
                        primsWaiting.Remove(e.Properties.ObjectID);

                        if (primsWaiting.Count == 0)
                            allObjPropsReceived.Set();
                    }
                };

            Agent.Objects.ObjectProperties += objPropsReply_handler;
            while (i < objects.Count) {
                int j = 0;
                lock (primsWaiting) {
                    primsWaiting.Clear();
                    while (j < MAX_PROPS_REQ_SIZE && i < objects.Count) {
                        localids[i] = objects[i].LocalID;
                        primsWaiting.Add(objects[i].ID, objects[i]);
                        i++;
                        j++;
                    }
                }
                Agent.Objects.SelectObjects(Agent.Network.CurrentSim, localids);
                if (!allObjPropsReceived.WaitOne(2000 + msPerRequest * j, false)) {
                    Console.WriteLine("Unable to retrieve properties of following objects:");
                    lock (primsWaiting) {
                        foreach (UUID uuid in primsWaiting.Keys)
                            Console.WriteLine(uuid);
                    }
                    complete = false;
                }
            }
            Agent.Objects.ObjectProperties -= objPropsReply_handler;
            return complete;
        }


        public List<List<string>> LookForAvatarsAction()
        {
            Vector3 mypos = Agent.Self.SimPosition;
            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            int avcount =0;
            lock (Agent.Network.Simulators) {
                for (int i = 0; i < Agent.Network.Simulators.Count; i++) {
                    Agent.Network.Simulators[i].ObjectsAvatars.ForEach(
                        delegate (Avatar av) {
                            avcount++;
                            string avid = av.ID.ToString();
                            Vector3 avpos = av.Position;
                            float dist = Vector3.Distance(avpos, mypos);
                            results.Add(percepts.Add("avatar",  avid, 
                                    av.Name, 
                                    dist.ToString(),
                                    av.Position.X.ToString() ,
                                    av.Position.Y.ToString() ,
                                    av.Position.Z.ToString() ));
                            percepts.Add("name", avid, av.Name.ToString());
                            percepts.Add("dist", avid, dist.ToString());
                            percepts.Add("region", avid, Agent.Network.Simulators[i].Name.ToString());
                            percepts.Add("region_id", avid, Agent.Network.Simulators[i].RegionID.ToString());
                            percepts.Add("pos", avid,
                                    av.Position.X.ToString(),
                                    av.Position.Y.ToString(),
                                    av.Position.Z.ToString());
                            percepts.Add("local_id", avid, av.LocalID.ToString());

                        }
                    );
                }
            }
            percepts.Add("avatars_count", UUID.Zero.ToString(),  avcount.ToString() );
            if (percepts.Count > 0)
                Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("avatars list",results);
        }



    }
}

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
//   Class:     ModificationActions 
//   Purpose:   To implement actions for the agent to be able to modify
//              object on virtual world 
//   Author:    João Carlos Gluz 
//
//***********************************************************************

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
#if USE_LIBREMETAVERSE_VR_LIB
using LibreMetaverse;
using LibreMetaverse.StructuredData;
using LibreMetaverse.Assets;
#else
using OpenMetaverse;
using OpenMetaverse.StructuredData;
using OpenMetaverse.Assets;
#endif

#if USE_LIBREMETAVERSE_VR_LIB
namespace LibreMetaverse
#else
namespace OpenMetaverse
#endif
{
    public class ModificationActions : Actions
    {

        public ModificationActions(VRAgentController agent) : base(agent)
        {
        }

        private bool CheckConvertIDArg(string argobjuid, out UUID objRootPrimUID, out Primitive objRootPrim)
        {
            objRootPrim = null;
            if (!UUID.TryParse(argobjuid, out objRootPrimUID))
                return VRAgentController.fail("arg 1 syntax error");
            // Find the requested prim
            UUID searchUID = objRootPrimUID;
            objRootPrim = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim) { return prim.ID == searchUID; });
            if (objRootPrim == null)
                // Not found the prim/object
                return VRAgentController.fail("obj not found");
            if (objRootPrim.ParentID != 0)
                // Prim is not root
                return VRAgentController.fail("obj is not root");
            return true;
        }

        private bool CheckObjPermissions(UUID objRootPrimUID)
        {
            AutoResetEvent gotPermissionsEvent = new AutoResetEvent(false);
            Primitive.ObjectProperties rcvdObjProperties = null;
            bool gotPermissions = false;
            EventHandler<ObjectPropertiesFamilyEventArgs> objPropsFamilyReply_handler =
                delegate (object sender, ObjectPropertiesFamilyEventArgs e){
                    rcvdObjProperties = new Primitive.ObjectProperties();
                    rcvdObjProperties.SetFamilyProperties(e.Properties);
                    gotPermissions = true;
                    gotPermissionsEvent.Set();
                };

            Agent.Objects.ObjectPropertiesFamily += objPropsFamilyReply_handler;
            Agent.Objects.RequestObjectPropertiesFamily(
                            Agent.Network.CurrentSim, objRootPrimUID);
            gotPermissionsEvent.WaitOne(1000 * 10, false);
            Agent.Objects.ObjectPropertiesFamily -= objPropsFamilyReply_handler;
            if (!gotPermissions || rcvdObjProperties == null) {
                // Not allowed
                return VRAgentController.fail("not allowed");
            } else {
                if (rcvdObjProperties.OwnerID != Agent.Self.AgentID) {
                    // Not owned
                    return VRAgentController.fail("not owner");
                }
            }
            return true;
        }

        public bool MoveObjAction(string argobjuid, int argx, int argy, int argz)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            float z = (float)(argz);
            return MoveObjAction(argobjuid, x, y, z);
        }

        public bool MoveObjAction(string argobjuid, string argx, string argy, string argz)
        {
            float x = float.Parse(argx);
            float y= float.Parse(argy);
            float z = float.Parse(argz);
            return MoveObjAction(argobjuid, x, y, z);
        }

        public bool MoveObjAction(string argobjuid, float argx, float argy, float argz)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            // Check arguments first
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            // Now check for permissions
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            // Change object's property
            Vector3 newPosition = new Vector3(argx, argy, argz);
            Agent.Objects.SetPosition(Agent.Network.CurrentSim,
                        objRootPrim.LocalID, newPosition, false);
            return VRAgentController.ok("moving obj");
        }

        public bool ResizeObjAction(string argobjuid, int argx, int argy, int argz)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            float z = (float)(argz);
            return ResizeObjAction(argobjuid, x, y, z);
        }

        public bool ResizeObjAction(string argobjuid, string argx, string argy, string argz)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            float z = float.Parse(argz);
            return ResizeObjAction(argobjuid, x, y, z);
        }

        public bool ResizeObjAction(string argobjuid, float argx, float argy, float argz)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            // Check arguments first
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            // Now check for permissions
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            // Change object's property
            Vector3 newScale = new Vector3(argx, argy, argz);
            Agent.Objects.SetScale(Agent.Network.CurrentSim,
                        objRootPrim.LocalID, newScale, false, true);
            return VRAgentController.ok("resizing obj");
        }

        public bool RotateObjAction(string argobjuid, string argunit, 
                                    int argroll, int argpitch, int argyaw)
        {
            float roll = (float)(argroll);
            float pitch = (float)(argpitch);
            float yaw = (float)(argyaw);
            return RotateObjAction(argobjuid, argunit, roll, pitch, yaw);
        }

        public bool RotateObjAction(string argobjuid, string argunit, 
                                    string argroll, string argpitch, string argyaw)
        {
            float roll = float.Parse(argroll);
            float pitch = float.Parse(argpitch);
            float yaw = float.Parse(argyaw);
            return RotateObjAction(argobjuid, argunit, roll, pitch, yaw);
        }


        public bool RotateObjAction(string argobjuid, string argunit, 
                                    float argroll, float argpitch, float argyaw)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            // Check arguments first
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            // Now check for permissions
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            // Change object's property
            float roll; float pitch; float yaw;
            if (argunit.ToLower() == "dg") {
                roll = (argroll / 180.0f) * (float)Math.PI;
                pitch = (argpitch / 180.0f) * (float)Math.PI;
                yaw = (argyaw / 180.0f) * (float)Math.PI;
            } else if (argunit.ToLower() == "rad") {
                roll = argroll;
                pitch = argpitch;
                yaw = argyaw;
            } else
                return VRAgentController.fail("param 2 syntax error");
            Quaternion newRot = Quaternion.CreateFromEulers(roll, pitch, yaw);
            Agent.Objects.SetRotation(Agent.Network.CurrentSim,
                        objRootPrim.LocalID, newRot, false);
            return VRAgentController.ok("rotating obj");
        }

        public bool SetNameAction(string argobjuid, string argname)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            // Check arguments first
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            // Now check for permissions
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            // Change object's property
            Agent.Objects.SetName(Agent.Network.CurrentSim,
                        objRootPrim.LocalID, argname);
            return VRAgentController.ok("setting obj name");
        }

        public bool SetDescrAction(string argobjuid, string argdescr)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            // Check arguments first
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            // Now check for permissions
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            // Change object's property
            Agent.Objects.SetDescription(Agent.Network.CurrentSim,
                        objRootPrim.LocalID, argdescr);
            return VRAgentController.ok("setting obj descr");
        }

        public bool SetMaterialAction(string argobjuid, string argmat)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            Material matType;

            // Check arguments first
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            // Now check for permissions
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            // Change object's property
            if (!MatTypes.TryGetValue(argmat.ToLower(), out matType))
                return VRAgentController.fail("param 2 syntax error");
            Agent.Objects.SetMaterial(Agent.Network.CurrentSim,
                        objRootPrim.LocalID, matType);
            return VRAgentController.ok("setting obj material");
        }

        public bool SetFlagsAction(string argobjuid, bool argphys,
                            bool argtemp, bool argphant, bool argshad)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            // Check arguments first
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            // Now check for permissions
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            // Change object's property
            Agent.Objects.SetFlags(Agent.Network.CurrentSim,
                        objRootPrim.LocalID, argphys, argtemp, argphant, argshad);
            return VRAgentController.ok("setting obj flags");
        }

        public bool PaintObjAction(string argobjuid, string argtextuid)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            UUID textureID;
            // Check arguments first
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            // Now check for permissions
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            if (!UUID.TryParse(argtextuid, out textureID))
                return VRAgentController.fail("param 2 syntax error");
            // Change object's property
            Primitive.TextureEntry textures = new Primitive.TextureEntry(textureID);
            Agent.Objects.SetTextures(Agent.Network.CurrentSim, objRootPrim.LocalID, textures);
            return VRAgentController.ok("painting obj");
        }

        public bool SelObjAction(string argobjuid)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            Agent.Objects.SelectObject(Agent.Network.CurrentSim,objRootPrim.LocalID,false);
            return VRAgentController.ok("selecting obj");
        }


        public bool DeselObjAction(string argobjuid)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            Agent.Objects.DeselectObject(Agent.Network.CurrentSim, objRootPrim.LocalID);
            return VRAgentController.ok("deselecting obj");
        }


        public bool ClickObjAction(string argobjuid)
        {
            UUID objRootPrimUID;
            Primitive objRootPrim;
            if (!CheckConvertIDArg(argobjuid, out objRootPrimUID, out objRootPrim))
                return false;
            if (!CheckObjPermissions(objRootPrimUID))
                return false;
            Agent.Objects.ClickObject(Agent.Network.CurrentSim, objRootPrim.LocalID);
            return VRAgentController.ok("selecting obj");
        }


        public bool CheckConvertRezArgs(string argtype, string argsubtype,
                                        out RezActionObjType rezObjType,
                                        out PrimType rezObjPrimType,
                                        out Grass rezObjGrassType,
                                        out Tree rezObjTreeType,
                                        out InventoryItem rezObjFromItem)
        {
            rezObjType = RezActionObjType.invalid;
            rezObjPrimType = PrimType.Unknown;
            rezObjGrassType = Grass.Grass0;
            rezObjTreeType = Tree.Eucalyptus;
            rezObjFromItem = null;
            if (argtype == "prim") {
                if (!PrimTypes.TryGetValue(argsubtype, out rezObjPrimType))
                    return VRAgentController.fail("param 2 syntax error");
                rezObjType = RezActionObjType.prim;
            } else if (argtype == "tree") {
                if (!TreeTypes.TryGetValue(argsubtype, out rezObjTreeType))
                    return VRAgentController.fail("param 2 syntax error");
                rezObjType = RezActionObjType.tree;
            } else if (argtype == "grass") {
                if (!GrassTypes.TryGetValue(argsubtype, out rezObjGrassType))
                    return VRAgentController.fail("param 2 syntax error");
                rezObjType = RezActionObjType.grass;
            } else if (argtype == "item") {
                InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
                rezObjFromItem = FindItem(rootFolder, "/", argsubtype);
                if (rezObjFromItem == null)
                    // Inventory item not found
                    return VRAgentController.fail("item not found");
                rezObjType = RezActionObjType.item;
            } else {
                return VRAgentController.fail("param 1 syntax error");
            }
            return true;
        }

        public string RezObjAction(string argname, string argtype, string argsubtype,
                                    int argx, int argy, int argz)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            float z = (float)(argz);
            return RezObjAction(argname, argtype, argsubtype, x, y, z);
        }

        public string RezObjAction(string argname, string argtype, string argsubtype,
                                    string argx, string argy, string argz)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            float z = float.Parse(argz);
            return RezObjAction(argname, argtype, argsubtype, x, y, z);
        }

        public string RezObjAction(string argname, string argtype, string argsubtype,
                                    float argx, float argy, float argz)
        {
            RezActionObjType rezObjType;
            PrimType rezObjPrimType;
            Grass rezObjGrassType;
            Tree rezObjTreeType;
            InventoryItem rezObjFromItem;
            if (!CheckConvertRezArgs(argtype, argsubtype, 
                                    out rezObjType, out rezObjPrimType, out rezObjGrassType, 
                                    out rezObjTreeType, out rezObjFromItem)) {
                return null;
            }
            Vector3 rezObjPos = new Vector3(argx, argy, argz);
            Vector3 rezObjSize = new Vector3(0.5f, 0.5f, 0.5f);
            Quaternion rezObjRot = Quaternion.Identity;
            return DoRezObj(argname, rezObjType, rezObjPrimType, rezObjGrassType,
                            rezObjTreeType, rezObjFromItem, rezObjPos, rezObjSize, 
                            rezObjRot);
        }

        public string RezObjSizeAction(string argname, string argtype, string argsubtype,
                                    int argx, int argy, int argz,
                                    int argsx, int argsy, int argsz)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            float z = (float)(argz);
            float sx = (float)(argsx);
            float sy = (float)(argsy);
            float sz = (float)(argsz);
            return RezObjSizeAction(argname, argtype, argsubtype, x, y, z, sx, sy, sz);
        }

        public string RezObjSizeAction(string argname, string argtype, string argsubtype,
                                    string argx, string argy, string argz,
                                     string argsx, string argsy, string argsz)
       {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            float z = float.Parse(argz);
            float sx = float.Parse(argsx);
            float sy = float.Parse(argsy);
            float sz = float.Parse(argsz);
            return RezObjSizeAction(argname, argtype, argsubtype, x, y, z, sx, sy, sz);
        }

        public string RezObjSizeAction(string argname, string argtype, string argsubtype,
                float argx, float argy, float argz,
                float argsx, float argsy, float argsz)
        {
            RezActionObjType rezObjType;
            PrimType rezObjPrimType;
            Grass rezObjGrassType;
            Tree rezObjTreeType;
            InventoryItem rezObjFromItem;
            if (!CheckConvertRezArgs(argtype, argsubtype,
                                    out rezObjType, out rezObjPrimType, out rezObjGrassType,
                                    out rezObjTreeType, out rezObjFromItem)) {
                return null;
            }
            Vector3 rezObjPos = new Vector3(argx, argy, argz);
            Vector3 rezObjSize = new Vector3(argsx, argsy, argsz);
            Quaternion rezObjRot = Quaternion.Identity;
            return DoRezObj(argname, rezObjType, rezObjPrimType, rezObjGrassType,
                            rezObjTreeType, rezObjFromItem, rezObjPos, rezObjSize,
                            rezObjRot);
        }

        public string RezObjRotAction(string argname, string argtype, string argsubtype,
                                    int argx, int argy, int argz, string argrotunit,
                                    int argroll, int argpitch, int argyaw)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            float z = (float)(argz);
            float roll = (float)(argroll);
            float pitch = (float)(argpitch);
            float yaw = (float)(argyaw);
            return RezObjRotAction(argname, argtype, argsubtype, x, y, z,
                                    argrotunit, roll, pitch, yaw);
        }

        public string RezObjRotAction(string argname, string argtype, string argsubtype,
                                    string argx, string argy, string argz, string argrotunit,
                                    string argroll, string argpitch, string argyaw)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            float z = float.Parse(argz);
            float roll = float.Parse(argroll);
            float pitch = float.Parse(argpitch);
            float yaw = float.Parse(argyaw);
            return RezObjRotAction(argname, argtype, argsubtype, x, y, z,
                                    argrotunit, roll, pitch, yaw);
        }

        public string RezObjRotAction(string argname, string argtype, string argsubtype,
                        float argx, float argy, float argz, string argrotunit, 
                        float argroll, float argpitch, float argyaw)
        {
            RezActionObjType rezObjType;
            PrimType rezObjPrimType;
            Grass rezObjGrassType;
            Tree rezObjTreeType;
            InventoryItem rezObjFromItem;
            if (!CheckConvertRezArgs(argtype, argsubtype,
                                    out rezObjType, out rezObjPrimType, out rezObjGrassType,
                                    out rezObjTreeType, out rezObjFromItem)) {
                return null;
            }
            Vector3 rezObjPos = new Vector3(argx, argy, argz);
            Vector3 rezObjSize = new Vector3(0.5f, 0.5f, 0.5f);
            float roll; float pitch; float yaw;
            if (argrotunit.ToLower() == "dg") {
                roll = (argroll / 180.0f) * (float)Math.PI;
                pitch = (argpitch / 180.0f) * (float)Math.PI;
                yaw = (argyaw / 180.0f) * (float)Math.PI;
            } else if (argrotunit.ToLower() == "rad") {
                roll = argroll;
                pitch = argpitch;
                yaw = argyaw;
            } else
                return VRAgentController.nulstr("rotation is not dg or rad");
            Quaternion rezObjRot = Quaternion.CreateFromEulers(roll, pitch, yaw);
            return DoRezObj(argname, rezObjType, rezObjPrimType, rezObjGrassType,
                           rezObjTreeType, rezObjFromItem, rezObjPos, rezObjSize,
                           rezObjRot);
        }

        public string RezObjSizeRotAction(string argname, string argtype, string argsubtype,
                                    int argx, int argy, int argz, string argrotunit,
                                    int argsx, int argsy, int argsz,
                                    int argroll, int argpitch, int argyaw)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            float z = (float)(argz);
            float sx = (float)(argsx);
            float sy = (float)(argsy);
            float sz = (float)(argsz);
            float roll = (float)(argroll);
            float pitch = (float)(argpitch);
            float yaw = (float)(argyaw);
            return RezObjSizeRotAction(argname, argtype, argsubtype, x, y, z,
                                    sx, sy, sz, argrotunit, roll, pitch, yaw);
        }

        public string RezObjSizeRotAction(string argname, string argtype, string argsubtype,
                                    string argx, string argy, string argz, string argrotunit,
                                    string argsx, string argsy, string argsz,
                                    string argroll, string argpitch, string argyaw)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            float z = float.Parse(argz);
            float sx = float.Parse(argsx);
            float sy = float.Parse(argsy);
            float sz = float.Parse(argsz);
            float roll = float.Parse(argroll);
            float pitch = float.Parse(argpitch);
            float yaw = float.Parse(argyaw);
            return RezObjSizeRotAction(argname, argtype, argsubtype, x, y, z,
                                    sx, sy, sz, argrotunit, roll, pitch, yaw);
        }

        public string RezObjSizeRotAction(string argname, string argtype, string argsubtype,
                        float argx, float argy, float argz,
                        float argsx, float argsy, float argsz,
                        string argrotunit, float argroll, float argpitch, float argyaw )
        {
            RezActionObjType rezObjType;
            PrimType rezObjPrimType;
            Grass rezObjGrassType;
            Tree rezObjTreeType;
            InventoryItem rezObjFromItem;
            if (!CheckConvertRezArgs(argtype, argsubtype,
                                    out rezObjType, out rezObjPrimType, out rezObjGrassType,
                                    out rezObjTreeType, out rezObjFromItem)) {
                return null;
            }
            Vector3 rezObjPos = new Vector3(argx, argy, argz);
            Vector3 rezObjSize = new Vector3(argsx, argsy, argsz);
            float roll; float pitch; float yaw;
            if (argrotunit.ToLower() == "dg") {
                roll = (argroll / 180.0f) * (float)Math.PI;
                pitch = (argpitch / 180.0f) * (float)Math.PI;
                yaw = (argyaw / 180.0f) * (float)Math.PI;
            } else if (argrotunit.ToLower() == "rad") {
                roll = argroll;
                pitch = argpitch;
                yaw = argyaw;
            } else
                return VRAgentController.nulstr("rotation is not dg or rad");
            Quaternion rezObjRot = Quaternion.CreateFromEulers(roll, pitch,yaw);
            return DoRezObj(argname, rezObjType, rezObjPrimType, rezObjGrassType,
                            rezObjTreeType, rezObjFromItem, rezObjPos, rezObjSize,
                            rezObjRot);
        }


        public string DoRezObj( string rezObjName,
                                RezActionObjType rezObjType, 
                                PrimType rezObjPrimType,
                                Grass rezObjGrassType,
                                Tree rezObjTreeType,
                                InventoryItem rezObjFromItem,
                                Vector3 rezObjPos,
                                Vector3 rezObjSize,
                                Quaternion rezObjRot)
        {
            bool newprimok = false;
            bool rezzingObj= false;
            UUID rezObjID = UUID.Zero;
            AutoResetEvent newPrimDoneEvent = new AutoResetEvent(false);

            EventHandler<PrimEventArgs> onNewPrim_handler =
                delegate (object sender, PrimEventArgs primEvMsg)
                {
                    Primitive prim = primEvMsg.Prim;
                    if (!rezzingObj || (prim.Flags & PrimFlags.CreateSelected) == 0)
                        return; // We received an update for an object we didn't create
                    if (!String.IsNullOrEmpty(rezObjName))
                        Agent.Objects.SetName(Agent.Network.CurrentSim, prim.LocalID, 
                                               rezObjName);
                    newPrimDoneEvent.Set();
                    rezObjID = prim.ID;
                };

            switch (rezObjType) {
                case RezActionObjType.prim:
                    rezzingObj = true;
                    Agent.Objects.ObjectUpdate += onNewPrim_handler;
                    Agent.Objects.AddPrim(Agent.Network.CurrentSim,
                                    ObjectManager.BuildBasicShape(rezObjPrimType),
                                    UUID.Zero,
                                    rezObjPos, rezObjSize, rezObjRot);
                    break;
                case RezActionObjType.tree:
                    rezzingObj= true;
                    Agent.Objects.ObjectUpdate += onNewPrim_handler;
                    Agent.Objects.AddTree(Agent.Network.CurrentSim,
                                rezObjSize, rezObjRot, rezObjPos,
                                rezObjTreeType, UUID.Zero, false, PrimFlags.CreateSelected);
                    break;
                case RezActionObjType.grass:
                    rezzingObj = true;
                    Agent.Objects.ObjectUpdate += onNewPrim_handler;
                    Agent.Objects.AddGrass(Agent.Network.CurrentSim,
                                rezObjSize, rezObjRot, rezObjPos,
                                rezObjGrassType, UUID.Zero, PrimFlags.CreateSelected);
                    break;
                case RezActionObjType.item:
                    rezzingObj = true;
                    Agent.Objects.ObjectUpdate += onNewPrim_handler;
                    Agent.Inventory.RequestRezFromInventory(Agent.Network.CurrentSim,
                                rezObjRot, rezObjPos, rezObjFromItem, Agent.Self.ActiveGroup,
                                UUID.Random(), true);
                    break;

                default:
                    return VRAgentController.nulstr("invalid rez type");

            }
            newprimok = newPrimDoneEvent.WaitOne(10000, false);
            Agent.Objects.ObjectUpdate -= onNewPrim_handler;
            if (!newprimok) {
                return VRAgentController.nulstr("timeout on rez confirmation");
            }
            return VRAgentController.ok("rezzing obj", rezObjID.ToString());
        }



        InventoryItem FindItem(InventoryFolder fold, string basepath, string itempath)
        {
            List<InventoryBase> contents =
                    Agent.Inventory.FolderContents(
                        fold.UUID, Agent.Self.AgentID,
                        true, true, InventorySortOrder.ByName, 3000);
            if (contents == null)
                return null;
            foreach (InventoryBase i in contents) {
                string name = i.Name.Replace("'", "''");
                string basepath1 = basepath + name;
                //				Console.WriteLine("itempath="+itempath+" basepath1="+basepath1);
                if (i is InventoryItem) {
                    if (itempath == basepath1) {
                        return (InventoryItem)i;
                    }
                } else if (i is InventoryFolder) {
                    InventoryFolder folder = (InventoryFolder)i;
                    InventoryItem item = FindItem(folder, basepath1 + "/", itempath);
                    if (item != null) {
                        return item;
                    }
                }
            };
            return null;
        }

        public bool DerezObjAction(string argobjuid)
        {
            UUID objUID;

            if (UUID.TryParse(argobjuid, out objUID)) {
                Primitive target = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim) { return prim.ID == objUID; }
                );

                if (target != null) {
                    uint objLocalID = target.LocalID;
                    Agent.Inventory.RequestDeRezToInventory(
                                objLocalID, DeRezDestination.TrashFolder,
                                Agent.Inventory.FindFolderForType(AssetType.TrashFolder),
                                UUID.Random());
                    return VRAgentController.ok("derezzing obj");
                } else {
                    return VRAgentController.fail("obj not found");
                }
            } else {
                return VRAgentController.fail("param 1 syntax error");
            }
        }

        UUID FindFolder(InventoryFolder f, string basepath, string path)
        {
            List<InventoryBase> contents = Agent.Inventory.FolderContents(f.UUID, Agent.Self.AgentID,
                true, true, InventorySortOrder.ByName, 3000);

            if (contents == null)
                return UUID.Zero;
            if (basepath == path)
                return f.UUID;
            else {
                if (contents == null)
                    return UUID.Zero;
                foreach (InventoryBase i in contents) {
                    string name = i.Name.Replace("'", "''");
                    if (i is InventoryFolder) {
                        InventoryFolder folder = (InventoryFolder)i;
                        string basepath1 = basepath + name + "/";
                        UUID ff = FindFolder(folder, basepath1, path);
                        if (!ff.Equals(UUID.Zero))
                            return ff;
                    }
                };
                return UUID.Zero;
            }
        }

        public bool TakeObjAction(string argobjuid, string foldname)
        {
            UUID objUID;

            if (UUID.TryParse(argobjuid, out objUID)) {
                Primitive target = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim) { return prim.ID == objUID; }
                );

                if (target != null) {
                    InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
                    UUID foldID = FindFolder(rootFolder, "/", foldname);
                    if (foldID == UUID.Zero) {
                        return VRAgentController.fail("folder not found");
                    }
                    uint objLocalID = target.LocalID;
                    Agent.Inventory.RequestDeRezToInventory(
                                objLocalID, DeRezDestination.AgentInventoryTake,
                                foldID, UUID.Random());
                    return VRAgentController.ok("derezzing obj");
                } else {
                    return VRAgentController.fail("obj not found");
                }
            } else {
                return VRAgentController.fail("param 1 syntax error");
            }
        }

        public bool TouchAction(string argobjuid)
        {
            UUID targetUID;
            Primitive targetPrim;
            if (UUID.TryParse(argobjuid, out targetUID)) {
                targetPrim = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim)
                    {
                        return prim.ID == targetUID;
                    }
                );
                if (targetPrim != null) {
                    Agent.Self.Touch(targetPrim.LocalID);
                    return VRAgentController.ok("touching obj");
                }
            }
            return VRAgentController.fail("obj not found");
        }

        public bool GrabAction(string argobjuid)
        {
            UUID targetUID;
            Primitive targetPrim;
            if (UUID.TryParse(argobjuid, out targetUID)) {
                targetPrim = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim)
                    {
                        return prim.ID == targetUID;
                    }
                );
                if (targetPrim != null) {
                    Agent.Self.Grab(targetPrim.LocalID);
                    return VRAgentController.ok("grabbing obj");
                }
            }
            return VRAgentController.fail("obj not found");
        }

        public bool DeGrabAction(string argobjuid)
        {
            UUID targetUID;
            Primitive targetPrim;
            if (UUID.TryParse(argobjuid, out targetUID)) {
                targetPrim = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                    delegate (Primitive prim)
                    {
                        return prim.ID == targetUID;
                    }
                );
                if (targetPrim != null) {
                    Agent.Self.DeGrab(targetPrim.LocalID);
                    return VRAgentController.ok("degrabbing obj");
                }
            }
            return VRAgentController.fail("obj not found");
        }




        private enum ImporterState
        {
            RezzingParent,
            RezzingChildren,
            Linking,
            Idle
        }

        private class Linkset
        {
            public Primitive RootPrim;
            public List<Primitive> Children = new List<Primitive>();
            public Linkset()
            {
                RootPrim = new Primitive();
            }
            public Linkset(Primitive rootPrim)
            {
                RootPrim = rootPrim;
            }
        }


        public bool ImportObjectAction(string objfile, int argx, int argy, int argz)
        {
            float x = (float)(argx);
            float y = (float)(argy);
            float z = (float)(argz);
            return ImportObjectAction(objfile, x, y, z);
        }

        public bool ImportObjectAction(string objfile, string argx, string argy, string argz)
        {
            float x = float.Parse(argx);
            float y = float.Parse(argy);
            float z = float.Parse(argz);
            return ImportObjectAction(objfile, x, y, z);
        }

        public bool ImportObjectAction(string objfile, float x, float y, float z)
        {
            Primitive currentPrim = null;
            Vector3 currentPosition = Vector3.Zero;
            AutoResetEvent primDoneEvent = new AutoResetEvent(false);
            List<Primitive> primsCreated = null;
            List<uint> linkQueue = null;
            uint rootLocalID = 0;
            ImporterState importingState = ImporterState.Idle;
            Vector3 importObjPos = new Vector3(x, y, z);
            string xml;
            List<Primitive> prims;

            EventHandler<PrimEventArgs> onNewPrim_handler =
                delegate (object sender, PrimEventArgs e)
                {
                    Primitive prim = e.Prim;

                    if ((prim.Flags & PrimFlags.CreateSelected) == 0)
                        return; // We received an update for an object we didn't create

                    switch (importingState) {
                        case ImporterState.RezzingParent:
                            rootLocalID = prim.LocalID;
                            goto case ImporterState.RezzingChildren;
                        case ImporterState.RezzingChildren:
                            if (!primsCreated.Contains(prim)) {
                                Console.WriteLine("Setting properties for " + prim.LocalID);
                                // TODO: Is there a way to set all of this at once, and update more ObjectProperties stuff?
                                Agent.Objects.SetPosition(e.Simulator, prim.LocalID, currentPosition);
                                Agent.Objects.SetTextures(e.Simulator, prim.LocalID, currentPrim.Textures);
                                if (currentPrim.Light != null && currentPrim.Light.Intensity > 0) {
                                    Agent.Objects.SetLight(e.Simulator, prim.LocalID, currentPrim.Light);
                                }
                                if (currentPrim.Flexible != null) {
                                    Agent.Objects.SetFlexible(e.Simulator, prim.LocalID, currentPrim.Flexible);
                                }
                                if (currentPrim.Sculpt != null && currentPrim.Sculpt.SculptTexture != UUID.Zero) {
                                    Agent.Objects.SetSculpt(e.Simulator, prim.LocalID, currentPrim.Sculpt);
                                }
                                if (currentPrim.Properties != null && !String.IsNullOrEmpty(currentPrim.Properties.Name)) {
                                    Agent.Objects.SetName(e.Simulator, prim.LocalID, currentPrim.Properties.Name);
                                }
                                if (currentPrim.Properties != null && !String.IsNullOrEmpty(currentPrim.Properties.Description)) {
                                    Agent.Objects.SetDescription(e.Simulator, prim.LocalID, currentPrim.Properties.Description);
                                }
                                primsCreated.Add(prim);
                                primDoneEvent.Set();
                            }
                            break;
                        case ImporterState.Linking:
                            lock (linkQueue) {
                                int index = linkQueue.IndexOf(prim.LocalID);
                                if (index != -1) {
                                    linkQueue.RemoveAt(index);
                                    if (linkQueue.Count == 0)
                                        primDoneEvent.Set();
                                }
                            }
                            break;
                    }
                };


            try { 
                xml = File.ReadAllText(objfile); 
            } catch (Exception e) {
                Console.WriteLine("Error: " + e.Message);
                return VRAgentController.fail("Error: "+e.Message); 
            }
            try { 
                prims = Helpers.OSDToPrimList(OSDParser.DeserializeLLSDXml(xml)); 
            } catch (Exception e) {
                Console.WriteLine("Failed to deserialize " + objfile + ": " + e.Message);
                return VRAgentController.fail("Failed to deserialize "+objfile+": "+e.Message); 
            }

            // Build an organized structure from the imported prims
            Dictionary<uint, Linkset> linksets = new Dictionary<uint, Linkset>();
            for (int i = 0; i < prims.Count; i++) {
                Primitive prim = prims[i];
                if (prim.ParentID == 0) {
                    if (linksets.ContainsKey(prim.LocalID))
                        linksets[prim.LocalID].RootPrim = prim;
                    else
                        linksets[prim.LocalID] = new Linkset(prim);
                } else {
                    if (!linksets.ContainsKey(prim.ParentID))
                        linksets[prim.ParentID] = new Linkset();

                    linksets[prim.ParentID].Children.Add(prim);
                }
            }

            primsCreated = new List<Primitive>();
            Console.WriteLine("Importing " + linksets.Count + " structures.");
            Agent.Objects.ObjectUpdate += onNewPrim_handler;

            foreach (Linkset linkset in linksets.Values) {
                if (linkset.RootPrim.LocalID != 0) {
                    importingState = ImporterState.RezzingParent;
                    currentPrim = linkset.RootPrim;
                    // HACK: Import the structure just above our head
                    // We need a more elaborate solution for importing with relative or absolute offsets
                    //linkset.RootPrim.Position = Agent.Self.SimPosition;
                    //linkset.RootPrim.Position.Z += 3.0f;
                    linkset.RootPrim.Position = importObjPos;
                    currentPosition = linkset.RootPrim.Position;

                    // Rez the root prim with no rotation
                    Quaternion rootRotation = linkset.RootPrim.Rotation;
                    linkset.RootPrim.Rotation = Quaternion.Identity;

                    Agent.Objects.AddPrim(Agent.Network.CurrentSim, linkset.RootPrim.PrimData, 
                        UUID.Zero, linkset.RootPrim.Position, linkset.RootPrim.Scale, 
                        linkset.RootPrim.Rotation);

                    if (!primDoneEvent.WaitOne(10000, false)) {
                        Agent.Objects.ObjectUpdate -= onNewPrim_handler;
                        Console.WriteLine("Rez failed, timed out while creating the root prim.");
                        return VRAgentController.fail("Rez failed, timed out while creating the root prim.");
                    }
                    Agent.Objects.SetPosition(Agent.Network.CurrentSim, 
                        primsCreated[primsCreated.Count - 1].LocalID, 
                        linkset.RootPrim.Position);

                    importingState = ImporterState.RezzingChildren;

                    // Rez the child prims
                    foreach (Primitive prim in linkset.Children) {
                        currentPrim = prim;
                        currentPosition = prim.Position + linkset.RootPrim.Position;

                        Agent.Objects.AddPrim(Agent.Network.CurrentSim, prim.PrimData, 
                            UUID.Zero, currentPosition, prim.Scale, prim.Rotation);

                        if (!primDoneEvent.WaitOne(10000, false)) {
                            Agent.Objects.ObjectUpdate -= onNewPrim_handler;
                            Console.WriteLine("Rez failed, timed out while creating child prim.");
                            return VRAgentController.fail("Rez failed, timed out while creating child prim.");
                        }
                        Agent.Objects.SetPosition(Agent.Network.CurrentSim, 
                            primsCreated[primsCreated.Count - 1].LocalID, currentPosition);

                    }

                    // Create a list of the local IDs of the newly created prims
                    List<uint> primIDs = new List<uint>(primsCreated.Count);
                    primIDs.Add(rootLocalID); // Root prim is first in list.

                    if (linkset.Children.Count != 0) {
                        // Add the rest of the prims to the list of local IDs
                        foreach (Primitive prim in primsCreated) {
                            if (prim.LocalID != rootLocalID)
                                primIDs.Add(prim.LocalID);
                        }
                        linkQueue = new List<uint>(primIDs.Count);
                        linkQueue.AddRange(primIDs);

                        // Link and set the permissions + rotation
                        importingState = ImporterState.Linking;
                        Agent.Objects.LinkPrims(Agent.Network.CurrentSim, linkQueue);

                        if (primDoneEvent.WaitOne(1000 * linkset.Children.Count, false))
                            Agent.Objects.SetRotation(Agent.Network.CurrentSim, rootLocalID, 
                                rootRotation);
                        else
                            Console.WriteLine("Warning: Failed to link {0} prims", 
                                linkQueue.Count);

                    } else {
                        Agent.Objects.SetRotation(Agent.Network.CurrentSim, rootLocalID, 
                            rootRotation);
                    }

                    // Set permissions on newly created prims
                    Agent.Objects.SetPermissions(Agent.Network.CurrentSim, primIDs,
                        PermissionWho.Everyone | PermissionWho.Group | PermissionWho.NextOwner,
                        PermissionMask.All, true);

                    importingState = ImporterState.Idle;
                } else {
                    // Skip linksets with a missing root prim
                    Console.WriteLine("WARNING: Skipping a linkset with a missing root prim");
                }

                // Reset everything for the next linkset
                primsCreated.Clear();
            }

            Agent.Objects.ObjectUpdate -= onNewPrim_handler;
            Console.WriteLine("Import complete.");
            return VRAgentController.ok("Import complete.");
        }



        List<UUID> DownloadedTextures = new List<UUID>(); 

        public bool ExportObjectAction(string objid, string objfile)
        {
            UUID objUUID;
            uint localid;

            if (!UUID.TryParse(objid, out objUUID)) {
                Console.WriteLine("invalid object id");
                return VRAgentController.fail("invalid object id");
            }

            Primitive exportPrim;
            // Find object to export
            exportPrim = Agent.Network.CurrentSim.ObjectsPrimitives.Find(
                delegate (Primitive prim) { 
                    return prim.ID == objUUID; 
                }
            );
            if (exportPrim == null) {
                Console.WriteLine("Couldn't find object witg UUID " + objUUID.ToString());
                return VRAgentController.fail("Couldn't find object witg UUID " + objUUID.ToString());
            }

            // Check for permissions
            if (!CheckObjPermissions(objUUID)) {
                Console.WriteLine("Do not have permission to export it");
                return VRAgentController.fail("Do not have permission to export it");
            }
            if (exportPrim.ParentID != 0)
                localid = exportPrim.ParentID;
            else
                localid = exportPrim.LocalID;
            List<Primitive> prims = Agent.Network.CurrentSim.ObjectsPrimitives.FindAll(
                delegate (Primitive prim)
                {
                    return (prim.LocalID == localid || prim.ParentID == localid);
                }
            );

            bool complete = RequestObjectProperties(prims, 250);

            string output = OSDParser.SerializeLLSDXmlString(Helpers.PrimListToOSD(prims));
            try { 
                File.WriteAllText(objfile, output); 
            } catch (Exception e) {
                Console.WriteLine("Error: " + e.Message);
                return VRAgentController.fail("Error: "+e.Message); 
            }

            Console.WriteLine("Exported " + prims.Count + " prims to " + objfile);

            // Create a list of all of the textures to download
            List<ImageRequest> textureRequests = new List<ImageRequest>();

            lock (DownloadedTextures) {
                for (int i = 0; i < prims.Count; i++) {
                    Primitive prim = prims[i];
                    if (prim.Textures.DefaultTexture.TextureID != Primitive.TextureEntry.WHITE_TEXTURE &&
                        !DownloadedTextures.Contains(prim.Textures.DefaultTexture.TextureID)) {
                        DownloadedTextures.Add(prim.Textures.DefaultTexture.TextureID);
                    }
                    for (int j = 0; j < prim.Textures.FaceTextures.Length; j++) {
                        if (prim.Textures.FaceTextures[j] != null &&
                            prim.Textures.FaceTextures[j].TextureID != Primitive.TextureEntry.WHITE_TEXTURE &&
                            !DownloadedTextures.Contains(prim.Textures.FaceTextures[j].TextureID)) {
                            DownloadedTextures.Add(prim.Textures.FaceTextures[j].TextureID);
                        }
                    }
                    if (prim.Sculpt != null && prim.Sculpt.SculptTexture != UUID.Zero && !DownloadedTextures.Contains(prim.Sculpt.SculptTexture)) {
                        DownloadedTextures.Add(prim.Sculpt.SculptTexture);
                    }
                }
                // Create a request list from all of the images
                for (int i = 0; i < DownloadedTextures.Count; i++)
                    textureRequests.Add(new ImageRequest(DownloadedTextures[i], ImageType.Normal, 1013000.0f, 0));
            }
            // Download all of the textures in the export list
            foreach (ImageRequest request in textureRequests) {
                Agent.Assets.RequestImage(request.ImageID, request.Type, OnImageReceived_Handler);
            }
            Console.WriteLine("XML file exported, downloading" + DownloadedTextures.Count + " textures");
            return VRAgentController.ok("XML file exported, downloading" + DownloadedTextures.Count + " textures");
        }

        private bool RequestObjectProperties(List<Primitive> objects, int msPerRequest)
        {
            // Create an array of the local IDs of all the prims we are requesting properties for
            uint[] localids = new uint[objects.Count];
            bool complete;
            AutoResetEvent allPropertiesReceived = new AutoResetEvent(false);
            Dictionary<UUID, Primitive> primsWaiting = new Dictionary<UUID, Primitive>();

            EventHandler<ObjectPropertiesEventArgs> objPropsReply_handler =
                delegate (object sender, ObjectPropertiesEventArgs e) {
                    lock (primsWaiting) {
                        primsWaiting.Remove(e.Properties.ObjectID);
                        if (primsWaiting.Count == 0)
                            allPropertiesReceived.Set();
                    }
                };

            for (int i = 0; i < objects.Count; ++i) {
                localids[i] = objects[i].LocalID;
                primsWaiting.Add(objects[i].ID, objects[i]);
            }

            Agent.Objects.ObjectProperties += objPropsReply_handler;
            Agent.Objects.SelectObjects(Agent.Network.CurrentSim, localids);
            complete = allPropertiesReceived.WaitOne(2000 + msPerRequest * objects.Count, false);
            Agent.Objects.ObjectProperties -= objPropsReply_handler;
            if (!complete) {
                Console.WriteLine("Unable to retrieve properties of following objects:");
                foreach (UUID uuid in primsWaiting.Keys)
                    Console.WriteLine(uuid.ToString(), Helpers.LogLevel.Warning, Agent);
            }

            return complete;
        }

        private void OnImageReceived_Handler(TextureRequestState state, AssetTexture asset)
        {

            if (state == TextureRequestState.Finished && DownloadedTextures.Contains(asset.AssetID)) {
                lock (DownloadedTextures)
                    DownloadedTextures.Remove(asset.AssetID);

                if (state == TextureRequestState.Finished) {
                    try { 
                        File.WriteAllBytes(asset.AssetID + ".jp2", asset.AssetData); 
                    } catch (Exception ex) { 
                        Console.WriteLine(ex.Message); 
                    }

                    if (asset.Decode()) {
                        try { 
                            File.WriteAllBytes(asset.AssetID + ".tga", asset.Image.ExportTGA()); 
                        } catch (Exception ex) { 
                            Console.WriteLine(ex.Message); 
                        }
                    } else {
                        Console.WriteLine("Failed to decode image " + asset.AssetID);
                    }

                    Console.WriteLine("Finished downloading image " + asset.AssetID);
                } else {
                    Console.WriteLine("Failed to download image " + asset.AssetID + ":" + state);
                }
            }
        }



    }
}

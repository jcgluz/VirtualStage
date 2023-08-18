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
//   Class:     SelfObservationActions 
//   Purpose:   To implement actions for the agent be able to observe
//              the state of its avatar on virtual world
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
    public class SelfObservationActions : Actions
    {

        public SelfObservationActions(VRAgentController agent) : base(agent)
        {
        }

        public List<string> LookMyInfoAction()
        {
            string avid = Agent.Self.AgentID.ToString();
            PerceptList percepts = new PerceptList();
            List<string> result = percepts.Add("myinfo", avid, 
                    Agent.Self.Name.ToString().Replace("'", "''"),
                    Agent.Self.FirstName.ToString(),
                    Agent.Self.LastName.ToString(),
                    Agent.Self.LocalID.ToString(),
                    Agent.Self.AgentAccess,
                    Agent.Self.Health.ToString(),
                    Agent.Self.Balance.ToString(),
                    Agent.Self.SittingOn.ToString(),
                    Agent.Self.ActiveGroup.ToString(),
                    Agent.Self.ActiveGroupPowers.ToString()
                    );
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get my info",result);
        }

        public List<string> LookMyPositionAction()
        {
            PerceptList percepts = new PerceptList();
            List<string> result = percepts.Add("mypos", 
                    Agent.Self.AgentID.ToString(),
                    Agent.Self.SimPosition.X.ToString() ,
                    Agent.Self.SimPosition.Y.ToString() ,
                    Agent.Self.SimPosition.Z.ToString() );
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get my position", result);
        }

        public List<string> LookMyRotationAction()
        {
            float roll, pitch, yaw;
            Agent.Self.SimRotation.GetEulerAngles(out roll, out pitch, out yaw);
            PerceptList percepts = new PerceptList();
            List<string> result = percepts.Add("myrot", Agent.Self.AgentID.ToString(),
                        roll.ToString() ,
                        pitch.ToString() ,
                        yaw.ToString() );
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get my rotation", result);
        }

        public List<string> LookMyVelocityAction()
        {
            PerceptList percepts = new PerceptList();
            List<string> result = percepts.Add("myvel",
                        Agent.Self.AgentID.ToString(),
                        Agent.Self.Velocity.X.ToString(),
                        Agent.Self.Velocity.Y.ToString(),
                        Agent.Self.Velocity.Z.ToString());
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get my velocity", result);
        }

        public List<string> LookMyAccelerationAction()
        {
            PerceptList percepts = new PerceptList();
            List<string> result = percepts.Add("myaccel",
                        Agent.Self.AgentID.ToString(),
                        Agent.Self.Acceleration.X.ToString(),
                        Agent.Self.Acceleration.Y.ToString(),
                        Agent.Self.Acceleration.Z.ToString());
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get my acceleration", result);
        }

        public List<string> LookMyAngularVelocityAction()
        {
            PerceptList percepts = new PerceptList();
            List<string> result = percepts.Add("myangvel",
                        Agent.Self.AgentID.ToString(),
                        Agent.Self.AngularVelocity.X.ToString(),
                        Agent.Self.AngularVelocity.Y.ToString(),
                        Agent.Self.AngularVelocity.Z.ToString());
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get my ang velocity", result);
        }

        public List<string> LookMyHeightAction()
        {
            float height;
            string rid = Agent.Network.CurrentSim.ID.ToString();
            Vector3 agentPos = Agent.Self.SimPosition;
            PerceptList percepts = new PerceptList();

            if (!Agent.Network.CurrentSim.TerrainHeightAtPoint(Convert.ToInt32(agentPos.X),
                                                        Convert.ToInt32(agentPos.Y), out height))
                return VRAgentController.nullst("cannot get height info");

            List<string> result = percepts.Add("my_terrain_height", rid, 
                                    agentPos.X.ToString(), agentPos.Y.ToString(),
                                    height.ToString());
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get height info", result);
        }

        public List<string> LookMyWindAction()
        {
            // Get the agent's current "patch" position, where each patch of
            // wind data is a 16x16m square
            string rid = Agent.Network.CurrentSim.ID.ToString();
            Vector3 agentPos = Agent.Self.SimPosition;
            int xPos = (int)Utils.Clamp(agentPos.X, 0.0f, 255.0f) / 16;
            int yPos = (int)Utils.Clamp(agentPos.Y, 0.0f, 255.0f) / 16;
            Vector2 windSpeed = Agent.Network.CurrentSim.WindSpeeds[yPos * 16 + xPos];
            PerceptList percepts = new PerceptList();
            List<string> result = percepts.Add("my_wind_speed", rid,
                                    agentPos.X.ToString(), agentPos.Y.ToString(),
                                    windSpeed.X.ToString(), windSpeed.Y.ToString());
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get wind info", result);
        }

        public List<string> LookMyRegionAction()
        {
            PerceptList percepts = new PerceptList();
            string rid = Agent.Network.CurrentSim.ID.ToString();
            List<string> result = percepts.Add("myregion", 
                                    rid, 
                                    Agent.Network.CurrentSim.Name.ToString().Replace("'", "''") );
            percepts.Add("region", rid, Agent.Network.CurrentSim.Name.ToString().Replace("'", "''"));
            percepts.Add("name", rid , Agent.Network.CurrentSim.Name.ToString().Replace("'", "''") );
            uint x, y;
            Utils.LongToUInts(Agent.Network.CurrentSim.Handle, out x, out y);
            percepts.Add("handle", rid , Agent.Network.CurrentSim.Handle.ToString() );
            percepts.Add("world_coord", rid , x.ToString() , y.ToString() );
            percepts.Add("access_level", rid , Agent.Network.CurrentSim.Access.ToString() );
            percepts.Add("flags", rid + "', [" + Agent.Network.CurrentSim.Flags.ToString().ToLower() + "])");
            percepts.Add("terr_hght_rng0", rid + Agent.Network.CurrentSim.TerrainHeightRange00.ToString());
            percepts.Add("terr_hght_rng1", rid + Agent.Network.CurrentSim.TerrainHeightRange01.ToString());
            percepts.Add("terr_hght_rng2", rid + Agent.Network.CurrentSim.TerrainHeightRange10.ToString());
            percepts.Add("terr_hght_rng3", rid + Agent.Network.CurrentSim.TerrainHeightRange11.ToString());
            percepts.Add("terr_strt_hght0", rid + Agent.Network.CurrentSim.TerrainStartHeight00.ToString());
            percepts.Add("terr_strt_hght1", rid + Agent.Network.CurrentSim.TerrainStartHeight01.ToString());
            percepts.Add("terr_strt_hght2", rid + Agent.Network.CurrentSim.TerrainStartHeight10.ToString());
            percepts.Add("terr_strt_hght3", rid + Agent.Network.CurrentSim.TerrainStartHeight11.ToString());
            percepts.Add("terr_base0", rid + Agent.Network.CurrentSim.TerrainBase0.ToString() );
            percepts.Add("terr_base1", rid + Agent.Network.CurrentSim.TerrainBase1.ToString() );
            percepts.Add("terr_base2", rid + Agent.Network.CurrentSim.TerrainBase2.ToString() );
            percepts.Add("terr_base3", rid + Agent.Network.CurrentSim.TerrainBase3.ToString() );
            percepts.Add("terr_detail0", rid + Agent.Network.CurrentSim.TerrainDetail0.ToString() );
            percepts.Add("terr_detail1", rid + Agent.Network.CurrentSim.TerrainDetail1.ToString() );
            percepts.Add("terr_detail2", rid + Agent.Network.CurrentSim.TerrainDetail2.ToString() );
            percepts.Add("terr_detail3", rid + Agent.Network.CurrentSim.TerrainDetail3.ToString() );
            percepts.Add("water_height", rid + "', '" + Agent.Network.CurrentSim.WaterHeight.ToString() );
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get my region info", result);
        }

        private Inventory Inventory;
        private InventoryManager Manager;

        public List<List<string>> LookMyInventoryAction()
        {
            Manager = Agent.Inventory;
            Inventory = Manager.Store;
            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            InventoryFolder rootFolder = Inventory.RootFolder;
            GetFullInventory(rootFolder, "/", percepts, results);
            if (percepts.Count > 0) {
                Agent.PerceptsBase.Update(percepts);
            }
            return VRAgentController.ok("my inventory list", results);
        }

        void GetFullInventory(InventoryFolder startfolder, string currpath, 
                            PerceptList percepts, List<List<string>> results )
        {
            List<InventoryBase> foldercontents = 
                    Manager.FolderContents(startfolder.UUID, Agent.Self.AgentID,
                                            true, true, InventorySortOrder.ByName, 3000);
            if (foldercontents != null) {
                foreach (InventoryBase entry in foldercontents) {
                    string name = entry.Name.Replace("'", "''");
                    string id = entry.UUID.ToString();
                    string avid = Agent.Self.AgentID.ToString();
                    if (entry is InventoryFolder) {
                        InventoryFolder folder = (InventoryFolder)entry;
                        results.Add(percepts.Add("myfolder", id, name, currpath));
                        //percepts.Add("folder", id);
                        //percepts.Add("folder", id, avid);
                        //percepts.Add("name", id, name);
                        //percepts.Add("path", id, currpath);
                        string folderpath = currpath + name + "/";
                        GetFullInventory(folder, folderpath, percepts, results);
                    } else if (entry is InventoryItem) {
                        InventoryItem item = (InventoryItem)entry;
                        string invtype =
                            (item.InventoryType.ToString() != String.Empty) ?
                                item.InventoryType.ToString() : "unknown";
                        string assetype =
                            (item.AssetType.ToString() != String.Empty) ?
                                item.AssetType.ToString() : "unknown";
                        string assetid = item.AssetUUID.ToString();
                        string descr = item.Description.Replace("'", "''");
                        results.Add(percepts.Add("myitem", id, name, 
                            currpath, descr, invtype, assetype, assetid ));
                        //percepts.Add("item", id);
                        //percepts.Add("item", id, avid);
                        //percepts.Add("name", id, name);
                        //percepts.Add("path", id, currpath);
                    }
                }
            }
        }

        public List<List<string>> LookMyFolderAction(string argpath)
        {
            Manager = Agent.Inventory;
            Inventory = Manager.Store;
            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            InventoryFolder rootFolder = Inventory.RootFolder;
            if (!FindPrintFolder(rootFolder, "/", argpath, percepts, results))
                return null;
            if (percepts.Count > 0) {
                Agent.PerceptsBase.Update(percepts);
            }
            return VRAgentController.ok("my folder list", results);
        }

        bool FindPrintFolder(InventoryFolder startfolder, string currpath, string searchpath,
                           PerceptList percepts, List<List<string>> results)
        {
            List<InventoryBase> foldercontents =
                        Manager.FolderContents(startfolder.UUID, Agent.Self.AgentID,
                                            true, true, InventorySortOrder.ByName, 3000);
            if (foldercontents == null)
                return false;
            if (currpath != searchpath) {
                foreach (InventoryBase entry in foldercontents) {
                    if (entry is InventoryFolder) {
                        InventoryFolder folder = (InventoryFolder)entry;
                        string name = folder.Name.Replace("'", "''");
                        string folderpath = currpath + name + "/";
                        if (FindPrintFolder(folder, folderpath, searchpath, percepts, results))
                            return true;
                    }
                }
                return false;
            }
            foreach (InventoryBase entry in foldercontents) {
                string name = entry.Name.Replace("'", "''");
                string id = entry.UUID.ToString();
                string avid = Agent.Self.AgentID.ToString();
                if (entry is InventoryFolder) {
                    results.Add(percepts.Add("myfolder", id, name, currpath));
                    //percepts.Add("folder", id);
                    //percepts.Add("folder", id, avid);
                    //percepts.Add("name", id, name);
                    //percepts.Add("path", id, currpath);
                } else if (entry is InventoryItem) {
                    InventoryItem item = (InventoryItem)entry;
                    string invtype =
                        (item.InventoryType.ToString() != String.Empty) ?
                            item.InventoryType.ToString() : "unknown";
                    string assetype =
                        (item.AssetType.ToString() != String.Empty) ?
                            item.AssetType.ToString() : "unknown";
                    string assetid = item.AssetUUID.ToString();
                    string descr = item.Description.Replace("'", "''");
                    results.Add(percepts.Add("myitem", id, name, 
                        currpath, descr, invtype, assetype, assetid ));
                    //percepts.Add("item", id);
                    //percepts.Add("item", id, avid);
                    //percepts.Add("name", id, name);
                    //percepts.Add("path", id, currpath);
                }
            }
            return true;

        }


        public List<string> LookMyItemAction(string argpath)
        {
            Manager = Agent.Inventory;
            Inventory = Manager.Store;
            PerceptList percepts = new PerceptList();
            
            InventoryFolder rootFolder = Inventory.RootFolder;
            List<string> result = FindPrintItem(rootFolder, "/", argpath, percepts);
            if (result==null)
                return VRAgentController.nullst("item not found");
            Agent.PerceptsBase.Update(percepts);
            return VRAgentController.ok("get my item", result);
        }

        List<string> FindPrintItem(InventoryFolder startfolder, string currpath, 
                            string searchpath, PerceptList percepts)
        {
            Console.WriteLine("retrieving folder: "+currpath);
            List<InventoryBase> foldercontents = 
                            Manager.FolderContents(startfolder.UUID, Agent.Self.AgentID,
                                        true, true, InventorySortOrder.ByName, 3000);
            Console.WriteLine("folder retrieved");
            if (foldercontents == null)
                return null;
            foreach (InventoryBase entry in foldercontents) {
                string name = entry.Name.Replace("'", "''");
                string entrypath = currpath + name;
                //				Console.WriteLine("itempath="+itempath+" basepath1="+basepath1);
                if (entry is InventoryItem) {
                    if (searchpath == entrypath) {
                        Console.WriteLine("found item: " + entrypath);

                        List<string> result;
                        InventoryItem item = (InventoryItem)entry;
                        string avid = Agent.Self.AgentID.ToString();
                        string id = item.UUID.ToString();
                        string invtype = 
                            (item.InventoryType.ToString() != String.Empty)?
                                item.InventoryType.ToString() : "unknown";
                        string assetype =
                            (item.AssetType.ToString() != String.Empty) ?
                                item.AssetType.ToString() : "unknown";
                        string assetid = item.AssetUUID.ToString();
                        string descr = item.Description.Replace("'", "''");
                        result = percepts.Add("myitem", id, name, 
                                    entrypath, descr, invtype, assetype, assetid );                              
                        //percepts.Add("item", id);
                        //percepts.Add("item", id, avid);
                        //percepts.Add("name", id, name);
                        //percepts.Add("path", id, entrypath);
                        percepts.Add("owner_perms", id, PermMaskStr(item.Permissions.OwnerMask));
                        percepts.Add("group_perms", id, PermMaskStr(item.Permissions.GroupMask));
                        percepts.Add("all_perms", id, PermMaskStr(item.Permissions.EveryoneMask));
                        percepts.Add("base_perms", id, PermMaskStr(item.Permissions.BaseMask));
                        percepts.Add("nextown_perms", id, PermMaskStr(item.Permissions.NextOwnerMask));
                        if (item.AssetUUID.ToString() != String.Empty)
                            percepts.Add("asset_id", id, item.AssetUUID.ToString());
                        //if (item.AssetType.ToString() != String.Empty)
                        //    percepts.Add("asset_type", id, item.AssetType.ToString());
                        //if (item.InventoryType.ToString() != String.Empty)
                        //    percepts.Add("inventory_type", id, item.InventoryType.ToString());
                        if (item.CreatorID.ToString() != String.Empty)
                            percepts.Add("creat_id", id, item.CreatorID.ToString());
                        //if (item.Description != String.Empty)
                        //    percepts.Add("descr", id, item.Description.Replace("'", "''"));
                        if (item.OwnerID.ToString() != String.Empty)
                            percepts.Add("owner_id", id, item.OwnerID.ToString());
                        if (item.SalePrice.ToString() != String.Empty)
                            percepts.Add("sale_price", id, item.SalePrice.ToString());
                        if (item.SaleType.ToString() != String.Empty)
                            percepts.Add("sale_type", id, item.SaleType.ToString());
                        if (item.Flags.ToString() != String.Empty)
                            percepts.Add("flags", id + "', [" + item.Flags.ToString().ToLower() + "])");
                        if (item.CreationDate.ToString() != String.Empty)
                            percepts.Add("creat_date", id, item.CreationDate.ToString());
                        if (item.TransactionID.ToString() != String.Empty)
                            percepts.Add("transact_id", id, item.TransactionID.ToString());
                        if (item.LastOwnerID.ToString() != String.Empty)
                            percepts.Add("lastown_id", id, item.LastOwnerID.ToString());
                        return result;
                    }
                } else if (entry is InventoryFolder) {
                    InventoryFolder folder = (InventoryFolder)entry;
                    List<string> result;
                    string folderpath = entrypath + "/";
                    Console.WriteLine("will look new folder");
                    result = FindPrintItem(folder, folderpath, searchpath, percepts);
                    if (result != null)
                        return result;
                }
            };
            return null;
        }


        private static string PermMaskStr(PermissionMask mask)
        {
            string str = "[";
            string sep = "";
            if (((uint)mask | (uint)PermissionMask.Copy) == (uint)PermissionMask.Copy){
                str += "cpy";
                sep = ",";
            }
            if (((uint)mask | (uint)PermissionMask.Modify) == (uint)PermissionMask.Modify) {
                str += sep+"mod";
                sep = ",";
            }
            if (((uint)mask | (uint)PermissionMask.Transfer) == (uint)PermissionMask.Transfer){
                str += sep+"trf";
                sep = ",";
            }
            if (((uint)mask | (uint)PermissionMask.Export) == (uint)PermissionMask.Export){
                str += sep + "exp";
                sep = ",";
            }
            if (((uint)mask | (uint)PermissionMask.Move) == (uint)PermissionMask.Move){
                str += sep + "mov";
                sep = ",";
            }
            if (((uint)mask | (uint)PermissionMask.Damage) == (uint)PermissionMask.Damage) {
                str += sep + "dam";
                sep = ",";
            }
            str += "]";
           return str;
        }

        public List<List<string>> LookMyAttachmentsAction()
        {
            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            List<Primitive> attachments = Agent.Network.CurrentSim.ObjectsPrimitives.FindAll(
                delegate (Primitive prim) { return prim.ParentID == Agent.Self.LocalID; }
            );
            for (int i = 0; i < attachments.Count; i++) {
                Primitive prim = attachments[i];
                AttachmentPoint point = StateToAttachmentPoint(prim.PrimData.State);
                // TODO: Fetch properties for the objects with missing property sets so we can show names
                string pid = prim.ID.ToString();
                string typ = prim.PrimData.PCode.ToString().ToLower();
                string subtyp =
                    prim.PrimData.PCode == PCode.Prim ?
                        prim.Type.ToString().ToLower() :
                        (prim.PrimData.PCode == PCode.Tree || prim.PrimData.PCode == PCode.NewTree ?
                            prim.TreeSpecies.ToString().ToLower() :
                            (prim.PrimData.PCode == PCode.Grass ?
                                ((Grass)prim.TreeSpecies).ToString().ToLower() : ""));
                results.Add(percepts.Add("myattach", pid,
                                typ, subtyp, 
                                point.ToString(),
                                prim.LocalID.ToString(),
                                prim.Position.X.ToString() ,
                                prim.Position.Y.ToString() ,
                                prim.Position.Z.ToString() ,
                                prim.Scale.X.ToString() ,
                                prim.Scale.Y.ToString() ,
                                prim.Scale.Z.ToString() ));
            }
            if (percepts.Count > 0) {
                Agent.PerceptsBase.Update(percepts);
            }
            return VRAgentController.ok("my attachments list", results);
        }

        public static AttachmentPoint StateToAttachmentPoint(uint state)
        {
            const uint ATTACHMENT_MASK = 0xF0;
            uint fixedState = (((byte)state & ATTACHMENT_MASK) >> 4) | (((byte)state & ~ATTACHMENT_MASK) << 4);
            return (AttachmentPoint)fixedState;
        }

        public List<List<string>> LookMyWearablesAction()
        {
            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            Dictionary<WearableType, AppearanceManager.WearableData> wearables = Agent.Appearance.GetWearables();
            // Console.WriteLine("wearables.Count=" + wearables.Count);
            foreach (AppearanceManager.WearableData wearable in wearables.Values) {
                    results.Add(percepts.Add("mywearable",
                                    wearable.ItemID.ToString(),
                                    wearable.WearableType.ToString(),
                                    wearable.AssetType.ToString(),
                                    wearable.Asset.Name,
                                    wearable.AssetID.ToString()
                                    ));
            }
            if (percepts.Count > 0) {
                Agent.PerceptsBase.Update(percepts);
            }
            return VRAgentController.ok("my wearables list", results);
        }

        string FindAssetIdItem(UUID assetid, InventoryFolder f, string basepath)
        {
            List<InventoryBase> contents = Agent.Inventory.FolderContents(f.UUID, Agent.Self.AgentID,
                true, true, InventorySortOrder.ByName, 3000);
            if (contents == null)
                return "";
            foreach (InventoryBase i in contents) {
                string name = i.Name.Replace("'", "''");
                //				Console.WriteLine("itempath="+itempath+" basepath1="+basepath1);
                if (i is InventoryItem) {
                    InventoryItem item = (InventoryItem)i;
                    if (assetid == item.AssetUUID) {
                        return basepath+name;
                    }
                } else if (i is InventoryFolder) {
                    InventoryFolder folder = (InventoryFolder)i;
                    string itempath = FindAssetIdItem(assetid,folder,basepath+name+"/");
                    if (itempath!="") {
                        return itempath;
                    }
                }
            };
            return "";
        }


        public List<List<string>> LookMyAnimationsPlayingAction()
        {
            PerceptList percepts = new PerceptList();
            List<List<string>> results = new List<List<string>>();
            //private Dictionary<UUID, string> m_BuiltInAnimations = 
                //new Dictionary<UUID, string>(Animations.ToDictionary());

            Agent.Self.SignaledAnimations.ForEach(delegate (KeyValuePair<UUID, int> kvp) {
                string typeanim, nameanim;
                if (StdAnimations.ContainsKey(kvp.Key)) {
                    typeanim = "std_anim"; nameanim = StdAnimations[kvp.Key];
                } else {
                    InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
                    nameanim = FindAssetIdItem(kvp.Key,rootFolder,"/");
                    if (nameanim=="") {
                        nameanim = kvp.Key.ToString(); typeanim = "asset_id"; 
                    }  else {
                        typeanim = "item";
                    }
                }
                results.Add(percepts.Add("myanim_playing",
                        kvp.Key.ToString(), kvp.Value.ToString(), typeanim, nameanim
                        ));
            });
            if (percepts.Count > 0) {
                Agent.PerceptsBase.Update(percepts);
            }
            return VRAgentController.ok("my anims playing list", results);
        }

    }
}

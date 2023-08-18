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
//   Class:     SelfModificationActions 
//   Purpose:   Implement actions for the agent to be able to modify the
//              characteristics of its avatar in the virtual world
//   Author:    João Carlos Gluz 
//
//***********************************************************************
using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Drawing;
#if USE_LIBREMETAVERSE_VR_LIB
using LibreMetaverse;
using LibreMetaverse.Packets;
using LibreMetaverse.Imaging;
using LibreMetaverse.Assets;
#else
using OpenMetaverse;
using OpenMetaverse.Packets;
using OpenMetaverse.Imaging;
using OpenMetaverse.Assets;
#endif

#if USE_LIBREMETAVERSE_VR_LIB
namespace LibreMetaverse
#else
namespace OpenMetaverse
#endif
{
    public class SelfModificationActions : Actions
    {
        public SelfModificationActions(VRAgentController agent) : base(agent)
        {
        }

        public bool SetAppearanceAction(bool argrebake)
        {
            Agent.Appearance.RequestSetAppearance(argrebake);
            return VRAgentController.ok("setting appearance");
        }


        public bool WearAction(string argopt, string argitemfold)
        {
  //           Console.WriteLine("running wear action");
            if (argopt == "item") {
 //                Console.WriteLine("trying to find folder: " + argitemfold);
                InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
                InventoryItem item = FindItem(rootFolder, "/", argitemfold);
                if (item == null) {
                    return VRAgentController.fail("item not found");
                }
                Agent.Appearance.AddToOutfit(item, true);
                return VRAgentController.ok("wearing item");
            } else if (argopt == "folder") {
//                Console.WriteLine("trying to find folder: " + argitemfold);
                InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
                UUID folder = FindFolder(rootFolder, "/", argitemfold);
                if (folder == UUID.Zero) {
                    return VRAgentController.fail("folder not found");
                }
                List<InventoryBase> contents = Agent.Inventory.FolderContents(folder, Agent.Self.AgentID, true, true, InventorySortOrder.ByName, 20 * 1000);
                List<InventoryItem> items = new List<InventoryItem>();
                if (contents == null) {
                    return VRAgentController.fail("cannot get outfit");
                }
                foreach (InventoryBase item in contents) {
                    if (item is InventoryItem)
                        items.Add((InventoryItem)item);
                }
                Agent.Appearance.ReplaceOutfit(items);
                return VRAgentController.ok("wearing folder");
            } else {
                return VRAgentController.fail("param 1 error");
            }
        }

        public bool TakeOffAction(string argitem)
        {
//            Console.WriteLine("running takeoff action");
//            Console.WriteLine("trying to find item: " + argitem);
            InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
            InventoryItem item = FindItem(rootFolder, "/", argitem);
            if (item == null) {
                return VRAgentController.fail("item not found");
            }
            Agent.Appearance.RemoveFromOutfit(item);
            return VRAgentController.ok("taking off");
        }


        public bool AttachAction(string argattpt, string argitem)
        {
            AttachmentPoint attPoint;

            if (!AttachPoints.TryGetValue(argattpt, out attPoint))
                return VRAgentController.fail("param 1 error");
            InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
            InventoryItem item = FindItem(rootFolder, "/", argitem);
            if (item == null) {
                return VRAgentController.fail("item not found");
            }
            Agent.Appearance.Attach(item, attPoint, true);
            return VRAgentController.ok("attaching item");
        }


        public bool DetachAction(string argitem)
        {
//            Console.WriteLine("running detach action");
//            Console.WriteLine("trying to find item: " + argitem);

            //            UUID folder = Client.Inventory.FindObjectByPath(Client.Inventory.Store.RootFolder.UUID, Client.Self.AgentID, target, 20 * 1000);
            InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
            InventoryItem item = FindItem(rootFolder, "/", argitem);
            if (item == null) {
                return VRAgentController.fail("item not found");
            }
            Agent.Appearance.Detach(item);
            return VRAgentController.ok("detaching item");
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

        InventoryItem FindItem(InventoryFolder f, string basepath, string itempath)
        {
            List<InventoryBase> contents = Agent.Inventory.FolderContents(f.UUID, Agent.Self.AgentID,
                true, true, InventorySortOrder.ByName, 3000);

            if (contents == null)
                return null;
            foreach (InventoryBase i in contents) {
                string name = i.Name.Replace("'", "''");
                string basepath1 = basepath + name;
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

        public bool StartPlayAction(string argopt, string arganim)
        {
            UUID animationID;
            if (argopt.Equals("item")) {
                InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
                animationID = FindItemAssetId(rootFolder, "/", arganim);
                if (animationID.Equals(UUID.Zero)) {
                    return VRAgentController.fail("anim item not found");
                }
                Agent.Self.AnimationStart(animationID, true);
                return VRAgentController.ok("starting animation");
            } if (argopt.Equals("asset_id")) {
                if (UUID.TryParse(arganim, out animationID)) {
                    Agent.Self.AnimationStart(animationID, true);
                    return VRAgentController.ok("starting animation");
                } else {
                    return VRAgentController.fail("anim asset not found");
                }
            } else if (argopt.Equals("std_anim")) {
                foreach (var kvp in StdAnimations) {
                        if (kvp.Value.Equals(arganim.ToUpper())) {
                            Agent.Self.AnimationStart(kvp.Key, true);
                            return VRAgentController.ok("starting animation");
                        }
                }
                return (VRAgentController.fail("invalid std anim"));
            } else {
                return VRAgentController.fail("param 1 unknown option");
            }
        }

        public bool StopPlayAction(string argopt, string arganim)
        {
            UUID animationID;
            if (argopt.ToLower().Equals("item")) {
                InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
                animationID = FindItemAssetId(rootFolder, "/", arganim);
                if (animationID.Equals(UUID.Zero)) {
                    return VRAgentController.fail("anim item not found");
                }
                Agent.Self.AnimationStop(animationID, true);
                return VRAgentController.ok("stoping animation");
            } else if (argopt.ToLower().Equals("asset_id")) {
                if (UUID.TryParse(arganim, out animationID)) {
                    Agent.Self.AnimationStop(animationID, true);
                    return VRAgentController.ok("stoping animation");
                } else {
                    return (VRAgentController.fail("anim asset not found"));
                }
            } else if (argopt.ToLower().Equals("std_anim")) {
                foreach (var kvp in StdAnimations) {
                    if (kvp.Value.Equals(arganim.ToUpper())) {
                        Agent.Self.AnimationStop(kvp.Key, true);
                        return VRAgentController.ok("stoping animation");
                    }
                }
                return VRAgentController.fail("invalid std anim");
            } else {
                    return VRAgentController.fail("param 1 error");
            }
        }


        public bool PlayGestureAction(string assetgestid)
        {
            UUID assetGestureID;
            if (UUID.TryParse(assetgestid, out assetGestureID)) {
                Agent.Self.PlayGesture(assetGestureID);
                return VRAgentController.ok("will try to start gesture");
            } else {
                return VRAgentController.fail("invalid asset gesture ID");
            }
        }

        public bool ActivateGestureAction(string itemgestid, string assetgestid)
        {
            UUID assetGestureID;
            UUID itemGestureID;
            if (UUID.TryParse(itemgestid, out itemGestureID) &&
                UUID.TryParse(assetgestid, out assetGestureID)) {
                Agent.Self.ActivateGesture(itemGestureID,assetGestureID);
                return VRAgentController.ok("will try to activate gesture");
            } else {
                return VRAgentController.fail("invalid item or asset gesture ID");
            }
        }

        public bool DeactivateGestureAction(string itemgestid)
        {
            UUID itemGestureID;
            if (UUID.TryParse(itemgestid, out itemGestureID)) {
                Agent.Self.DeactivateGesture(itemGestureID);
                return VRAgentController.ok("will try to deactivate gesture");
            } else {
                return VRAgentController.fail("invalid item gesture ID");
            }
        }


        public bool PlaySoundAction(string soundid)
        {
            UUID soundID;
            if (UUID.TryParse(soundid, out soundID)) {
                Agent.Sound.PlaySound (soundID);
                return VRAgentController.ok("starting to play sound");
            } else {
                return VRAgentController.fail("invalid sound ID");
            }
        }




        UUID FindItemAssetId(InventoryFolder f, string basepath, string itempath)
        {
            List<InventoryBase> contents = Agent.Inventory.FolderContents(f.UUID, Agent.Self.AgentID,
                true, true, InventorySortOrder.ByName, 3000);

            if (contents == null)
                return UUID.Zero;
            foreach (InventoryBase i in contents) {
                string name = i.Name.Replace("'", "''");
                string basepath1 = basepath + name;
                //				Console.WriteLine("itempath="+itempath+" basepath1="+basepath1);
                if (i is InventoryItem) {
                    if (itempath == basepath1) {
                        InventoryItem item = (InventoryItem)i;
                        return item.AssetUUID;
                    }
                } else if (i is InventoryFolder) {
                    InventoryFolder folder = (InventoryFolder)i;
                    UUID assetid = FindItemAssetId(folder, basepath1 + "/", itempath);
                    if (!assetid.Equals(UUID.Zero)) {
                        return assetid;
                    }
                }
            };
            return UUID.Zero;
        }

        uint SleepSerialNum = 1;

        public bool SleepAction(string argseconds)
        {
            int seconds;
            if (!Int32.TryParse(argseconds, out seconds))
                return VRAgentController.fail("param 1 error");
            AgentPausePacket pause = new AgentPausePacket();
            pause.AgentData.AgentID = Agent.Self.AgentID;
            pause.AgentData.SessionID = Agent.Self.SessionID;
            pause.AgentData.SerialNum = SleepSerialNum++;
            Agent.Network.SendPacket(pause);
            // Sleep
            System.Threading.Thread.Sleep(seconds * 1000);
            AgentResumePacket resume = new AgentResumePacket();
            resume.AgentData.AgentID = Agent.Self.AgentID;
            resume.AgentData.SessionID = Agent.Self.SessionID;
            resume.AgentData.SerialNum = pause.AgentData.SerialNum;
            Agent.Network.SendPacket(resume);
            return VRAgentController.ok("paused");
        }



        const int TEXTURE_UPLOAD_TIMEOUT = 1000 * 10;

        public string UploadTextureAction(string textrfile, string textrname,
                                    string textrdescr)
        {
            UUID newItemID = UUID.Zero;
            string uploadMsg = string.Empty;
            bool uploadSuccess = false;
            AutoResetEvent finishUploadEvent = new AutoResetEvent(false);

            Console.WriteLine("Loading texture " + textrfile);
            byte[] data = doLoadImage(textrfile);
            if (data == null) {
                Console.WriteLine("Failed to load texture");
                return VRAgentController.nulstr("Failed to load texture");
            }
            Console.WriteLine("Finish loading texture, now uploading");
            try {
                    Agent.Inventory.RequestCreateItemFromAsset(
                        data, 
                        textrname, 
                        textrdescr,
                        AssetType.Texture, 
                        InventoryType.Texture, 
                        Agent.Inventory.FindFolderForType(AssetType.Texture),
                        delegate (bool success, string status, UUID itemID, UUID assetID)
                        {
                            Console.WriteLine(String.Format(
                                "RequestCreateItemFromAsset() returned: Success={0}, Status={1}, ItemID={2}, AssetID={3}",
                                success, status, itemID, assetID));
                            newItemID = itemID;
                            uploadSuccess = success;
                            uploadMsg = status;
                            finishUploadEvent.Set();
                        });
                    if (!finishUploadEvent.WaitOne((int)TEXTURE_UPLOAD_TIMEOUT, false))
                            uploadMsg = "Timeout uploading texture";
            } catch (Exception ex) {
                Console.WriteLine("Error uploading texture: "+ex.ToString());
                uploadMsg = "Error uploading texture: " + ex.ToString();
            }

            if (uploadSuccess && newItemID != UUID.Zero) {
                Console.WriteLine("Texture upload OK: "+newItemID.ToString());
                return VRAgentController.ok("Texture upload OK: "+newItemID.ToString(),
                                    newItemID.ToString());
            } else {
                Console.WriteLine("Texture upload error: " + uploadMsg);
                return VRAgentController.nulstr("Texture upload error: "+uploadMsg);
            }
        }


        private byte[] doLoadImage(string fileName)
        {
            byte[] UploadData;
            string lowfilename = fileName.ToLower();
            Bitmap bitmap = null;

            try {
                if (lowfilename.EndsWith(".jp2") || lowfilename.EndsWith(".j2c")) {
                    Image image;
                    ManagedImage managedImage;

                    // Upload JPEG2000 images untouched
                    UploadData = System.IO.File.ReadAllBytes(fileName);
                    OpenJPEG.DecodeToImage(UploadData, out managedImage, out image);
                    bitmap = (Bitmap)image;
                } else {
                    if (lowfilename.EndsWith(".tga"))
                        bitmap = LoadTGAClass.LoadTGA(fileName);
                    else
                        bitmap = (Bitmap)System.Drawing.Image.FromFile(fileName);

                    int oldwidth = bitmap.Width;
                    int oldheight = bitmap.Height;

                    if (!IsPowerOfTwo((uint)oldwidth) || !IsPowerOfTwo((uint)oldheight)) {
                        Bitmap resized = new Bitmap(256, 256, bitmap.PixelFormat);
                        Graphics graphics = Graphics.FromImage(resized);

                        graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.HighQuality;
                        graphics.InterpolationMode =
                           System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic;
                        graphics.DrawImage(bitmap, 0, 0, 256, 256);

                        bitmap.Dispose();
                        bitmap = resized;

                        oldwidth = 256;
                        oldheight = 256;
                    }

                    // Handle resizing to prevent excessively large images
                    if (oldwidth > 1024 || oldheight > 1024) {
                        int newwidth = (oldwidth > 1024) ? 1024 : oldwidth;
                        int newheight = (oldheight > 1024) ? 1024 : oldheight;

                        Bitmap resized = new Bitmap(newwidth, newheight, bitmap.PixelFormat);
                        Graphics graphics = Graphics.FromImage(resized);

                        graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.HighQuality;
                        graphics.InterpolationMode =
                           System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic;
                        graphics.DrawImage(bitmap, 0, 0, newwidth, newheight);

                        bitmap.Dispose();
                        bitmap = resized;
                    }

                    UploadData = OpenJPEG.EncodeFromImage(bitmap, false);
                }
            } catch (Exception ex) {
                Console.WriteLine(ex.ToString() + " VRAgents Image Upload Error");
                return null;
            }
            return UploadData;
        }

        private static bool IsPowerOfTwo(uint n)
        {
            return (n & (n - 1)) == 0 && n != 0;
        }


        const int ANIMATION_UPLOAD_TIMEOUT = 1000 * 10;

        public string UploadAnimationAction(string animfile, string animname,
                                    string animdescr)
        {
            UUID newItemID = UUID.Zero;
            string uploadMsg = string.Empty;
            bool uploadSuccess = false;
            AutoResetEvent finishUploadEvent = new AutoResetEvent(false);

            Console.WriteLine("Loading animation " + animfile);
            byte[] data = File.ReadAllBytes(animfile);
            if (data == null) {
                Console.WriteLine("Failed to load animation");
                return VRAgentController.nulstr("Failed to load animation");
            }
            Console.WriteLine("Finish loading animation, now uploading");
            try {
                Agent.Inventory.RequestCreateItemFromAsset(
                    data,
                    animname,
                    animdescr,
                    AssetType.Animation,
                    InventoryType.Animation,
                    Agent.Inventory.FindFolderForType(AssetType.Animation),
                    delegate (bool success, string status, UUID itemID, UUID assetID)
                    {
                        Console.WriteLine(String.Format(
                            "RequestCreateItemFromAsset() returned: Success={0}, Status={1}, ItemID={2}, AssetID={3}",
                            success, status, itemID, assetID));
                        newItemID = itemID;
                        uploadSuccess = success;
                        uploadMsg = status;
                        finishUploadEvent.Set();
                    });
                if (!finishUploadEvent.WaitOne((int)ANIMATION_UPLOAD_TIMEOUT, false))
                    uploadMsg = "Timeout uploading animation";
            } catch (Exception ex) {
                Console.WriteLine("Error uploading animation: " + ex.ToString());
                uploadMsg = "Error uploading animation: " + ex.ToString();
            }

            if (uploadSuccess && newItemID != UUID.Zero) {
                Console.WriteLine("Animation upload OK: " + newItemID.ToString());
                return VRAgentController.ok("Animation upload OK: " + newItemID.ToString(),
                                    newItemID.ToString());
            } else {
                Console.WriteLine("Animation upload error: " + uploadMsg);
                return VRAgentController.nulstr("Animation upload error: " + uploadMsg);
            }
        }


        const int NOTECARD_UPLOAD_TIMEOUT = 1000 * 10;

        public string UploadNotecardAction(string notefile, string notename, 
                                        string notedescr)
        {
            UUID newItemID = UUID.Zero;
            string uploadMsg = string.Empty;
            bool partialUploadSuccess = false, uploadSuccess = false;
            AutoResetEvent finishUploadEvent = new AutoResetEvent(false);
            AssetNotecard notecard = new AssetNotecard();
            string fileData;

            if (!File.Exists(notefile)) {
                Console.WriteLine("Notecard file: " + notefile + " not exists");
                return VRAgentController.nulstr("Notecard file: " + notefile + " not exists");
            }
            try { 
                fileData = File.ReadAllText(notefile); 
            } catch (Exception ex) {
                Console.WriteLine("Failed to open " + notefile + " file: " + ex.Message);
                return VRAgentController.nulstr("Failed to open " + notefile + " file: " + ex.Message); 
            }

            notecard.BodyText = fileData;
            notecard.Encode();

            try {
                Agent.Inventory.RequestCreateItem(
                    Agent.Inventory.FindFolderForType(AssetType.Notecard),
                    notename,
                    notedescr,
                    AssetType.Notecard,
                    UUID.Random(),
                    InventoryType.Notecard,
                    PermissionMask.All,
                    delegate (bool createSuccess, InventoryItem item)
                    {
                        if (createSuccess) {
                        // Upload an empty notecard asset first
                        AutoResetEvent emptyNoteEvent = new AutoResetEvent(false);
                            AssetNotecard empty = new AssetNotecard();
                            empty.BodyText = "\n";
                            empty.Encode();
                            Agent.Inventory.RequestUploadNotecardAsset(
                                empty.AssetData,
                                item.UUID,
                                delegate (bool success, string status,
                                        UUID itemID, UUID assetID)
                                {
                                    Console.WriteLine(String.Format(
                                        "RequestUploadNotecardAsset() returned: Success={0}, Status={1}, ItemID={2}, AssetID={3}",
                                        success, status, itemID, assetID));
                                    partialUploadSuccess = success;
                                    uploadMsg = status ?? "Unknown error uploading notecard asset";
                                    emptyNoteEvent.Set();
                                });
                            emptyNoteEvent.WaitOne(NOTECARD_UPLOAD_TIMEOUT, false);

                            if (partialUploadSuccess) {
                            // Upload the actual notecard asset
                            Agent.Inventory.RequestUploadNotecardAsset(
                                    notecard.AssetData,
                                    item.UUID,
                                    delegate (bool success, string status,
                                            UUID itemID, UUID assetID)
                                    {
                                        Console.WriteLine(String.Format(
                                            "RequestUploadNotecardAsset() returned: Success={0}, Status={1}, ItemID={2}, AssetID={3}",
                                            success, status, itemID, assetID));
                                        newItemID = itemID;
                                        uploadSuccess = success;
                                        uploadMsg = status ?? "Unknown error uploading notecard asset";
                                        finishUploadEvent.Set();
                                    });
                            } else {
                                finishUploadEvent.Set();
                            }
                        } else {
                            uploadMsg = "Notecard item creation failed";
                            finishUploadEvent.Set();
                        }
                    });
                if (!finishUploadEvent.WaitOne((int)NOTECARD_UPLOAD_TIMEOUT, false))
                    uploadMsg = "Timeout uploading notecard";
            } catch (System.Exception e) {
                Console.WriteLine("Error creating notecard: " + e.ToString());
                return VRAgentController.nulstr("Error creating notecard: " + e.ToString());
            }

            if (uploadSuccess && newItemID != UUID.Zero) {
                Console.WriteLine("Notecard successfully created: " + newItemID);
                return VRAgentController.ok("Notecard successfully created: " + newItemID,
                                newItemID.ToString());
            } else {
                Console.WriteLine(uploadMsg);   
                return VRAgentController.nulstr(uploadMsg);
            }
        }


        const int SCRIPT_UPLOAD_TIMEOUT = 1000 * 10;

        public string UploadScriptAction(string scriptfile, string scriptname,
                                    string scriptdescr)
        {
            UUID newItemID = UUID.Zero;
            string uploadMsg = string.Empty;
            bool uploadSuccess = false;
            bool compileSuccess = false;
            AutoResetEvent finishUploadEvent = new AutoResetEvent(false);

            if (!File.Exists(scriptfile)) {
                Console.WriteLine("Script file: " + scriptfile + " not exists");
                return VRAgentController.nulstr("Script file: " + scriptfile + " not exists");
            }
            try {
                using (StreamReader reader = new StreamReader(scriptfile)) {
                    string scriptbody = reader.ReadToEnd();
                    // create the asset
                    Agent.Inventory.RequestCreateItem(
                        Agent.Inventory.FindFolderForType(AssetType.LSLText), 
                        scriptname, 
                        scriptdescr, 
                        AssetType.LSLText, 
                        UUID.Random(), 
                        InventoryType.LSL, 
                        PermissionMask.All,
                        delegate (bool success, InventoryItem item)
                        {
                            Console.WriteLine(String.Format(
                                "RequestCreateItem() returned: Success={0}, Status={1}, ItemID={2}, AssetID={3}",
                                success, item));
                            if (success)
                                // upload the asset
                                Agent.Inventory.RequestUpdateScriptAgentInventory(
                                    EncodeScript(scriptbody), 
                                    item.UUID, 
                                    true, 
                                    new InventoryManager.ScriptUpdatedCallback(
                                        delegate (bool uploadOK, 
                                            string uploadStatus, 
                                            bool compileOK, 
                                            List<string> compileMessages, 
                                            UUID itemid, 
                                            UUID assetid)
                                        {
                                            uploadSuccess = uploadOK;
                                            compileSuccess = compileOK;
                                            newItemID = itemid;
                                            if (uploadOK)
                                                uploadMsg = String.Format(" Script successfully uploaded, ItemID {0} AssetID {1}", itemid, assetid);
                                            if (compileOK)
                                                uploadMsg += " compilation successful";
                                        }));
                        });
                    if (!finishUploadEvent.WaitOne((int)SCRIPT_UPLOAD_TIMEOUT, false))
                        uploadMsg = "Timeout uploading script";
                }
            } catch (System.Exception e) {
                Console.WriteLine("Error creating script: " + e.ToString());
                return VRAgentController.nulstr("Error creating script: "+e.ToString());
            }
            if (uploadSuccess && compileSuccess && newItemID != UUID.Zero) {
                Console.WriteLine(uploadMsg);
                return VRAgentController.ok(uploadMsg, newItemID.ToString());
            } else {
                Console.WriteLine(uploadMsg);
                return VRAgentController.nulstr(uploadMsg);
            }
        }
        /// <summary>
        /// Encodes the script text for uploading
        /// </summary>
        /// <param name="body"></param>
        public static byte[] EncodeScript(string body)
        {
            // Assume this is a string, add 1 for the null terminator ?
            byte[] stringBytes = System.Text.Encoding.UTF8.GetBytes(body);
            byte[] assetData = new byte[stringBytes.Length]; //+ 1];
            Array.Copy(stringBytes, 0, assetData, 0, stringBytes.Length);
            return assetData;
        }


        const int ITEM_UPLOAD_TIMEOUT = 1000 * 10;
        UUID NewUploadItemID = UUID.Zero;
        string UploadMsg = string.Empty;

        public string UploadItemAssetAction(string itemType, string itemFile, 
                                    string itemName, string itemDescr, string itemPath)
        {
            NewUploadItemID = UUID.Zero;
            byte[] data;
            Console.WriteLine("Loading asset: " + itemFile+ " into item: "+itemName);
            if (itemType == "texture") {
                data = doLoadImage(itemFile);
                if (data == null) {
                    Console.WriteLine("Failed to load texture asset file");
                    return VRAgentController.nulstr("Failed to load texture asset file");
                }
                Console.WriteLine("Finished loading texture asset file");
            } else {
                data = File.ReadAllBytes(itemFile);
                if (data == null) {
                    Console.WriteLine("Failed to load asset file");
                    return VRAgentController.nulstr("Failed to load asset file");
                }
                Console.WriteLine("Finished loading asset file");
            }

            Console.WriteLine("Creating item and uploading asset ");
            InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
            if (itemPath!=null && itemPath!="")
                if (!itemPath.EndsWith("/"))
                    itemPath += "/";
            UUID folderID = UUID.Zero;
            bool success = false;
            if (itemType == "clothing") {
                if (itemPath == null || itemPath == "")
                    folderID = Agent.Inventory.FindFolderForType(AssetType.Clothing);
                else
                    folderID = FindFolder(rootFolder, "/", itemPath);
                if (folderID != UUID.Zero)
                    success = doUploadItemAsset(data, itemName, itemDescr, AssetType.Clothing,
                                        InventoryType.Wearable, folderID);
            } else if (itemType == "bodypart") {
                if (itemPath == null || itemPath == "")
                    folderID = Agent.Inventory.FindFolderForType(AssetType.Bodypart);
                else
                    folderID = FindFolder(rootFolder, "/", itemPath);
                if (folderID != UUID.Zero)
                    success = doUploadItemAsset(data, itemName, itemDescr, AssetType.Bodypart,
                                        InventoryType.Wearable, folderID);
            } else if (itemType == "animation") {
                success = doUploadItemAsset(data, itemName, itemDescr, AssetType.Animation,
                                        InventoryType.Animation, folderID);
            } else if (itemType == "sound") {
                if (itemPath == null || itemPath == "")
                    folderID = Agent.Inventory.FindFolderForType(AssetType.Sound);
                else
                    folderID = FindFolder(rootFolder, "/", itemPath);
                if (folderID != UUID.Zero)
                    success = doUploadItemAsset(data, itemName, itemDescr, AssetType.Sound,
                                        InventoryType.Sound, folderID);
            } else if (itemType == "texture") {
                if (itemPath == null || itemPath == "")
                    folderID = Agent.Inventory.FindFolderForType(AssetType.Texture);
                else
                    folderID = FindFolder(rootFolder, "/", itemPath);
                if (folderID != UUID.Zero)
                    success = doUploadItemAsset(data, itemName, itemDescr, AssetType.Texture,
                                        InventoryType.Texture, folderID);
            }

            if (success && NewUploadItemID!=UUID.Zero) {
                Console.WriteLine("New item created: " + NewUploadItemID);
                return VRAgentController.ok("New item created: "+NewUploadItemID, 
                    NewUploadItemID.ToString());
            } else {
                Console.WriteLine(UploadMsg);
                return VRAgentController.nulstr(UploadMsg);
            }
        }


        private bool doUploadItemAsset(
                        byte[] data,
                        string name,
                        string description,
                        AssetType assetType,
                        InventoryType invType,
                        UUID folderID)       
        {
            bool createItemSuccess = false;

            if (data == null)
                return false;

            AutoResetEvent finishUploadEvent = new AutoResetEvent(false);

            Permissions permissions = new Permissions();
            permissions.EveryoneMask = PermissionMask.All;
            permissions.GroupMask = PermissionMask.All;
            permissions.NextOwnerMask = PermissionMask.All;

            Agent.Inventory.RequestCreateItemFromAsset(
                    data, 
                    name, 
                    description,
                    (AssetType) assetType, 
                    (InventoryType) invType, 
                    folderID,
                    permissions,
                    delegate (bool success, string status, UUID itemID, UUID assetID)
                    {
                        Console.WriteLine(String.Format(
                            "RequestCreateItemFromAsset() returned: Success={0}, Status={1}, ItemID={2}, AssetID={3}",
                            success, status, itemID, assetID));
                        NewUploadItemID = itemID;
                        createItemSuccess = success;
                        UploadMsg = status;
                        finishUploadEvent.Set();
                    }
            );
            if (!finishUploadEvent.WaitOne((int)ITEM_UPLOAD_TIMEOUT, false)) {
                UploadMsg = "Timeout uploading new item and asset";
                return false;
            }
            return createItemSuccess;

        }


        public bool DeleteFolderAction(string folderpath)
        {
            InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
            UUID folderID = FindFolder(rootFolder, "/", folderpath);
            if (folderID == UUID.Zero) {
                Console.WriteLine("Folder does not exist");
                return VRAgentController.fail("Folder does not exist");
            }
            if (folderID == rootFolder.UUID) {
                Console.WriteLine("Invalid folder");
                return VRAgentController.fail("Invalid folder");
            }
            Agent.Inventory.MoveFolder(folderID, 
                                    Agent.Inventory.FindFolderForType(AssetType.TrashFolder));
            Console.WriteLine("Moved folder to Trash folder");
            return VRAgentController.ok("Moved folder to Trash folder");
        }


        public bool DeleteItemAction(string itempath)
        {
            InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
            InventoryItem item = FindItem(rootFolder, "/", itempath);
            if (item.UUID == UUID.Zero) {
                Console.WriteLine("Item does not exist");
                return VRAgentController.fail("Item does not exist");
            }
            Agent.Inventory.MoveItem(item.UUID,
                                    Agent.Inventory.FindFolderForType(AssetType.TrashFolder));
            Console.WriteLine("Moved item to Trash folder");
            return VRAgentController.ok("Moved item to Trash folder");
        }

        public bool MoveItemAction(string srcitempath, string destfoldpath)
        {
            InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
            InventoryItem srcitem = FindItem(rootFolder, "/", srcitempath);
            UUID destfolderID = FindFolder(rootFolder, "/", destfoldpath);
            if (destfolderID == UUID.Zero) {
                Console.WriteLine("Folder does not exist");
                return VRAgentController.fail("Folder does not exist");
            }
            if (srcitem.UUID == UUID.Zero) {
                Console.WriteLine("Item does not exist");
                return VRAgentController.fail("Item does not exist");
            }
            Agent.Inventory.MoveItem(srcitem.UUID,destfolderID);
            Console.WriteLine("Moved item " + srcitem.Name + " to " + destfoldpath);
            return VRAgentController.ok("Moved item "+srcitem.Name+" to "+destfoldpath);
        }



        public bool GiveItemAction(string avname, string itempath)
        {
            Avatar av = Agent.Network.CurrentSim.ObjectsAvatars.Find(
                    delegate (Avatar avatar) 
                    { 
                        return (avatar.Name == avname); 
                    });
            if (av == null) {
                Console.WriteLine("Avatar not found");
                return VRAgentController.fail("Avatar not found");
            }
            InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
            InventoryItem item = FindItem(rootFolder, "/", itempath);
            if (item.UUID == UUID.Zero) {
                Console.WriteLine("Item does not exist");
                return VRAgentController.fail("Item does not exist");
            }
            Agent.Inventory.GiveItem(item.UUID, item.Name, item.AssetType, av.ID, true);
            Console.WriteLine("Gave " + item.Name + " to agent " + avname);
            return VRAgentController.ok("Gave "+item.Name+ " to agent "+avname);
        }

        UUID AssetID;
        AssetType AssetTYPE;
        AutoResetEvent AssetDownloadHandle = new AutoResetEvent(false);
        bool AssetDownloadSuccess;
        string AssetFile;
        PerceptList AssetPercepts = new PerceptList();
        List<string> AssetInfo = new List<string>();

        public List<string> DownloadAssetAction(string assetid, string assetyp, 
                                            string assetfile)
        {
            AssetDownloadSuccess = false;
            AssetID = UUID.Zero;
            AssetTYPE = AssetType.Unknown;
            AssetDownloadHandle.Reset();
            AssetPercepts = new PerceptList();
            AssetInfo = new List<string>();
            AssetFile = null;

            if (!UUID.TryParse(assetid, out AssetID)) {
                Console.WriteLine("Asset does not exist");
                return VRAgentController.nullst("Asset does not exist");
            }

            try {
                AssetTYPE = (AssetType)Enum.Parse(typeof(AssetType), assetyp, true);
            } catch (ArgumentException) {
                Console.WriteLine("Invalid asset type");
                return VRAgentController.nullst("Invalid asset type");
            }
            if (!Enum.IsDefined(typeof(AssetType), AssetTYPE)) {
                Console.WriteLine("Invalid asset type");
                return VRAgentController.nullst("Invalid asset type");
            }

            // Start the asset download
            AssetFile = assetfile;
            Agent.Assets.RequestAsset(AssetID, AssetTYPE, true, OnAssetReceived);

            if (AssetDownloadHandle.WaitOne(120 * 1000, false)) {
                if (AssetDownloadSuccess) {
                    Agent.PerceptsBase.Update(AssetPercepts);
                    Console.WriteLine("Saved asset to file "+assetfile);
                    return VRAgentController.ok("Saved asset to file " + assetfile,
                                        AssetInfo);
                } else {
                    Console.WriteLine(String.Format("Failed to download asset {0}, perhaps {1} is the incorrect asset type?",
                                    AssetID, AssetTYPE));
                    return VRAgentController.nullst(
                                String.Format("Failed to download asset {0}, perhaps {1} is the incorrect asset type?",
                                    AssetID, AssetTYPE));
                }
            } else {
                Console.WriteLine("Timed out waiting for asset download");
                return VRAgentController.nullst("Timed out waiting for asset download");
            }
        }


        public List<string> DownloadItemAssetAction(string itempath, string assetfile)
        {
            AssetDownloadSuccess = false;
            AssetID = UUID.Zero;
            AssetTYPE = AssetType.Unknown;
            AssetDownloadHandle.Reset();
            AssetPercepts = new PerceptList();
            AssetInfo = new List<string>();
            AssetFile = null;

            InventoryFolder rootFolder = Agent.Inventory.Store.RootFolder;
            InventoryItem item = FindItem(rootFolder, "/", itempath);
            if (item.UUID == UUID.Zero) {
                Console.WriteLine("Item does not exist");
                return VRAgentController.nullst("Item does not exist");
            }

            // Start the asset download
            AssetFile = assetfile;
            Agent.Assets.RequestInventoryAsset(item, true, OnAssetReceived);

            if (AssetDownloadHandle.WaitOne(120 * 1000, false)) {
                if (AssetDownloadSuccess) {
                    Agent.PerceptsBase.Update(AssetPercepts);
                    Console.WriteLine("Saved item asset to file " + assetfile);
                    return VRAgentController.ok("Saved item asset to file " + assetfile,
                                    AssetInfo);
                } else {
                    Console.WriteLine("Failed to download item asset " + item.Name);
                    return VRAgentController.nullst("Failed to download item asset " + item.Name);
                }
            } else {
                Console.WriteLine("Timed out waiting for item asset download");
                return VRAgentController.nullst("Timed out waiting for item asset download");
            }
        }


        private void OnAssetReceived(AssetDownload transfer, Asset asset)
        {
            if (transfer.AssetID == AssetID) {
                if (transfer.Success) {
                    try {
                        File.WriteAllBytes(AssetFile, asset.AssetData);
                        AssetDownloadSuccess = true;
                        AssetInfo = AssetPercepts.Add("asset", asset.AssetID.ToString(),
                                            asset.AssetType.ToString().ToLower());
                    } catch (Exception ex) {
                        Console.WriteLine("Asset download error: "+ex.Message);
                    }
                }
                AssetDownloadHandle.Set();
            }
        }


        public string UploadAssetAction(string assetyp, string assetfile)
        {
            byte[] assetdata;
            AssetType assetType = AssetType.Unknown;

            foreach (AssetType at in Enum.GetValues(typeof(AssetType))) {
                if (at.ToString().ToLower() == assetyp) {
                    assetType = at;
                    break;
                }
            }
            if (assetType==AssetType.Unknown) {
                Console.WriteLine("Invalid asset type");
                return VRAgentController.nulstr("Invalid asset type");
            }
            Console.WriteLine("Loading asset: " + assetfile + " to asset database");
            if (assetyp == "texture") {
                assetdata = doLoadImage(assetfile);
                if (assetdata == null) {
                    Console.WriteLine("Failed to load texture asset file");
                    return VRAgentController.nulstr("Failed to load texture asset file");
                }
                Console.WriteLine("Finished loading texture asset file");
            } else {
                assetdata = File.ReadAllBytes(assetfile);
                if (assetdata == null) {
                    Console.WriteLine("Failed to load asset file");
                    return VRAgentController.nulstr("Failed to load asset file");
                }
                Console.WriteLine("Finished loading asset file");
            }
            Console.WriteLine("Uploading asset ");

            UUID uploadedAssetID = Agent.Assets.RequestUpload(assetType, assetdata, true);
            if (uploadedAssetID != UUID.Zero) {
                Console.WriteLine("New asset uploaded: " + uploadedAssetID);
                return VRAgentController.ok("New asset uploaded: " + uploadedAssetID,
                    uploadedAssetID.ToString());
            } else {
                Console.WriteLine("Failed to upload asset");
                return VRAgentController.nulstr("Failed to upload asset");
            }
        }




    }
}

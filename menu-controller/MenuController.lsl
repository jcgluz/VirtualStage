//#############################################################
//#############################################################
//
//   MenuController
//   --------------
//
//   This program is free software; you can redistribute it and/or
//   modify it under the terms of the GNU Lesser General Public
//   License as published by the Free Software Foundation; either
//   version 2.1 of the License, or (at your option) any later version.
//   This software is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
//   This software is provided "as is" and any express or implied 
//   warranties, including, but not limited to, the implied warranties 
//   of merchantability and fitness for a particular purpose are 
//   disclaimed. The entire risk as to the quality and performance of the 
//   program is with you. Should the program prove defective, you assume 
//   the cost of all necessary servicing, repair or correction.
//   In no event shall the copyright owner or contributors be liable 
//   for any direct, indirect, incidental, special, exemplary, or 
//   consequential damages (including, but not limited to, procurement of 
//   substitute goods or services; loss of use, data, or profits; or 
//   business interruption) however caused and on any theory of liability, 
//   whether in contract, strict liability, or tort (including negligence 
//   or otherwise) arising in any way out of the use of this software, 
//   even if advised of the possibility of such damage.
//   See the GNU Lesser General Public License for more details.
//   You should have received a copy of the GNU Lesser General Public
//   License along with this software; if not, print to the Free Software
//   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
//
//********************************************************
//
//   LSL Script:    MenuController.lsl
//   Purpose:       Controls the menu interface for VirtualStage 
//                  actors
//   Author:     João Carlos Gluz - 2023
//   E-mail:     jcgluz@gmail.com
//   Copyright (C): 2023, Joao Carlos Gluz
//
//   Version:  1.0
//   Revision: 0
//
//
//#############################################################
//#############################################################


// Format of message that user A has to send to create a menu 
// for user B:
//
// @<user A UUID>|<user B UUID>|<menu message>|<menu option 1>|<menu option 2>|...
//
// Example:
//  User A UUID: 6e96b510-5657-4b09-8113-4f2044edb0a5
//  User B UUID: ac863c6b-5957-4d29-818e-babc2030d638
//  Menu message: Que direção?
//  Menu option 1: Norte
//  Menu option 1: Sul
//  Menu option 1: Leste
//  Menu option 1: Oeste
// Message sent:
// @6e96b510-5657-4b09-8113-4f2044edb0a5|ac863c6b-5957-4d29-818e-babc2030d638|Que direção?|Norte|Sul|Leste|Oeste


// Format of message that user A has to send to create an input
// text box for user B:
//
// &<user A UUID>|<user B UUID>|<text message>
//
// Example:
//  User A UUID: 6e96b510-5657-4b09-8113-4f2044edb0a5
//  User B UUID: ac863c6b-5957-4d29-818e-babc2030d638
//  Text message: Entre com sua identificação:
// Message sent:
// &6e96b510-5657-4b09-8113-4f2044edb0a5|ac863c6b-5957-4d29-818e-babc2030d638|Entre com sua identificação:


// UUID of the avatar that owns the user menu
string MenuOwnerID="";

// Chat channel used by the menu controller
integer MenuChannel=-98186;

// Note: The default chat channel used to interact with MenuController 
//       script has the number -98186. Is a random number that probably
//       will work fine and not cause interference with other scripts 
//       running in the virtual world. However, if other VirtualStage 
//       actors  are in the same virtual world and also use menus to 
//       communicate with users, then the MenuController scripts running 
//       on attached objects of these actor's will need to have different 
//       chat channel numbers. Modify the MenuController script that is 
//       loaded in the attached object changing the MenuChannel variable
//       to some appropriate new chat number, and call show_menu_to_avatar() 
//       with the last parameter, menu_chann, with this new chat number.

default
{
    state_entry()  
    {
        // This script operates listening messages on MenuChannel chat channel
        llListen(MenuChannel,"","","");        
    }
    
    listen(integer chann, string name, key id, string msg)
    {
        if (chann!=MenuChannel) 
            // Listened something not in MenuChannel, ignore 
            return;
                
        if (llGetSubString(msg,0,0)=="@") 
        {
            // Messages to create user menus are sent by the actor's avatar
            // and are prefixed by an '@' character
            // The have the format:
            // @<user A UUID>|<user B UUID>|<menu message>|<menu option 1>|<menu option 2>|...
            // Parse the message:
            list menu_cmd = llParseString2List(llGetSubString(msg,1,-1),["|"],[]);
            // Extract the ID of the avatar that sent the message and is menu owner
            MenuOwnerID = llList2String(menu_cmd,0);
            // Create and show the dialog box with the menu
            llDialog( llList2String(menu_cmd,1), llList2String(menu_cmd,2),
                    llList2List(menu_cmd,3,-1), MenuChannel);       
        } 
        else if (llGetSubString(msg,0,0)=="&") 
        {
            // Messages to create user input boxes are sent by the actor's avatar
            // and are prefixed by an '&' character
            // The have the format:
            // &<user A UUID>|<user B UUID>|<text message>
            // Parse the message:
            list input_cmd = llParseString2List(llGetSubString(msg,1,-1),["|"],[]);
            // Extract the ID of the avatar that sent the message and is menu owner
            MenuOwnerID = llList2String(input_cmd,0);
            // Create and show the dialog box with the input box
            llTextBox( llList2String(input_cmd,1), llList2String(input_cmd,2), MenuChannel);       
        } 
        else  
        {
            if (MenuOwnerID!="") 
            {
                // Received a message from dialog box with the selection/input of user,
                // sent this information to the avatar that owns this menu/input box
                llInstantMessage( MenuOwnerID, msg);
            }              
        }
    }
}

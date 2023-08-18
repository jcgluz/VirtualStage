# VRAgents Library

## Introduction

The ***VRAgents*** interface library provide access to *OpenSimulator* [\[1\]](#ref1) VR simulators. This library implements an actions/perceptions abstraction layer on top of *LibOpenMetaverse* [\[2\]](#ref2) library. It provides a high-level API, which allow agents (and ***VirtualStage*** actors) to interact with VR entities or objects through:
 
- **Actions**: operations that can change the properties of an entity or object (it may be the agent's avatar), or properties of the environment itself. Actions that seek information about the environment are called *observations* and form the *senses* of the agent.

- **Perceptions**: information obtained by agent's observation actions (its senses) form the perceptions of the agent. These perceptions register information about what objects or entities exist in the VR environment and what are the properties of these entities and objects.

The main entry point of ***VRAgents*** library is the **VRAgentManager** class, which is a singleton class that creates and manages new VR agents. This class implements the login process of VR agents and its corresponding avatars into *OpenSimulator* [\[1\]](#ref1) VR worlds, creating a new agent controller and associating this agent with the avatar recently logged in the virtual world. It provides access to the agent controllers of previously logged agents.

The agent controllers are implemented by the **VRAgentController** class. All VR actions that the agent can execute and the perceptions and beliefs (memories) bases that the agent can access are implemented by classes of ***VRAgents*** library. These classes are included as parts of the **VRAgentController** class, so this class can control how the agent execute VR actions and how it access its beliefs and perceptions. This class also handle VR events sent by *OpenSimulator* [\[1\]](#ref1) to the agent. The **VRAgentController** class was defined as a subclass of *GridClient* class of *LibOpenMetaverse* [\[2\]](#ref2) library, to allow it to expose all functionality of *OpenSimulator* [\[1\]](#ref1) grid clients to the VR actions classes. Thus, ***VRAgents*** agents operate as clients (like VR viewers) of *OpenSimulator* grids. 

The remaining VR actions and the management of beliefs (memories) and perceptions is implemented by the following classes:

- **Actions**: this superclass implements some methods and fields used by other action classes.

- **Beliefs**: this class implements agent's access to its belief base (its memory).

- **BeliefBase**: this class implements agent's beliefs base (the memory of the agent).

- **CommunicationActions**: this class implement actions for the agent to be able to communicate with others avatars on virtual world. 

- **ModificationActions**: this class implement actions for the agent to be able to modify object on virtual world.

- **MovementActions**: this class implement actions for the agent to be able to move its avatar on virtual world.

- **ObservationActions**: this class implement actions for the agent to be able to observe objects on virtual world (it provides senses for objects on VR world).

- **Perceptions**: this class implements agent's access to its perceptions base.

- **PerceptionsBase**: this class implement the agent's perceptions base.

- **PositionActions**: this class implement actions for the agent to be able to modify the positioning and rotation of its avatar on virtual world.

- **SelfModificationActions**: this class implement actions for the agent to be able to modify the characteristics of its avatar in the virtual world.

- **SelfObservationActions**: this class implement actions for the agent be able to observe the state of its avatar on virtual world (it provides senses for itself).

- **SocialModificationActions**: this class implement actions for agents be able to modify their social relationships with other avatars on virtual world.

- **SocialObservationActions**: this class implement actions for agents be able to observe the state of their social relationships with other avatars on virtual world.

- **SystemActions**: this class implements system actions.

- **TimerTask**: this class implements an abstract class for timers.

## Installation

A precompiled VRAgents library is distributed on `VirtualStage\bin` directory, but if necessary this library can be recompiled using VisualStudio solution file `VirtualStage\VRAgents\VRAgents.sln`.

## References

<a id="ref1">1. [Open Simulator](http://opensimulator.org)

<a id="ref2">2. [LibOpenMetaverse, Release 0.9.3](https://github.com/openmetaversefoundation/libopenmetaverse)

# TasKey - v0.0.0 (XX Feb, 2024)

[Report an Issue](https://github.com/andrewdget/TasKey/issues) | [View Changelog](https://github.com/andrewdget/TasKey/blob/main/CHANGELOG.md) | [Licensed under the MIT License](https://github.com/andrewdget/TasKey/blob/main/LICENSE.md)

## Table of Contents

<ol>
	<li><a href="url">Introduction</a></li>
	<li><a href="url">Instillation</a></li>
	<li><a href="url">Getting Started</a></li>
	<li><a href="url">Usage/Command Line Syntax
		<ol>
			<li><a href="url">Creating a Task</a></li>
			<li><a href="url">Viewing Task Information</a></li>
			<li><a href="url">Editing a Task</a></li>
			<li><a href="url">Completing a Task</a></li>
			<li><a href="url">Deleting a Task</a></li>
			<li><a href="url">Viewing Archive (Completed/Deleted Tasks)</a></li>
			<li><a href="url">Switching Tabs</a></li>
			<li><a href="url">Other Actions (Save, Prune, Kill)</a></li>
			<li><a href="url">Creating/Managing Tabs</a></li>
			<li><a href="url">Customizing Appearance</a></li>
			<li><a href="url">Other Settings</a></li>
		</ol>
	</li>
	<li><a href="url">Theory of Operation</a></li>
	<li><a href="url">Future Development</a></li>	
</ol>

## Introduction

TasKey is a ASCII based task ("to-do") management tool that is **powerful, simple, and fast.**

Many products (not just software) try to pack in so many "features" that they compromise the "easy of use" and/or functionality of their primary function. Conversely, there are very few minimalist products that perform a single function, strive to do it well, and do nothing else... not as the result of a lack of ability, but rather clarity of purpose. 

TasKey takes inspiration from the latter. It's core design principle is to provide a task management tool that is **just powerful enough to be effective while remaining easy and fast to use.** In other words you can track/manage your tasks and then get back to whatever you were doing before! Keeping track of your tasks shouldn't become a task in and of itself.

Key features of TasKey:

<ul>
	<li>Keyboard only inputstriking a balance between speed and simplicity.</li>
	<li>Simple but effective task management algorithm (see <a href="url">Theory of Operation</a> section) which dynamically places the most important/near-term tasks on top and lower priority tasks below.</li>
	<li>A clean, light weight, and easy to read "at a glance" format.</li>
	<li>Both local and collaborative task management (see <a href="url">Creating/Managing Tabs</a> section) .</li>
</ul>

## Instillation

## Usage/Command Line Syntax

TasKey utilizes a simple command line interface, based around and alphabetical index and contextual "flags" (i.e. "-a", "-b", etc.) which can be accompanied (when needed) by a string containing additional information called an "attribute", together flags and attributes form "command pairs".

**Great!... but what does that actually mean? How do we use it? Lets go through a few examples.**

### Standalone Flags

Lets start off with the simplest type of command, a standalone flag. Let's say we want to switch from the main task view to the archived task view (more on this later), the following simple command is used:

```
TasKey >> -a
```

Where ```-a``` is a flag and, and because it is not followed by a string containing more information (i.e. an "attribute"), it is considered to be "standalone". These types of commands are used for general purpose commands such as changing views, setting task priority, or closing TasKey. 

### Command Pair

When additional information is required flags may also be accompanied by a string called an "attribute". For example, when creating a new task, the following command is used: 

```
TasKey >> -n Send Jim the new working directory
```

Where ```-n``` is the flag used for creating a new task and ```Send Jim the new working directory``` is an attribute representing the name of the task, together they form a "command pair".

Some commands may include more than one set of command pairs (flags/attributes). For example, we want to create the same task used in the last example, but this time we want to set it as a high priority and set a deadline:

```
TasKey >> -n Send Jim the new working directory -h -d 02202024
```

Where the ```-n Send Jim the new working directory``` command pair is used the same, but also included is the standalone flag ```-h``` which represents the tasks priority and the ```-d``` flag used to set a deadline paired with an attribute representing the deadline date, in this case ```02202024``` (Feb 20, 2024).

### Leader/Follower Flags or Command Pairs

Now that there are multiple flags being used, we must distinguish between "leader" and "follower" flags.

<ul>
	<li>Leader flags, as their name suggest, are the first flag used in a command (<code>-n</code> in the example above).</li>
	<li>Follower flags are any flag that comes after the leader flag (<code>-h</code> and <code>-d</code> in the example above).</li>
</ul>

The order of follower flags is unimportant. For example, the command above could be reordered as follows and would have the same result:

```
TasKey >> -n Send Jim the new working directory -d 02202024 -h
```

However, leader flags must be chosen with care as they determine the interpretation of the follower flags. For example the flag ```-d``` used above, as a follower, is used to set a deadline... but as a leader flag, ```-d``` is used to delete a task.

### Alpha Indices

Now, what if we want to do something to an existing task, say mark a task complete? How do we select existing tasks? The answer is an "alpha index". An alpha index consists of two letters which represent a numerical index (for example ```aa```, ```bd```, and ```gi``` would respectivly represent the XXXX, XXXX, and XXXX items of a list).

Lets say we have the following task list:

!!INSERT IMAGE!!

we could use the command 


Alpha indicies are used rather than numerical indicies for their speed/ease of typing. 

## Create a New Task ```-n```
Creating a new task can be accomplished quickly by simply passing the ```-n``` leader flag followed by the desired task name, relying on TasKey's defaults to take care of the rest. For example:

```
TasKey >> -n Send Jim the new working directory.
```

However, if more control is required, the follower flags below can be 
used:

**Add a Footnote** ```-f```<br>Allows for the inclusion of additional information about/for the task and are always displayed, subtly, underneath the task name. Footnotes are optional, if no footnote is given for a task, none will be included. For example:

```
TasKey >> -n Send Jim the new working directory. -f Needs dir for Project_B along with permissions.
```

>[!TIP]
>Keep task names concise. If necessary, use footnotes to capture more nuanced information. 

**Set Task Priority** ```-l``` (low), ```-m``` (medium), ```-h``` (high), ```-c``` (critical)<br>The priority of a task influences how quickly that task will be at the top of the task list. Naturally, tasks with higher priority will be listed above other tasks with the same deadline/number of working days remaining. Furthermore, if a deadline is not manually set, the priority of the task influences the deadline that is automatically set (i.e. how many working days are provided to complete the task), see [Theory of Operation](url) for more. If no priority is set, TasKey will set the task to a medium priority. For example, creating a high priority task:

```
TasKey >> -n Send Jim the new working directory. -h 
```

**Set Task Deadline** ```-d```<br>A task's deadline (specifically, the number of working days remaining before the deadline), along with that task's level of priority, influence how quickly that task will be at the top of the task list. All TasKey tasks are assigned a deadline at creation, if not done manually (given in mmddyyyy format), a deadline will be automatically set based on priority, see [Theory of Operation](url) for more. For example, setting a deadline of February 18 2024:

```
TasKey >> -n Send Jim the the new working directory. -d 02182024
```

## Edit an Existing Task ```-e```

Editing a task works much the same as creating one, with all the same flag/attribute pairs, with two exceptions; the necessity of including an [alpha index](url) which points to the task to be edited, and the addition of the ```-n``` flag used to edit the tasks name.

When making adjustments to a task, only the flag(s) for the specific element(s) you wish to edit (i.e. the name, footnote, priority, or deadline) need to be called, all other elements will be inherited from the original task. 

**Edit Task Name** ```-n```<br>The attribute (task name string) provided will completely replace the original task name. For example, editing the name of a task at alpha index ```ab```:

```
TasKey >> -e ab -n Send Carla the the new working directory.
```

**Edit Task Footnote** ```-f```<br>The attribute (footnote string) provided will completely replace the original footnote. For example, editing the footnote of a task at alpha index ```ab```:

```
TasKey >> -e ab -f Needs dir for Project_C along with permissions.
```

>[!TIP]
>In order to remove a footnote from a task all together, simply pass ```None``` as the attribute.

**Edit Task Priority** ```-l``` (low), ```-m``` (medium), ```-h``` (high), ```-c``` (critical)<br>When a tasks priority is edited the deadline for that task (if it was not manually set) will be adjusted accordingly, see [Theory of Operation](url). However, the number of working days provided to complete the task remains relative to the original creation date (i.e. the deadline is re-set as if the task was given the new priority, when the task was originally created). For example, changing the priority of a task at alpha index ```ab``` to critical:

```
TasKey >> -e ab -c
```

**Edit Task Deadline** ```-d```<br>The attribute (task deadline - given in mmddyyyy format) provided will completely replace the original. For example, changing the deadline of a task at alpha index ```ab``` to March 18 2024:

```
TasKey >> -e ab -d 03182024
```

>[!TIP]
>In order to remove a manually set deadline, simply pass ```None``` as the attribute and a deadline will be set automatically according to the tasks priority (see [Theory of Operation](url)).

## Completing a Task ```-c```

When a task has been completed, it can be marked as such and subsequently moved from the main database to the archive database. This is acomplished by simply passing the ```-c``` flag along with the alpha index pointing to the target task. For example, marking a task complete at alpha index ```ab```:

```
TasKey >> -c ab
```

## Deleting a Task ```-d```

When necesary tasks can be deleted by simply passing the ```-d``` flag along with the alpha index pointing to the target task. The behavior of the delete command is context specific. If used within the main view, the task will be moved from the main database to the archive database. If used within the archive view, the task will be permanently delted from all databases. For example, deleting a task at alpha index ```ab```:

```
TasKey >> -d ab
```

## Restore a Completed/Deleted Task ```-r```

If a task has been completed or deleted in error, it can be restored (from the [archvie view](url)) by uising the ```-f``` flag along with the alpha index pointing to the target task. For example, restoring a task at alpha index ```ab```:

```
TasKey >> -r ab
``` 

## View Task Information ```-i```

All elements/information about a task can be displayed by passing the ```-i``` flag and the alpha index pointing to the target task. This will open a file-tree like drop down containing the additional information. For example, displaying additional information for a task at alpha index ```ab```:

```
TasKey >> -i ab
```

When done, the additional information can be hidden but using the same ```-i``` flag can be passeed but with ```None``` as the attribute.

## Switching to Archive View ```-a```

When an active task is completed or delted, it is moved from the active ("main") database to the archvie database. This database can be viewed by using the ```-a``` standalone flag. From the archive view, information about completed/deleted tasks can be viewed or restored.

## Returning to Main View ```-m```

In order to return to the active ("main") database view from the archive view, the standalone flag ```-m``` can be passed.

## Switch Tabs ```-t```

TasKey can support multiple task databases (such as one for a current project, another for personal tasks, etc.). These databases are organized into "tabs" which can be switched between at will, using the ```-t``` flag with the name of the tab as an attribute (Note, the tab name is case-sensitive). For example, switching to a tab/task database called "Project_C":

```
TasKey >> -t Project_C
```

## Generate Savestate ```-s```

## Clean Up/Prune Savestates ```-p```

## Close/Kill Application ```-k```

## Command Quick Reference

### Create a new Task

| Flag | Action | Attribute | Default Behavior |
| --- | --- | --- | --- |
| ```-n``` [Leader] | Create New Task | Task Name String | ~ |
| ```-f``` | Add a Footnote | Footnote String | ```None``` |
| ```-l```, ```-m```, ```-h```, ```-c``` | Set Task Priority (respectively; low, medium, high, critical) | None | ```-m``` |
| ```-d``` | Set Task Deadline| Deadline (mmddyyyy) | Dynamically Set[^1] |

### Edit an Existing Task

| Flag | Action | Attribute |
| --- | --- | --- |
| ```-e``` [Leader] | Edit an Existing Task | Target Alpha Index |
| ```-n``` | Edit Task | Task Name (string) |
| ```-f``` | Edit Task Footnote | Footnote (string) |
| ```-l```, ```-m```, ```-h```, ```-c``` | Edit Task Priority (respectively; low, medium, high, critical) | None |
| ```-d``` | Edit Task Deadline | Deadline (mmddyyyy) |

### Other Commands

| Flag | Action | Attribute |
| --- | --- | --- |
| ```-c``` | Complete a Task | Target Alpha Index |
| ```-d``` | Delete a Task[^2] | Target Alpha Index |
| ```-r``` | Restore a Completed/Deleted Task | Target Alpha Index |
| ```-i``` | View Task Information | Target Alpha Index |
| ```-a``` | Switch to Archive Database View | None |
| ```-m``` | Switch to Main Database View | None |
| ```-t``` | Switch Tabs | Tab Name |
| ```-s``` | Save Task Database | None |
| ```-p``` | Clean Up ("prune") Old Database Savestates | None |
| ```-k``` | Close ("kill") Application | None |

[^1]: See [Theory of Operation](url). 
[^2]: Behavior of delete command is context specific. See [Delete a Task](url).

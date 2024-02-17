
# TasKey - v0.0.0 (XX Feb, 2024)

[Report an Issue](https://github.com/andrewdget/TasKey/issues) | [View Changelog](https://github.com/andrewdget/TasKey/blob/main/CHANGELOG.md) | [Licensed under the MIT License](https://github.com/andrewdget/TasKey/blob/main/LICENSE.md)

## Create a New Task ```-n```
Creating a new task can be accomplished quickly by simply passing the ```-n``` leader flag followed by the desired task name, relying on TasKey's defaults to take care of the rest. For example:

```
TasKey >> -n Send Jim the new working directory.
```

However, if more control is required, the follower flags below can be used:

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
## Deleting a Task ```-d```

Behavior of delete command is context specific: If in main view, task will be moved to archive as a deleted task. If in archive view, task will be permanently deleted from database. 


## View Task Information ```-i```
## Switching to Archive View ```-a```
## Returning to Main View ```-m```
## Switch Tabs ```-t```
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
| ```-c``` | Complete a task. | Target Alpha Index |
| ```-d``` | Delete a task.[^2] | Target Alpha Index |
| ```-i``` | View task information. | Target Alpha Index |
| ```-a``` | Switch to archive view. | None |
| ```-m``` | Switch to main/default view. | None |
| ```-t``` | Switch tabs. | Tab Name |
| ```-s``` | Save task database. | None |
| ```-p``` | Clean up ("prune") old database savestates. | None |
| ```-k``` | Close ("kill") application. | None |

[^1]: See [Theory of Operation](url). 
[^2]: Behavior of delete command is context specific. See [Delete a Task](url).
